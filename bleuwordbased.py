import nltk
from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction
import pandas
#file = open('C:\\thesis\\afrikaans.txt',encoding="utf8") 
file = open('C:\\thesis\\zulu.txt',encoding="utf8")
afrlist = []
afrcount = 0
#goes through text file and adds each line to array
for line in file:
	afrlist.append(line)
	afrcount = afrcount+1
file.close() 
#print(afrlist[afrcount-50])
#print(afrcount)

#file = open('C:\\thesis\\english.txt',encoding="utf8") 
file = open('C:\\thesis\\englishzulu.txt',encoding="utf8") 

englist = []
engcount = 0
#goes through text file and adds each line to array
for line in file:
	englist.append(line)
	engcount = engcount+1
file.close() 
#print(englist[engcount-50])
#print(engcount)


eng_afr = []
#commontable ={'die':'the','dit':'it','om':'to','te':'','van':'from','dat':'that',"'":'','n':'a','of':'or','wat':'what','en':'and','vir':'for','is':'is','in':'in',',':',','.':'.','het':'have',')':')',"(":"(","word":"become"}
#commontable = {"'":"'", ".":"." ,";":";", ":":":", '"':'"',"die":"the","(":"(",")":")", ",":","}
commontable = {}

T_table = {}   #dictionary with english words as keys corresponding to dictionaries containing their top 3 possible translations and their counts
T_table2 = {}
T_table3 = {}
engcountdict = {} #dictionary with english words and their counts
counter = 0

for i in range (20000):
	temp_pair = []
	temp_pair.append(nltk.word_tokenize(englist[i]))
	temp_pair.append(nltk.word_tokenize(afrlist[i]))
	eng_afr.append(temp_pair)
	#need to initialise each word in the T-table
	for g in eng_afr[i][0]:  #iterating through tokens of english sentence
		if g not in T_table:  #if eng word not yet in dict, add it
		
			temp_dict = {}
			T_table[g] = temp_dict  #initialise an empty dict for the eng word
			engcountdict[g] = 1  # make eng count 1
			
	
		else:
			engcountdict[g] = engcountdict[g] + 1 #increment eng count dict
			
		for k in eng_afr[i][1]:   #iterate through mirror afrikaans sentence
			# I don't really want to limit the number of possible translations for each word as maybe halfway through the corpus there is a sudden change in context and a different meaning is implied - thus resulting in a different valid translation
			if k not in T_table[g]:
				T_table[g][k] = 1     #make dictionary entry of afr word and count for specific english word
			else:
				T_table[g][k] = T_table[g][k] + 1   #increment the count
	counter = counter+1
	if counter %1000 == 0:
		print(counter)
		


for word in T_table:  #shortening all translation possibilities to only 10
	
	for w in commontable:   #go through top 20 afr words for specific english word
		if w in T_table[word]:	  #if the word is in the commontable, remove it from T_table
			
			del T_table[word][w]
			
			
	sortedarray = sorted(T_table[word], key=T_table[word].get, reverse=True)   #sorted probabilities for specific eng word	
	topten = sortedarray[0:10]	  #make a top ten translation list
	
	
	
	for afrword in sortedarray: #go through all translation possibilities of english word
		
		
		if (afrword not in topten):	#if the word is not in top ten
			                                                                                                                                                                                                                                                                                                                                            
			del T_table[word][afrword] #delete from the translationtable
	


#we can do a kind of expectation maximisation - we already have a guess for each english word (the current world alignment table)
#create a T_table v2
#we can start off with the old table and re-iterate  over the corpus
#go through each sentence with the probabilities we have
#look at each afrikaans word and see the most probable english match and then add this entry or update the count in the T_table v2
engcountdict2 = {}
counter = 0
print("second iteration of T_table")
for i in range (20000):

	for g in eng_afr[i][0]:  #iterating through tokens of english sentence
		if g not in T_table2:  #if eng word not yet in dict, add it
		
			temp_dict = {}
			T_table2[g] = temp_dict  #initialise an empty dict for the eng word
			engcountdict2[g] = 1  # make eng count 1
			
	
		else:
			engcountdict2[g] = engcountdict2[g] + 1 #increment eng count dict
			
	for afr in eng_afr[i][1]:   #iterate through mirror afrikaans sentence
		maxprob = 0
		expectation = ""
		for eng in eng_afr[i][0]:  #go through the english words in the parallel sentence and only add the translation+count increment to the highest probability
			if afr in T_table[eng]:   #remember the original T_table has ben reduced to top 10 possibilities, so we must check that afr word is actually one of those
				if T_table[eng][afr]/engcountdict[eng] > maxprob:
					maxprob = T_table[eng][afr]/engcountdict[eng]
					expectation = eng
		#then only the expected translation is considered
		if expectation !="":      #must make sure that expectation was actually made
			if afr not in T_table2[expectation]:
				T_table2[expectation][afr] = 1     #make dictionary entry of afr word and count for specific english word
			else:
				T_table2[expectation][afr] = T_table2[expectation][afr] + 1   #increment the count
				
	#using this method, we have expectations from the previous T_table and only the expectations are incremented
	#eg. 'The' has 'die' as its most probable translation, but so does 'meeting', but since the-die is the greatest expectation
	#only the-die is incremented for instances of die. Same as how only vergadering will be incremented for instances of meeting
	counter = counter+1
	if counter %1000 == 0:
		print(counter)
		
		
