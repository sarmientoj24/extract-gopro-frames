import logging
import os
import subprocess

import fire

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S",
    )
)
LOGGER.addHandler(sh)


TMP_DIR = "tmp"
GPMD2CSV_PATH = "src/github.com/JuanIrache/gopro-utils/bin/gpmd2csv"


def make_bin(filepath):
    """
    Runs the ff command to create a bin file to be used for telemetry data extraction
        ffmpeg -y -i xxxx.MP4 -codec copy -map 0:3 -f rawvideo xxxx.bin
    Args:
        filepath: str
            path to the MP4 file
    ------------------
    """
    ### ffmpeg -y -i xxxx.MP4 -codec copy -map 0:3 -f rawvideo xxxx.bin
    file_name = os.path.basename(filepath)
    basename = os.path.splitext(file_name)[0]
    bin_file = f"{basename}.bin"
    bin_path = os.path.join(TMP_DIR, basename, bin_file)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        filepath,
        "-codec",
        "copy",
        "-map",
        "0:3",
        "-f",
        "rawvideo",
        bin_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    result.check_returncode()

    if result.returncode != 0:
        LOGGER.error("WARNING! Running {cmd} failed. Stopping script...")
        exit()

    LOGGER.info(f"Saved bin file to {bin_path}")
    return bin_path


def extract_gps_telemetry(bin_path):
    """
    Runs the ff command to extract telemetry data
        ./gpmd2csv -i GH030013.bin -o GH030013.csv
    Args:
        filepath: str
            path to the bin file
    ------------------
    """
    """
        ./gpmd2csv -i GH030013.bin -o GH030013.csv
    """
    try:
        
    except Exception as e:
        LOGGER.error("Set GOLANG PATH")
        raise e
#     golang_path = os.environ.get("GOLANG_PATH")

    # Get csv filename
    csv_file = bin_path.replace(".bin", ".csv")

    # Get current directory so we can go back
    PWD = os.getcwd()

    # Append current working directory path
    bin_path = os.path.join(PWD, bin_path)
    csv_path = os.path.join(PWD, csv_file)

    # Change directory to GOLANG Path
#     target_path = os.path.join(golang_path, GPMD2CSV_PATH)
#     os.chdir(target_path)
#     LOGGER.info(f"Changed directory to {target_path}")

    # Run CLI command
    cmd = ["./gpmd2csv", "-i", bin_path, "-o", csv_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    result.check_returncode()

    # Get back to parent dir
    os.chdir(PWD)
    LOGGER.info(f"Changed directory back to {PWD}")

    if result.returncode != 0:
        LOGGER.error("WARNING! Running {cmd} failed. Stopping script...")
        exit()

    LOGGER.info(f"Saved telemetry data to {csv_path}")


def extract_telemetry(filepath: str):
    file_name = os.path.basename(filepath)
    basename = os.path.splitext(file_name)[0]

    # Create tmp/<base_name>/ inside the parent directory
    os.makedirs(os.path.join(TMP_DIR, basename), exist_ok=True)

    bin_path = make_bin(filepath)
    extract_gps_telemetry(bin_path)


if __name__ == "__main__":
    fire.Fire(extract_telemetry)
