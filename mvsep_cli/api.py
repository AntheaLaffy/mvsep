import os
import time
import json
import requests
from typing import Optional, Dict, Any, List, Union
from requests.exceptions import RequestException

TASK_META_FILE = os.path.expanduser("~/.mvsep_tasks.json")


class UploadProgressFile:
    def __init__(self, filepath, callback=None):
        self.filepath = filepath
        self.callback = callback
        self.filesize = os.path.getsize(filepath)
        self.uploaded = 0
        self._file = None

    def __enter__(self):
        self._file = open(self.filepath, "rb")
        return self

    def __exit__(self, *args):
        if self._file:
            self._file.close()

    def read(self, size=-1):
        chunk = self._file.read(size)
        if chunk:
            self.uploaded += len(chunk)
            if self.callback:
                self.callback(self.uploaded, self.filesize)
        return chunk


class MVSEP_API:
    STATUS_WAITING = "waiting"
    STATUS_PROCESSING = "processing"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"
    STATUS_DISTRIBUTING = "distributing"
    STATUS_MERGING = "merging"
    STATUS_NOT_FOUND = "not_found"

    FINAL_STATUSES = {STATUS_DONE, STATUS_FAILED, STATUS_NOT_FOUND}

    def __init__(
        self,
        api_token: str,
        base_url: Optional[str] = None,
        retries: int = 30,
        retry_interval: int = 20,
        debug: bool = False,
    ):
        self.api_token = api_token
        self.retries = retries
        self.retry_interval = retry_interval
        self.debug = debug
        if base_url:
            self.base_url = base_url
        else:
            from mvsep_cli.config import Config

            config = Config()
            self.base_url = config.base_url

        self.api_url = f"{self.base_url}/api"
        self.headers = {"User-Agent": "MVSEP Python Client/1.0"}

    def _log_debug(self, message: str) -> None:
        if self.debug:
            print(f"[DEBUG] {message}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        stream: bool = False,
    ) -> requests.Response:
        url = f"{self.api_url}/{endpoint.lstrip('/')}"

        self._log_debug(f"Making {method} request to {url}")

        for attempt in range(self.retries + 1):
            try:
                response = requests.request(
                    method,
                    url,
                    params=params,
                    data=data,
                    files=files,
                    headers=self.headers,
                    stream=stream,
                    timeout=(600, 1200),
                )

                self._log_debug(f"Response status: {response.status_code}")

                if response.status_code == 429:
                    retry_after = int(
                        response.headers.get("Retry-After", self.retry_interval)
                    )
                    self._log_debug(f"Rate limited, retrying after {retry_after}s")
                    time.sleep(retry_after)
                    continue
                if response.status_code == 400:
                    time.sleep(self.retry_interval)
                    continue
                if 500 <= response.status_code < 600 and attempt < self.retries:
                    self._log_debug(f"Server error {response.status_code}, retrying...")
                    time.sleep(self.retry_interval)
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.HTTPError as e:
                self._log_debug(f"HTTP error: {str(e)}")
                if e.response.status_code // 100 == 4 and e.response.status_code != 429:
                    raise
                if attempt == self.retries:
                    raise
                time.sleep(self.retry_interval)
            except RequestException as e:
                self._log_debug(f"Request exception: {str(e)}")
                if attempt == self.retries:
                    raise Exception(
                        f"Request failed after {self.retries} retries: {str(e)}"
                    )
                time.sleep(self.retry_interval)
        raise Exception("Unexpected error in request handling")

    def _save_task_meta(self, hash_val: str, original_filename: str):
        meta = {}
        if os.path.exists(TASK_META_FILE):
            with open(TASK_META_FILE, "r") as f:
                meta = json.load(f)

        # Extract filename without extension
        name_without_ext = os.path.splitext(os.path.basename(original_filename))[0]
        meta[hash_val] = {"original_name": name_without_ext}

        with open(TASK_META_FILE, "w") as f:
            json.dump(meta, f)

    def _get_task_meta(self, hash_val: str) -> Optional[str]:
        if not os.path.exists(TASK_META_FILE):
            return None
        with open(TASK_META_FILE, "r") as f:
            meta = json.load(f)
        return meta.get(hash_val, {}).get("original_name")

    def _upload_progress(self, uploaded: int, total: int):
        percent = (uploaded / total) * 100
        print(
            f"\rUploading: {percent:.1f}% ({uploaded}/{total} bytes)",
            end="",
            flush=True,
        )

    def create_task(
        self,
        audio_file: Optional[str] = None,
        sep_type: int = 20,
        output_format: int = 0,
        add_opt1: Optional[str] = None,
        add_opt2: Optional[str] = None,
        add_opt3: Optional[str] = None,
        remote_url: Optional[str] = None,
        remote_type: Optional[str] = None,
        is_demo: bool = False,
    ) -> Dict[str, Any]:
        api_url = f"{self.api_url}/separation/create"

        if audio_file and remote_url:
            raise ValueError("Cannot specify both audio_file and remote_url")

        files = {}
        data = {
            "api_token": self.api_token,
            "sep_type": str(sep_type),
            "output_format": str(output_format),
            "is_demo": "1" if is_demo else "0",
        }

        if add_opt1:
            data["add_opt1"] = add_opt1
        if add_opt2:
            data["add_opt2"] = add_opt2
        if add_opt3:
            data["add_opt3"] = add_opt3

        if audio_file:
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file not found: {audio_file}")

            filesize = os.path.getsize(audio_file)
            print(f"File size: {filesize / 1024 / 1024:.1f} MB", flush=True)
            print("Uploading...", flush=True)

            with UploadProgressFile(audio_file, self._upload_progress) as upload_file:
                files = {
                    "audiofile": (
                        os.path.basename(audio_file),
                        upload_file,
                        "audio/wav",
                    )
                }
                response = requests.post(api_url, files=files, data=data)
                print()  # newline after progress
        elif remote_url:
            self._log_debug(f"Processing remote URL: {remote_url}")
            data["url"] = remote_url
            if remote_type:
                data["remote_type"] = remote_type
            response = requests.post(api_url, data=data)
        else:
            raise ValueError("Either audio_file or remote_url must be provided")

        if response.status_code != 200:
            print(f"Server error ({response.status_code}): {response.text[:500]}")

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            error_msg = result.get("data", {}).get("message", "Unknown error")
            raise Exception(f"Failed to create task: {error_msg}")

        task_data = result["data"]
        hash_val = task_data.get("hash")
        if hash_val and audio_file:
            self._save_task_meta(hash_val, audio_file)

        return task_data

    def get_status(self, hash: str, mirror: int = 0) -> Dict[str, Any]:
        url = f"{self.api_url}/separation/get"
        params = {"hash": hash, "mirror": str(mirror)}
        if mirror == 1:
            params["api_token"] = self.api_token

        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        return result

    def wait_for_completion(
        self, hash: str, interval: int = 5, max_wait: Optional[int] = None
    ) -> Dict[str, Any]:
        start_time = time.time()

        while True:
            result = self.get_status(hash)
            status = result.get("status")

            if status in self.FINAL_STATUSES:
                return result

            if max_wait and (time.time() - start_time) > max_wait:
                raise TimeoutError(f"Max wait time ({max_wait}s) exceeded")

            if status == self.STATUS_WAITING:
                queue_count = result.get("data", {}).get("queue_count", "?")
                print(f"Status: {status} (queue: {queue_count})")
            else:
                print(f"Status: {status}")

            time.sleep(interval)

    def download_file(self, url: str, output_path: str) -> str:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with open(output_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = (downloaded / total_size) * 100
                        print(f"\rDownloading: {progress:.1f}%", end="", flush=True)

        print()
        return output_path

    def download_results(self, hash: str, output_dir: str = ".") -> List[str]:
        result = self.get_status(hash)

        if result.get("status") != self.STATUS_DONE:
            raise Exception(f"Task not completed yet. Status: {result.get('status')}")

        files = result.get("data", {}).get("files", [])
        if not files:
            raise Exception("No files to download")

        # Try to get original filename from local metadata
        original_name = self._get_task_meta(hash)
        if not original_name:
            # Fallback: extract from hash
            hash_parts = hash.split("-")
            if len(hash_parts) >= 2:
                original_name = (
                    "-".join(hash_parts[2:]) if len(hash_parts) > 2 else hash_parts[-1]
                )
                original_name = os.path.splitext(original_name)[0]
            else:
                original_name = "output"

        os.makedirs(output_dir, exist_ok=True)

        downloaded_files = []
        for file_info in files:
            url = file_info.get("url")
            if not url:
                continue

            # Extract suffix from URL (last part after last underscore)
            url_basename = os.path.basename(url)
            url_name = os.path.splitext(url_basename)[0]
            suffix_parts = url_name.rsplit("_", 1)
            if len(suffix_parts) > 1:
                suffix = suffix_parts[-1]
            else:
                suffix = url_name

            ext = os.path.splitext(url)[1] or ".mp3"

            # Combine original filename with suffix
            final_name = f"{original_name}_{suffix}{ext}"
            output_path = os.path.join(output_dir, final_name)

            print(f"Downloading {final_name}...")
            self.download_file(url, output_path)
            downloaded_files.append(output_path)

        return downloaded_files

    def cancel_task(self, hash: str) -> Dict[str, Any]:
        url = f"{self.api_url}/separation/cancel"
        data = {"api_token": self.api_token, "hash": hash}

        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def get_algorithms(self, scopes: str = "single_upload") -> List[Dict[str, Any]]:
        url = f"{self.api_url}/app/algorithms"
        params = {"scopes": scopes}

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_algorithms_formatted(self, scopes: str = "single_upload") -> Dict[int, str]:
        algorithms = self.get_algorithms(scopes)
        import json

        algo_dict = {}

        for algo in algorithms:
            s = f"\nID: {algo['render_id']} - {algo['name']}"
            algo_dict[algo["render_id"]] = s + "\n"

            for field in algo.get("algorithm_fields", []):
                s = f"\t{field['name']}"
                algo_dict[algo["render_id"]] += s + "\n"
                try:
                    options = json.loads(field["options"])
                    for key, value in sorted(options.items(), key=lambda x: str(x[0])):
                        s = f"\t\t{key}: {value}"
                        algo_dict[algo["render_id"]] += s + "\n"
                except (json.JSONDecodeError, KeyError):
                    pass

        return algo_dict

    def get_queue_info(self) -> Dict[str, Any]:
        response = self._make_request("GET", "app/queue")
        return response.json()

    def get_news(
        self, lang: str = "en", start: int = 0, limit: int = 10
    ) -> Dict[str, Any]:
        params = {"lang": lang, "start": start, "limit": limit}
        response = self._make_request("GET", "app/news", params=params)
        return response.json()

    def get_separation_history(self, start: int = 0, limit: int = 10) -> Dict[str, Any]:
        params = {"api_token": self.api_token, "start": start, "limit": limit}
        response = self._make_request("GET", "app/separation_history", params=params)
        return response.json()

    def enable_long_filenames(self) -> Dict[str, Any]:
        data = {"api_token": self.api_token}
        response = self._make_request("POST", "app/enable_long_filenames", data=data)
        return response.json()

    def disable_long_filenames(self) -> Dict[str, Any]:
        data = {"api_token": self.api_token}
        response = self._make_request("POST", "app/disable_long_filenames", data=data)
        return response.json()

    def enable_premium(self) -> Dict[str, Any]:
        data = {"api_token": self.api_token}
        response = self._make_request("POST", "app/enable_premium", data=data)
        return response.json()

    def disable_premium(self) -> Dict[str, Any]:
        data = {"api_token": self.api_token}
        response = self._make_request("POST", "app/disable_premium", data=data)
        return response.json()

    def create_quality_entry(
        self,
        zip_path: str,
        algo_name: str,
        main_text: str,
        dataset_type: int = 0,
        ensemble: int = 0,
        password: str = "",
    ) -> Dict[str, Any]:
        data = {
            "api_token": self.api_token,
            "algo_name": algo_name,
            "main_text": main_text,
            "dataset_type": str(dataset_type),
            "ensemble": str(ensemble),
            "password": password,
        }
        files = {"zipfile": open(zip_path, "rb")}
        response = self._make_request(
            "POST", "quality_checker/add", data=data, files=files
        )
        return response.json()
