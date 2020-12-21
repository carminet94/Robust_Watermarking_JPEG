from PIL import Image
import numpy as np


def permutation(image_to_process, side):
    # La funzione prende in input:
    # image_to_process: una stringa che rappresenta l'immagine da procesare (esempio: "image_input.png")
    # side: un numero che rappresenta la dimensioni del lato di un blocco quadrato (n x n) di cui l'immagine deve esserene divisa e permutata (esempio: 16)

    image = Image.open(image_to_process)

    image_input_array_3d = np.array(image, dtype = np.uint8) # Rappresento l'immagine come una matrice tridimensionale

    rows, cols = image_input_array_3d.shape[0], image_input_array_3d.shape[1]

    if rows % side == cols % side == 0:
        blocks_count = rows // side * cols // side
    else:
        raise ValueError(("ERRORE: la larghezza e l'altezza dell'immagine"
                          "deve essere un multiplo del numero n = {} fornito in input".format(side)))

    print("Numero di blocchi di dimensione {}: ".format(side), blocks_count)

    pixel_array = np.empty((blocks_count, side * side, 3), dtype = np.int32) # Rappresento ogni blocco dell'immagine sottoforma di una riga




    ################################################################################################
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




    ################################################################################################
    # Qui creo una nuova immagine a partire dall'immagine permutata, con i blocchi permutati,
    # andando a trasformare ogni riga in un blocco dell'immagine

    image_output_permutation_array_3d = np.empty((rows, cols, 3), dtype = np.uint8)

    array_permutation = []
    for number in range(blocks_count):
         array_permutation.append(number)
    array_permutation = np.random.permutation(array_permutation)

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




    ################################################################################################
    # Qui ricreo l'immagine originale a partire dall'immagine permutata, effettuando la depermutazione dei blocchi

    image_output_original_array_3d = np.empty((rows, cols, 3), dtype = np.uint8)

    array_permutation = np.sort(array_permutation)

    block_index = 0
    for i in range(0, rows, side):
        for j in range(0, cols, side):
            for k in range(3):
                ii = 0
                for r in range(0, side):
                    for c in range(0, side):
                        block[r][c] = pixel_array[array_permutation[block_index], ii, k]
                        ii += 1
                image_output_original_array_3d[i:i + side, j:j + side, k] = block
            block_index += 1

    image = Image.fromarray(image_output_original_array_3d)
    image.save("image_output_original.png")
    image.close()

    return



def dePermutation():
    # TODO rendere globali le variabili pixel_array ed array_permutation in modo tale da poter scrivere in questa funzione la parte della depermutazione della funzione precedente
    return