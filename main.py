import os
import random
import time
import threading
from pynput import mouse
import vlc
from dotenv import load_dotenv
import logging
import signal
import sys

load_dotenv()

# Configuration from .env
MEDIA_FOLDER = os.getenv('MEDIA_FOLDER', '/path/to/media_folder')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_SECONDS', '10'))  # seconds
IMAGE_DISPLAY_TIME = float(os.getenv('IMAGE_DISPLAY_TIME', '3'))  # seconds
VIDEO_DISPLAY_TIME = float(os.getenv('VIDEO_DISPLAY_TIME', '5'))  # seconds

IMAGE_EXTENSIONS = os.getenv('IMAGE_EXTENSIONS', '.jpg,.jpeg,.png,.gif,.bmp').split(',')
VIDEO_EXTENSIONS = os.getenv('VIDEO_EXTENSIONS', '.mp4,.avi,.mov,.mkv').split(',')

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize VLC player
instance = vlc.Instance()
player = instance.media_player_new()

timer = None  # Initialize timer variable

# Track user activity
last_activity = time.time()
activity_lock = threading.Lock()

def on_move(x, y):
    global last_activity
    with activity_lock:
        last_activity = time.time()

def on_click(x, y, button, pressed):
    global last_activity
    if pressed:
        with activity_lock:
            last_activity = time.time()

def monitor_mouse():
    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        listener.join()

def select_random_media():
    """Select a random media file from MEDIA_FOLDER."""
    media_files = [
        f for f in os.listdir(MEDIA_FOLDER)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS + VIDEO_EXTENSIONS
    ]
    if not media_files:
        return None, None
    media_file = random.choice(media_files)
    media_path = os.path.join(MEDIA_FOLDER, media_file)
    _, ext = os.path.splitext(media_file)
    ext = ext.lower()
    media_type = 'image' if ext in IMAGE_EXTENSIONS else 'video'
    return media_path, media_type

def play_image(media_path):
    """Play an image for IMAGE_DISPLAY_TIME seconds."""
    global timer
    with activity_lock:
        if timer is not None:
            timer.cancel()
        media = instance.media_new(media_path)
        player.set_media(media)
        player.play()
        # Start a timer to stop the image after IMAGE_DISPLAY_TIME
        timer = threading.Timer(IMAGE_DISPLAY_TIME, stop_player)
        timer.start()

def play_video(media_path):
    """Play a video for VIDEO_DISPLAY_TIME seconds or until it ends."""
    global timer
    with activity_lock:
        if timer is not None:
            timer.cancel()
        media = instance.media_new(media_path)
        player.set_media(media)
        player.play()
        # Start a timer to stop the video after VIDEO_DISPLAY_TIME seconds
        timer = threading.Timer(VIDEO_DISPLAY_TIME, stop_player)
        timer.start()

def stop_player():
    """Stop the VLC player."""
    global timer
    with activity_lock:
        if player.is_playing():
            player.stop()
        if timer is not None:
            timer.cancel()
            timer = None

def on_media_end(event):
    """Callback when media playback ends."""
    global timer
    with activity_lock:
        if timer is not None:
            timer.cancel()  # Cancel the timer if media ends naturally
    threading.Thread(target=handle_next_media, daemon=True).start()

def handle_next_media():
    """Handle the playback of the next media item."""
    media_path, media_type = select_random_media()
    if not media_path:
        logger.warning("No valid media files found in the MEDIA_FOLDER.")
        return

    if media_type == 'image':
        play_image(media_path)
    else:
        play_video(media_path)

def play_media_loop():
    """Main playback loop managed by VLC events."""
    # Set up event manager
    event_manager = player.event_manager()
    event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, on_media_end)

    while True:
        with activity_lock:
            idle_time = time.time() - last_activity

        if idle_time > CHECK_INTERVAL:
            if not player.is_playing():
                handle_next_media()
        else:
            if player.is_playing():
                stop_player()
            time.sleep(1)  # Check every second

def signal_handler(sig, frame):
    """Handle termination signals."""
    logger.info("Shutting down gracefully...")
    stop_player()
    sys.exit(0)

if __name__ == '__main__':
    # Validate MEDIA_FOLDER
    if not os.path.isdir(MEDIA_FOLDER):
        logger.error(f"MEDIA_FOLDER does not exist: {MEDIA_FOLDER}")
        exit(1)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start mouse monitoring in a separate thread
    mouse_thread = threading.Thread(target=monitor_mouse, daemon=True)
    mouse_thread.start()

    # Start media playback loop
    try:
        play_media_loop()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        stop_player()