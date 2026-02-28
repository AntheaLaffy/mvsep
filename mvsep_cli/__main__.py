#!/usr/bin/env python3
import argparse
import sys
import os
import time

from mvsep_cli.api import MVSEP_API
from mvsep_cli.config import Config, get_api_token


def cmd_upload(args):
    import sys

    api = MVSEP_API(get_api_token())
    config = Config()

    output_format = (
        args.output_format
        if args.output_format is not None
        else config.default_output_format
    )
    sep_type = args.sep_type if args.sep_type is not None else config.default_sep_type

    print(f"Audio file: {args.audio_file}", flush=True)
    print(f"Separation type: {sep_type}", flush=True)
    print(f"Output format: {output_format}", flush=True)
    print("Note: Uploading large file, please wait...", flush=True)

    result = api.create_task(
        audio_file=args.audio_file,
        sep_type=sep_type,
        output_format=output_format,
        add_opt1=args.add_opt1,
        add_opt2=args.add_opt2,
        add_opt3=args.add_opt3,
        is_demo=args.is_demo,
    )

    hash_val = result["hash"]
    print(f"\nTask created!", flush=True)
    print(f"Hash: {hash_val}", flush=True)
    print(f"Link: {result['link']}", flush=True)
    print(f"\nUse following commands to check status:", flush=True)
    print(f"  mvsep status {hash_val}", flush=True)
    print(f"  mvsep wait {hash_val}", flush=True)
    print(f"  mvsep download {hash_val}", flush=True)

    if args.wait:
        interval = args.interval if args.interval is not None else config.poll_interval
        print("\nWaiting for completion...")
        try:
            final_result = api.wait_for_completion(
                hash_val, interval=interval, max_wait=args.timeout
            )
            status = final_result.get("status")
            if status == "done":
                output_dir = (
                    args.output_dir if args.output_dir else config.default_output_dir
                )
                if not output_dir:
                    output_dir = os.path.dirname(os.path.abspath(args.audio_file))
                downloaded = api.download_results(hash_val, output_dir)
                print(f"\nDownloaded {len(downloaded)} files:")
                for f in downloaded:
                    print(f"  - {f}")
                return 0
        except TimeoutError:
            print(
                f"\nTimeout, but task is still running. Use 'mvsep wait {hash_val}' to continue waiting."
            )

    return 0


def cmd_status(args):
    api = MVSEP_API(get_api_token())

    result = api.get_status(args.hash)
    status = result.get("status")

    print(f"Task hash: {args.hash}")
    print(f"Status: {status}")

    if status == "done":
        data = result.get("data", {})
        print(f"Algorithm: {data.get('algorithm')}")
        print(f"Output format: {data.get('output_format')}")
        files = data.get("files", [])
        print(f"Output files ({len(files)}):")
        for f in files:
            name = f.get("name") or "unknown"
            url = f.get("url", "N/A")
            print(f"  - {name}: {url}")
    elif status == "failed":
        msg = result.get("data", {}).get("message", "Unknown error")
        print(f"Error: {msg}")
    elif status in ("waiting", "distributing"):
        queue = result.get("data", {}).get("queue_count", "?")
        order = result.get("data", {}).get("current_order", "?")
        print(f"Queue count: {queue}")
        print(f"Current order: {order}")
    elif status == "processing":
        print("Task is being processed...")
    elif status == "merging":
        chunks = result.get("data", {}).get("finished_chunks", "?")
        total = result.get("data", {}).get("all_chunks", "?")
        print(f"Merging: {chunks}/{total} chunks")

    return 0 if status == "done" else 1


def cmd_wait(args):
    api = MVSEP_API(get_api_token())
    config = Config()

    interval = args.interval if args.interval is not None else config.poll_interval

    print(f"Waiting for task {args.hash} to complete...")
    print(f"Polling interval: {interval}s")

    try:
        result = api.wait_for_completion(
            args.hash, interval=interval, max_wait=args.timeout
        )

        status = result.get("status")

        if status == "done":
            print("\nTask completed successfully!")
            data = result.get("data", {})
            print(f"Algorithm: {data.get('algorithm')}")
            files = data.get("files", [])
            print(f"Output files: {len(files)}")
            return 0
        elif status == "failed":
            msg = result.get("data", {}).get("message", "Unknown error")
            print(f"\nTask failed: {msg}")
            return 1
        else:
            print(f"\nTask status: {status}")
            return 1

    except TimeoutError as e:
        print(f"\nTimeout: {e}")
        return 1


