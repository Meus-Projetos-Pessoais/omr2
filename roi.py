from __future__ import print_function
import cv2
import numpy as np
import align_images as align
import findGabarito as gabarito 
import contornosInternos
import bubble as bubble
import imutils
from imutils.perspective import four_point_transform
from imutils import contours
import bitwiseImage as bt


def roi(im):

    dim =  (1595,556)
    nomalizacao =  np.ones(dim)
    gabaritoInteresse = cv2.addWeighted(gabaritoInteresse, 1.07, np.zeros(gabaritoInteresse.shape, gabaritoInteresse.dtype),0,0)
    gabaritoInteresse =  cv2.normalize(gabaritoInteresse,nomalizacao,150,255, cv2.NORM_MINMAX)
    #cv2.imshow("tetste",tetste)
    gabaritoInteresse = cv2.cvtColor(gabaritoInteresse,cv2.COLOR_BGR2GRAY)

    imageBT = bt.bitwise(gabaritoInteresse)

    blurred =  cv2.GaussianBlur(gabaritoInteresse, (17,17),1)

    thresh = cv2.adaptiveThreshold(gabaritoInteresse, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    edged = cv2.Canny(blurred, 100,200)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

    heirarchy = cnts[1][0]

    cnts = cnts[0] if imutils.is_cv4() else cnts[1]

    questions = []

    imageBT = bt.bitwise(gabaritoInteresse)
    #cv2.imshow("imageBT",imageBT)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if (w >= 20 and h >= 20) and (w <= 25  and h <= 25) and ar >= 0.7 and ar <= 1.3:
            box = [(x//5)*5, y]
            #box = [x+w/2, y+h/2, w/2]
            
            questions.append([c, box])
            #print(x, y)
            #cv2.rectangle(gabarito, (x, y), (x+w, y+h), (255, 0, 0), 1)

    questions = sorted(questions, key=lambda q: q[1][1])

    questionCnts = []
    ''' 
      Agora estamos classificando da esquerda para a direita tomando um lote de 30 contornos 
      que são basicamente uma linha inteira e, em seguida, classificá-los a partir da ordem crescente de x 
    ''' 

    boxes = []
    for i in np.arange(0, len(questions), 30):
        # take a row of bubbles
        q = list(questions[i: i+30])
        #print(q)
        for o in q:
            boxes.append(o[1])
        # append each contour sorted from left to right in a row
        # sort them using x
        q = sorted(q, key=lambda k: k[1][0])
        for o in q:
            # append each contour sorted from left to right in a row
            #questionCnts.append(o[0])
            questionCnts.append(o[0])

    # each question has 5 possible answers, to loop over the
    # question in batches of 5

    #matrizRespostas = np.empty((0,4))
    #print(matrizRespostas.shape)
    respostas = np.empty(0,int)

    questao = []
    letra = []
    t=0

    matriz = []

    for (q, i) in enumerate(np.arange(0, len(questionCnts), 30)):
        # calculate the old question no
        row = q // 5
        col = q % 5
        old_question_no = col  + row

        #print(q)
        #print(i)
        cnts = contours.sort_contours(questionCnts[i:i+30])[0]


        #cnts = cnts[0:4:5]
        
        for (l ,k )in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(k)
            if (w >= 20 and h >= 20) and (w <= 25  and h <= 25) and ar >= 0.7 and ar <= 1.3:
                box = [(x//5)*5, y]
            #print(x, y)
            respostas = np.append(respostas,(l),)

            #rect = np.array(cv2.boundingRect(k)).reshape(1,4)
            #print(len(rect.shape))
            #matrizRespostas = np.append(matrizRespostas,rect,0)

            cv2.rectangle(bolhas, (x, y), (x+w, y+h), (0, 0, 255), 1)

      

    #print(len(cnts))  
    #respostas = respostas.reshape(75//5,5)
    respostas = respostas.reshape(len(respostas)//5,5)
    #respostas = respostas.reshape(89,5)
    print((respostas))
    #respostas = np.reshape(respostas,(5)

    return respostas