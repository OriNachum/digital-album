# Digital Album

This repository provides a Python-based media playback application that monitors mouse activity to detect user inactivity and plays random media files (images or videos) when the user is idle. The application uses `pynput` for mouse tracking and `vlc` for media playback.

---

## Features Checklist

- [x] Define images and videos by file extension
- [x] Separate play duration for images and videos
- [x] Configurable idle time and media stash location  

---

## Assumptions

1. **Media Files:** The application assumes that the `MEDIA_FOLDER` contains valid media files (images and/or videos).
2. **Dependencies Installed:** Required Python packages (`pynput`, `python-vlc`, `python-dotenv`) are installed in your environment.
3. **VLC Installed:** VLC media player is installed and accessible on the system.
4. **Environment Variables:** Configuration is managed using a `.env` file with the required variables.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/media-playback-idle-detector.git
   cd media-playback-idle-detector
   ```

2. Install required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install VLC media player (if not already installed):

   - **Linux:**
     ```bash
     sudo apt install vlc
     ```
   - **MacOS:** Download and install from [VLC website](https://www.videolan.org/).
   - **Windows:** Download and install from [VLC website](https://www.videolan.org/).

4. Set up your `.env` file:

   ```env
   MEDIA_FOLDER=/path/to/media_folder
   CHECK_INTERVAL_SECONDS=10
   IMAGE_DISPLAY_TIME=3
   VIDEO_DISPLAY_TIME=5
   IMAGE_EXTENSIONS=.jpg,.jpeg,.png,.gif,.bmp
   VIDEO_EXTENSIONS=.mp4,.avi,.mov,.mkv
   ```

---

## Usage

1. Ensure the `MEDIA_FOLDER` contains the media files you want to play.
2. Run the script:
   ```bash
   python idle_detector.py
   ```
3. The application will:
   - Monitor mouse activity.
   - Play random media files when the user is idle for the configured interval.
   - Stop media playback upon detecting user activity.

---

## How It Works

1. **Mouse Monitoring:**

   - Listens for mouse movement and clicks using the `pynput` library.
   - Updates the `last_activity` timestamp on user activity.

2. **Idle Detection:**

   - Continuously checks the elapsed time since the last user activity.
   - Starts media playback if the user is idle for more than `CHECK_INTERVAL_SECONDS`.

3. **Media Playback:**

   - Randomly selects a media file from the `MEDIA_FOLDER`.
   - Uses VLC for playback, with separate timers for images and videos.

4. **Graceful Shutdown:**

   - Listens for termination signals (`SIGINT`, `SIGTERM`) to stop playback and exit cleanly.

---

## Configuration Options

- **`MEDIA_FOLDER`:** Path to the folder containing media files.
- **`CHECK_INTERVAL_SECONDS`:** Time (in seconds) of inactivity before media playback starts.
- **`IMAGE_DISPLAY_TIME`:** Time (in seconds) to display images.
- **`VIDEO_DISPLAY_TIME`:** Time (in seconds) to play videos.
- **`IMAGE_EXTENSIONS`:** Comma-separated list of supported image file extensions.
- **`VIDEO_EXTENSIONS`:** Comma-separated list of supported video file extensions.

---

## Troubleshooting

- **Media Playback Not Starting:**

  - Ensure the `MEDIA_FOLDER` contains valid media files.
  - Check VLC installation.

- **Dependencies Error:**

  - Verify that all required Python packages are installed.
  - Run: `pip install -r requirements.txt`

- **Incorrect Path Error:**

  - Double-check the `MEDIA_FOLDER` path in the `.env` file.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

Special thanks to all contributors and the open-source community for their invaluable tools and libraries.

