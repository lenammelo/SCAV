import subprocess


class VideoProcessor3:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def extract_yuv_histogram(self):
        # we extract YUV histogram using ffmpeg
        extract_command = [
            'ffmpeg',
            '-i', self.input_path,
            '-vf', 'colorbalance=rs=0.2:gs=0.2:bs=0.2',
            '-c:v', 'libx264',
            '-crf', '20',
            '-c:a', 'copy',
            self.output_path
        ]
        subprocess.run(extract_command, check=True)
