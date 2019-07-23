import numpy as np
import cv2

#img = 'C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/template/templatePreenchido.png'
#img = 'C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/template/GabaritoTemplatePreenchido.png'

def bolhas(im):



    image_color= im
    image_ori = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)


    image = image_color

    mask = cv2.adaptiveThreshold(image_ori,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,33,2)

    kernel = np.ones((3,3), np.uint8)

    #Use erosion and dilation combination to eliminate false positives. 
    #In this case the text Q0X could be identified as circles but it is not.
    mask = cv2.erode(mask, kernel, iterations=6)
    #cv2.imshow("mask1", mask)
    mask = cv2.dilate(mask, kernel, iterations=3)
    #cv2.imshow("mask2", mask)
    closing = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    contours.sort(key=lambda x:cv2.boundingRect(x)[0])

    array = []
    #ii = 1
    #print(len(contours))
    for c in contours:
        (x,y),r = cv2.minEnclosingCircle(c)
        #(x, y, w, h) = cv2.boundingRect(c)
        #ar = w / float(h)
        center = (int(x ),int(y))
        r = int(r)
        #if (w >= 15 and h >= 15) and (w <= 17  and h <= 17) :
        #cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 3)
        if r >= 6 and r<=10:
            cv2.circle(image,center,r,(0,255,0),2)
            #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
            array.append(center)



    array =  sorted(array)
  
    #center =sorted(center)

    #print(type(array))
    #print(type(center))
    array = np.asarray(array)
    array =  np.arange(90).reshape(15,6)
    #center = np.asarray(center)

    contours = np.asarray(contours)
    #contours = np.arange(90).reshape(15,5)

    #array = contours.sort_contours(array, method="top-to-bottom")[0]  
    #contours = contours.sort_contours(contours, method="top-to-bottom")[0]
    
    return image_color,array , contours


#cv2.imshow("preprocessed", image_color)
#cv2.waitKey(0)