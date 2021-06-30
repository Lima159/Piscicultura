import csv
import numpy as np

def closest(colors,color): #busca a cor mais próxima numa lista pre definida
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance 

def get_closet_color(color, arquivo):
	print(arquivo)
	with open(arquivo) as csv_file:
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
	    #color = [15,100,100]
	    print("\nCor:" + str(color))
	    closest_color = closest(array_colors,color) #Calculo de aproximação
	    print("\nCor aproximada:" + str(closest_color))
	    return closest_color

def get_resultado(closest_color, arquivo):
	red = closest_color[0][0]
	green = closest_color[0][1]
	blue = closest_color[0][2]

	with open(arquivo) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		result = 0

		for row in csv_reader:
			if line_count != 0:
				if(int(row[0]) == red and int(row[1]) == green and int(row[2]) == blue):
					result = row[3]					

			line_count += 1

	return result