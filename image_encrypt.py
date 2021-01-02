from PIL import Image
import numpy as np
from imageshuffle import imageshuffle as imageShuffle


#Function's input:
#image_to_encrypt: a string that represents the image to process (example: "image_input.png")
#key: a number that represents the encryption key (example: 123456789)
def encryption(image_to_encrypt, key):
    image = Image.open(image_to_encrypt)
    image_input_array_3d = np.array(image, dtype = np.uint8)


    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]
    side = 8
    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERROR: wrong width and height of the image"
                          "It has to be a multiple of the of the variable n = {} taken by input".format(side)))


    ##########################################  E N C R Y P T I O N  #####################################################
    #Here each "n" 8 x 8 blocks are turned into 1 x 64 block
    #Then are inserted into a 3d table of n x 64 size, at the end encryption is applied to the table

    pixel_array_nocipher = np.empty((blocks_count, side * side, 3), dtype = np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                block = image_input_array_3d[i:i + side, j:j + side, k]
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                       pixel_array_nocipher[block_index, ii, k] = block[r, c]
                       ii += 1
            block_index += 1
    s = imageShuffle.Rand(key)
    encrypt_image_array = s.enc(pixel_array_nocipher)




    #### S W A P ####
    #Swapping 3d AC's column of the unmodified image with 3d the AC's column of the encrypted image
    swap_array = np.array(encrypt_image_array[:, 0])
    encrypt_image_array[:, 0] = pixel_array_nocipher[:, 0]
    pixel_array_nocipher[:, 0] = swap_array




    #Translating the "n" 1 x 64 blocks into 8 x 8 blocks, then are inserted into a 3d table of rows x cols size; in this way
    #the encrypted image has AC's pixels encrypted and DC's pixels without any modify
    image_output_array_3d = np.empty((rows, cols, 3), dtype = np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        block[r][c] = encrypt_image_array[block_index, ii, k]
                        ii += 1
                image_output_array_3d[i:i + side, j:j + side, k] = block
            block_index += 1
    image = Image.fromarray(image_output_array_3d)
    image.save("image_AC_encrypt.png")
    image.close()

    return "image_AC_encrypt.png", pixel_array_nocipher



#Function's input:
#image_to_encrypt: a string that represents the image to process (example: "image_encrypted.png")
#key: a number that represents the decryption key, it has to be the same used for the encryption phase (example: 123456789)
#pixel_array_nocipher: all images's pixels that aren't encrypted
def deCryption(image_to_decrypt, key, pixel_array_nocipher):
    image = Image.open(image_to_decrypt)
    image_output_array_3d = np.array(image, dtype=np.uint8)
    rows, cols = image_output_array_3d.shape[0], image_output_array_3d.shape[1]
    side = 8
    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERROR: wrong width and height of the image"
                          "It has to be a multiple of the of the variable n = {} taken by input".format(side)))




    ############################################  D E C R Y P T I O N ###############################################
    #Here each "n" 8 x 8 blocks containing encrypted ACs are translated into 1 x 64 blocks, then are inserted into a 3d table of n x 64 size

    pixel_array_cipher2 = np.empty((blocks_count, side * side, 3), dtype=np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                block = image_output_array_3d[i:i + side, j:j + side, k]
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        pixel_array_cipher2[block_index, ii, k] = block[r, c]
                        ii += 1
            block_index += 1
    s = imageShuffle.Rand(key)




    #### S W A P ####
    #Swapping between ACs 3d column of the unmodified image and the same column of the ecrypted image
    pixel_array_cipher2[:, 0] = pixel_array_nocipher[:, 0]




    #Decryption 3d n x 64 table
    decrypt_image_array = s.dec(pixel_array_cipher2)



    #Translating the "n" 1 x 64 blocks into 8 x 8 blocks, then are inserted into a 3d table of rows x cols size; in this way
    #the decrypted image is obtained
    output_array_cipher = np.empty((rows, cols, 3), dtype=np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        block[r][c] = decrypt_image_array[block_index, ii, k]
                        ii += 1
                output_array_cipher[i:i + side, j:j + side, k] = block
            block_index += 1
    image = Image.fromarray(output_array_cipher)
    image.save("image_decrypted.png")
    image.close()

    return "image_decrypted.png"
