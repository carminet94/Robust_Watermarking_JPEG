import argparse
import encoder as encoder
import decoder as decoder
import image_block_permutation as img_permutation
import image_encrypt as img_encrypt
import watermarking as wm
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input image")
    parser.add_argument("encrypted_array", help="path to the encrypted array")
    parser.add_argument("watermarking_blocks", help="path to the watermarking's blocks")
    args = parser.parse_args()

    input_file = args.input
    array_encrypt_file = args.encrypted_array
    watermarking_blocks_file = args.watermarking_blocks



    ####################################  D E C O D E R  ###############################################################
    print("I'm doing the decompression...")
    image_decompression , dc_Y_mod = decoder.decoder(input_file)


    ####################################  D E C R Y P T I O N  #######################################################
    print("I'm decrypting...")
    key_cipher = 1234567899
    array_encrypt = np.load(array_encrypt_file)
    image_decrypt = img_encrypt.deCryption(image_decompression, key_cipher, array_encrypt)


    ####################################  E X T R A C T W A T E R M A R K  #############################################
    print("I'm extracting the watermark...")
    watermarking_blocks = np.load(watermarking_blocks_file)
    wm.extractWatermark(dc_Y_mod, watermarking_blocks)


    ####################################  D E P E R M U T A T I O N  #################################################
    print("I'm depermuting...")
    key_permutation = 0
    image_depermutation = img_permutation.dePermutation(image_decrypt, 16, key_permutation)



if __name__ == "__main__":
    main()

