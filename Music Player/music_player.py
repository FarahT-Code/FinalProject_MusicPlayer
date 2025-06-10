import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
import os
import pygame

#=================================================================================

# Initialize the pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Global variables to track play/pause state, current track, and track index
is_playing = False
is_paused = False
current_track_index = 0

# Create the main window
root = tk.Tk()
root.title("Music Player")
root.geometry("250x400")
root.overrideredirect(1)
root.configure(bg="#323232")
root.wm_attributes("-transparent", "TRUE")

def move_app(e):
    root.geometry(f"+{e.x_root}+{e.y_root}")

# List of tracks and their corresponding cover images
tracks = [
    {"file": "Spring.mp3", "cover": "Image_spring.png"},
    {"file": "Summer.mp3", "cover": "Image_summer.png"},
    {"file": "Fall.mp3", "cover": "Image_fall.png"},
    {"file": "Winter.mp3", "cover": "Image_winter.png"}
]

def play_music(index):
    global is_playing, is_paused, current_track_index
    current_track_index = index
    track = tracks[current_track_index]
    pygame.mixer.music.load(os.path.expanduser(f"~/Documents/Music Player/{track['file']}"))
    pygame.mixer.music.play()
    update_cover()
    load_music()
    is_playing = True
    is_paused = False
    update_timeline()
    check_music_end()
    play_label.config(image=pause_photo)

def toggle_play_pause():
    global is_playing, is_paused, current_track_index
    if current_track_index < len(tracks):
        if is_playing and not is_paused:
            pygame.mixer.music.pause()
            is_paused = True
            play_label.config(image=play_photo)
        elif is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
            play_label.config(image=pause_photo)
        elif not is_playing:
            play_music(current_track_index)

def update_cover():
    track = tracks[current_track_index]
    cover_image = Image.open(os.path.expanduser(f"~/Documents/Music Player/{track['cover']}")).convert("RGBA")
    cover_scaled_image = cover_image.resize((250, 266), Image.LANCZOS)
    cover_photo = ImageTk.PhotoImage(cover_scaled_image)
    cover_label.config(image=cover_photo)
    cover_label.image = cover_photo
    cover_label.place(x=0, y=55)

def update_timeline():
    if is_playing and not is_paused:
        position = pygame.mixer.music.get_pos() / 1000
        timeline_scale.set(position)
    root.after(1000, update_timeline)

def check_music_end():
    global is_playing, is_paused, current_track_index
    if is_playing and not is_paused and not pygame.mixer.music.get_busy():
        is_playing = False
        is_paused = False
        if current_track_index < len(tracks) - 1:
            play_music(current_track_index + 1)
        else:
            play_music(0)  # Loop back to the first track
    else:
        root.after(1000, check_music_end)

def next_track():
    if current_track_index < len(tracks) - 1:
        play_music(current_track_index + 1)
    else:
        play_music(0)  # Loop to first track if at the end

def prev_track():
    if current_track_index > 0:
        play_music(current_track_index - 1)
    else:
        play_music(len(tracks) - 1)  # Loop to last track if at the start

def load_music():
    # Adjust timeline based on current track length
    global current_track_index
    track = tracks[current_track_index]
    try:
        audio = MP3(os.path.expanduser(f"~/Documents/Music Player/{track['file']}"))
        music_length = int(audio.info.length)  # Get track length in seconds
        timeline_scale.config(to=music_length)
        timeline_scale.set(0)  # Reset timeline position
    except Exception as e:
        print(f"Error getting music length: {e}")
        timeline_scale.config(to=0)

def close_app():
    root.destroy()

# Load image paths
play_icon_path = os.path.expanduser("~/Documents/Music Player/Icon_play.png")
pause_icon_path = os.path.expanduser("~/Documents/Music Player/Icon_pause.png")
next_icon_path = os.path.expanduser("~/Documents/Music Player/Icon_next.png")
prev_icon_path = os.path.expanduser("~/Documents/Music Player/Icon_prev.png")
close_icon_path = os.path.expanduser("~/Documents/Music Player/Icon_close.png")
frame_photo_path = os.path.expanduser("~/Documents/Music Player/Frame_rounded.png")

# Load, resize, and convert images
frame_image = Image.open(frame_photo_path).convert("RGBA")
frame_photo = ImageTk.PhotoImage(frame_image)

play_image = Image.open(play_icon_path).convert("RGBA").resize((24, 24), Image.LANCZOS)
play_photo = ImageTk.PhotoImage(play_image)

pause_image = Image.open(pause_icon_path).convert("RGBA").resize((24, 24), Image.LANCZOS)
pause_photo = ImageTk.PhotoImage(pause_image)

next_image = Image.open(next_icon_path).convert("RGBA").resize((18, 18), Image.LANCZOS)
next_photo = ImageTk.PhotoImage(next_image)

prev_image = Image.open(prev_icon_path).convert("RGBA").resize((18, 18), Image.LANCZOS)
prev_photo = ImageTk.PhotoImage(prev_image)

close_image = Image.open(close_icon_path).convert("RGBA").resize((20, 20), Image.LANCZOS)
close_photo = ImageTk.PhotoImage(close_image)

# Frame with draggable functionality
frame_label = tk.Label(root, image=frame_photo, bg=root.cget('bg'))
frame_label.pack(fill=tk.BOTH, expand=True)
frame_label.bind("<B1-Motion>", move_app)

# Cover image setup
cover_label = tk.Label(root, bg="white", border=0)
update_cover()

# Play/Pause button
play_label = tk.Label(root, image=play_photo, bg="white", border=0)
play_label.place(x=113, y=346)
play_label.bind("<Button-1>", lambda e: toggle_play_pause())

# Next button
next_label = tk.Label(root, image=next_photo, bg="white", border=0)
next_label.place(x=153, y=349)
next_label.bind("<Button-1>", lambda e: next_track())

# Prev button
prev_label = tk.Label(root, image=prev_photo, bg="white", border=0)
prev_label.place(x=79, y=349)
prev_label.bind("<Button-1>", lambda e: prev_track())

# Close button
close_label = tk.Label(root, image=close_photo, bg=root.cget('bg'))
close_label.place(x=213, y=14)
close_label.bind("<Button-1>", lambda e: close_app())

# Timeline Scale
timeline_scale = ttk.Scale(root, from_=0, to=0, orient='horizontal', length=220)
timeline_scale.place(x=15, y=310)

load_music()  # Initialize music timeline

# Run the main event loop
root.mainloop()

