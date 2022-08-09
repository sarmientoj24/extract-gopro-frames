import logging
import os

import cv2
import fire
import geopy.distance as dist
import pandas as pd

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


def read_dataframe_from_csv(filepath):
    df = pd.read_csv(filepath)
    df["time"] = pd.to_datetime(df["Milliseconds"], unit="ms").dt.time

    return df


TMP_DIR = "tmp"


def extract_frames(video, gps_csv, interval=5):
    file_name = os.path.basename(video)
    basename = os.path.splitext(file_name)[0]
    save_path = os.path.join(TMP_DIR, basename, "frames")

    df = read_dataframe_from_csv(gps_csv)

    # Get data from dataframe
    data_time = [t.strftime("%H:%M:%S.%f")[:-3] for t in df.time.tolist()]
    lats = df["Latitude"].tolist()
    long = df["Longitude"].tolist()
    millis = df["Milliseconds"].tolist()

    # Latitude-Longitude-Time
    data = list(zip(lats, long, data_time))

    time_frames = []
    indices = []

    # Start indices
    i = 0
    cnt = 0

    # Append start frame of the video at time 0
    time_frames.append(data_time[i])
    indices.append(i)

    # Loop on per data row
    # Save timeframes and indices of timestamp where the position
    # is x meters greater than the last

    LOGGER.info("Calculating location of per intervals...")
    while i < len(data):
        lat, long, data_time = data[i]
        j = i + 1

        while j < len(data):
            n_lat, n_long, n_data_time = data[j]
            mdist = dist.distance((lat, long), (n_lat, n_long)).km * 1000

            if mdist >= interval:
                time_frames.append(n_data_time)
                indices.append(j)
                cnt += 1
                break
            j += 1
        i = j

    # Get milliseconds
    ms = [millis[i] for i in indices]

    LOGGER.info("Extracting frames from the video...")
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()

    frame_count = 0
    saved_frames = 0
    time_frame = None

    while success:
        if frame_count % 50 == 0 and frame_count > 0:
            LOGGER.info(f"Reading at timestamp: {time_frame}")
        if frame_count == len(time_frames):
            break
        time_frame = time_frames[frame_count]
        vidcap.set(cv2.CAP_PROP_POS_MSEC, ms[frame_count])  # added this line
        success, image = vidcap.read()
        if success:
            img_name = f"{time_frame}_{basename}.jpg"
            cv2.imwrite(f"{os.path.join(save_path, img_name)}", image)
            saved_frames += 1
        else:
            LOGGER.info(f"Error reading at frame: {time_frame}!")
            success = True
        frame_count += 1

    LOGGER.info(f"Extracted {saved_frames} frames...")


if __name__ == "__main__":
    fire.Fire(extract_frames)
