import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from PIL import Image
import sys
import pytesseract


file = sys.argv[1]

img = cv2.imread(file,0)
print(img.shape)


thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
img_bin = 255-img_bin

# cv2.imwrite('inverted_file.png',img_bin)
# plotting = plt.imshow(img_bin,cmap = 'gray')
# plt.show()


kernel_len = np.array(img).shape[1]//100
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,kernel_len))
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len,1))

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))

image1 = cv2.erode(img_bin, ver_kernel, iterations =3)
vertical_lines = cv2.dilate(image1, ver_kernel, iterations=3)

# cv2.imwrite('vertical.jpg', vertical_lines)
# plotting = plt.imshow(image1,cmap = 'gray')
# plt.show()

image2 = cv2.erode(img_bin, hor_kernel, iterations =3)
horizontal_lines = cv2.dilate(image2, hor_kernel, iterations=3)

# cv2.imwrite('horizontal.jpg', horizontal_lines)

img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines,0.5,0.0)

img_vh = cv2.erode(~img_vh, kernel, iterations = 2)
thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
# cv2.imwrite('add.jpg',img_vh)

bitxor = cv2.bitwise_xor(img, img_vh)
bitnot = cv2.bitwise_not(bitxor)

# plotting = plt.imshow(bitnot,cmap = 'gray')
# plt.show()

contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def sort_contours(cnts, method = "left-to-right"):
    reverse= False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    
    if method == "top-to-bottom" or method == "bottom-to-top":
        i=1
    
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b:b[1][i], reverse=reverse))

    return (cnts, boundingBoxes)

contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")


heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
mean = np.mean(heights)

box = []
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    if (w<1000 and h<500):
        image = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        box.append([x,y,w,h])
plotting = plt.imshow(image,cmap='gray')
plt.show()

row = []
column = []
j = 0

for i in range(len(box)):
    if (i==0):
        column.append(box[i])
        previous = box[i]
    else:
        if(box[i][1]<=previous[1]+mean/2):
            column.append(box[i])
            previous = box[i]

            if i == len(box)-1:
                row.append(column)
        else:
            row.append(column)
            column = []
            previous = box[i]
            column.append(box[i])

# print(column)
# print(row)

countcol = 0
for i in range(len(row)):
    countcol = len(row[i])
    if countcol > countcol:
        countcol = countcol

centre = [int(row[i][j][0] + row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
centre= np.array(centre)
centre.sort()

finalboxes = []
for i in range(len(row)):
    lis=[]
    for k in range(countcol):
        lis.append([])
    for j in range(len(row[i])):
        diff = abs(centre-(row[i][j][0]+row[i][j][2]/4))
        minimum = min(diff)
        indexing = list(diff).index(minimum)
        lis[indexing].append(row[i][j])
    finalboxes.append(lis)


outer=[]
for i in range(len(finalboxes)):
    for j in range(len(finalboxes[i])):
        inner=''
        if(len(finalboxes[i][j])==0):
            outer.append(' ')
        else:
            for k in range(len(finalboxes[i][j])):
                y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
                finalimg = bitnot[x:x+h, y:y+w]
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                dilation = cv2.dilate(resizing, kernel,iterations=1)
                erosion = cv2.erode(dilation, kernel,iterations=1)

                
                out = pytesseract.image_to_string(erosion)
                if(len(out)==0):
                    out = pytesseract.image_to_string(erosion, config='--psm 3')
                inner = inner +" "+ out
            outer.append(inner)

#Creating a dataframe of the generated OCR list
arr = np.array(outer)
dataframe = pd.DataFrame(arr.reshape(len(row),countcol))
print(dataframe)
#Converting it into a csv file
dataframe.to_csv('file.csv')