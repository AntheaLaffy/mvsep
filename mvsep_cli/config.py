import os
import json
from typing import Optional, Dict, List


DEFAULT_CONFIG_PATH = os.path.expanduser("~/.mvsep_cli_config")


class Config:
    DEFAULT_OUTPUT_FORMAT = 1
    DEFAULT_INTERVAL = 5
    DEFAULT_OUTPUT_DIR = "."
    DEFAULT_MIRROR = "main"

    MIRRORS = {
        "main": "https://mvsep.com",
        "mirror": "https://mirror.mvsep.com",
    }

    OUTPUT_FORMATS = {
        0: "mp3 (320 kbps)",
        1: "wav (16 bit)",
        2: "flac (16 bit)",
        3: "m4a (lossy)",
        4: "wav (32 bit)",
        5: "flac (24 bit)",
    }

    SEP_TYPES = {
        0: "spleeter",
        3: "UnMix",
        7: "MDX A/B",
        9: "Ultimate Vocal Remover VR",
        10: "Demucs3 Model",
        12: "MDX-B Karaoke",
        13: "Demucs2",
        14: "Zero Shot (Query Based)",
        15: "Danna Sep",
        16: "Byte Dance",
        17: "UVRv5 Demucs",
        18: "MVSep DNR",
        19: "MVSep Old Vocal Model",
        20: "Demucs4 HT",
        22: "Reverb Removal",
        23: "MDX B",
        24: "MVSep Demucs4HT DNR",
        25: "MDX23C",
        26: "Ensemble (vocals, instrum)",
        27: "Demucs4 Vocals 2023",
        28: "Ensemble (4 stems)",
        29: "MVSep Piano",
        30: "Ensemble All-In",
        31: "MVSep Guitar",
        33: "Vit Large 23",
        34: "MVSep Crowd removal",
        35: "MVSep MelBand Roformer",
        36: "BandIt Plus",
        37: "DrumSep",
        38: "LarsNet",
        39: "Whisper",
        40: "BS Roformer",
        41: "MVSep Bass",
        42: "MVSep MultiSpeaker",
        43: "MVSep Multichannel BS",
        44: "MVSep Drums",
        45: "BandIt v2",
        46: "SCNet",
        47: "DeNoise",
        48: "MelBand Roformer",
        49: "MVSep Karaoke",
        50: "Aspiration",
        51: "Apollo Enhancers",
        52: "MVSep Bowed Strings",
        53: "Medley Vox",
        54: "MVSep Wind",
        55: "Phantom Centre extraction",
        56: "MVSep DnR v3",
        57: "MVSep Male/Female separation",
        58: "MVSep Organ",
        59: "AudioSR",
        60: "FlashSR",
        61: "MVSep Saxophone",
        62: "Stable Audio Open Gen",
        63: "BS Roformer SW",
        64: "Parakeet",
        65: "MVSep Violin",
        66: "MVSep Acoustic Guitar",
        67: "MVSep Flute",
        68: "Matchering",
        69: "MVSep Viola",
        70: "MVSep Cello",
        71: "MVSep Trumpet",
        72: "MVSep Harp",
        73: "MVSep Double Bass",
        74: "MVSep Mandolin",
        75: "MVSep Trombone",
        76: "MVSep Tambourine",
        77: "MVSep Oboe",
        78: "MVSep Clarinet",
        79: "MVSep Digital Piano",
        80: "SOME",
        81: "MVSep Electric Guitar",
        82: "MVSep French Horn",
        83: "MVSep Banjo",
        84: "MVSep Marimba",
        85: "MVSep Glockenspiel",
        86: "MVSep Timpani",
        87: "MVSep Harmonica",
        88: "MVSep Synth",
        89: "MVSep Triangle",
        90: "MVSep Sitar",
        91: "MVSep Harpsichord",
        92: "MVSep Tuba",
        93: "MVSep Bassoon",
        94: "MVSep Congas",
        95: "MVSep Bells",
        96: "MVSep Ukulele",
        97: "MVSep Dobro",
        98: "MVSep Wind Chimes",
        99: "MVSep Accordion",
        101: "MVSep Lead/Rhythm Guitar",
        102: "MVSep Plucked Strings",
        103: "VibeVoice",
        104: "VibeVoice TTS",
        105: "MVSep Percussion",
        106: "MVSep Keys",
        107: "MVSep Brass",
        108: "MVSep Woodwind",
        109: "MVSep Xylophone",
        110: "MVSep Celesta",
        111: "MVSep SATB Choir",
        112: "MVSep Choir",
        113: "Transkun",
        114: "Basic Pitch",
        115: "Bark",
        116: "MVSep Bagpipes",
        117: "MVSep Braam",
    }

    MODEL_OPTIONS: Dict[int, Dict[str, List[Dict[str, str]]]] = {
        9: {
            "add_opt1": [
                {"value": "0", "name": "HP2-4BAND-3090_4band_arch-500m_1"},
                {"value": "1", "name": "HP2-4BAND-3090_4band_2"},
                {"value": "2", "name": "HP2-4BAND-3090_4band_1"},
                {"value": "3", "name": "HP_4BAND_3090"},
                {"value": "4", "name": "Vocal_HP_4BAND_3090"},
                {"value": "5", "name": "Vocal_HP_4BAND_3090_AGG"},
                {"value": "6", "name": "HP2-MAIN-MSB2-3BAND-3090"},
                {"value": "7", "name": "HP-4BAND-V2"},
                {"value": "8", "name": "HP-KAROKEE-MSB2-3BAND-3090"},
                {"value": "9", "name": "WIP-Piano-4band-129605kb"},
                {"value": "10", "name": "drums-4BAND-3090_4band"},
                {"value": "11", "name": "bass-4BAND-3090_4band"},
                {"value": "12", "name": "karokee_4band_v2_sn"},
                {"value": "13", "name": "UVR-De-Echo-Aggressive"},
                {"value": "14", "name": "UVR-De-Echo-Normal"},
                {"value": "15", "name": "UVR-DeNoise"},
                {"value": "16", "name": "UVR-DeEcho-DeReverb"},
                {"value": "17", "name": "UVR-BVE-4B_SN-44100-1"},
            ],
            "add_opt2": [
                {"value": "0.3", "name": "0.3"},
                {"value": "0.1", "name": "0.1"},
                {"value": "0.2", "name": "0.2"},
                {"value": "0.4", "name": "0.4"},
                {"value": "0.5", "name": "0.5"},
                {"value": "0.6", "name": "0.6"},
                {"value": "0.7", "name": "0.7"},
                {"value": "0.8", "name": "0.8"},
                {"value": "0.9", "name": "0.9"},
                {"value": "1.0", "name": "1.0"},
            ],
        },
        17: {
            "add_opt1": [
                {"value": "0", "name": "UVR_Demucs_Model_1"},
                {"value": "1", "name": "UVR_Demucs_Model_2"},
                {"value": "2", "name": "UVR_Demucs_Model_Bag"},
            ]
        },
        20: {
            "add_opt1": [
                {"value": "0", "name": "htdemucs_ft (High Quality, Slow)"},
                {"value": "1", "name": "htdemucs (Good Quality, Fast)"},
                {"value": "2", "name": "htdemucs_6s (6 stems, piano + guitar)"},
            ]
        },
        23: {
            "add_opt1": [
                {"value": "0", "name": "MDX UVR 2022.01.01 (SDR: 8.83)"},
                {"value": "1", "name": "MDX UVR 2022.07.25 (SDR: 8.67)"},
                {"value": "2", "name": "MDX Kimberley Jensen v1 (SDR: 9.48)"},
                {"value": "4", "name": "UVR-MDX-NET-Inst_HQ_2 (SDR: 9.12)"},
                {"value": "5", "name": "UVR_MDXNET_Main (SDR: 8.79)"},
                {"value": "6", "name": "MDX Kimberley Jensen Inst (SDR: 9.28)"},
                {"value": "7", "name": "MDX Kimberley Jensen v2 (SDR: 9.60)"},
                {"value": "8", "name": "UVR-MDX-NET-Inst_HQ_3 (SDR: 9.38)"},
                {"value": "9", "name": "UVR-MDX-NET-Voc_FT (SDR: 9.64)"},
                {"value": "11", "name": "UVR-MDX-NET-Inst_HQ_4 (SDR: 9.71)"},
                {"value": "12", "name": "UVR-MDX-NET-Inst_HQ_5 (SDR: 9.45)"},
            ]
        },
        24: {
            "add_opt1": [
                {"value": "0", "name": "Single (SDR: 9.62)"},
                {"value": "1", "name": "Ensemble (SDR: 10.16)"},
            ]
        },
        25: {
            "add_opt1": [
                {"value": "0", "name": "12K FFT (SDR: 9.68)"},
                {"value": "1", "name": "12K FFT, 6 Poolings (SDR: 9.49)"},
                {"value": "2", "name": "12K FFT, Large Conv (SDR: 9.71)"},
                {"value": "3", "name": "12K FFT, Large Conv, Hop 1024 (SDR: 9.95)"},
                {"value": "4", "name": "8K FFT (SDR: 10.17)"},
                {"value": "7", "name": "8K FFT (SDR: 10.36)"},
            ]
        },
        26: {
            "add_opt2": [
                {"value": "1", "name": "SDR Vocals 10.44"},
                {"value": "2", "name": "SDR Vocals 10.75"},
                {"value": "3", "name": "SDR Vocals 11.06"},
                {"value": "4", "name": "SDR Vocals 11.33"},
                {"value": "5", "name": "SDR Vocals 11.50"},
                {"value": "6", "name": "SDR Vocals 11.61"},
                {"value": "7", "name": "SDR Vocals 11.93"},
                {"value": "8", "name": "High Vocal Fullness (SDR: 11.69)"},
                {"value": "9", "name": "High Instrumental Fullness (SDR: 17.69)"},
            ]
        },
        28: {
            "add_opt2": [
                {"value": "1", "name": "SDR average: 11.21"},
                {"value": "2", "name": "SDR average: 11.87"},
                {"value": "3", "name": "SDR average: 12.03"},
                {"value": "4", "name": "SDR average: 12.17"},
                {"value": "5", "name": "SDR average: 12.34"},
                {"value": "6", "name": "SDR average: 12.66"},
                {"value": "7", "name": "SDR average: 12.76"},
                {"value": "8", "name": "SDR average: 12.84"},
                {"value": "9", "name": "SDR average: 13.01"},
                {"value": "10", "name": "SDR average: 13.07"},
                {"value": "11", "name": "SDR average: 13.67"},
            ]
        },
        30: {
            "add_opt2": [
                {"value": "1", "name": "SDR average: 11.21"},
                {"value": "2", "name": "SDR average: 11.87"},
                {"value": "3", "name": "SDR average: 12.03"},
                {"value": "4", "name": "SDR average: 12.17"},
                {"value": "5", "name": "SDR average: 12.32"},
                {"value": "6", "name": "SDR average: 12.66"},
                {"value": "7", "name": "SDR average: 12.76"},
                {"value": "8", "name": "SDR average: 12.84"},
                {"value": "9", "name": "SDR average: 13.01"},
                {"value": "10", "name": "SDR average: 13.07"},
                {"value": "11", "name": "SDR average: 13.67"},
            ]
        },
        40: {
            "add_opt1": [
                {"value": "3", "name": "ver. 2024.02 (SDR: 10.42)"},
                {"value": "4", "name": "viperx edition (SDR: 10.87)"},
                {"value": "5", "name": "ver 2024.04 (SDR: 11.24)"},
                {"value": "29", "name": "ver 2024.08 (SDR: 11.31)"},
                {"value": "81", "name": "ver 2025.07 (SDR: 11.89)"},
                {"value": "85", "name": "unwa high instrum fullness"},
                {"value": "142", "name": "unwa BS Roformer HyperACE v2 instrum"},
                {"value": "143", "name": "unwa BS Roformer HyperACE v2 vocals"},
            ]
        },
        41: {
            "add_opt1": [
                {"value": "0", "name": "BS Roformer (SDR: 12.49)"},
                {"value": "1", "name": "HTDemucs4 (SDR: 12.52)"},
                {"value": "2", "name": "SCNet XL (SDR: 13.81)"},
                {"value": "3", "name": "BS + HTDemucs + SCNet (SDR: 14.07)"},
                {"value": "4", "name": "BS Roformer SW (SDR: 14.62)"},
                {"value": "5", "name": "BS Roformer SW + SCNet XL (SDR: 14.87)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        44: {
            "add_opt1": [
                {"value": "0", "name": "HTDemucs (SDR: 12.04)"},
                {"value": "1", "name": "MelBand Roformer (SDR: 12.76)"},
                {"value": "2", "name": "SCNet Large (SDR: 13.01)"},
                {"value": "3", "name": "SCNet XL (SDR: 13.42)"},
                {"value": "4", "name": "Mel + SCNet XL (SDR: 13.78)"},
                {"value": "5", "name": "BS Roformer SW (SDR: 14.11)"},
                {"value": "6", "name": "Mel + SCNet XL + BS Roformer SW (SDR: 14.35)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        48: {
            "add_opt1": [
                {"value": "0", "name": "Kimberley Jensen edition (SDR: 11.01)"},
                {"value": "1", "name": "ver 2024.08 (SDR: 11.17)"},
                {"value": "2", "name": "Bas Curtiz edition (SDR: 11.18)"},
                {"value": "3", "name": "unwa Instrumental v1 (SDR: 10.24)"},
                {"value": "4", "name": "ver 2024.10 (SDR: 11.28)"},
                {"value": "5", "name": "unwa Instrumental v1e (SDR: 10.05)"},
                {"value": "6", "name": "unwa big beta v5e (SDR: 10.59)"},
                {"value": "7", "name": "becruily instrum high fullness"},
                {"value": "8", "name": "becruily vocals high fullness"},
                {"value": "9", "name": "unwa Instrumental v1e plus"},
                {"value": "10", "name": "gabox Instrumental v7"},
                {"value": "11", "name": "becruily deux (SDR: 11.35)"},
            ]
        },
        49: {
            "add_opt1": [
                {"value": "0", "name": "Model by viperx and aufr33 (SDR: 9.45)"},
                {"value": "1", "name": "Model by becruily (SDR: 9.61)"},
                {"value": "2", "name": "Model by gabox (SDR: 9.67)"},
                {"value": "3", "name": "Model fuzed gabox & aufr33/viperx (SDR: 9.85)"},
                {"value": "4", "name": "SCNet XL IHF by becruily (SDR: 9.53)"},
                {
                    "value": "5",
                    "name": "BS Roformer by frazer and becruily (SDR: 10.11)",
                },
                {"value": "6", "name": "BS Roformer by MVSep Team (SDR: 10.41)"},
                {"value": "7", "name": "BS Roformer by anvuew (SDR: 10.22)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Use as is"},
                {"value": "1", "name": "Extract vocals first"},
            ],
        },
        7: {
            "add_opt1": [
                {"value": "0", "name": "MDX A (Contest Version)"},
                {"value": "1", "name": "MDX UVR 2022.01.01 (SDR: 8.62)"},
                {"value": "2", "name": "MDX UVR 2022.07.25 (SDR: 8.51)"},
                {"value": "3", "name": "MDX Kimberley Jensen 2023.02.12 (SDR: 9.30)"},
            ]
        },
        12: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture (SDR: 6.81)"},
                {"value": "1", "name": "Extract from vocals part (SDR: 7.94)"},
            ]
        },
        33: {
            "add_opt1": [
                {"value": "0", "name": "v1 (SDR: 9.78)"},
                {"value": "1", "name": "v2 (SDR: 9.90)"},
            ]
        },
        34: {
            "add_opt1": [
                {"value": "0", "name": "Mel Roformer (SDR: 6.07)"},
                {"value": "1", "name": "Ensemble MDX23C + Mel Roformer (SDR: 6.27)"},
                {"value": "2", "name": "BS Roformer (SDR: 7.21)"},
                {"value": "8", "name": "MDX23C v1 (SDR: 5.57)"},
                {"value": "9", "name": "MDX23C v2 (SDR: 6.06)"},
            ]
        },
        37: {
            "add_opt1": [
                {"value": "0", "name": "DrumSep model by inagoy (HDemucs, 4 stems)"},
                {
                    "value": "1",
                    "name": "DrumSep model by aufr33 and jarredou (MDX23C, 4 stems)",
                },
                {"value": "2", "name": "DrumSep SCNet XL (5 stems)"},
                {"value": "3", "name": "DrumSep SCNet XL (6 stems)"},
                {"value": "4", "name": "DrumSep SCNet XL (4 stems)"},
                {"value": "5", "name": "DrumSep Ensemble of 4 models (8 stems)"},
                {"value": "6", "name": "DrumSep MelBand Roformer (4 stems)"},
                {"value": "7", "name": "DrumSep MelBand Roformer (6 stems)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Apply Drums model before"},
                {"value": "1", "name": "Use as is"},
            ],
        },
        38: {
            "add_opt1": [
                {"value": "0", "name": "Apply Demucs4HT first to get drums"},
                {"value": "1", "name": "Use as is"},
            ]
        },
        42: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from vocals part"},
            ]
        },
        43: {
            "add_opt1": [
                {"value": "0", "name": "BS Roformer (SDR: 11.81)"},
                {"value": "1", "name": "MDX23C (SDR: 10.36)"},
                {"value": "2", "name": "MelBand Roformer (SDR: 11.17)"},
                {"value": "3", "name": "MelBand Roformer XL (SDR: 11.28)"},
            ]
        },
        45: {
            "add_opt1": [
                {"value": "0", "name": "Multi language model"},
                {"value": "1", "name": "English model"},
                {"value": "2", "name": "German model"},
                {"value": "3", "name": "French model"},
                {"value": "4", "name": "Spanish model"},
                {"value": "5", "name": "Chinese model"},
                {"value": "6", "name": "Faroese model"},
            ]
        },
        46: {
            "add_opt1": [
                {"value": "0", "name": "SCNet (SDR: 10.25)"},
                {"value": "1", "name": "SCNet Large (SDR: 10.74)"},
                {"value": "2", "name": "SCNet XL (SDR: 10.96)"},
                {"value": "3", "name": "SCNet XL (high fullness)"},
                {"value": "4", "name": "SCNet XL (very high fullness)"},
                {"value": "5", "name": "SCNet XL IHF (SDR: 11.11)"},
                {"value": "6", "name": "SCNet XL IHF (high instrum fullness)"},
            ]
        },
        47: {
            "add_opt1": [
                {"value": "0", "name": "Standard"},
                {"value": "1", "name": "Aggressive"},
            ]
        },
        50: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from vocals part"},
            ]
        },
        51: {
            "add_opt1": [
                {"value": "0", "name": "MP3 Enhancer (by JusperLee)"},
                {"value": "1", "name": "Universal Super Resolution (by Lew)"},
                {"value": "2", "name": "Vocals Super Resolution (by Lew)"},
                {"value": "3", "name": "Universal Super Resolution (by MVSep Team)"},
                {"value": "4", "name": "Universal Super Resolution (by baicai1145)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "No cutoff"},
                {"value": "2000", "name": "2000 Hz"},
                {"value": "4000", "name": "4000 Hz"},
                {"value": "8000", "name": "8000 Hz"},
                {"value": "16000", "name": "16000 Hz"},
            ],
        },
        52: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C (SDR: 3.84)"},
                {"value": "1", "name": "BS Roformer (SDR: 5.41)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        53: {
            "add_opt1": [
                {"value": "0", "name": "Apply to original file"},
                {"value": "1", "name": "Extract vocals first"},
            ]
        },
        54: {
            "add_opt1": [
                {"value": "0", "name": "MelBand Roformer (SDR: 6.73)"},
                {"value": "1", "name": "SCNet Large (SDR: 6.76)"},
                {"value": "2", "name": "Mel + SCNet (SDR: 7.22)"},
                {"value": "3", "name": "BS Roformer (SDR: 9.82)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
            "add_opt3": [
                {"value": "0", "name": "Standard set"},
                {"value": "1", "name": "Include results of independent models"},
            ],
        },
        55: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract vocals first"},
            ]
        },
        56: {
            "add_opt1": [
                {"value": "0", "name": "SCNet Large (SDR: 11.22)"},
                {"value": "1", "name": "MelBand Roformer (SDR: 10.99)"},
                {"value": "2", "name": "Mel + SCNet (SDR: 11.54)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Use vocals model to help"},
            ],
            "add_opt3": [
                {"value": "0", "name": "Standard set"},
                {"value": "1", "name": "Include results of independent models"},
            ],
        },
        57: {
            "add_opt1": [
                {"value": "0", "name": "BSRoformer by Sucial (SDR: 6.52)"},
                {"value": "1", "name": "SCNet XL (SDR: 11.83)"},
                {"value": "2", "name": "MelRoformer (SDR: 13.03)"},
                {"value": "3", "name": "BSRoformer by aufr33 (SDR: 8.18)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract vocals first with BS Roformer"},
            ],
        },
        58: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL (SDR: 2.71)"},
                {"value": "1", "name": "MelBand Roformer (SDR: 2.77)"},
                {"value": "2", "name": "Mel + SCNet (SDR: 3.05)"},
                {"value": "3", "name": "BS Roformer (SDR: 5.08)"},
            ]
        },
        59: {
            "add_opt1": [
                {"value": "0", "name": "Automatic"},
                {"value": "2000", "name": "2000 Hz"},
                {"value": "4000", "name": "4000 Hz"},
                {"value": "6000", "name": "6000 Hz"},
                {"value": "8000", "name": "8000 Hz"},
                {"value": "11000", "name": "11000 Hz"},
                {"value": "16000", "name": "16000 Hz"},
                {"value": "22000", "name": "22000 Hz"},
            ]
        },
        60: {
            "add_opt1": [
                {"value": "0", "name": "Automatic"},
                {"value": "2000", "name": "2000 Hz"},
                {"value": "4000", "name": "4000 Hz"},
                {"value": "6000", "name": "6000 Hz"},
                {"value": "8000", "name": "8000 Hz"},
                {"value": "11000", "name": "11000 Hz"},
                {"value": "16000", "name": "16000 Hz"},
                {"value": "22000", "name": "22000 Hz"},
            ]
        },
        61: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL (SDR: 6.15)"},
                {"value": "1", "name": "MelBand Roformer (SDR: 6.97)"},
                {"value": "2", "name": "Mel + SCNet (SDR: 7.13)"},
                {"value": "3", "name": "BS Roformer (SDR: 9.77)"},
            ]
        },
        62: {
            "add_opt1": [
                {"value": "0", "name": "Text prompt"},
            ],
            "add_opt2": [
                {"value": "3", "name": "3 seconds"},
                {"value": "5", "name": "5 seconds"},
                {"value": "8", "name": "8 seconds"},
                {"value": "10", "name": "10 seconds"},
                {"value": "15", "name": "15 seconds"},
                {"value": "20", "name": "20 seconds"},
                {"value": "30", "name": "30 seconds"},
                {"value": "47", "name": "47 seconds"},
            ],
        },
        63: {
            "add_opt1": [
                {"value": "0", "name": "ver. 2024.02 (SDR: 10.42)"},
                {"value": "4", "name": "viperx edition (SDR: 10.87)"},
                {"value": "5", "name": "ver 2024.04 (SDR: 11.24)"},
                {"value": "29", "name": "ver 2024.08 (SDR: 11.31)"},
                {"value": "81", "name": "ver 2025.07 (SDR: 11.89)"},
                {"value": "85", "name": "unwa high instrum fullness"},
            ]
        },
        64: {
            "add_opt1": [
                {"value": "0", "name": "Apply to original file"},
                {"value": "1", "name": "Extract vocals first"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Parakeet v2"},
                {"value": "1", "name": "Parakeet v3"},
            ],
        },
        65: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from strings part"},
            ],
        },
        66: {
            "add_opt1": [
                {"value": "0", "name": "mdx23c (SDR: 4.78)"},
                {"value": "2", "name": "mdx23c (SDR: 6.34)"},
                {"value": "3", "name": "MelRoformer (SDR: 7.02)"},
                {"value": "5", "name": "BSRoformer (SDR: 7.16)"},
                {"value": "6", "name": "Ensemble (SDR: 7.51)"},
                {"value": "7", "name": "BS Roformer SW (SDR: 9.05)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from guitar part"},
            ],
        },
        67: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL (SDR: 6.27)"},
                {"value": "1", "name": "BS Roformer (SDR: 9.46)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        69: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from strings part"},
            ],
        },
        70: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from strings part"},
            ],
        },
        71: {
            "add_opt1": [
                {"value": "0", "name": "MelBand Roformer"},
                {"value": "1", "name": "SCNet Large"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        72: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "MelBand Roformer"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ]
        },
        73: {
            "add_opt1": [
                {"value": "0", "name": "BS Roformer"},
                {"value": "1", "name": "HTDemucs4"},
                {"value": "2", "name": "SCNet XL"},
                {"value": "3", "name": "BS + HTDemucs + SCNet"},
                {"value": "4", "name": "BS Roformer SW"},
                {"value": "5", "name": "BS Roformer SW + SCNet XL"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from strings part"},
            ],
        },
        74: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        75: {
            "add_opt1": [
                {"value": "0", "name": "MelBand Roformer"},
                {"value": "1", "name": "SCNet Large"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        76: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        77: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        78: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        79: {
            "add_opt1": [
                {"value": "0", "name": "mdx23c (SDR: 4.79)"},
                {"value": "1", "name": "mdx23c (SDR: 5.59)"},
                {"value": "2", "name": "MelRoformer (SDR: 5.71)"},
                {"value": "3", "name": "SCNet Large (SDR: 5.89)"},
                {"value": "4", "name": "Ensemble (SDR: 6.20)"},
                {"value": "5", "name": "BS Roformer SW (SDR: 7.83)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from piano part"},
            ],
        },
        81: {
            "add_opt1": [
                {"value": "0", "name": "mdx23c"},
                {"value": "2", "name": "mdx23c (2024.06)"},
                {"value": "3", "name": "MelRoformer"},
                {"value": "5", "name": "BSRoformer"},
                {"value": "6", "name": "Ensemble (BS + Mel)"},
                {"value": "7", "name": "BS Roformer SW"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from guitar part"},
            ],
        },
        82: {
            "add_opt1": [
                {"value": "0", "name": "MelBand Roformer"},
                {"value": "1", "name": "SCNet Large"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        83: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        84: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        85: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        86: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        87: {
            "add_opt1": [
                {"value": "0", "name": "MelBand Roformer"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        88: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ]
        },
        89: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        90: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        91: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "MelBand Roformer"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ]
        },
        92: {
            "add_opt1": [
                {"value": "0", "name": "MelBand Roformer"},
                {"value": "1", "name": "SCNet Large"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        93: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ],
        },
        94: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        95: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        96: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        97: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        98: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        99: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "MelBand Roformer"},
                {"value": "2", "name": "Mel + SCNet"},
                {"value": "3", "name": "BS Roformer"},
            ]
        },
        101: {
            "add_opt1": [
                {"value": "0", "name": "Two-stage model (SDR: 9.21)"},
                {"value": "1", "name": "One-stage model (SDR: 9.02)"},
            ]
        },
        102: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ],
        },
        103: {
            "add_opt1": [
                {"value": "0", "name": "VibeVoce 1.5B (Small)"},
                {"value": "1", "name": "VibeVoce 7B (Large)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Text prompt"},
            ],
            "add_opt3": [
                {"value": "0", "name": "Apply to original file"},
                {"value": "1", "name": "Extract vocals first"},
            ],
        },
        104: {
            "add_opt1": [
                {"value": "0", "name": "VibeVoce 1.5B (Small)"},
                {"value": "1", "name": "VibeVoce 7B (Large)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Text prompt"},
            ],
        },
        105: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ]
        },
        106: {
            "add_opt1": [
                {"value": "0", "name": "mdx23c (SDR: 4.79)"},
                {"value": "1", "name": "mdx23c (SDR: 5.59)"},
                {"value": "2", "name": "MelRoformer (SDR: 5.71)"},
                {"value": "3", "name": "SCNet Large (SDR: 5.89)"},
                {"value": "4", "name": "Ensemble (SDR: 6.20)"},
                {"value": "5", "name": "BS Roformer SW (SDR: 7.83)"},
            ]
        },
        107: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from wind part"},
            ]
        },
        108: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from instrumental part"},
            ]
        },
        109: {
            "add_opt1": [
                {"value": "0", "name": "MDX23C"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        110: {
            "add_opt1": [
                {"value": "0", "name": "SCNet XL"},
                {"value": "1", "name": "BS Roformer"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract from percussion part"},
            ],
        },
        111: {
            "add_opt1": [
                {"value": "2", "name": "SCNet Masked (SDR: 4.07)"},
                {"value": "3", "name": "BS Roformer (SDR: 7.39)"},
            ],
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract vocals first"},
            ],
        },
        112: {
            "add_opt2": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract vocals first"},
            ]
        },
        113: {
            "add_opt1": [
                {"value": "0", "name": "Extract directly from mixture"},
                {"value": "1", "name": "Extract piano first"},
            ]
        },
        114: {
            "add_opt1": [
                {"value": "0", "name": "Apply to original file"},
                {"value": "1", "name": "Extract vocals first"},
            ]
        },
        115: {
            "add_opt1": [
                {"value": "0", "name": "Text prompt"},
            ],
            "add_opt2": [
                {"value": "en_0", "name": "English Male 1"},
                {"value": "en_1", "name": "English Male 2"},
                {"value": "en_6", "name": "English Male 6 (Best)"},
                {"value": "en_9", "name": "English Female 1"},
                {"value": "zh_0", "name": "Chinese Male"},
                {"value": "zh_4", "name": "Chinese Female"},
                {"value": "ja_0", "name": "Japanese Female"},
                {"value": "ko_0", "name": "Korean Female"},
            ],
        },
    }

    POPULAR_SEP_TYPES = {
        20: "Demucs4 HT (vocals, drums, bass, other)",
        26: "Ensemble (vocals, instrum)",
        28: "Ensemble (4 stems)",
        30: "Ensemble All-In",
        40: "BS Roformer (vocals, instrumental)",
        25: "MDX23C (vocals, instrumental)",
        23: "MDX B (vocals, instrumental)",
        24: "Demucs4HT DNR (speech, music, effects)",
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._config = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    @property
    def api_token(self) -> Optional[str]:
        return self._config.get("api_token")

    @api_token.setter
    def api_token(self, value: str):
        self._config["api_token"] = value
        self.save()

    @property
    def default_sep_type(self) -> Optional[int]:
        return self._config.get("sep_type")

    @default_sep_type.setter
    def default_sep_type(self, value: int):
        self._config["sep_type"] = value
        self.save()

    @property
    def default_output_format(self) -> int:
        return self._config.get("output_format", self.DEFAULT_OUTPUT_FORMAT)

    @default_output_format.setter
    def default_output_format(self, value: int):
        self._config["output_format"] = value
        self.save()

    @property
    def poll_interval(self) -> int:
        return self._config.get("interval", self.DEFAULT_INTERVAL)

    @poll_interval.setter
    def poll_interval(self, value: int):
        self._config["interval"] = value
        self.save()

    @property
    def default_output_dir(self) -> str:
        return self._config.get("output_dir", self.DEFAULT_OUTPUT_DIR)

    @default_output_dir.setter
    def default_output_dir(self, value: str):
        self._config["output_dir"] = value
        self.save()

    @property
    def mirror(self) -> str:
        return self._config.get("mirror", self.DEFAULT_MIRROR)

    @mirror.setter
    def mirror(self, value: str):
        if value not in self.MIRRORS:
            raise ValueError(
                f"Invalid mirror. Available: {', '.join(self.MIRRORS.keys())}"
            )
        self._config["mirror"] = value
        self.save()

    @property
    def base_url(self) -> str:
        return self.MIRRORS.get(self.mirror, self.MIRRORS["main"])

    def get_model_options(
        self, sep_type: int
    ) -> Optional[Dict[str, List[Dict[str, str]]]]:
        return self.MODEL_OPTIONS.get(sep_type)


def get_api_token() -> str:
    env_token = os.environ.get("MVSEP_API_TOKEN")
    if env_token:
        return env_token

    config = Config()
    token = config.api_token
    if token:
        return token

    raise ValueError(
        "API token not found. Please either:\n"
        "  1. Set environment variable: export MVSEP_API_TOKEN='your_token'\n"
        "  2. Or configure with: mvsep config set-token <your_token>"
    )
