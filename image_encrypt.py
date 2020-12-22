from PIL import Image
import numpy as np
import copy
from imageshuffle import imageshuffle as imageShuffle

def encryption(image_to_encrypt, key):
    # La funzione prende in input:
    # image_to_encrypt: una stringa che rappresenta l'immagine da procesare (esempio: "image_input.png")
    # key: un numero che rappresenta la chiave di cifratura/shuffling (esempio: 123456789)

    image = Image.open(image_to_encrypt)
    image_input_array_3d = np.array(image, dtype = np.uint8)


    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]
    side = 8
    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERRORE: la larghezza e l'altezza dell'immagine"
                          "deve essere un multiplo del numero n = {} fornito in input".format(8)))








    ##########################################  C I F R A T U R A  #####################################################
    # Qui trasformo gli "n" blocchi quadrati di dimensione 8 x 8 dell'immagine di partenza in blocchi di dimensione 1 x 64,
    # li inserisco in una tabella tridimensionale di dimensione n x 64 e la cifro

    pixel_array_nocypher = np.empty((blocks_count, side * side, 3), dtype = np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                block = image_input_array_3d[i:i + side, j:j + side, k]
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                       pixel_array_nocypher[block_index, ii, k] = block[r, c]
                       ii += 1
            block_index += 1
    s = imageShuffle.Rand(key)
    encrypt_image_array = s.enc(pixel_array_nocypher)


    #### S W A P ####
    # Qui effettuo lo swap tra la colonna tridimensionale degli AC dell'immagine in chiaro, con quella cifrata

    swap_array = np.array(encrypt_image_array[:, 0])
    encrypt_image_array[:, 0] = pixel_array_nocypher[:, 0]
    pixel_array_nocypher[:, 0] = swap_array


    # Qui trasformo gli "n" blocchi di dimensione 1 x 64 in blocchi quadrati di dimensione 8 x 8 e li inserisco in
    # una tabella tridimensionale di dimensione rows x cols; avrò l'immagine cifrata con i soli pixel DC in chiaro

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









    ############################################  D E C I F R A T U R A  ###############################################
    # Qui trasformo gli "n" blocchi quadrati con gli AC cifrati di dimensione 8 x 8 dell'immagine in blocchi di dimensione
    # 1 x 64, li inserisco in una tabella tridimensionale di dimensione n x 64

    pixel_array_cypher2 = np.empty((blocks_count, side * side, 3), dtype=np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                block = image_output_array_3d[i:i + side, j:j + side, k]
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        pixel_array_cypher2[block_index, ii, k] = block[r, c]
                        ii += 1
            block_index += 1


    #### S W A P ####
    # Qui effettuo lo swap tra la colonna tridimensionale degli AC dell'immagine in chiaro, con quella cifrata

    pixel_array_cypher2[:, 0] = pixel_array_nocypher[:, 0]
    image = Image.fromarray(pixel_array_cypher2)


    # Qui decifro la tabella tridimensionale di dimensione n x 64

    decrypt_image_array = s.dec(pixel_array_cypher2)


    # Qui trasformo gli "n" blocchi decifrati di dimensione 1 x 64 in blocchi quadrati di dimensione 8 x 8, li
    # inserisco in una tabella tridimensionale di dimensione rows x cols; avrò l'immagine completamente decifrata

    output_array_cypher = np.empty((rows, cols, 3), dtype=np.uint8)
    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        block[r][c] = decrypt_image_array[block_index, ii, k]
                        ii += 1
                output_array_cypher[i:i + side, j:j + side, k] = block
            block_index += 1
    image3 = Image.fromarray(output_array_cypher)
    image3.save("image_decypher.png")
    image3.close()

    return

def decryption(image_to_decrypt, key):
    # TODO rendere globali la variabile pixel_array_nocypher in modo tale da poter scrivere in questa funzione la parte della decifratura della funzione precedente
    return