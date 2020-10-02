import csv
import numpy as np

def closest(colors,color): #busca a cor mais próxima numa lista pre definida
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance 

with open('tableColors.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    array_colors = []
    line_count = 0

    #Insere valores (exluindo nome da coluna) num array
    for row in csv_reader:
    	if line_count != 0:
    		array_color_row = []
    		array_color_row.append(row[0])
    		array_color_row.append(row[1])
    		array_color_row.append(row[2])
    		array_colors.append(array_color_row)
    	line_count += 1

    #Converte array em inteiros
    for i, elem in enumerate(array_colors):
    	array_colors[i] = [int(i) for i in elem]
    print(array_colors)
    color = [15,100,100]
    print("\nCor:" + str(color))
    closest_color = closest(array_colors,color) #Calculo de aproximação
    print("\nCor aproximada:" + str(closest_color))