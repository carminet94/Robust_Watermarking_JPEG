import itertools
import numpy as np

def watermark(dcfile):
    # Array that stores the index of the "modified" blocks
    modified_blocks = []

    # Thresholds for the watermarking algorithm
    T1 = 15
    T2 = 18

    #Indexes to save where watermark's bits are placed
    index = 0
    index_rows = -1

    # File in which each line is a DC of a different MCU
    f = open(dcfile, "r")

    # New file with the new DC
    dc_Y_modified = open("dc_Y_modified.txt", "w")

    #Example of a watermark
    bitwatermark = [1,0,0,1,1,0]

    #Algorithm to insert watermaking's bits
    #Iteration through the file 2 by 2 lines each time
    for line1, line2 in itertools.zip_longest(*[f] * 2):

        # DCs values
        DC0 = [int(i) for i in line1.split()]
        DC1 = [int(i) for i in line2.split()]

        index_rows += 1

        for i in range(0,len(DC0)-1, 2):
            DC00 = DC0[i]
            DC11 = DC0[i+1]
            DC22 = DC1[i]
            DC33 = DC1[i+1]

            A = (DC11 + DC22 + DC33) / 3
            minimum = min([DC00, DC11, DC22, DC33])
            maximum = max([DC00, DC11, DC22, DC33])
            if ((maximum - minimum) <= T1):
                P = 1
            elif (T1 <= (maximum - minimum) < T2):
                P = 2
            else:
                P = 3
            if(index<len(bitwatermark) and bitwatermark[index]== 1 ):
                if (DC00 < A + P):
                    new_DC0 = A + P
                    if (abs(DC00 - new_DC0) <= 3):
                        DC0[i] = int(round(new_DC0, 1))
                        modified_blocks.append([index_rows,i])
                        index += 1
                else:
                    continue


            elif (index<len(bitwatermark) and bitwatermark[index] == 0):
                if (DC00 > A - P):
                    new_DC0 = A - P
                    if (abs(DC00 - new_DC0) <= 3):
                        DC0[i] = int(round(new_DC0, 1))
                        modified_blocks.append([index_rows,i])
                        index += 1
                else:
                    continue
        dc_Y_modified.write(str(DC0))
        dc_Y_modified.write('\n')
        dc_Y_modified.write(str(DC1))
        dc_Y_modified.write('\n')
    if(index!=len(bitwatermark)):
       raise ValueError(("Error no watermark"))
    dc_Y_modified.close()



    #Indexes to iterate through the file and find watermark's bits
    index = 0
    index_rows = -1

    #Extracted bits are inserted in this array
    bitdewatermark=[]

    print(modified_blocks)

    #Opening the bitstream file of the DCs after the watermarking algorithm
    dc_Y_modified= open("dc_Y_modified.txt", "r")
    DC0= []
    DC1= []

    #Algorithm to extract watermarking's bits
    #Iterate through file lines 2 by 2
    for line1, line2 in itertools.zip_longest(*[dc_Y_modified] * 2):
        # DCs values
        for x in line1.replace("[","").replace("]","").split(","):
            DC0.append(x)
        for x in line2.replace("[","").replace("]","").split(","):
            DC1.append(x)
        #print(DC0)
        index_rows += 1

        #Iterate 2 by 2 through the obtained lines
        for i in range(0,len(DC0)-1, 2):
            DC00 = int(DC0[i])
            DC11 = int(DC0[i+1])
            DC22 = int(DC1[i])
            DC33 = int(DC1[i+1])
            print(DC00)
            if(modified_blocks[index][0]==index_rows and modified_blocks[index][1]==i):
                if(DC00>((DC11+DC22+DC33)/3)):
                    print("hallo")
                    bitdewatermark.append(1)
                    index += 1
                else:
                    bitdewatermark.append(0)
                    index += 1
            if(index == len(modified_blocks)):
                break
        if (index == len(modified_blocks)):
            break

    print(bitdewatermark)

    dc_Y_modified.close()

