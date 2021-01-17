# Robust Watermarking JPEG

A Python tool that allow an user to insert and extract a robust (permutation + encryption) watermark into a JPEG image.

## Getting Started

Just clone the github repository to get all the files you need to execute the code. Make sure to have some 16x16 images to test.

### Prerequisites

All you need to install is *Python 3.7* (we used *Anaconda3* environment but it's not necessary) and these libraries:
* *Scipy*, is a Python-based ecosystem of open-source software for mathematics, science, and engineering.
* *Numpy*, The fundamental package for scientific computing with Python. (it allows us to manipulate images's datas as arrays)
* *ImageShuffle*. It is a python package to degrade image data. (useful for the encryption scheme)

## Running and tests

The tool is divided into 2 main scripts: starter_encoder.py and starter_decoder.py

1. starter_encoder.py
* Given 5 parameters by input: 
> input : path to the input image (must be a 8x8 image at least) <br />
> output : path to the output image (compressed image) <br />
> watermark_input : path to a file containing the watermark array bit by bit (the size depends on the images passed by input) <br />
> key_permutation : a key number for the permutation <br />
> key_cypher : a key number for the encryption

It compress the image after permuting,encrypting and inserting the watermark in it. The output image cannot be opened because it is compressed so the second script (starter_decoder.py) must be ran to decompress it.

2. starter_decoder.py
* Given 4 parameters by input:
> input : path to the input image (compressed image that has been computed before) <br />
> output : path to the output image (decompressed image) <br />
> swap_encrypted_array : path to the encrypted array file (it has been created after the encryption phase of the first script) <br />
> watermarking_blocks : path to the watermarking's blocks file (it has been created after the watermarking phase of the first script)

It decompress the image after (un)permuting, decrypting and extracting the watermark from it to check if it is the same of the file passed by input. The extraction doesn't remove watermark's bits from the image so it will be permanently marked by those, showing that even with several attacks the watermark's bits won't be removed.

## Built With

* [Pycharm](https://www.jetbrains.com/pycharm/) - Python IDE
* [Anaconda3](https://www.anaconda.com/) - Package Management
* [ImageShuffle](https://github.com/mastnk/imageshuffle) - It is a python package to degrade image data.
* [jpeg-python](https://github.com/ghallak/jpeg-python) - Tool to implement JPEG algorithm (compression and decompression)

## Authors
* **Gianmarco Beato** - *Initial work* - [gianmarco594](https://github.com/gianmarco594)
* **Silvia Castelli** - *Initial work* - [scastelli95](https://github.com/scastelli95)
* **Silvio Corso** - *Initial work* - [s-corso-98](https://github.com/s-corso-98)
* **Francesco Maria D'Auria** - *Initial work* - [K1NG-CRIM50N](https://github.com/K1NG-CR1M50N)
* **Carmine Tramontano** - *Initial work* - [carminet94](https://github.com/carminet94)
* **Angela Vecchione** - *Initial work* - [angellavec94](https://github.com/angelavec94)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
