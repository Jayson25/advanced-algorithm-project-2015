import math, time

##########################################################################################

#Fonction naive

def NaiveRec(text,max,temp,i):
	#Si la phrase est inférieure ou égale au max
	if len(text) <= max:
		return text
		
	else:
		#On divise la phrase en liste de mots
		arrayText = text.split()
		
		#Si on atteint un index i égal à la taille de la liste de mots
		#on retourne la dernière ligne (on pense à vous les lecteurs ^^ )
		if i == len(arrayText):
			return temp
			
		#Si la phrase + mot actuel est inférieur au max, on rajoute notre mot dans la 
		#ligne et on passe au mot suivant
		if  len(temp) + len(arrayText[i]) < max:
			return NaiveRec(text,max,temp + " " + arrayText[i],i+1) 
		
		#Sinon on stock la ligne + saut de ligne + mot actuel dans une variable et on passe 
		#au prochain mot
		else:
			result = temp.strip() + "\n" + NaiveRec(text,max,arrayText[i],i+1)
		
		#on retourne le résultat
		return result
		
##########################################################################################
	
#Top-Down
	
def TopDown(text, arrayText, max, i, track):
	#Si l'index est supérieur à la taille de la liste de mots
	if i >= len(arrayText):
		return track[i-1]
	
	#Si la phrase est vide
	if len(text) == 0:
		return ""
	
	#Si la phrase est suffisament petite pour tenir sur une seule ligne
	elif len(text) <= max:
		return text
	
	#Si le track à l'index i est déjà rempli
	elif track[i] != "":
		return track[i]
		
	else:
		#On prend la dernière ligne
		lastLine = track[i-1].split("\n")
		#Si ligne + mot est plus petite que la limite
		if  len(lastLine[-1]) + len(arrayText[i]) < max:
			track[i] = track[i-1] + " " + arrayText[i]
			#On fait deux récursives à la fois sinon c'est pas drole :)
			return TopDown(text,arrayText,max,i+1,track) or TopDown(text,arrayText,max,i+2,track) 
		
		#sinon
		else:
			#On rajout le "\n" avant le mot dans le track
			track[i] = track[i-1].strip() + "\n" + arrayText[i]
			return TopDown(text,arrayText,max, i+1, track) or TopDown(text,arrayText,max,i+2,track) 
		

def ApplyTopDown(text, max):
	#On divise la phrase en une liste de mots
	arrayText = text.split()
	#On initialise un track qui va sauvegarder la progression/valeurs de notre fonction
	track = [""] * len(arrayText)
	return TopDown(text, arrayText, max, 0, track)

		

##########################################################################################

#Matrice des coûts sur une phrase

def Matrix(max, text):
	#Vu que tout les éléments de la matrice sont de la forme O(n^3) car on met tout au cube,
	#on a alors une complexité cubique
	
	arrayText = text.split()
	
	#On initialise la matrice qui est un carré de la taille de la ligne du texte à traiter
	matrix = [[0 for j in range(len(arrayText))] for i in range(len(arrayText))]
	
	for i in range(len(arrayText)):
		for j in range(len(arrayText)):
				#On initialise un compteur comportant le nombre d'espaces occupés
				count = 0
				
				#On rempli la case en faisant le max - (mot d'index i -> j)
				for k in range(i, j+1, 1):
					if k < j:
						count+=1
					count += len(arrayText[k])
				
				#On met le nombre d'éspaces restants dans la case
				matrix[i][j] = max - count
				
				#Si la case a pour valeur la taille de la ligne
				if matrix[i][j] == max:
					matrix[i][j] = float("inf")
				
				#Si la case est de taille inférieure
				else:
					matrix[i][j] = matrix[i][j]**3
				
				#Si on se retrouve en dessous de la diagonale (on pense au design pour le prof :D )
				if (i > j):
					matrix[i][j] = 0
				
				#Si on est largement supérieur au nombre d'espaces autorisé, alors on dit qu'il est infini
				if matrix[i][j] < 0:
					matrix[i][j] = float("inf")
	return matrix
	
##########################################################################################
	
#Bottom-Up

#On parcours la fin de la matrice.En effet, on part du général
#vers du précis. Du coup, le principe du bottom-up consiste à partir du plus petit sous-problème au 
#plus gros problème. Ainsi, on part de la plus petite solution jusqu'à la solution du problème.