def cmd_download(args):
    api = MVSEP_API(get_api_token())
    config = Config()

    output_dir = args.output_dir if args.output_dir else config.default_output_dir

    print(f"Downloading results for {args.hash}...")

    downloaded = api.download_results(args.hash, output_dir)

    print(f"\nDownloaded {len(downloaded)} files:")
    for f in downloaded:
        print(f"  - {f}")

    return 0


def cmd_run(args):
    api = MVSEP_API(get_api_token())
    config = Config()

    # Use args value if provided, otherwise use config default
    output_format = (
        args.output_format
        if args.output_format is not None
        else config.default_output_format
    )
    # sep_type is required, no default
    sep_type = args.sep_type if args.sep_type is not None else None
    interval = args.interval if args.interval is not None else config.poll_interval

    if sep_type is None:
        print(
            "Error: sep_type is required. Use -t <type> or mvsep list to see available types."
        )
        return 1

    print(f"Starting separation task for: {args.audio_file}")
    print(f"Separation type: {sep_type}")
    print(f"Output format: {output_format}")

    result = api.create_task(
        audio_file=args.audio_file,
        sep_type=sep_type,
        output_format=output_format,
        add_opt1=args.add_opt1,
        add_opt2=args.add_opt2,
        add_opt3=args.add_opt3,
        is_demo=args.is_demo,
    )

    hash_value = result["hash"]
    print(f"\nTask created! Hash: {hash_value}")
    print("Waiting for completion...")

    try:
        final_result = api.wait_for_completion(
            hash_value, interval=interval, max_wait=args.timeout
        )

        status = final_result.get("status")

        if status == "done":
            print("\nSeparation completed!")

            output_dir = (
                args.output_dir if args.output_dir else config.default_output_dir
            )
            if not output_dir:
                output_dir = os.path.dirname(os.path.abspath(args.audio_file))
            downloaded = api.download_results(hash_value, output_dir)

            print(f"\nDownloaded {len(downloaded)} files:")
            for f in downloaded:
                print(f"  - {f}")

            return 0
        else:
            print(f"\nTask ended with status: {status}")
            return 1

    except TimeoutError as e:
        print(f"\nTimeout: {e}")
        return 1


def cmd_config(args):
    config = Config()

    if not args.subcommand:
        print(
            "Usage: mvsep config <show|set-token|set-mirror|set-output-dir|set-output-format|set-interval>"
        )
        print("\nCommands:")
        print("  show                 Show current config")
        print("  set-token <token>   Set API token")
        print("  set-mirror <mirror> Set mirror (main/mirror)")
        print("  set-output-dir <dir> Set default output directory")
        print("  set-output-format <val>  Set default output format")
        print("  set-interval <val>  Set poll interval")
        return 0

    if args.subcommand == "show":
        print(
            f"API Token: {'*' * 8}{config.api_token[-4:] if config.api_token else 'Not set'}"
        )
        print(f"Mirror: {config.mirror} ({config.base_url})")
        print(f"Default output_dir: {config.default_output_dir}")
        print(f"Default output_format: {config.default_output_format}")
        print(f"Poll interval: {config.poll_interval}s")

    elif args.subcommand == "set-token":
        if not args.token:
            print("Error: Token required. Usage: mvsep config set-token <token>")
            return 1
        config.api_token = args.token
        print("API token saved!")

    elif args.subcommand == "set-mirror":
        if not args.value:
            print(
                "Error: Mirror required. Usage: mvsep config set-mirror <main|mirror>"
            )
            return 1
        try:
            config.mirror = args.value
            print(f"Mirror set to: {args.value} ({config.base_url})")
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    elif args.subcommand == "set-output-dir":
        config.default_output_dir = args.value
        print(f"Default output_dir set to: {args.value}")

    elif args.subcommand == "set-output-format":
        config.default_output_format = args.value
        print(f"Default output_format set to: {args.value}")

    elif args.subcommand == "set-interval":
        config.poll_interval = args.value
        print(f"Poll interval set to: {args.value}s")

    return 0


