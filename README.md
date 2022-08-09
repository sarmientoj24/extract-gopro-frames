# extract-gopro-frames
A script for extracting image frames from GoPro Video for every X meters


# Setup (Manual for Windows or Ubuntu)
1. Install Go.
2. Install required Python libraries from the requirements.txt with `pip install -r requirements.txt`
3. Install `ffmpeg`.
    For Ubuntu 18+ you can use `snap` to install `ffmpeg`
    ```
    # Install using snap
    sudo snap install ffmpeg

    # Check if properly installed
    ffmpeg --version
    ```

    If it doesn't work, you can go [here](https://linuxize.com/post/how-to-install-ffmpeg-on-ubuntu-18-04/).

    For Windows, follow instructions [here](https://lucaselbert.medium.com/extracting-gopro-gps-and-other-telemetry-data-fadf97ed1834) up to Step #2

4. Follow instructions 5-8 [here](https://lucaselbert.medium.com/extracting-gopro-gps-and-other-telemetry-data-fadf97ed1834)

If the instructions are unclear for the setup in Windows, kindly follow the instructions here up to **Step 8**.
https://lucaselbert.medium.com/extracting-gopro-gps-and-other-telemetry-data-fadf97ed1834

# Easier setup for Ubuntu
I also created a setup script that uses `snap` to install `Go` and `ffmpeg` and sets up the whole thing.

    chmod +x setup_ubuntu.sh
    ./setup_ubuntu.sh /path/to/go

After this, you just need to run the essential scripts.

# Running
Files that will be created are in this tree structure:
```
├── extract_frames.py
├── extract_telemetry.py
├── GH051804.MP4                <---- video file
├── README.md
├── requirements.txt
├── setup_ubuntu.sh
└── tmp
    └── GH051804
        ├── GH051804-accl.csv
        ├── GH051804.bin        <---- bin file
        ├── GH051804-gps.csv    <---- gps csv
        ├── GH051804-gyro.csv
        ├── GH051804-temp.csv
        └── frames              <---- contains image frames
            ├── 00:01.GH051804.jpg
```

1. Extract telemetry data
    This creates the `.bin` file and the `gps` csv file.
    ```
        python extract_telemetry.py --filepath XXXXX.MP4
    ```
2. Extract image frames from the video using the `.gps` file that was created.
    ```
        python extract_frames.py --video XXXXX.MP4 \
            --gps_csv tmp/XXXXX/XXXXX-gps.csv \
            --interval 5
    ```

    `interval` is in meters. Image frames are extracted for each `interval` meters. For this, image frames per 5 meters are extracted from the video.
