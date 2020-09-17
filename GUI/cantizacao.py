import numpy as np
import cv2

def filtro(self):
	imagemOriginal = cv2.imread('Lena.jpg')

	imagemVetorizada = imagemOriginal.reshape((-1, 3))
	imagemVetorizada = np.float32(imagemVetorizada)

	K = 8
	maximoDeIteracoes = 10
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, maximoDeIteracoes, 1.0)

	ret, label, center = cv2.kmeans(imagemVetorizada, K, None, criteria, maximoDeIteracoes, cv2.KMEANS_RANDOM_CENTERS)

	center = np.uint8(center)
	imagemQuantizada = center[label.flatten()]
	imagemQuantizada = imagemQuantizada.reshape((imagemOriginal.shape))

	return imagemQuantizada
	"""
	cv2.imshow('Imagem Original', imagemOriginal)
	cv2.imshow('Imagem Quantizada', imagemQuantizada)

	cv2.waitKey(0)
	"""