def BottomUp(text, matrix):
	#On divise la phrase en une liste de mots
	arrayText = text.split()
	
	#Ce tableau permet de récupérer le coût minimum pour chaque ligne
	cost = [0] * len(matrix) 
	#Ce tableau permet de savoir le nombre de mots pour chaque ligne
	nbWord = [0] * len(matrix) 
	#On initialise l'index qui permet de créer le résultat
	index = 0
	#le résultat final
	result = ""
	
	for i in range(len(matrix)-1,-1,-1):
		#On va mettre le coût de la dernière colonne de la ligne
		cost[i] = matrix[i][len(matrix)-1]
		
		#on va ensuite initialiser la ligne où le mot va se placer
		nbWord[i] = len(matrix)
		
		#On va maintenant comparer le coût de chaque colonne de la ligne
		#On s'arrète à i pour eviter d'aller dans l'autre côté de la diagonal
		for j in range(len(matrix)-1, i, -1):
			#si l'élément est infini, on évite la suite de l'itération jusqu'à incrémentation de j sans 
			#casser la boucle
			if matrix[i][j-1] == float("inf"):
				continue
			
			#Si le coût actuel est supérieur (aux coûts précédents + la valeur de la colonne
			#précédente de la matrice (Pourquoi? car on veut voir à quel niveau on veut couper
			#la phrase par rapport aux résultats précédents)
			if cost[i] > (cost[j] + matrix[i][j-1]):
				cost[i] = cost[j] + matrix[i][j-1]
				nbWord[i] = j
	
	#Tant que nous ne somme pas dans le dernier élément de la liste de texte
	while (index<len(matrix)):
		#Notre maximum d'éléments (attention, elements ne sera pas réinitialisé à zero) dans la ligne
		elements = nbWord[index]
		#On copie le nombre d'éléments entre le premier mot (index = premier mot de la ligne dont 
		#dont sa valeur correspond à l'index de arrayText) et le dernier mot(element correspond à l'index+1 
		#arrayText du dernier mot de la ligne)
		for i in range(index, elements):
			result += arrayText[i] + " "
		result += "\n"
		index = elements
				
	return result
	
	
	
#########################################################################################

#Algorithme de Glouton
'''
	La solution gloutonne a pour but de mettre le plus de mots possible sur une ligne
	mais ce n'est pas optimisé car on voir d'après l'exemple 'sss uu pp iiiii' q'on ne peut
	pas avoir à tous les coups le moins d'espaces possible
'''	

def Glouton(text, max):
	#On divise la phrase en liste de mots
	arrayText = text.split()
	#sum correspond à la somme d'éspaces occupés de la ligne
	sum = 0
	#result est le résultat final
	result = ""
	
	#Pour chaque mot
	for i in range(len(arrayText)):
		#Si la taille du mot est plus grande que le nombre d'éspaces restants
		if (len(arrayText[i]) <= (max - sum)):
			result += arrayText[i] + " "
			sum += len(arrayText[i]) + 1
		
		#Sinon retour à la ligne 
		else:
			result += "\n" + arrayText[i] + " "
			#On ne l'initialise pas à 0 car on a mis un mot et un espace sur la nouvelle ligne
			sum = len(arrayText[i]) + 1
			
	return(result)
	
##########################################################################################

#Traitement de texte d'un fichier
	
def StreamFile(file, max):
	#Ouverture du fichier en mode read
	myFile = open(file,'r')
	#récupération du contenu du fichier
	fileContent =  myFile.read()
	#Ouverture/Création du fichier en mode write
	finalResult = open("after.txt","w")
	
	#liste des lignes du fichier
	arrayText = fileContent.split("\n")
	
	#On fait un bottom up pour chaque ligne
	for i in range(len(arrayText)):
		result = BottomUp(arrayText[i], Matrix(max, arrayText[i]))
		finalResult.write(result + "\n")	

	
##########################################################################################

#Les résultats

#string = "i am working very late at SUPINFO International University for finishing this exam"
string = "sss uu pp iiiii"
file = "before.txt"
#max = 20
max = 6

#Petite présentation sympatoche

print("\n---------------------2ADS - SPACE OPTIMIZATION-------------------\n",
	  "       Don't worry we did not made line cut in advanced ;)\n\n")

#Fonction naive

print("\n################### NAIVE ##################\n")
start = time.clock()
naive = NaiveRec(string, max, "", 0)
print(naive)
end = time.clock()
#permet d'estimer le temps d'exécution de la fonction
print ("%.2gs" % (end-start))

#TopDown

print("\n################### TOP-DOWN #####################\n")
start = time.clock()
topDown = ApplyTopDown(string, max)
print(topDown)
end = time.clock()
print ("%.2gs" % (end - start))

#Fonction bottom-up
	
print("\n################### BOTTOM-UP #############\n")
start = time.clock()
matrix = Matrix(max,string)
bottom = BottomUp(string, matrix)
print(bottom)
end = time.clock()
print ("%.2gs" % (end - start))

#traitement d'un fichier

print("\n################### FILE-STREAM #############\n")
start = time.clock()
StreamFile(file, 20)
end = time.clock()
print ("%.2gs" % (end - start))

#fonction gloutonne

print("\n################### GLOUTON #############\n")
start = time.clock()
glouton = Glouton(string, max)
print(glouton)
end = time.clock()
print ("%.2gs" % (end - start))

