#direwolf.py
#Dean Mock
#Version 8 April 2019
#Used with the permission of and giving credit to sci-kit learn


import requests, json, re
from pprint import pprint
from bs4 import BeautifulSoup
import sys
import re, string, unicodedata
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import pairwise_distances_argmin_min



from sklearn.cluster import KMeans

def Intro():
	print("WELCOME TO THE DIREWOLF PROGRAM..")
	print("This program allows you to efficiently explore")
	print("large amounts of data from Backpage.com.")
	print("Choose a city, a category, and a date and save")
	print("that webpage as an HTML file. Then, using standard input,")
	print("run that HTML page through the terminal. The Direwolf")
	print("program will then open the page as a file and then use BeautifulSoup")
	print("to parse the file. It will then clean up the text, removing all the ")
	print("HTML tags. Next, comes further cleaning. The text will be tokenized and")
	print(" made lowercase. Then non ASCII compatible characters, punctuation marks,")
	print(" white space, and stop words (is, and, I, etc) will be removed. *****If ")
	print("you wish to include stop words, simply go into the code, and put a # in ")
	print(" front of the noStopWords line in the preProcess function. This will make ")
	print("the program allow stop words.*****")
	answer = input("Type 'run' to start the program. Type 'stop' to quit. \n")
	if answer != "run":
		exit()


#IF YOU WISH TO READ IN ONLY 1 FILE THROUGH STANDARD INPUT
#opens saved HTML page through standard input and stores it
#in a file. Returns string
# def openStdIn():
# 	si_file = ""
# 	for line in sys.stdin:
# 		si_file += line.rstrip()
# 	return si_file


def getFilenames(file_dir):
	files = os.listdir(file_dir)
	allFiles = []
	for file in files:
		path = os.path.join(file_dir, file)
		allFiles.append(path)
	return allFiles



#Parses the file with BeautifulSoup. Returns string.
def Process(file_list):
	print("\n Processing data...")
	all_data = []
	for filename in file_list:
		print("    ", filename)
		file = open(filename, "r")
		page_content = BeautifulSoup(file, "html.parser")
		data = preProcess(page_content)
		all_data.extend(data)
		file.close()
	return all_data
	#print(all_data)


##################################################################################################	

#cleans the string up removing HTML tags. Puts result in dictionary. 
#Returns a dictionary.
def cleanText(page_content):
	titles = page_content.find_all('div', attrs={'class': 'cat'})
	data  = []
	for title in titles:
		data.append(title.get_text())
	return data



#tokenizes the string from one lng string into "words." Returns a string.
def Tokenize(data):
	for i in range(len(data)):
		text_val = data[i]
		data[i] = nltk.word_tokenize(text_val.lower())


#turns the string of tokenized text into a list of strings with only ascii characters
def onlyASCII(data):
	for i in range(len(data)):
		text_list = data[i]
		for j in range(len(text_list)):
			word = text_list[j]
			ascii_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
			text_list[j] = ascii_word
		data[i] = text_list



#makes list of strings lowercase. returns list of strings
def noPunctuation(data):
	for i in range(len(data)):
		just_words_or_nums = []
		text_list = data[i]
		for j in range(len(text_list)):
			word = re.sub(r'[^\w\s]', '', text_list[j])
			if word != '':
				just_words_or_nums.append(word)
		data[i] = just_words_or_nums


#removes white spaces
def removeWhitespace(data):
	for i in range(len(data)):
		text_list = data[i]
		for j in range(len(text_list)):
			word = text_list[j]
			text_list[j] = word.strip()
		data[i] = text_list
	

#removes stop words
def noStopWords(data):
	for i in range(len(data)):
		go_words = []
		text_list = data[i]
		for j in range(len(text_list)):
			word = text_list[j]
			if word not in stopwords.words('english', 'spanish'):
				go_words.append(word)
		data[i] = go_words

#joins the items in the text list
def joinTextList(data):
	for i in range(len(data)):
		text_list = data[i]
		data[i] = ' '.join(text_list)


##############################################################################################

#prints data to file
def printData(data, outfile_name):
	outfile = open(outfile_name, "w")
	for i in range(len(data)):
		print(data[i], file = outfile)
	outfile.close()
		#print(' '.join(text_list))




def createVectorizer(data):
	print("Which vectorizer would you like to use?")
	vec = input("1) TfidfVectorizer 2) CountVectorizer 3) HashingVectorizer \n")
	if vec == "1":
		vectorizer = TfidfVectorizer()
	elif vec == "2":
		vectorizer = CountVectorizer()
	else:
		vectorizer = HashingVectorizer()
	return vectorizer






#preprocesses and then returns file
def preProcess(content):
	data = cleanText(content)
	Tokenize(data)
	onlyASCII(data)
	noPunctuation(data)
	removeWhitespace(data)
	noStopWords(data)
	joinTextList(data)
	#printData(data)
	return data




def Cluster(data):
	print("\n Initiating clustering...")
	vectorizer = createVectorizer(data)
	feature_matrix = vectorizer.fit_transform(data)
	print("\n Vectorization complete")
	print("\n Which clustering method would you like to use?")
	method = input("\n 1) KMeans 2) AffinityPropagation ")
	if method == "1":
		print("Clustering...")
		kmeans = KMeans(n_clusters = 2, random_state = 0).fit(feature_matrix)
		print(kmeans.labels_)
		filename = input("Type a name for you new file. Ex: newfile \n")
		outputClusterstoFiles(filename, data, kmeans.labels_)
		print("Number of iterations: ", kmeans.n_iter_)
		print("Sum of squared distances from closest cluster center: ", kmeans.inertia_)
		print("Coordinates of cluster centers: ", kmeans.cluster_centers_)
		closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, feature_matrix)
		print(closest)
		print("closest to centroid 0: ", data[closest[0]])
		print("closest to centroid 1: ", data[closest[1]])
	else:
		print("Clustering...")
		affprop = AffinityPropagation().fit(feature_matrix)
		print(affprop.labels_)
		filename = input("Type a name for you new file. Ex: newfile \n")
		outputClusterstoFiles(filename, data, affprop.labels_)
		print("Number of iterations: ", affprop.n_iter_)
		print("Coordinates of cluster centers: ", affprop.cluster_centers_)





def outputClusterstoFiles(filename, data, labels):
	outputcluster_0 = open(filename + "0.txt", "w")
	outputcluster_1 = open(filename + "1.txt", "w")
	for i in range(len(data)):
		if labels[i] == 0:
			print(data[i], file = outputcluster_0)
		else:
			print(data[i], file = outputcluster_1)
	outputcluster_0.close()
	outputcluster_1.close()



		#data[i] = nltk.word_tokenize(text_val.lower())
	#1 - open 2 files to write to (call the first one outputcluster_0, outputcluster_1)
	#2 - loop over indexes in data like def tokenize. 
	#3 - if labels[i] = 0, output to 0 file
			#print data[i] to outputcluster_0 file
		# else
			#.....






def main():
	Intro()
	#file = openStdIn()  ---> CALL THIS FUNCTION IF USING STANDARD INPUT
	file_dir = input("Please input the name of your directory of HTML files \n")
	file_list = getFilenames(file_dir)
	data = Process(file_list)
	print(data)
	print(len(data), " ads analyzed ")
	Cluster(data)



main()










