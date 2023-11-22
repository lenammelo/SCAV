import subprocess

def download_subtitles(subtitle_url, output_subtitle_path):
    # Download subtitles using youtube-dl
    download_command = [
        'youtube-dl',
        '--write-sub',
        '--skip-download',
        '--sub-lang', 'en',  # Specify the language of subtitles
        '--sub-format', 'srt',  # Specify the format of subtitles
        '-o', output_subtitle_path,  # Output file path
        subtitle_url
    ]
    subprocess.run(download_command, check=True)


class VideoProcessor2:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def integrate_subtitles(self, subtitle_path):
        # Integrate subtitles into the video
        integrate_command = [
            'ffmpeg',
            '-i', self.input_path,
            '-vf', f'subtitles={subtitle_path}',  # Use the subtitles filter
            '-c:a', 'copy',  # Copy audio stream
            '-c:v', 'libx264',  # Encode video with libx264
            '-crf', '20',  # Set Constant Rate Factor (0-51, lower is better quality)
            self.output_path
        ]
        subprocess.run(integrate_command, check=True)
