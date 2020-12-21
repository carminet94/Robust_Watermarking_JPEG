from PIL import Image
import numpy as np
from imageshuffle import imageshuffle as ims

def encrypt(num_array, key):
    img = Image.open('Lena.png')
    ar = np.asarray(img)
    print(ar)



    # We scrambles image block-by-block. Size of input data should be multiples of size of block.
    print("Preimage shuffle")
    #s = ims.RandBlock(key, [16, 16],nb_bits = 4, rev_mode = ims.REV_NONE, rev_ratio = 0.5 )
    s = ims.RandBlock(key, [512, 512])
    print("Preimage encryption")
    print(num_array)
    enc = s.enc(num_array)
    #print("Preimage dencryption")
    #dec = s.dec(enc)
    return enc

def decrypt(num_array, key):
    s = ims.RandBlock(key, [512, 512])
    dec = s.dec(num_array)

    output_filename = "image-decrypted.png"
    f = Image.fromarray(dec)
    f.save(output_filename)

    return dec