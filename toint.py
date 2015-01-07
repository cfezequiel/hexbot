'''
Convert hex representation of data matrix to integers
'''

import csv

src = 'data.csv'
dst = 'data_int.csv'
with open(src, 'rb') as fp:
    reader = csv.reader(fp, delimiter=',')
    with open(dst, 'wt') as fpw:
        writer = csv.writer(fpw, delimiter=',')
        for row in reader:
            new_row = [int('0x' + ri, 16) for ri in row]
            writer.writerow(new_row)