engcountdict3 = {}
counter = 0
print("third iteration of T_table")
for i in range (20000):

	for g in eng_afr[i][0]:  #iterating through tokens of english sentence
		if g not in T_table3:  #if eng word not yet in dict, add it
		
			temp_dict = {}
			T_table3[g] = temp_dict  #initialise an empty dict for the eng word
			engcountdict3[g] = 1  # make eng count 1
			
	
		else:
			engcountdict3[g] = engcountdict3[g] + 1 #increment eng count dict
			
	for afr in eng_afr[i][1]:   #iterate through mirror afrikaans sentence
		maxprob = 0
		expectation = ""
		for eng in eng_afr[i][0]:  #go through the english words in the parallel sentence and only add the translation+count increment to the highest probability
			if afr in T_table2[eng]:   #remember the original T_table has ben reduced to top 10 possibilities, so we must check that afr word is actually one of those
				if T_table2[eng][afr]/engcountdict2[eng] > maxprob:
					maxprob = T_table2[eng][afr]/engcountdict2[eng]
					expectation = eng
		#then only the expected translation is considered
		if expectation !="":      #must make sure that expectation was actually made
			if afr not in T_table3[expectation]:
				T_table3[expectation][afr] = 1     #make dictionary entry of afr word and count for specific english word
			else:
				T_table3[expectation][afr] = T_table3[expectation][afr] + 1   #increment the count
				
	#using this method, we have expectations from the previous T_table and only the expectations are incremented
	#eg. 'The' has 'die' as its most probable translation, but so does 'meeting', but since the-die is the greatest expectation
	#only the-die is incremented for instances of die. Same as how only vergadering will be incremented for instances of meeting
	counter = counter+1
	if counter %1000 == 0:
		print(counter)


#go through the third T_table and populate the entries that have less than 5 possible translations - current entries have the greatest weight attached to them
#go through possible translations in the 2nd T_table and attach a lesser weight to them and populate the third table
#go through first T_table translations and attach an even smaller weight to these translations and populate the leftover spaces

for entry in T_table3: #go through each english word
	if len(T_table3[entry])<5:  #if it doesnt have 5 possible translations
		lowestcount = 100000
		
		for currenttrans in T_table3[entry]:
			if T_table3[entry][currenttrans] < lowestcount:
				lowestcount = T_table3[entry][currenttrans]  #get what the lowest count entry is
		for translation in T_table2[entry]: #go through T_table 2
			
			if translation not in T_table3[entry]: #if there is a possible translation in 2 that isn't in 3, add it
				prob =  T_table2[entry][translation]/engcountdict2[entry] #get prob of T_table2 entry
				#make s ure en  try has a lower count than all the other current entries
				if prob<1:
					T_table3[entry][translation] = lowestcount*(T_table2[entry][translation]/engcountdict2[entry]) 
				else:
					T_table3[entry][translation] = lowestcount-1
				
for entry in T_table3: #go through each english word
	if len(T_table3[entry])<5:  #if it doesnt have 5 possible translations
		lowestcount = 100000
		
		for currenttrans in T_table3[entry]:
			if T_table3[entry][currenttrans] < lowestcount:
				lowestcount = T_table3[entry][currenttrans]  #get what the lowest count entry is
		for translation in T_table[entry]: #go through T_table 2
			
			if translation not in T_table3[entry]: #if there is a possible translation in 2 that isn't in 3, add it
				prob =  T_table[entry][translation]/engcountdict2[entry] #get prob of T_table2 entry
				#make sure entry has a lower count than all the other current entries
				if prob<1:
					T_table3[entry][translation] = lowestcount*(T_table[entry][translation]/engcountdict[entry]) 
				else:
					T_table3[entry][translation] = lowestcount-1
					
					

