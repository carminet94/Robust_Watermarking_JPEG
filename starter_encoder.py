import argparse
import compression as compression
import image_block_permutation as img_permutation
import image_encrypt as img_encrypt
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input image")
    parser.add_argument("output", help="path to the output image")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output



    ####################################  P E R M U T A T I O N  #######################################################
    print("I'm permuting...")
    key_permutation = 0
    image_permutation = img_permutation.permutation(input_file, 16, key_permutation)



    ####################################  E N C R Y P T I O N  #########################################################
    print("I'm encrypting...")
    key_cipher = 1234567899
    image_encrypt, swap_array = img_encrypt.encryption(image_permutation, key_cipher)
    np.save("swap_encrypted_array.npy", swap_array)



    ###########################  W A T E R M A K  A N D  C O M P R E S S I O N   #######################################
    print("I'm doing the compression...")
    image_compression, blocks_modified = compression.compression(image_encrypt, output_file)
    np.save("watermark_blocks.npy", blocks_modified)



if __name__ == "__main__":
    main()