def cmd_history(args):
    import json
    from mvsep_cli.api import TASK_META_FILE

    if not os.path.exists(TASK_META_FILE):
        print("No task history found.")
        return 0

    with open(TASK_META_FILE, "r") as f:
        meta = json.load(f)

    if not meta:
        print("No task history found.")
        return 0

    print(f"Task history ({len(meta)} tasks):")
    print()
    for hash_val, info in meta.items():
        original_name = info.get("original_name", "unknown")
        print(f"  {hash_val}")
        print(f"    Original file: {original_name}")
        print(f"    Download: mvsep download {hash_val}")
        print()


def cmd_list_types(args):
    from mvsep_cli.api import MVSEP_API

    api = MVSEP_API(get_api_token())
    algorithms = api.get_algorithms()

    if args.models:
        for algo in algorithms:
            if algo["render_id"] == args.models:
                print(f"Separation type: {algo['render_id']} - {algo['name']}")
                print(f"\nModel options:")
                import json

                for field in algo.get("algorithm_fields", []):
                    print(f"\n  {field['name']}:")
                    try:
                        options = json.loads(field["options"])
                        for key, value in sorted(
                            options.items(), key=lambda x: str(x[0])
                        ):
                            print(f"    {key}: {value}")
                    except (json.JSONDecodeError, KeyError):
                        pass
                return 0
        print(f"Algorithm with ID {args.models} not found.")
        return 1

    if args.search:
        keyword = args.search.lower()
        results = [
            (algo["render_id"], algo["name"])
            for algo in algorithms
            if keyword in algo["name"].lower()
        ]
        if results:
            print(f"Search results for '{args.search}':")
            for val, name in results:
                print(f"  {val}: {name}")
        else:
            print(f"No results found for '{args.search}'")
        return 0

    if args.popular:
        print("Popular separation types:")
        for algo in sorted(algorithms, key=lambda x: x["render_id"])[:10]:
            print(f"  {algo['render_id']}: {algo['name']}")
    else:
        print("All separation types:")
        for algo in sorted(algorithms, key=lambda x: x["render_id"]):
            print(f"  {algo['render_id']}: {algo['name']}")
    return 0


