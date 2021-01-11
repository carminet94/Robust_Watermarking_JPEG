import argparse

from PIL import Image

import compression as compression
import image_block_permutation as img_permutation
import image_encrypt as img_encrypt
import numpy as np
import watermarking as wm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input image")
    args = parser.parse_args()

    input_file = args.input



    ####################################  P E R M U T A T I O N  #######################################################
    print("I'm permuting...")
    key_permutation = 0
    image_permutation = img_permutation.permutation(input_file, 16, key_permutation)



    ####################################  E N C R Y P T I O N  #########################################################
    print("I'm encrypting...")
    key_cipher = 1234567899
    image_encrypt, swap_array = img_encrypt.encryption(image_permutation, key_cipher)
    np.save("swap_encrypted_array.npy", swap_array)



    image = Image.open(image_encrypt)
    ycbcr = image.convert('YCbCr')

    # "npmat" is tridimensional array
    npmat = np.array(ycbcr, dtype=np.uint8)

    rows, cols = npmat.shape[0], npmat.shape[1]
    count = 0
    # check image size: 8x8
    if rows % 8 == cols % 8 == 0:
        blocks_count = rows // 8 * cols // 8
    else:
        raise ValueError(("the width and height of the image "
                          "should both be mutiples of 8"))

    # dc is the top-left cell of the block, ac are all the other cells

    # "dc" is bidimensional array
    dc = np.empty((blocks_count, 3), dtype=np.int32)

    dc_Y = open("dc_Y_attack.txt", "w")
    image_hight, image_width = image.size

    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            try:
                block_index += 1
            except NameError:
                block_index = 0

            for k in range(3):
                # split 8x8 block and center the data range on zero
                # [0, 255] --> [-128, 127]
                # "block" is bidimensional array
                block = npmat[i:i + 8, j:j + 8, k] - 128

                dct_matrix = compression.dct_2d(block)
                quant_matrix = compression.quantize(dct_matrix,
                                        'lum' if k == 0 else 'chrom')

                zz = compression.block_to_zigzag(quant_matrix)
                # fills the array with the previously transformed and quantized DCs
                dc[block_index, k] = zz[0]

                # We save the DC for Y component in a file "dc_Y.txt"
                if (k == 0):
                    dc_Y.write(str(dc[block_index, k]))
                    dc_Y.write(" ")
                    count += 1
                    if (count == (image_width // 8)):
                        dc_Y.write('\n')
                        count = 0

    dc_Y.close()

    dc_Y_attack = open("dc_Y_attack.txt", "r")
    watermarking_blocks = np.load("watermark_blocks.npy")
    wm.extractWatermark(dc_Y_attack, watermarking_blocks)
    dc_Y_attack.close()


if __name__ == "__main__":
    main()