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
from matplotlib import pyplot as plt
import h5py
import numpy as np
from skimage import morphology


im = 'template/templatePreenchido.png'





#alinhamento da imagem 
imagemAlinhada =  align.alignImages(im)
cv2.imwrite('template/processadaAlinhada.png', imagemAlinhada)
gabarito = gabarito.findGabarito(imagemAlinhada)

dim =  (1595,556)
gabarito =  cv2.resize(gabarito, dim, interpolation=cv2.INTER_CUBIC )

cv2.imwrite('template/gabarito.png', gabarito)


gabaritoInteresse = cv2.imread('template/gabarito.png')



bolhas, alternativaMarcada, contornosCirculos  =  bubble.bolhas(gabaritoInteresse)

nomalizacao =  np.ones(dim)
gabaritoInteresse = cv2.addWeighted(gabaritoInteresse, 1.07, np.zeros(gabaritoInteresse.shape, gabaritoInteresse.dtype),0,0)
gabaritoInteresse =  cv2.normalize(gabaritoInteresse,nomalizacao,150,255, cv2.NORM_MINMAX)
gabaritoInteresse = cv2.cvtColor(gabaritoInteresse.copy(),cv2.COLOR_BGR2GRAY)

blurred =  cv2.GaussianBlur(gabaritoInteresse, (17,17),1)

thresh = cv2.adaptiveThreshold(gabaritoInteresse, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

edged = cv2.Canny(blurred, 100,200)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

heirarchy = cnts[1][0]

cnts = cnts[0] if imutils.is_cv4() else cnts[1]

questions = []

#bolhas, alternativaMarcada, contornosCirculos  =  bubble.bolhas(gabaritoInteresse.copy())

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    if (w >= 18 and h >= 18) and (w <= 25  and h <= 25) and ar >= 0.7 and ar <= 1.3:
        box = [(x//5)*5, y]
        #box = [x+w/2, y+h/2, w/2]
        
        questions.append([c, box])
        #print(x, y)
        cv2.rectangle(gabarito, (x, y), (x+w, y+h), (255, 0, 0), 1)

questions = sorted(questions, key=lambda q: q[1][1])
questions =  np.asarray(questions)

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

#print(type(questionCnts))
# each question has 5 possible answers, to loop over the
# question in batches of 5

#matrizRespostas = np.empty((0,4))
#print(matrizRespostas.shape)
#posicaoRespostas = np.empty(0,int)
posicaoRespostas = []


questao = 0

questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

questaoMarcada = []

#questionCnts = np.asarray(questionCnts)

questions =  np.arange(450).reshape(450//30,30)

for (q, i) in enumerate(np.arange(0, len(questionCnts), 30)):
    # calculate the old question no

    cnts = contours.sort_contours(questionCnts[i:i+30], method="top-to-bottom")[0]

    #cnts =  np.asarray(cnts).reshape(1,5)
    Marcada = None
    for (l ,k )in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(k)
        ar = w / float(h)
        if (w >= 20 and h >= 20) and (w <= 25  and h <= 25) and ar >= 0.7 and ar <= 1.3:
            box = [(x//5)*5, y]

            cv2.rectangle(bolhas, (x, y), (x+w, y+h), (0, 0, 255), )

        #posicaoRespostas = np.append(posicaoRespostas,(l))
        posicaoRespostas.append(l)
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [k], -1, (255,0,0), -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)



        if Marcada is None or total > Marcada[0]:
            Marcada = [total,l]



    color = (0, 0, 255)
    xd = contornosCirculos[q]

    #if xd == Marcada[1]:
        #color = (0, 255, 0)
        #questaoMarcada.append(xd)
        #questao += 1

    #cv2.drawContours(gabarito, [cnts[k]], -1, color, 3) 

#xd = [x for x in xd if tuple(x) == (0, 0)]


print(type(xd))
print(type(Marcada))
print(type(posicaoRespostas))
print(type(questions))
print(type(alternativaMarcada))
print(type(contornosCirculos))
print(type(questionCnts))




#testeMatch =  cv2.matchShapes(questionCnts,alternativaMarcada,1,0.0)

#print((posicaoRespostas))

plt.imshow(bolhas)
plt.show()

#cv2.imshow("new_roi",new_roi)
#cv2.imshow("Bolhas",bolhas)
#cv2.imshow("Imagem Alinhada",imagemAlinhada)
#cv2.imshow("Gabarito",gabarito)


cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
