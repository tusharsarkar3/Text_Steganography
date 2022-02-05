import numpy as np
import pandas as pd
import os

import cv2

def BinaryTointeger(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary!=0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return (decimal)


def message2binary(message):
    if type(message) == str:
        result = ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        result = [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        result = format(message, "08b")
    else:
        raise TypeError("Input type is not supported")
    return result

def encode_data(img):
    list1 = []
    data=input("Enter the data to be Encoded:")
    if (len(data) == 0):
        raise ValueError('Data is empty')
    filename = input("Enter the name of the New Image after Encoding(with extension):")
    no_bytes=(img.shape[0] * img.shape[1] * 3) // 8
    print("Maximum bytes to encode:", no_bytes)
    if(len(data)>no_bytes):
        raise ValueError("Error encountered Insufficient bytes, Need Bigger Image or give Less Data !!")
    data +='*****'
    data_binary=message2binary(data)
    print(data_binary)
    data_len=len(data_binary)
    print("The Length of Binary data",data_len)
    data_index = 0
    for i in img:
        for pixel in i:
          r, g, b = message2binary(pixel)
          if data_index < data_len:
              pixel[0] = int(r[:-1] + data_binary[data_index], 2)
              data_index += 1
              list1.append(pixel[0])
          if data_index < data_len:
              pixel[1] = int(g[:-1] + data_binary[data_index], 2)
              data_index += 1
              list1.append(pixel[1])
          if data_index < data_len:
              pixel[2] = int(b[:-1] + data_binary[data_index], 2)
              data_index += 1
              list1.append(pixel[2])
          if data_index >= data_len:
              break
    cv2.imwrite(filename,img)
    print("Encoded the data successfully and the image is successfully saved as ",filename)


def decode_data(img):
    binary_data = ""
    for i in img:
        for pixel in i:
            r, g, b = message2binary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*****":
            break
    print("The Encoded data was :--", decoded_data[:-5])

if __name__=="__main__":
    option = input("Select 1 for encoder and 2 decoder: ")
    if option == "1":
        path_to_img = input("Enter path to image: ")
        encode_data(cv2.imread(path_to_img))
    else:
        path_to_img = input("Enter path to image: ")
        decode_data(cv2.imread(path_to_img))