import argparse
import binascii
import os
import math
import numpy as np
from arc4 import ARC4
from utils import *
from scipy import fftpack
from PIL import Image
from huffman import HuffmanTree
import scramble as sc
import itertools
import watermarking as wm
import encoder
import image_block_permutation as img_permutation
import image_encrypt as img_encrypt



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input image")
    parser.add_argument("output", help="path to the output image")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    # img_permutation.permutation("lena.png", 16)
    # key = 1234567899
    # img_encrypt.encryption("image_output_permutation.png", key)
    # img_encrypt_decrypt.decryption("image_AC_encrypt.png", key)
    # img_permutation.dePermutation("image_decypher.png", key)

    #Permutation
    image_name = img_permutation.permutation(input_file, 16,0)
    #img_permutation.dePermutation(image_name, 16)

    #Encryption
    key = 1234567899
    enc, array_nocypher = img_encrypt.encryption(image_name, key)

    #decr = img_encrypt.decryption("image_AC_encrypt.png",key,array_nocypher)
    #We convert RGB image in YCbCr image
    image = Image.open(enc)
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

    # "ac" is tridimensional array
    ac = np.empty((blocks_count, 63, 3), dtype=np.int32)

    dc_Y = open("dc_Y.txt", "w")
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

                dct_matrix = encoder.dct_2d(block)
                quant_matrix = encoder.quantize(dct_matrix,
                                        'lum' if k == 0 else 'chrom')

                zz = encoder.block_to_zigzag(quant_matrix)
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

                # fills the array with the previously transformed and quantized ACs
                ac[block_index, :, k] = zz[1:]

    dc_Y.close()


    # Watermarking process
    wm.watermark("dc_Y.txt")

    # Overwriting DC coefficient of luminance with modified DC coefficient
    block_index = 0
    index_columns = 0

    dc_Y_modified = open("dc_Y_modified.txt", "r")

    # Iteration through dc_Y_modified.txt 1 lines each time
    for line1 in dc_Y_modified:
        intDC_modified = [int(i) for i in line1.split()]

        # Overwrite dc[block-index,0] with dc_Y_modified values
        for index_columns in range(0, len(intDC_modified)):
            for i in range(0, rows, 8):
                for j in range(0, cols, 8):
                    try:
                        block_index += 1
                    except NameError:
                        block_index = 0
                        for k in range(3):
                            dc[block_index, 0] = intDC_modified[index_columns]
    dc_Y_modified.close()

    H_DC_Y = HuffmanTree(np.vectorize(bits_required)(dc[:, 0]))
    H_DC_C = HuffmanTree(np.vectorize(bits_required)(dc[:, 1:].flat))
    H_AC_Y = HuffmanTree(
        flatten(encoder.run_length_encode(ac[i, :, 0])[0]
                for i in range(blocks_count)))
    H_AC_C = HuffmanTree(
        flatten(encoder.run_length_encode(ac[i, :, j])[0]
                for i in range(blocks_count) for j in [1, 2]))

    tables = {'dc_y': H_DC_Y.value_to_bitstring_table(),
              'ac_y': H_AC_Y.value_to_bitstring_table(),
              'dc_c': H_DC_C.value_to_bitstring_table(),
              'ac_c': H_AC_C.value_to_bitstring_table()}




    encoder.write_to_file(output_file, dc, ac, blocks_count, tables)

if __name__ == "__main__":
    main()

