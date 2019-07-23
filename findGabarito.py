# Referências :
#     Amey Umarekar https://github.com/AmeyCaps/Document_Scanner/blob/master/scan_doc.py
#     Adrian Rosenbrook https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
#	  https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

from __future__ import print_function
import cv2
import numpy as np

#importando a imagem
#
#img = "imagens/photo_2018-08-10_12-55-51.jpg"
#img = "imagens/photo_2019-07-04_13-33-00.jpg"
#img ='C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/imgs/03MARCADO.jpg'
#img = 'C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/template/template25.png'
#img = 'C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/processadas/processadaAlinhada.png'

def findGabarito(img):
	#é que print(img)
	#imagemInicial = cv2.imread(img)
	imagemInicial =  img 
	#print(imagemInicial.shape)
	#redimensionando a imagem para facilitar a extração dos dados

	#scale_percent = 100 # percent of original size
	#width = int(imagemInicial.shape[1] * scale_percent / 100)
	#height = int(imagemInicial.shape[0] * scale_percent / 100)
	#dim = (width, height)

	#imagemInicial =  cv2.resize(imagemInicial,dim, interpolation=cv2.INTER_AREA)

	#convertendo para escalas de cinza, para que fique mais fácil de manipular a imagem
	cinza = cv2.cvtColor(imagemInicial, cv2.COLOR_BGR2GRAY)

	#passando no primeiro filtro de Gauss
	filtroGauss = cv2.GaussianBlur(cinza, (5,5),0)

	#buscando os contornos externos da imagem com o operador Canny	
	contornosExternos = cv2.Canny(filtroGauss, 0 ,50)

	#buscando os contornos da imagem
	#cv2.RETR_LIST : Recupera todos os contornos, mas não cria relacionamento entre os dados
	#CHAIN_APPROX_SIMPLE : Recupera todos os pontos do contorno, não somente os limites superiores da imagem.

	contornos, _ = cv2.findContours(contornosExternos, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#classificando a área dos contornos identificados
	contornos = sorted(contornos, key=cv2.contourArea, reverse= True)

	#Desenhando os contornos da imagem

	#cv2.arcLength : Cria os contornos da imagem de interesse

	#cv2.approxPolyDP : Mostra a curva criada para os contornos da imagem. 

	for i in contornos:
		elipse =  cv2.arcLength(i, True)
		aproximacao = cv2.approxPolyDP(i,0.08*elipse, True)

		if len(aproximacao) == 4 :
			documentoMatriz = aproximacao
			break

	#Desenhando os contornos da imagem, em que as bordas mostradas na cor verde
	#cv2.drawContours(imagemInicial, [documentoMatriz], -1,(0,255,0),2)

	#Redimensionando a matriz para evitar erros à frente.  A Matriz terá a dimensão 4x2
	documentoMatriz =documentoMatriz.reshape((4,2))


	#Criando uma nova matriz 4x2 para manipular a frente os dados da imagem
	novoDocumentoMatriz = np.zeros((4,2), dtype="float32")

	#Fazendo a soma dos valores do eixo da linha, criando um vetor com os valores obtidos.
	soma = documentoMatriz.sum(axis = 1 )

	#Adicionando valores a matriz criada
	novoDocumentoMatriz[0] = documentoMatriz[np.argmin(soma)]
	novoDocumentoMatriz[2] = documentoMatriz[np.argmax(soma)]	

	#Fazendo a diferença dos eixos 
	diferenca =  np.diff(documentoMatriz, axis = 1)

	novoDocumentoMatriz[1] = documentoMatriz[np.argmin(diferenca)]
	novoDocumentoMatriz[3] = documentoMatriz[np.argmax(diferenca)]

	(tl,tr,br,bl) = novoDocumentoMatriz

	#Encontrando a distância entre os pontos e obtenha o valor máximo
	#normalizando os dados obtidos
	distancia1 = np.linalg.norm(br-bl)
	distancia2 = np.linalg.norm(tr-tl)

	#Encontrando o valor máximo das distâncias
	tamanhoMaximo = max(int(distancia1), int(distancia2))

	#Encontrando a distância entre os pontos e obtenha o valor máximo
	#normalizando os dados obtidos
	distancia3 = np.linalg.norm(tr-br)
	distancia4 = np.linalg.norm(tl-bl)

	#Encontrando a altura máxima das distâncias
	alturaMaxima = max(int(distancia3), int(distancia4))

	#criando uma matriz com os valores máximos obtidos
	dst = np.array([[0,0],[tamanhoMaximo-1, 0],[tamanhoMaximo-1, alturaMaxima-1], [0, alturaMaxima-1]], dtype=	"float32")

	N = cv2.getPerspectiveTransform(novoDocumentoMatriz, dst)
	# Criando a deformação da perspectiva
	deformacao = cv2.warpPerspective(imagemInicial, N, (tamanhoMaximo, alturaMaxima))
	#Criando uma nova imagem com o processamento obtido
	#imagemSaida = cv2.cvtColor(deformacao, cv2.COLOR_BGR2GRAY)
	imagemSaida =  np.array(deformacao)
	#Redimensionando a imagem
	#imagemSaida = cv2.resize(imagemSaida


	#cv2.imshow("Imagem Original",imagemInicial)
	#cv2.imshow("Escala de Cinza",cinza)
	#cv2.imshow("Filtro Gaussiano",filtroGauss)
	#cv2.imshow("Contornos com operador de Canny",contornosExternos)
	#cv2.imshow("Threshold.jpg",threshold)



	#scale_percent = 160 # percent of original size
	#width = int(imagemSaida.shape[1] * scale_percent / 100)
	#height = int(imagemSaida.shape[0] * scale_percent / 100)
	#dim = (width, height)
	#imagemSaida = cv2.resize(imagemSaida, dim, interpolation = cv2.INTER_AREA)

	#cv2.imshow("Contornos", imagemInicial)
	#print(imagemSaida.shape)
	#cv2.imshow("Escaneado", imagemSaida)

	return imagemSaida

#cv2.imwrite("C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/testes/imagemCortada.jpg", imagemSaida)



#cv2.imwrite("C:/Users/Andre/Desktop/Softwillians/Processamento de imagens/OMR/imgs/photo3Copia1Escaneado.jpg", imagemSaida)
#esperando uma tecla para poder fechar as janelas
#cv2.waitKey(0)
#limpa a memória 
#cv2.destroyAllWindows()

