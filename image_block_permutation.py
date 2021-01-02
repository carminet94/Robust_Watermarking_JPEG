from PIL import Image
import numpy as np
import random


def permutation(image_to_permutation, side, key):
    # La funzione prende in input:
    # image_to_permutation: una stringa che rappresenta l'immagine da procesare (esempio: "image_input.png")
    # side: un numero che rappresenta la dimensioni del lato di un blocco quadrato (n x n) di cui l'immagine deve esserene divisa e permutata (esempio: 16)
    # key: la chiave di permutazione (esempio: 0)

    image = Image.open(image_to_permutation)

    image_input_array_3d = np.array(image, dtype = np.uint8) # Rappresento l'immagine come una matrice tridimensionale

    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]

    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERRORE: la larghezza e l'altezza dell'immagine"
                          "deve essere un multiplo del numero n = {} fornito in input".format(side)))

    # print("Numero di blocchi di dimensione {}: ".format(side), blocks_count)

    pixel_array = np.empty((blocks_count, side * side, 3), dtype = np.int32) # Rappresento ogni blocco dell'immagine sottoforma di una riga




    ####################################  P E R M U T A Z I O N E  #################################################
    # Qui trasformo ogni blocco quadrato dell'immagine in una riga, quindi effettua la copia dei pixel dell'immagine

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




    ##################
    # Qui creo una nuova immagine avente con i blocchi permutati, andando a trasformare ogni riga 
    # in un blocco dell'immagine

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
    image.save("image_output_permutation.png")
    image.close()

    return "image_output_permutation.png"


def dePermutation(image_to_depermutation, side, key):
    # La funzione prende in input:
    # image_to_depermutation: una stringa che rappresenta l'immagine da procesare (esempio: "image_output_permutation.png")
    # side: un numero che rappresenta la dimensioni del lato di un blocco quadrato (n x n) di cui l'immagine deve esserene divisa e depermutata (esempio: 16), e
    # che deve coincidere con il valore inserito nella fase di permutazione
    # key: la chiave di depermutazione, che deve necessariamente coincidere con la chiave utilizzata nella permutazione (esempio: 0)

    image = Image.open(image_to_depermutation)
    image_input_array_3d = np.array(image, dtype=np.uint8)  # Rappresento l'immagine come una matrice tridimensionale
    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]
    image_output_original_array_3d = np.empty((rows, cols, 3), dtype=np.uint8)

    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERRORE: la larghezza e l'altezza dell'immagine"
                          "deve essere un multiplo del numero n = {} fornito in input".format(side)))


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
    image.save("image_output_original.png")
    image.close()
