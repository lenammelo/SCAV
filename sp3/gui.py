import tkinter as tk
from tkinter import filedialog, ttk
from functools import partial
import subprocess

class VideoConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Video Converter")

        # Load an image
        self.logo_image = tk.PhotoImage(file='layout.png')

        # Display the image using a label
        self.logo_label = ttk.Label(master, image=self.logo_image)
        self.logo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Convert Buttons
        codecs = ['VP8', 'VP9', 'H.265', 'AV1']
        for i, codec in enumerate(codecs):
            convert_button = ttk.Button(master, text=f"Convert to {codec}",
                                        command=partial(self.convert_video, self.get_codec(codec),
                                                        f'output_{codec.lower()}.mkv'))
            convert_button.place(x=70 + i*150, y=20 + i * 150, width=120, height=120)

        # Input Entry
        self.input_label = ttk.Label(master, text="Input Video:")
        self.input_label.place(x=90, y=410 + (len(codecs) + 1) * 40, width=80, height=30)

        self.input_entry = ttk.Entry(master)
        self.input_entry.place(x=180, y=410 + (len(codecs) + 1) * 40, relwidth=0.6, height=30)

        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.place(x=990, y=370 + (len(codecs) + 2) * 40, width=120, height=30)

        self.browse_button = ttk.Combobox(master, values=["Option 1", "Option 2", "Option 3"])

    def get_codec(self, codec):
        codecs_mapping = {
            'VP8': 'libvpx',
            'VP9': 'libvpx-vp9',
            'H.265': 'libx265',
            'AV1': 'libaom-av1',
        }
        return codecs_mapping.get(codec, 'libvpx')  # Default to libvpx if codec is not found

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

    def convert_video(self, codec, output_file):
        input_file = self.input_entry.get()
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', codec,
            '-c:a', 'copy',
            output_file
        ]
        subprocess.run(cmd)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterGUI(root)
    root.geometry("1280x680")
    root.mainloop()