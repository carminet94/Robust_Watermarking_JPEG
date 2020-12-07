from PIL import Image
import numpy as np
from imageshuffle import imageshuffle as im
from imageshuffle import imagescramble as ims

def shuffling(image_name):
    # We open the image as array
    img = Image.open(image_name)
    ar = np.asarray(img)

    # We scrambles image block-by-block. Size of input data should be multiples of size of block.
    key = 11245533231
    print("Preimage shuffle")
    s = ims.RandBlock(key, [16, 16],nb_bits = 4, rev_mode = ims.REV_RAND, rev_ratio = 0.5 )
    print("Preimage encryption")
    enc = s.enc(ar)
    #print("Preimage dencryption")
    #dec = s.dec(enc)

    output_filename = "Lena-shuffled.png"
    f = Image.fromarray(enc)
    f.save(output_filename)

    return output_filename
