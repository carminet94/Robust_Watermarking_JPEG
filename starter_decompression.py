import argparse
import encoder as encoder
import decoder as decoder
import image_block_permutation as img_permutation
import image_encrypt as img_encrypt
import watermarking as wm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input image")
    parser.add_argument("output", help="path to the output image")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    ####################################  P E R M U T A T I O N  #####################################################
    print("I'm permuting...")
    key_permutation = 0
    image_permutation = img_permutation.permutation(input_file, 16, key_permutation)



    ####################################  E N C R Y P T I O N  ###########################################################
    print("I'm encrypting...")
    key_cypher = 1234567899
    image_encrypt, array_nocypher = img_encrypt.encryption(image_permutation, key_cypher)


    ####################################  E N C O D E R  ###############################################################
    print("I'm doing the compression...")
    image_compression, blocks_modified = encoder.encoder(image_encrypt, output_file)




    #___________________________________________________________________________________________________________________
    print("\n")


    ####################################  D E C O D E R  ###############################################################
    print("I'm doing the decompression...")
    image_decompression , dc_Y_mod = decoder.decoder(image_compression)


    ####################################  D E C R Y P T I O N  #######################################################
    print("I'm dencrypting...")
    image_decrypt = img_encrypt.deCryption(image_decompression, key_cypher, array_nocypher)


    ####################################  E X T R A C T W A T E R M A R K  #############################################
    print("I'm extracting the watermark...")
    wm.extractWatermark(dc_Y_mod, blocks_modified)


    ####################################  D E P E R M U T A T I O N  #################################################
    print("I'm depermuting...")
    image_depermutation = img_permutation.dePermutation(image_decrypt, 16, key_permutation)



if __name__ == "__main__":
    main()