#a reordering method must now be implemented
#with the alignment we have, word order can now be remembered
#the word order will be based on the positioning of the word in the english sentence
position_dict = {}     #maps english word to a dictionary containing its different positions that match up to the corresponding afr position
positionnumber_dict = {} # need to count the number of times an english word appears in a certain position so we can average the answer in position_dict afterwards
'''
print("Get position matches for english and afrikaans words")
counter = 0
for i in range (10000):
	engsentlen = len(eng_afr[i][0])  #length of english sentence
	afrsentlen = len(eng_afr[i][1])  #length of afrikaans sentence
	poscount = 0
	#go through english sentence and look for duplicate words
	# this will ensure that duplicate words are not mapped to the same translation, but still allows different words to be mapped to the same translation
	duplicatetracker = {}  #dictionary that remembers eng words and their counts in this sentence
	for eng in eng_afr[i][0]:  #go through english sentence
		if eng not in duplicatetracker:
			duplicatetracker[eng] = 1
		else:
			duplicatetracker[eng] = duplicatetracker[eng]+1
		
		poscount = poscount +1
		matches = [] #array of top translations for eng word
		for translation in T_table3:
			matches.append(translation)
		
		#go through afrikaans sentence
		afrposcount = 0
		matchcount = 0   #number of times the eng word has found a translation match
		for afr in eng_afr[i][1]: # go through afr sentence
			afrposcount = afrposcount+1 #increment word position counter
			if afr == matches[0]:  # if the afrikaans word is a top match for the english word
				matchcount = matchcount +1     #increment the number of times the english word has found a match
			if duplicatetracker[eng] == matchcount: #if the match counter is equal to the current duplicate tracker number of the english word
				break								#then this is the corresponding afr word to this specific english word (in case there are duplicates)
													#so the current afrposcount is kept and the loop is broken
		
		if eng not in position_dict:   #if english word not yet in pos dict - add it
			tempdict = {}
			tempdict2 = {}    #keeps track of the number of times an english word is in a specific position
			tempdict2[round(poscount/engsentlen,1)] = 1
			tempdict[round(poscount/engsentlen,1)] = round(afrposcount/afrsentlen,1)       # initialise dictionary that maps eng position (as a fraction) to afrikaans position
			position_dict[eng] = tempdict
			
			positionnumber_dict[eng] = tempdict2
		
		else:
			if round(poscount/engsentlen,1) not in position_dict[eng]:			#if this english position does not yet exist in the dict
				position_dict[eng][round(poscount/engsentlen,1)] = round(afrposcount/afrsentlen,2)
				positionnumber_dict[eng][round(poscount/engsentlen,1)]=1
				
			else:
				position_dict[eng][round(poscount/engsentlen,1)] = position_dict[eng][round(poscount/engsentlen,1)] +round(afrposcount/afrsentlen,1)
				positionnumber_dict[eng][round(poscount/engsentlen,1)] = positionnumber_dict[eng][round(poscount/engsentlen,1)] + 1

	counter = counter+1
	if counter%1000 == 0:
		print(counter)
#need to go through posdict and get average position
for eng in position_dict:
		print(eng)
		for pos in position_dict[eng]:
			print (str(position_dict[eng][pos]) + " " +str(positionnumber_dict[eng][pos]))
			position_dict[eng][pos] = position_dict[eng][pos] / positionnumber_dict[eng][pos]
			
			

wordinput = input("enter a word")

while wordinput != 'exit':
	
	for pos in position_dict[wordinput]:
		print("eng pos = " +str(pos)+ " | afrikaans pos = "+str(position_dict[wordinput][pos]))
	

'''






