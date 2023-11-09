import tkinter as tk
from tkinter import filedialog
from gtts import gTTS
import moviepy.editor as mp
import tempfile
import os
from datetime import datetime


def generate_unique_filename(extension):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"output_video_{current_time}.{extension}"


def process_and_save():
    text = text_entry.get()
    image_path = filedialog.askopenfilename()

    # Text to Speech
    tts = gTTS(text)

    try:
        # Create a temporary audio file
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio_file.name)
        temp_audio_file.close()

        audio_clip = mp.AudioFileClip(temp_audio_file.name)
        video_clip = mp.VideoFileClip(image_path)

        # Set the audio of the video
        video_clip = video_clip.set_audio(audio_clip)

        # Set the video duration to match the audio duration
        video_clip = video_clip.set_duration(audio_clip.duration)

        # Generate a unique filename for the output video
        output_filename = generate_unique_filename("mp4")

        # Write the video to the unique filename with the same frame rate
        video_clip.write_videofile(output_filename, codec='libx264', fps=video_clip.fps)

        # Clean up the temporary audio file
        os.remove(temp_audio_file.name)
    except Exception as e:
        print(f"An error occurred: {e}")


def quit_app():
    app.quit()


# Creating the GUI
app = tk.Tk()
app.title("Text to Image with Audio")
text_label = tk.Label(app, text="Enter Text:")
text_label.pack()
text_entry = tk.Entry(app)
text_entry.pack()
file_button = tk.Button(app, text="Select Image", command=process_and_save)
file_button.pack()

# Add a Quit button
quit_button = tk.Button(app, text="Quit", command=quit_app)
quit_button.pack()

app.mainloop()
