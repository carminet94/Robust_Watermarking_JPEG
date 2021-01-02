import os
from utils import *
from scipy import fftpack
from PIL import Image
from huffman import HuffmanTree
import watermarking as watermark


def quantize(block, component):
    q = load_quantization_table(component)
    return (block / q).round().astype(np.int32)


def block_to_zigzag(block):
    return np.array([block[point] for point in zigzag_points(*block.shape)])


def dct_2d(image):
    return fftpack.dct(fftpack.dct(image.T, norm='ortho').T, norm='ortho')


def run_length_encode(arr):
    # determine where the sequence is ending prematurely
    last_nonzero = -1
    for i, elem in enumerate(arr):
        if elem != 0:
            last_nonzero = i

    # each symbol is a (RUNLENGTH, SIZE) tuple
    symbols = []

    # values are binary representations of array elements using SIZE bits
    values = []

    run_length = 0

    for i, elem in enumerate(arr):
        if i > last_nonzero:
            symbols.append((0, 0))
            values.append(int_to_binstr(0))
            break
        elif elem == 0 and run_length < 15:
            run_length += 1
        else:
            size = bits_required(elem)
            symbols.append((run_length, size))
            values.append(int_to_binstr(elem))
            run_length = 0
    return symbols, values


def write_to_file(filepath, dc, ac, blocks_count, tables):

    try:
        f = open(filepath, 'w') # LenaOutput.png
    except FileNotFoundError as e:
        raise FileNotFoundError(
                "No such directory: {}".format(
                    os.path.dirname(filepath))) from e

    for table_name in ['dc_y', 'ac_y', 'dc_c', 'ac_c']:

        # 16 bits for 'table_size'
        f.write(uint_to_binstr(len(tables[table_name]), 16))

        for key, value in tables[table_name].items():
            if table_name in {'dc_y', 'dc_c'}:
                # 4 bits for the 'category'
                # 4 bits for 'code_length'
                # 'code_length' bits for 'huffman_code'
                f.write(uint_to_binstr(key, 4))
                f.write(uint_to_binstr(len(value), 4))
                f.write(value)
            else:
                # 4 bits for 'run_length'
                # 4 bits for 'size'
                # 8 bits for 'code_length'
                # 'code_length' bits for 'huffman_code'
                f.write(uint_to_binstr(key[0], 4))
                f.write(uint_to_binstr(key[1], 4))
                f.write(uint_to_binstr(len(value), 8))
                f.write(value)

    # 32 bits for 'blocks_count'
    f.write(uint_to_binstr(blocks_count, 32))
    for b in range(blocks_count):
        for c in range(3):
            category = bits_required(dc[b, c])
            symbols, values = run_length_encode(ac[b, :, c])

            dc_table = tables['dc_y'] if c == 0 else tables['dc_c']
            ac_table = tables['ac_y'] if c == 0 else tables['ac_c']

            f.write(dc_table[category])
            f.write(int_to_binstr(dc[b, c]))


            for i in range(len(symbols)):
                f.write(ac_table[tuple(symbols[i])])
                f.write(values[i])

    f.close()


def encoder(image_encrypt, output_file):

    ####################################  C O M P R E S S I O N   #################################################
    # We convert RGB image in YCbCr image
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

                dct_matrix = dct_2d(block)
                quant_matrix = quantize(dct_matrix,
                                                'lum' if k == 0 else 'chrom')

                zz = block_to_zigzag(quant_matrix)
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
    dc_mod,block_modified = watermark.watermark("dc_Y.txt")
    dc_Y_modified = open(dc_mod, "r")

    # Overwriting DC coefficient of luminance with modified DC coefficient
    block_index = 0
    index_columns = 0


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
        flatten(run_length_encode(ac[i, :, 0])[0]
                for i in range(blocks_count)))
    H_AC_C = HuffmanTree(
        flatten(run_length_encode(ac[i, :, j])[0]
                for i in range(blocks_count) for j in [1, 2]))

    tables = {'dc_y': H_DC_Y.value_to_bitstring_table(),
              'ac_y': H_AC_Y.value_to_bitstring_table(),
              'dc_c': H_DC_C.value_to_bitstring_table(),
              'ac_c': H_AC_C.value_to_bitstring_table()}

    write_to_file(output_file, dc, ac, blocks_count, tables)

    return output_file, block_modified




