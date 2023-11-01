from PIL import Image
import numpy as np
import subprocess  # to be able to run ffmpeg commands


# exercise 1
def rgb2yuv(r, g, b):
    """
    Args:
        r (float): r color component
        g (float): g color component
        b (float): b color component

    Returns:
        y, u, v (tuple): yuv components
    """
    y = 0.257 * r + 0.504 * g + 0.098 * b + 16
    u = -0.148 * r - 0.291 * g + 0.439 * b + 128
    v = 0.439 * r - 0.368 * g - 0.071 * b + 128
    return y, u, v


def yuv2rgb(y, u, v):
    """
    Args:
        y (float): y color component
        u (float): u color component
        v (float): v color component

    Returns:
        r, g, b (tuple): rgb components
    """
    b = int(1.164 * (y - 16) + 2.018 * (u - 128))
    g = int(1.164 * (y - 16) - 0.813 * (v - 128) - 0.391 * (u - 128))
    r = int(1.164 * (y - 16) + 1.596 * (v - 128))
    return r, g, b


# exercise 2
def resizeandcompress(photo_in, photo_out, new_size):
    """
    Args:
        photo_in (str): name of the original image
        photo_out (str): name of the image compressed
        new_size (float): size to compress, smaller than one

    Returns:
        photo_out (image): compressed with the new scale
    """
    img = Image.open(photo_in)

    new_wid = int(img.size[0] * new_size)
    new_hgt = int(img.size[1] * new_size)
    # the ffmpeg command
    cmd = f'ffmpeg -i {photo_in} -vf "scale={new_wid}:{new_hgt}" {photo_out}'

    # we use subprocess to run the ffmpeg command
    subprocess.run(cmd, shell=True)


# exercise 3
def serpentine(photo_in):
    """
    Args:
        photo_in (str): name of the original image

    Returns:
        serpen (bytes): bytes in the serpentine order
    """
    # we read the image
    img = Image.open(photo_in)

    # we get the width and height
    wid, hgt = img.size

    # we load the pixels of the image for pixel-level access
    pixels = img.load()

    # we initialize a bytearray to store the result
    serpen = bytearray()

    # we start a loop that goes through the rows
    for i in range(hgt):
        # the behaviour of the algorithm depends on the parity of the rows
        # even rows travel to the right
        if i % 2 == 0:
            for j in range(wid):
                pixel = pixels[j, i]
                # add the pixel to the result
                serpen.extend(pixel)

        # odd rows travel to the left
        else:
            for j in range(wid - 1, -1, -1):
                pixel = pixels[j, i]
                # add the pixel to the result
                serpen.extend(pixel)

    return bytes(serpen)


# exercise 4
def bwandcompress(photo_in, photo_out):
    """
    Args:
        photo_in (str): name of the original image
        photo_out (str): name of the image compressed

    Returns:
        photo_out (image): black&white image and compressed
    """
    # we use -vf for the format, -q for the compression
    cmd = f'ffmpeg -i {photo_in} -vf "format = gray" -q:v 1 {photo_out}'
    subprocess.run(cmd, shell=True)


# exercise 5
def runlength_enc(photo_in):
    """
    Args:
        photo_in (str): name of the original image

    Returns:
        rle (numpy.array): array of tuples
    """
    # we read the image
    img = Image.open(photo_in)

    # we store the values of the pixels in the variable img_data using .getdata()
    img_data = img.getdata()
    # we initialize a variable to count the repeated data
    count = 1
    # we create an empty array to store the resulting data
    rle = []

    # we start a loop for all the data
    for i in range(len(img_data) - 1):
        # if the actual data point is the same as the next one, we check the following ones
        if img_data[i] == img_data[i + 1]:
            i += count
            count += 1
        # if the actual data point is different, we add the point to the resulting array and put one
        else:
            rle.append((count, img_data[i]))
            i += count
            count = 1
    return rle


# exercise 6
class DCT_converter:
    def __init__(self):
        pass

    def dct(self, input):
        return np.fft.fft2(input)

    def idct(self, input):
        return np.fft.ifft2(input)


pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # exercise 1
    y, u, v = rgb2yuv(23, 44, 231)
    r, g, b = yuv2rgb(y, u, v)
    print("The RGB colors have been converted to: ", y, u, v, "\nand reconverted to RGB: ", r, g, b)
    # exercise 2
    resizeandcompress('foto_SCAV.jpg', 'photo_compressed.png', 0.5)
    # exercise 3
    serp = serpentine('foto_SCAV.jpg')
    # exercise 4
    bwandcompress('foto_SCAV.jpg', 'photo_bw.png')
    # exercise 5
    matrix_enc = runlength_enc('foto_SCAV.jpg')
    # exercise 6

    converter = DCT_converter()

    # Create an example 2D input array
    input_data = np.array([[1, 2, 3, 4, 5, 6],
                           [7, 8, 9, 10, 11, 12],
                           [13, 14, 15, 16, 17, 18],
                           [19, 20, 21, 22, 23, 24],
                           [25, 26, 27, 28, 29, 30]])

    # Perform DCT on example matrix
    dct_data = converter.dct(input_data)
    print("DCT-transformed data:")
    print(dct_data)

    # Perform IDCT to reconstruct the original matrix
    # we use .ral to get the real part of the result
    reconstructed_data = converter.idct(dct_data).real
    print("Reconstructed data:")
    print(reconstructed_data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
