import itertools


def watermark(dcfile):
    # Array that stores the index of the "modified" blocks
    modified_blocks = []
    index = 0

    # Thresholds for the watermarking algorithm
    T1 = 15
    T2 = 18

    # File in which each line is a DC of a different MCU
    f = open(dcfile, "r")
    # Iteration through the file 4 by 4 lines each time
    for line1, line2, line3, line4 in itertools.zip_longest(*[f] * 4):
        # DCs values(bit stream)
        DC0 = line1
        DC1 = line2
        DC2 = line3
        DC3 = line4
        # Counting the MCU in which we are operating
        index += 1

        # Converting each DC in decimal so that we can make maths operations
        decimal_DC0 = int(DC0, 2)
        decimal_DC1 = int(DC1, 2)
        decimal_DC2 = int(DC2, 2)
        decimal_DC3 = int(DC3, 2)

        A = (decimal_DC1 + decimal_DC2 + decimal_DC3) / 3
        minimum = min([decimal_DC0, decimal_DC1, decimal_DC2, decimal_DC3])
        maximum = max([decimal_DC0, decimal_DC1, decimal_DC2, decimal_DC3])
        if ((maximum - minimum) <= T1):
            P = 1
        elif (T1 <= (maximum - minimum) < T2):
            P = 2
        else:
            P = 3
        if (decimal_DC0 < A + P):
            new_DC0 = A + P
        if (decimal_DC0 > A - P):
            new_DC0 = A - P

        # if this condition is true we have to modify our MCU with the watermarking bit and saving his index
        if (abs(decimal_DC0 - new_DC0) <= 3):
            decimal_DC0 = new_DC0
            modified_blocks.append(index)

    print(index)