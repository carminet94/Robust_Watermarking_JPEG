from PIL import Image
import numpy as np
import random


# Function's input:
# image_to_permutation: a string that is the image to apply the permutation (example: "image_input.png")
# side: a number that represents the size of a side of squared block (n x n) in which it has to be divided and permutated (example: 16x16)
# key: permutation key (example: 0)
def permutation(image_to_permutation, side, key):
    image = Image.open(image_to_permutation)

    image_input_array_3d = np.array(image, dtype = np.uint8) # convert img into a 3d matrix

    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]

    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERROR: wrong width and height of the image"
                          "It has to be a multiple of the of the variable n = {} taken by input".format(side)))


    pixel_array = np.empty((blocks_count, side * side, 3), dtype = np.int32) # Rappresento ogni blocco dell'immagine sottoforma di una riga




    ####################################  P E R M U T A T I O N  #################################################
    # Here each squared blocked is translated into a row, then each image's pixel are copied

    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                block = image_input_array_3d[i:i + side, j:j + side, k]
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                       pixel_array[block_index, ii, k] = block[r, c]
                       ii += 1
            block_index += 1




    # A new image is created composed by permutated blocks and previous rows are traslated back into squared blocks of the img
    image_output_permutation_array_3d = np.empty((rows, cols, 3), dtype = np.uint8)
    random.seed(key)
    array_permutation = random.sample(range(blocks_count),blocks_count)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        block[r][c] = pixel_array[array_permutation[block_index], ii, k]
                        ii += 1
                image_output_permutation_array_3d[i:i + side, j:j + side, k] = block
            block_index += 1


    image = Image.fromarray(image_output_permutation_array_3d)
    image.save("image_input_permutation.png")
    image.close()

    return "image_input_permutation.png"



#Function's input:
#image_to_depermutation: a string that represent the image that has to be "depermutated" (example: "image_output_permutation.png")
#side: a number that represents the size of a side of squared block (n x n) in which it has to be divided and "depermutated" (example: 16x16)
#this value has to be the same of the one of permutation phase
#key: depermutation key, it has to be the same of the permutation phase (example: 0)
def dePermutation(image_to_depermutation, side, key):
    image = Image.open(image_to_depermutation)
    image_input_array_3d = np.array(image, dtype=np.uint8)  # Rappresento l'immagine come una matrice tridimensionale
    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]
    image_output_original_array_3d = np.empty((rows, cols, 3), dtype=np.uint8)

    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERROR: wrong width and height of the image"
                          "It has to be a multiple of the of the variable n = {} taken by input".format(side)))


    pixel_array = np.empty((blocks_count, side * side, 3), dtype=np.int32)

    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                block = image_input_array_3d[i:i + side, j:j + side, k]
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        pixel_array[block_index, ii, k] = block[r, c]
                        ii += 1
            block_index += 1

    random.seed(key)
    array_permutation = random.sample(range(blocks_count),blocks_count)


    block_index = 0
    rand_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                ii = 0

                for r in range(0, side):
                    for c in range(0, side):
                        for randarr in range(blocks_count):
                            if array_permutation[randarr]==block_index:
                                rand_index = randarr
                                randarr =0
                                break



                        block[r][c] = pixel_array[rand_index, ii, k]
                        ii += 1
                image_output_original_array_3d[i:i + side, j:j + side, k] = block
            block_index += 1

    image = Image.fromarray(image_output_original_array_3d)
    image.save("image_input_depermutation_original.png")
    image.close()
