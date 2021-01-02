import itertools


def watermark(dcfile):
    #Array that stores the index of the "modified" blocks
    modified_blocks = []

    #Thresholds for the watermarking algorithm
    T1 = 15
    T2 = 18

    #Indexes to save where watermark's bits are placed
    index = 0
    index_rows = -2

    # File in which each line is a DC of a different MCU
    fileWithDC = open(dcfile, "r")

    # New file with the new DC
    dc_Y_modified = open("dc_Y_modified.txt", "w")

    #Example of a watermark
    bitwatermark = [1, 0, 1, 0, 1, 1]

    #Algorithm to insert watermaking's bits
    #Iteration through the file 2 by 2 lines each time
    for line1, line2 in itertools.zip_longest(*[fileWithDC] * 2):

        # DCs values
        DC0 = [int(i) for i in line1.split()]
        DC1 = [int(i) for i in line2.split()]

        index_rows += 2

        for index_columns in range(0,len(DC0)-1, 2):
            DC00 = DC0[index_columns]
            DC11 = DC0[index_columns+1]
            DC22 = DC1[index_columns]
            DC33 = DC1[index_columns+1]

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
                        DC0[index_columns] = int(round(new_DC0, 1))
                        modified_blocks.append([index_rows,index_columns])
                        index += 1
                else:
                    continue


            elif (index<len(bitwatermark) and bitwatermark[index] == 0):
                if (DC00 > A - P):
                    new_DC0 = A - P
                    if (abs(DC00 - new_DC0) <= 3):
                        DC0[index_columns] = int(round(new_DC0, 1))
                        modified_blocks.append([index_rows,index_columns])
                        index += 1
                else:
                    continue
        DC0M = [str(int) for int in DC0]
        DC1M = [str(int) for int in DC1]
        raw1 = " ".join(DC0M)
        raw2 = " ".join(DC1M)
        dc_Y_modified.write(raw1)
        dc_Y_modified.write('\n')
        dc_Y_modified.write(raw2)
        dc_Y_modified.write('\n')
    if(index!=len(bitwatermark)):
       raise ValueError(("Error no watermark"))
    dc_Y_modified.close()
    print(modified_blocks)
    return "dc_Y_modified.txt", modified_blocks


def extractWatermark(dc_Y_modified,modified_blocks):
    #Indexes to iterate through the file and find watermark's bits
    index = 0
    index_rows = -2

    #Extracted bits are inserted in this array
    bitWatermarkExtracted=[]

    print(modified_blocks)

    #Opening the bitstream file of the DCs after the watermarking algorithm
    dc_Y_modDec= open(dc_Y_modified, "r")
    DC0= []
    DC1= []

    #Algorithm to extract watermarking's bits
    #Iterate through file lines 2 by 2
    for line1, line2 in itertools.zip_longest(*[dc_Y_modDec] * 2):
        # DCs values
        DC0 = [int(i) for i in line1.split()]
        DC1 = [int(i) for i in line2.split()]
        #print(DC0)
        index_rows += 2

        #Iterate 2 by 2 through the obtained lines
        for index_columns in range(0,len(DC0)-1, 2):
            DC00 = int(DC0[index_columns])
            DC11 = int(DC0[index_columns+1])
            DC22 = int(DC1[index_columns])
            DC33 = int(DC1[index_columns+1])
            average = (DC11 + DC22 + DC33) / 3

            if(modified_blocks[index][0]==index_rows and modified_blocks[index][1]==index_columns):
                if(DC00 > average):
                    bitWatermarkExtracted.append(1)
                    index += 1
                else:
                    bitWatermarkExtracted.append(0)
                    index += 1
            if(index == len(modified_blocks)):
                break
        if (index == len(modified_blocks)):
            break
    print("bitwatermark restituiti: ",bitWatermarkExtracted)

    dc_Y_modDec.close()
    return bitWatermarkExtracted

