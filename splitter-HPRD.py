#!/usr/bin/python

import csv

ipfile = raw_input("enter input file: ")
ip = open (ipfile,'r')
opfile = raw_input("name of file to be saved: ")
op = open (opfile,'w')
ipreader = csv.reader(ip,delimiter='\t')
records = list(ipreader)
opwritter = csv.writer(op,delimiter='\t')

for col in records:
    f1 = col[0]
    f2 = col[3]
    opwritter.writerow([f1] + [f2])
ip.close()
op.close()
