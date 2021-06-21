# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 20:21:47 2021

@author: Admin
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image_path = "./barcode.jpg"

def decode(image_path):
    
    ##############################################################################
    '''take bits'''
    #image_path = "./barcode.jpg"
    img = Image.open(image_path)
    width, height = img.size
    basewidth = 4*width
    img = img.resize((basewidth, height), Image.ANTIALIAS)
    img.save('resize.jpg')
    
    hor_line_bw = img.crop((0, int(height/2), basewidth, int(height/2) + 1)).convert('L')
    hor_line_bw.save('crop.jpg')
    hor_data = np.asarray(hor_line_bw, dtype="int32")[0]
    
    hor_data = 255 - hor_data
    avg = np.average(hor_data)

    plt.plot(hor_data)
    plt.show()


    pos1, pos2 = -1, -1
    bits = ""
    for p in range(basewidth - 2):
        if hor_data[p] < avg and hor_data[p + 1] > avg:
            bits += "1"
            if pos1 == -1:
                pos1 = p
            if bits == "101":
                pos2 = p
                break
        if hor_data[p] > avg and hor_data[p + 1] < avg:
            bits += "0"
    
    bit_width = int((pos2 - pos1)/3)
    
    bits = ""
    for p in range(basewidth - 2):
        if hor_data[p] > avg and hor_data[p + 1] < avg:
            interval = p - pos1
            cnt = interval/bit_width
            bits += "1"*int(round(cnt))
            pos1 = p
        if hor_data[p] < avg and hor_data[p + 1] > avg:
            interval = p - pos1
            cnt = interval/bit_width
            bits += "0"*int(round(cnt))
            pos1 = p
            
    print(bits)
    ##############################################################################
    
    '''decode'''
    CODE128_CHART = open("./code 128.txt","r")
    VALUES = [] 
    VALUESA = []
    VALUESB = []
    VALUESC = []
    SYMBOLS = []
    for line in CODE128_CHART:
        line=line.split()
        VALUES.append(line[0])
        VALUESA.append(line[1])
        VALUESB.append(line[2])
        VALUESC.append(line[3])
        SYMBOLS.append(line[4])
        
    
    #CODE128B = dict(zip(SYMBOLS, VALUESB))
    
    sym_len = 11
    symbols = [bits[i:i+sym_len] for i in range(0, len(bits), sym_len)]
    '''str_out = ""
    print (999,VALUESB)
    print (999,SYMBOLS)
    print (999,CODE128B)'''
    temp = SYMBOLS.index(symbols[0])
    if(VALUESA[temp] == 'STARTA'):
        start = VALUESA
        print("START A")
    elif(VALUESA[temp] == 'STARTB'):
        start = VALUESB
        print("START B")
    else:
        start = VALUESC
        print("START C")
    str_out =""
    for sym in symbols[1:]:
        temp = SYMBOLS.index(sym)
        if start[temp] == 'STOP' or len(sym)<11:
            break
        elif start[temp] == 'SP':
            str_out += " "
        else:
            str_out += start[temp]
        print("  ", start[temp])
    
    
    print("Str:", str_out)
    return str_out

#decode(image_path)
    
    