'''
#######################################################################################################################
#phrase maker
########################################################################################################################





#PHRASEMAKER ITERATOR

phrasetable = {}
testsentence = ["the","local","building","will","become","important","when","there","are","many","people"]
testafr = ["die", "plaaslike", "gebou","sal","belangrik","word","wanneer","daar","baie","mense","is"]
#testsentence = ["freedom","of","artistic","creativity"]
#testafr = ["inkululeko","yokwakha","izinto","ngokusebenzisa","ubuciko"]

ngramfactor = 3

for i in range (1):   #iterate through entire corpora
	
	rankingtable = {}     # keeps track of which words are the most aligned
						  # english word corresponds to a dictionary of afr matches that correspond to their ranking
	tempwordtable = {}
	phraserank_arr =  [[0 for afr in range(len(testafr))] for eng in range(len(testsentence))] # 2-d array: each array is a vector with afr words being dimensions
	#for engword in eng_afr[i][0]: #iterate through word in english sentence
	poscount = 0
	for engword in testsentence:
		
		tempdict = {}  #will keep corresponding afr words and their rankings
		rankingtable[engword] = tempdict
		matchingafrwords = []
		toptranslations = []
		
		for t in T_table3[engword]:		# get top translation matches from T_table
			toptranslations.append(t)
		
		#for afrword in eng_afr[i][1]:  #look at each word in corresponding afrikaans sentence
		
		

		afrposcount =0
		for afrword in testafr:		# loop through afrikaans sentence
			
			matchrank = 1
			for match in toptranslations:
				if afrword == match:
					rankingtable[engword][afrword] = matchrank
					
					phraserank_arr[poscount][afrposcount] = round(1/matchrank,2)
				matchrank = matchrank+1
						
			afrposcount = afrposcount+1
			
		poscount = poscount+1
	#now the ranking table has been obtained
	#now the phrases can be extracted
	phrase_eng_arr = [0 for eng in range(len(testsentence))]
	phrase_afr_arr = [0 for afr in range(len(testafr))]
	phrasenum = 1    #the number of the phrase being worked with
	previousdotprod = -1
	
	for engword in range(len(phraserank_arr)):    #go through ranking table
		
		dotproduct = 0
		if engword > 0:
			for afrword in range(len(phraserank_arr[engword])): # use dot product with previous to determine relationship
			
				dotproduct = dotproduct +phraserank_arr[engword][afrword]*phraserank_arr[engword-1][afrword] 
			if dotproduct >previousdotprod:
				if engword>1:
					phrasenum = phrasenum+1
					phrase_eng_arr[engword-1] = phrasenum
				
				
					
			
			
		phrase_eng_arr[engword] = phrasenum
		previousdotprod = dotproduct
	#now eng phrases have been grouped
	#now afr phrases need to be grouped
	for afrword in range(len(phrase_afr_arr)):	  #look at each afr word
		max = 0
		posofmax = -1
		for engword in range(len(phrase_eng_arr)):   #go through eng sentence to find best match
			if phraserank_arr[engword][afrword]>max:
				max = phraserank_arr[engword][afrword]  #keep updating best translation match until best is found
				posofmax = engword    # keep position of the max
				phrase_afr_arr[afrword] = phrase_eng_arr[posofmax]  #assign the afr word to the phrasegrouping corresponding to the position of the max eng word
	
	#need to correct phrase positioning - even though a certain alignment might be correct, if it is all over the place we can't  make a successful phrase
	#check which neighbourng phrase group has less members - add it to that phrase
	print(phrase_afr_arr)
	for afr in range(len(phrase_afr_arr)):
		if afr ==0:							# if it's the first word
			if phrase_afr_arr[afr]!=phrase_afr_arr[afr+1] and phrase_afr_arr.count(phrase_afr_arr[afr])>1 :   #if its the first word
				phrase_afr_arr[afr] = phrase_afr_arr[afr+1]			#and there are other disjointed words that map to the same phrase, just add it to the phrase that comes after it
		elif afr == len(phrase_afr_arr)-1:   #else if it's the last word in the sentence
			if phrase_afr_arr[afr]!=phrase_afr_arr[afr-1] and phrase_afr_arr.count(phrase_afr_arr[afr])>1:		#
				phrase_afr_arr[afr] = phrase_afr_arr[afr-1]
		else:
			
			if phrase_afr_arr.count(phrase_afr_arr[afr])>1 and (phrase_afr_arr[afr]!=phrase_afr_arr[afr-1] and phrase_afr_arr[afr]!=phrase_afr_arr[afr+1]):
				if phrase_afr_arr.count(phrase_afr_arr[afr-1]) < phrase_afr_arr.count(phrase_afr_arr[afr+1]):   #add to smaller phrase
					phrase_afr_arr[afr] = phrase_afr_arr[afr-1]					
					
				elif phrase_afr_arr.count(phrase_afr_arr[afr-1]) > phrase_afr_arr.count(phrase_afr_arr[afr+1]):
					phrase_afr_arr[afr] = phrase_afr_arr[afr+1]
					
print("phrases - eng")
print(phrase_eng_arr)
print("phrases - afr")
print(phrase_afr_arr)
#matrix = pandas.DataFrame(phraserank_arr, testsentence, testafr)	


phrase_arr_T = [[0 for col in range(len(testsentence))] for row in range(len(testafr))]
for afr in range(len(testafr)):
	for eng in range(len(testsentence)):
		
		phrase_arr_T[afr][eng] = phraserank_arr[eng][afr]
			
matrix = pandas.DataFrame(phrase_arr_T, testafr, testsentence)	
print(matrix)

			

		tempwordtable[engword] = matchingafrwords  #make dictionary entry for eng word and corresponding afr words
	phrase = []
	prevword = ""
	tempwordtable[prevword] = {""}
	for elem in tempwordtable:   #go through dictionary made from english sentence
		
		for afr in tempwordtable[elem]: #go through each word's matching afr words
			if(afr in tempwordtable[prevword]): # if an eng word has a translation match to the previous eng word append to make a phrase
				if (prevword not in phrase):
					phrase.append(prevword)
				phrase.append(elem)
				print(phrase)
			else:
				tempphrase = ""
				for pword in phrase:
					tempphrase += pword + " "
				tempphrase = tempphrase[:-1]
				phrasetable[tempphrase] = ""
				phrase.clear()
				print(tempphrase)
		prevword = elem
		
'''
print("finished tokenising")

