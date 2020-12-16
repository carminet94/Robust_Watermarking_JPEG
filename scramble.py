from PIL import Image
import numpy as np
from imageshuffle import imageshuffle as ims

def encrypt(image_name, key):
    # We open the image as array
    img = Image.open(image_name)
    ar = np.asarray(img)

    # We scrambles image block-by-block. Size of input data should be multiples of size of block.
    #key = 123456789
    print("Preimage shuffle")
    #s = ims.RandBlock(key, [16, 16],nb_bits = 4, rev_mode = ims.REV_NONE, rev_ratio = 0.5 )
    s = ims.RandBlock(key, [512, 512])
    print("Preimage encryption")
    enc = s.enc(ar)
    #print("Preimage dencryption")
    #dec = s.dec(enc)

    output_filename = "image-encrypted.png"
    f = Image.fromarray(enc)
    f.save(output_filename)

    return enc

def decrypt(image_name, key):
    # We open the image as array
    img = Image.open(image_name)
    ar = np.asarray(img)

    s = ims.RandBlock(key, [512, 512])
    dec = s.dec(ar)

    output_filename = "image-decrypted.png"
    f = Image.fromarray(dec)
    f.save(output_filename)

    return dec