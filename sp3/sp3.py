import subprocess
import os


def conversion(input_video, output_file, scale):
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f'scale={scale}',
        '-strict', '-2',  # allow using the default codec
        output_file
    ]
    subprocess.run(cmd)


class VideoConverter:
    def __init__(self, input_file):
        self.input_file = input_file

    def convert_codec(self, codec, preset, output_file):
        cmd = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', codec,
            '-c:a', 'copy',
            '-preset', preset,
            output_file
        ]
        subprocess.run(cmd)

    def convert_to_vp8(self, output_file):
        self.convert_codec('libvpx', 'medium', output_file)

    def convert_to_vp9(self, output_file):
        self.convert_codec('libvpx-vp9', 'medium', output_file)

    def convert_to_h265(self, output_file):
        self.convert_codec('libx265', 'medium', output_file)

    def convert_to_av1(self, output_file):
        self.convert_codec('libaom-av1', 'medium', output_file)

    def compare_codecs(self, codec1, codec2, output_file):
        # we don't want to modify directly the original files so we declare two new variables
        # we use .mkv because of different reasons, it is open, flexible and has lossless preservation between others
        temp_file1 = 'temp1.mkv'
        temp_file2 = 'temp2.mkv'

        # Convert input video using Codec 1
        self.convert_codec(codec1, 'copy', temp_file1)

        # Convert input video using Codec 2
        self.convert_codec(codec2, 'copy', temp_file2)

        # Combine the two videos side by side
        cmd = [
            'ffmpeg',
            '-i', temp_file1,
            '-i', temp_file2,
            '-filter_complex', f'[0:v]pad=iw*2:ih[bg]; [bg][1:v]overlay=w',
            '-c:a', 'copy',
            output_file
        ]
        subprocess.run(cmd)

        print(f'Comparison video saved to {output_file}')

        # Cleanup temporary files
        os.remove(temp_file1)
        os.remove(temp_file2)


if __name__ == "__main__":
    input_file = "BBB.mp4"
    conversion(input_file, "output_720p.mp4", "1280:720")
    conversion(input_file, "output_480p.mp4", "854:480")
    conversion(input_file, "output_360x240.mp4", "360:240")
    conversion(input_file, "output_160x120.mp4", "160:120")
    converter = VideoConverter(input_file)

    converter.convert_to_vp8('output_vp8.webm')
    converter.convert_to_vp9('output_vp9.webm')
    converter.convert_to_h265('output_h265.mp4')
    converter.convert_to_av1('output_av1.mkv')


    output_comparison = 'output_comparison.mp4'
    converter.compare_codecs('libvpx', 'libvpx-vp9', output_comparison)
