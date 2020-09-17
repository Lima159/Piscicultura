import cv2

def filtro(self):
    #imagemColorida = cv2.imread('Lena.jpg', cv2.IMREAD_COLOR) 
    imagemEmTonsDeCinza = cv2.imread(self.fileName, cv2.IMREAD_GRAYSCALE)

    return imagemEmTonsDeCinza
"""
    cv2.imshow('Imagem Colorida', imagemColorida)
    cv2.imshow('Imagem em Tons de Cinza', imagemEmTonsDeCinza)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""