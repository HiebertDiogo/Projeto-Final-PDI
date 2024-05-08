import cv2
import numpy as np

# Carregar a imagem do mapa de calor
mapa_imagem = cv2.imread('mapa_densidade_pontos.png')

# Converter a imagem para escala de cinza
mapa_cinza = cv2.cvtColor(mapa_imagem, cv2.COLOR_BGR2GRAY)

# Aplicar um filtro de suavização para reduzir o ruído
mapa_suave = cv2.GaussianBlur(mapa_cinza, (5, 5), 0)

# Aplicar o algoritmo de Watershed para segmentação
_, mapa_segmentado = cv2.threshold(mapa_suave, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
mapa_segmentado = cv2.morphologyEx(mapa_segmentado, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

# Identificar as regiões de alta densidade de pontos
contornos, _ = cv2.findContours(mapa_segmentado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > 100:  # Definir um limiar de área para identificar regiões significativas
        cv2.drawContours(mapa_imagem, [contorno], -1, (0, 255, 0), 2)

# Mostrar a imagem segmentada com as regiões identificadas
cv2.imshow('Mapa Segmentado', mapa_imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
