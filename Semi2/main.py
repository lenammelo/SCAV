import subprocess  # to be able to run ffmpeg commands
import lab1_SCAV_video_240300
import subtitles
import yuv_histogram


# exercise 1 - convert mp4 to mp2
def mp42mp2(video_in, output):
    """
    Args:
        video_in (str): name of the original video
        output (str): name of the video converted

    Returns:
        None
    """
    # we convert the video to mp2
    cmd = f'ffmpeg -i {video_in} -c:v mpeg2video {output}'
    subprocess.run(cmd, shell=True)

    # we get the information
    info_cmd = f"ffmpeg -i {output} -f null - > output_info.txt 2>&1"
    subprocess.run(info_cmd, shell=True)
    print('the video converted to mp2 is named', output, '\n')


# exercise 2 - modify resolution using ffmpeg

def mod_resolution(video_in, output, scale_wid, scale_hgt):
    """
    Args:
        video_in (str): name of the original video
        output (str): name of the video converted
        scale_wid (int): desired new width scale
        scale_hgt (int): desired new height scale

    Returns:
        None
    """
    cmd = f'ffmpeg -i {video_in} -vf "scale={scale_wid}:{scale_hgt}" -c:v copy {output}'
    subprocess.run(cmd, shell=True)

    print('the video with modified resolution is called', output, '\n and the resolution has been changed to'
          , scale_wid, 'x', scale_hgt, '\n')


# exercise 3 - change the chroma subsampling

def chr_subsampling(input_video, output, subsampling_ratio):
    """
    Args:
        input_video (str): name of the original video
        output (str): name of the video converted
        subsampling_ratio (int): desired subsampling ratio

    Returns:
        None
    """
    if subsampling_ratio.isnumeric():
        cmd = (
            f'ffmpeg -i {input_video} -vf format=yuv{subsampling_ratio}p -c:v libx264 -pix_fmt yuv420p -y -q:v 0 -strict '
            f'-2 -bf 0 -refs 2 -g 30 -b:v 4000k -minrate 4000k -maxrate 4000k -bufsize 8000k -muxrate 5000k {output}')
        subprocess.run(cmd, shell=True)
        print(f"Chroma subsampling changed to {subsampling_ratio}\n")
    else:
        print("the subsampling format must be all together, such as 420 or 422\n")


# exercise 4 - read the video info and print at least 5 relevant data from the video

def get_info(input_video):
    """
    Args:
        input_video (str): name of the original video

    Returns:
        None
    """
    cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,codec_name,pix_fmt -i {input_video}'
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    print("Exercici 1: \n")
    mp42mp2('BBB_mp4.mp4', 'BBB.mp2')

    print("Exercici 2: \n")
    mod_resolution('BBB_mp4.mp4', 'BBB_less_res.mp4', 300, 300)

    print("Exercici 3: \n")
    chr_subsampling('BBB_mp4.mp4', 'chroma_subsampling.mp4', "420")

    print("\nExercici 4: \n")
    get_info('chroma_subsampling.mp4')

    #print("Runegem la pràctica anterior\n")
    #lab1_SCAV_video_240300.

    print("Afegim els subtitols a un video\n")
    subtitle_path = "Discurso motivador Don Ibai Llanos.srt"
    # i haven't been able to find directly form YouTube the url. Instead I downloaded the .STR file from another page.
    #subtitles.download_subtitles()
    processor_subtitles = subtitles.VideoProcessor2("Discurso motivador Don Ibai Llanos.mp4", "output_video_with_subtitles.mp4")
    processor_subtitles.integrate_subtitles(subtitle_path)

    print("Fem l'histograma YUV del video anterior\n")
    processor_yuv = yuv_histogram.VideoProcessor3('Discurso motivador Don Ibai Llanos.mp4', 'output_histogram.mp4')
    processor_yuv.extract_yuv_histogram()