def cmd_algorithms(args):
    from mvsep_cli.api import MVSEP_API

    api = MVSEP_API(get_api_token(), debug=args.debug)

    if args.id:
        algorithms = api.get_algorithms()
        for algo in algorithms:
            if algo["render_id"] == args.id:
                print(f"Separation type: {algo['render_id']} - {algo['name']}")
                print(f"\nModel options:")
                for field in algo.get("algorithm_fields", []):
                    print(f"\n  {field['name']}:")
                    import json

                    try:
                        options = json.loads(field["options"])
                        for key, value in sorted(
                            options.items(), key=lambda x: str(x[0])
                        ):
                            print(f"    {key}: {value}")
                    except (json.JSONDecodeError, KeyError):
                        pass
                return 0
        print(f"Algorithm with ID {args.id} not found.")
        return 1

    algo_dict = api.get_algorithms_formatted()
    for algo_id in sorted(algo_dict.keys()):
        print(algo_dict[algo_id])

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="MVSEP CLI - Music separation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    p_upload = subparsers.add_parser(
        "upload", help="Upload audio and create separation task"
    )
    p_upload.add_argument("audio_file", help="Audio file to process")
    p_upload.add_argument(
        "-t",
        "--sep-type",
        type=int,
        default=None,
        help="Separation type (default: config value)",
    )
    p_upload.add_argument(
        "-f",
        "--output-format",
        type=int,
        default=None,
        help="Output format (default: config value)",
    )
    p_upload.add_argument("--add-opt1", help="Additional option 1")
    p_upload.add_argument("--add-opt2", help="Additional option 2")
    p_upload.add_argument("--add-opt3", help="Additional option 3")
    p_upload.add_argument(
        "--demo", dest="is_demo", action="store_true", help="Publish to demo page"
    )
    p_upload.add_argument(
        "--wait", action="store_true", help="Wait for completion after upload"
    )
    p_upload.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for downloaded files",
    )
    p_upload.add_argument(
        "-i", "--interval", type=int, default=None, help="Poll interval in seconds"
    )
    p_upload.add_argument("--timeout", type=int, help="Max wait time in seconds")
    p_upload.set_defaults(func=cmd_upload)

    p_status = subparsers.add_parser("status", help="Check task status")
    p_status.add_argument("hash", help="Task hash")
    p_status.set_defaults(func=cmd_status)

    p_wait = subparsers.add_parser("wait", help="Wait for task completion")
    p_wait.add_argument("hash", help="Task hash")
    p_wait.add_argument(
        "-i", "--interval", type=int, default=None, help="Poll interval in seconds"
    )
    p_wait.add_argument("--timeout", type=int, help="Max wait time in seconds")
    p_wait.set_defaults(func=cmd_wait)

    p_download = subparsers.add_parser("download", help="Download results")
    p_download.add_argument("hash", help="Task hash")
    p_download.add_argument("-o", "--output-dir", default=None, help="Output directory")
    p_download.set_defaults(func=cmd_download)

    p_run = subparsers.add_parser(
        "run", help="Run full workflow (upload + wait + download)"
    )
    p_run.add_argument("audio_file", help="Audio file to process")
    p_run.add_argument(
        "-t",
        "--sep-type",
        type=int,
        default=None,
        help="Separation type (default: config value)",
    )
    p_run.add_argument(
        "-f",
        "--output-format",
        type=int,
        default=None,
        help="Output format (default: config value)",
    )
    p_run.add_argument("--add-opt1", help="Additional option 1")
    p_run.add_argument("--add-opt2", help="Additional option 2")
    p_run.add_argument("--add-opt3", help="Additional option 3")
    p_run.add_argument(
        "--demo", dest="is_demo", action="store_true", help="Publish to demo page"
    )
    p_run.add_argument(
        "-o", "--output-dir", type=str, default=None, help="Output directory"
    )
    p_run.add_argument(
        "-i", "--interval", type=int, default=None, help="Poll interval in seconds"
    )
    p_run.add_argument("--timeout", type=int, help="Max wait time in seconds")
    p_run.set_defaults(func=cmd_run)

    p_config = subparsers.add_parser("config", help="Configuration management")
    p_config_sub = p_config.add_subparsers(dest="subcommand", help="Config commands")
    p_config_sub.add_parser("show", help="Show current config")
    p_config_set = p_config_sub.add_parser("set-token", help="Set API token")
    p_config_set.add_argument("token", help="API token")

    p_set_dir = p_config_sub.add_parser(
        "set-output-dir", help="Set default output directory"
    )
    p_set_dir.add_argument("value", type=str, help="Directory path")

    p_set_mirror = p_config_sub.add_parser(
        "set-mirror", help="Set mirror (main or mirror)"
    )
    p_set_mirror.add_argument("value", type=str, help="Mirror: main or mirror")

    p_set_fmt = p_config_sub.add_parser(
        "set-output-format", help="Set default output format"
    )
    p_set_fmt.add_argument("value", type=int, help="Value")

    p_set_int = p_config_sub.add_parser("set-interval", help="Set poll interval")
    p_set_int.add_argument("value", type=int, help="Value")

    p_config.set_defaults(func=cmd_config)

    p_list = subparsers.add_parser("list", help="List available options")
    p_list.add_argument(
        "--popular", action="store_true", help="Show popular separation types"
    )
    p_list.add_argument("--formats", action="store_true", help="Show output formats")
    p_list.add_argument(
        "--models",
        type=int,
        metavar="SEP_TYPE",
        help="Show model options for a separation type",
    )
    p_list.add_argument(
        "-s",
        "--search",
        type=str,
        metavar="KEYWORD",
        help="Search separation types by keyword",
    )
    p_list.set_defaults(func=cmd_list_types)

    p_algos = subparsers.add_parser(
        "algorithms", help="List available algorithms from API"
    )
    p_algos.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug output"
    )
    p_algos.add_argument(
        "-i", "--id", type=int, help="Show detailed options for a specific algorithm ID"
    )
    p_algos.set_defaults(func=cmd_algorithms)

    p_history = subparsers.add_parser("history", help="Show task history")
    p_history.set_defaults(func=cmd_history)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        return args.func(args) or 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
