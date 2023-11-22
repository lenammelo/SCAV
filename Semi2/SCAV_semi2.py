import os
import subprocess  # to be able to run ffmpeg commands


class VideoProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def cut_and_process_video(self, start_time, end_time):
        # Step 1: Cut the video
        cut_command = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', self.input_path,
            '-t', str(end_time - start_time),
            '-c', 'copy',
            '-avoid_negative_ts', '1',
            self.output_path + '_cut.mp4'
        ]
        subprocess.run(cut_command, check=True)

        # Step 2: Extract macroblocks and motion vectors
        process_command = [
            'ffmpeg',
            '-i', self.output_path + '_cut.mp4',
            '-vf', 'mpdecimate,showinfo',
            '-vsync', 'vfr',
            '-q:v', '0',
            self.output_path
        ]
        subprocess.run(process_command, check=True)

    def create_bbb_container(self):
        # we cut BBB into a 50-second video
        cut_command = [
            'ffmpeg',
            '-i', self.input_path,
            '-t', '50',
            '-c', 'copy',
            '-avoid_negative_ts', '1',
            self.output_path + '_cut_50s.mp4'
        ]
        subprocess.run(cut_command, check=True)

        # we export BBB(50s) audio as MP3 mono track
        mp3_mono_command = [
            'ffmpeg',
            '-i', self.output_path + '_cut_50s.mp4',
            '-vn',  # No video
            '-ac', '1',  # Mono audio
            '-q:a', '0',  # High-quality
                  self.output_path + '_audio_mono.mp3'
        ]
        subprocess.run(mp3_mono_command, check=True)

        # we export BBB(50s) audio in MP3 stereo with lower bitrate
        mp3_stereo_low_bitrate_command = [
            'ffmpeg',
            '-i', self.output_path + '_cut_50s.mp4',
            '-vn',  # No video
            '-q:a', '5',  # Lower bitrate
                  self.output_path + '_audio_stereo_low_bitrate.mp3'
        ]
        subprocess.run(mp3_stereo_low_bitrate_command, check=True)

        # we export BBB(50s) audio in AAC codec
        aac_command = [
            'ffmpeg',
            '-i', self.output_path + '_cut_50s.mp4',
            '-vn',  # No video
            '-c:a', 'aac',
            '-strict', 'experimental',  # Required for using the experimental AAC encoder
                  self.output_path + '_audio.aac'
        ]
        subprocess.run(aac_command, check=True)

        # Step 5: Package everything in an .mp4 container
        package_command = [
            'ffmpeg',
            '-i', self.output_path + '_cut_50s.mp4',
            '-i', self.output_path + '_audio_mono.mp3',
            '-i', self.output_path + '_audio_stereo_low_bitrate.mp3',
            '-i', self.output_path + '_audio.aac',
            '-c', 'copy',
                  self.output_path + '_final_container.mp4'
        ]
        subprocess.run(package_command, check=True)

    def count_tracks_with_ffmpeg(self):
        # we use ffmpeg to list streams in the input video
        ffmpeg_command = [
            'ffmpeg',
            '-i', self.input_path,
            '-map', 'a',
            '-c', 'copy',
            '-f', 'null',
            '-'
        ]

        result = subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            # Extract lines containing audio streams information
            audio_stream_lines = [line for line in result.stderr.split('\n') if 'Audio:' in line]

            num_tracks = len(audio_stream_lines)
            print(f'The input video contains {num_tracks} audio tracks.')
            return num_tracks
        else:
            print('Error: Unable to get information about the input video.')

        return None


if __name__ == "__main__":
    input_video_path = "BBB.mp4"
    output_video_path = "BBB_processed.mp4"
    start_time = 35  # start time in seconds
    end_time = start_time + 9  # end time in seconds

    # exercise 1
    processor = VideoProcessor(input_video_path, output_video_path)
    processor.cut_and_process_video(start_time, end_time)

    # exercise 2
    processor.create_bbb_container()

    # exercise 3
    processor.count_tracks_with_ffmpeg()

