import re
import time
import sys
import os

#flag = False #True: read the file into memory at one time; False: read one line at a time
def tokenize (content):
	tokens = []
	tokens.extend(process_data(content))
	return tokens

def process_data(data):
	tokens = data.lower()
	tokens = re.sub(r'[-]', ' ', tokens) #replace '-' with ' '
	tokens = re.sub(r'[^a-z0-9\s]', '', tokens) #remove punctuations
	tokens = re.sub("\s+", ' ', tokens) #remove extra space
	tokens = tokens.lstrip() #remove spaces at the beginning
	tokens = tokens.rstrip() #remove spaces at the end
	tokens = tokens.split(" ")
	if len(tokens) == 1 and '' in tokens:
		result = []
	else:
		result = []
		for t in tokens:
			if len(t) != 1:
				result.append(t)
	return result

def computeWordFrequencies(tokens):
	maps = {}
	for token in tokens:
		if not maps.has_key(token):
			maps[token] = 1
		else:
			maps[token] = maps[token] + 1
	#return maps
	sorted_key_list = sorted(maps, key=maps.get, reverse = True)
	sorted_map = {}
	for s in sorted_key_list:
		print (s + ": " + str(maps[s]))
		sorted_map[s] = maps[s]
	return sorted_map


def Print(frequencies):
	sorted_key_list = sorted(frequencies, key=frequencies.get, reverse = True)
	target = open('./results.txt', 'w')
	for s in sorted_key_list:
		print (s + ": " + str(frequencies[s]))
		target.write(s + ": " + str(frequencies[s]))
		target.write("\n")

def main(argv):
	if len(argv) >= 1:
		flag = False;
		if len(argv) >=2 and argv[1] == 'true':
			flag = True
		textFilePath = argv[0]
	else:
		print "No file as input. Please add text file path to the command."
		return
	start_time = time.time()
	Print(computeWordFrequencies(tokenize(textFilePath, flag)))
	#tokenize(textFilePath)
	print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
	main(sys.argv[1:])