counterforaverage = 0

hypothesis = ["the"]

reference1 = ["the"]
#bleuscore = bleu([reference1],hypothesis)
#BLEUscore = nltk.translate.bleu_score.sentence_bleu([reference1], hypothesis, weights = (0.5, 0.5))
#BLEUscore = nltk.translate.bleu_score.sentence_bleu([reference1], hypothesis)



sum = 0
for i in range (1000):
	
	outputsent = list()
	reference = eng_afr[i][1] #reference sentence
	for a in reference:
		if a == "'":
			reference.remove(a)
	
	#sentence = nltk.word_tokenize(sentenceinput)
	sentence = eng_afr[i][0]
	for t in sentence:  #iterate through input sentence, t is a word
		if t not in T_table3:
			print(t + " not in corpus")
			break
		#print(t + " counter = " + str(engcountdict[t]))
		#print()
		a1_sorted_keys = sorted(T_table3[t], key=T_table3[t].get, reverse=True)  #create a sorted array of the translations by order of count
		counter = 0;
		#print(a1_sorted_keys[:10])
		#print("Translation Probabilities:")
		checktable = True
		#for b in commontable.values():
		#	if (t == b):
		#		for j in commontable:
		#			if (commontable[j] == t):
		#				checktable = False;
		#				outputsent.append(j)
		#				print(j)
			
		if (checktable == True):
			for r in a1_sorted_keys:
				
		#		if (0.4 <T_table2[t][r] / engcountdict2[t]):#<1.5) :
				#print (r, T_table['administration'][r])
				if counter == 0:
					outputsent.append(r)
				counter = counter+1
				if counter == 15:
					break
								
				prob = (T_table3[t][r] / engcountdict3[t])
					#if prob <1.5 :
				#print (r, prob)
			
	#print()
	for c in range(len(outputsent)):
		if outputsent[c] == "'":
			outputsent[c] = "n"
	tempcount = 0
	cc = SmoothingFunction()
	print("\n")
	
	if(len(reference)>4 and len(outputsent)>4):
		#if (len(reference)>1 and len(outputsent)>1 ):
			print(eng_afr[i][0])
			print(eng_afr[i][1])
			print(outputsent)
			counterforaverage = counterforaverage +1
			sum = sum +bleu([reference], outputsent, smoothing_function=cc.method4)
	'''
	if len(outputsent)<4 and len(reference)<4:
		
		sum = sum +nltk.translate.bleu_score.sentence_bleu([reference], outputsent, weights = (0.25, 0.25,0.25,0.25))
	else:
		sum = sum +nltk.translate.bleu_score.sentence_bleu([reference], outputsent)
		'''
	#print(outputsent)
	#sentenceinput = input("enter an english sentence: ")
print("BLEU = " + str(sum/counterforaverage) )