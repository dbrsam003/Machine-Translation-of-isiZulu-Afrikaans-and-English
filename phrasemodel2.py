import nltk
import pandas














file = open('C:\\thesis\\afrikaans.txt',encoding="utf8") 
#file = open('C:\\thesis\\zulu.txt',encoding="utf8")
afrlist = []
afrcount = 0
#goes through text file and adds each line to array
for line in file:
	afrlist.append(line)
	afrcount = afrcount+1
file.close() 
print("afr length ")
print(afrcount)
#print(afrlist[afrcount-50])
#print(afrcount)

file = open('C:\\thesis\\english.txt',encoding="utf8") 
#file = open('C:\\thesis\\englishzulu.txt',encoding="utf8") 
englist = []
engcount = 0
#goes through text file and adds each line to array
for line in file:
	englist.append(line)
	engcount = engcount+1
print("eng length ")
print(engcount)
file.close() 
#print(englist[engcount-50])
#print(engcount)
acount = 0
print(len(afrlist))
print(len(englist))
sentences = 20000
eng_afr = []
#commontable ={'die':'the','dit':'it','om':'to','te':'','van':'from','dat':'that',"'":'','n':'a','of':'or','wat':'what','en':'and','vir':'for','is':'is','in':'in',',':',','.':'.','het':'have',')':')',"(":"(","word":"become"}
#commontable = {"'":"'", ".":"." ,";":";", ":":":", '"':'"',"die":"the","(":"(",")":")", ",":","}
commontable = {}

T_table = {}   #dictionary with english words as keys corresponding to dictionaries containing their top 3 possible translations and their counts
T_table2 = {}
T_table3 = {}
engcountdict = {} #dictionary with english words and their counts
counter = 0

for i in range (sentences):
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
for i in range (sentences):

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
for i in range (sentences):

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







#######################################################################################################################
#phrase maker
########################################################################################################################



#TEST EXAMPLE


testsentence = ["the","local","building","will","become","important","when","there","are","many","people"]
testafr = ["die", "plaaslike", "gebou","sal","belangrik","word","wanneer","daar","baie","mense","is"]
#testsentence = ["freedom","of","artistic","creativity"]
#testafr = ["inkululeko","yokwakha","izinto","ngokusebenzisa","ubuciko"]
#phrase table will be a dictionary with keys = english phrase
#corresponding entries will be an array with first element = eng phrase pos, second element = afr phrase pos
# third element = afr sentence, last 4 elements - first 2 the two words preceding, second two the two words after
ngramfactor = 3
phrase_table = {}
beforereshape = ""
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
	print( phrase_afr_arr)
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
	#now the phrases can finally be assembled
	engstring_arr = []
	prevnum = 1
	phrase = []
	for word in range(len(phrase_eng_arr)):  # go through english sentence
		
		if phrase_eng_arr[word] == prevnum:  #if phrasenum equals previous phrasenum
			phrase.append(testsentence[word]) #add it to the phrase
		else:
			
			engstring_arr.append(phrase)    #otherwise phrase is finished and must be added to the phrase array/table
			phrase = []
			phrase.append(testsentence[word])				#phrase is started again
		prevnum = phrase_eng_arr[word]
	#last phrase must be added
	
	engstring_arr.append(phrase)    
	phrase = []
	phrase.append(testsentence[word])				#phrase is started again
	
	#the english phrases must be mapped to the other phrases
	for num in range(1,(len(engstring_arr)+1)): #go through english phrasenumbers
		afrphrase = []
		prevphrasenum = 0
		afrpos = 0
		phrasepos = 0
		for afrnum in range(len(phrase_afr_arr)):  #go through afr phrase number array
			if phrase_afr_arr[afrnum]!= prevphrasenum:  #if the afrikaans phrase match number changes, then we know we've moved onto the next phrase
				afrpos = afrpos +1
			if phrase_afr_arr[afrnum] == num:		#if the number matches the current english phrase
				phrasepos = afrpos 					#save the position
				afrphrase.append(testafr[afrnum])			#append it to the afrikaans phrase
			prevphrasenum = phrase_afr_arr[afrnum]
		entry = []
		entry.append(round(num/len(engstring_arr),1)) #eng phrase pos
		entry.append(round(phrasepos/len(engstring_arr),1)) #afr phrase pos
		
		for i in afrphrase:   #add afr phrase
			entry.append(i)
		beforenafter = ["",""]			#word before and after
		if len(engstring_arr)>1:		#if it's not  one word sentence
			if num > 1:					#if not first phrase in sentence
				beforenafter[0] = (engstring_arr[num-2][-1]) 		#get preceding word - last word of previous phrase
			if num < len(engstring_arr)-1:
				beforenafter[1] = (engstring_arr[num][0])		#get proceding word - first word of next phrase
		entry.append(beforenafter[0])
		entry.append(beforenafter[1])
		if tuple(engstring_arr[num-1]) not in phrase_table:			#add to phrasetable
			
			phrase_table[tuple(engstring_arr[num-1])] = []		#convert list to tuple because list is unhashable - cannot be used as key
			phrase_table[tuple(engstring_arr[num-1])].append(entry)
		else:
			phrase_table[tuple(engstring_arr[num-1])].append(entry)

phrase_arr_T = [[0 for col in range(len(testsentence))] for row in range(len(testafr))]
for afr in range(len(testafr)):
	for eng in range(len(testsentence)):
		
		phrase_arr_T[afr][eng] = phraserank_arr[eng][afr]
			
matrix = pandas.DataFrame(phrase_arr_T, testafr, testsentence)	
print(matrix)
print()			
print("phrases - eng")
print(phrase_eng_arr)
print("phrases - afr")
print("after")
print(phrase_afr_arr)
print()
for a in engstring_arr:
		print(a)


print()
#matrix = pandas.DataFrame(phraserank_arr, testsentence, testafr)	
print("PHRASE TABLE")
print(len(phrase_table))
for key in phrase_table:
	print(key)
	print(phrase_table[key])

'''
###################################################################################################################################

#ACTUAL PHRASEMAKING ITERATION

###################################################################################################################################
phrase_table = {}
phrasecounttracker = {} #keeps track of phrase counts fo probability calculation
engphrasecount = {}
count = 0
print("MAKING PHRASE TABLE")
for i in range (sentences):   #iterate through entire corpora
	
	rankingtable = {}     # keeps track of which words are the most aligned
						  # english word corresponds to a dictionary of afr matches that correspond to their ranking
	tempwordtable = {}
	phraserank_arr =  [[0 for afr in range(len(eng_afr[i][1]))] for eng in range(len(eng_afr[i][0]))] # 2-d array: each array is a vector with afr words being dimensions
	#for engword in eng_afr[i][0]: #iterate through word in english sentence
	poscount = 0
	for engword in eng_afr[i][0]:
		
		tempdict = {}  #will keep corresponding afr words and their rankings
		rankingtable[engword] = tempdict
		matchingafrwords = []
		toptranslations = []
		
		for t in T_table3[engword]:		# get top translation matches from T_table
			toptranslations.append(t)
		
		#for afrword in eng_afr[i][1]:  #look at each word in corresponding afrikaans sentence
		
		

		afrposcount =0
		for afrword in eng_afr[i][1]:		# loop through afrikaans sentence
			
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
	phrase_eng_arr = [0 for eng in range(len(eng_afr[i][0]))]
	phrase_afr_arr = [0 for afr in range(len(eng_afr[i][1]))]
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
	#print( phrase_afr_arr)
	if len(phrase_afr_arr) > 1:
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
	#now the phrases can finally be assembled
	engstring_arr = []
	prevnum = 1
	phrase = []
	for word in range(len(phrase_eng_arr)):  # go through english sentence
		
		if phrase_eng_arr[word] == prevnum:  #if phrasenum equals previous phrasenum
			phrase.append(eng_afr[i][0][word]) #add it to the phrase
		else:
			
			engstring_arr.append(phrase)    #otherwise phrase is finished and must be added to the phrase array/table
			phrase = []
			phrase.append(eng_afr[i][0][word])				#phrase is started again
		prevnum = phrase_eng_arr[word]
	#last phrase must be added
	
	engstring_arr.append(phrase)    
	phrase = []
	#print(word)
	#phrase.append(eng_afr[i][0][word])				#phrase is started again
	
	#the english phrases must be mapped to the other phrases
	for num in range(1,(len(engstring_arr)+1)): #go through english phrasenumbers
		afrphrase = []
		prevphrasenum = 0
		afrpos = 0
		phrasepos = 0
		for afrnum in range(len(phrase_afr_arr)):  #go through afr phrase number array
			if phrase_afr_arr[afrnum]!= prevphrasenum:  #if the afrikaans phrase match number changes, then we know we've moved onto the next phrase
				afrpos = afrpos +1
			if phrase_afr_arr[afrnum] == num:		#if the number matches the current english phrase
				phrasepos = afrpos 					#save the position
				
				afrphrase.append(eng_afr[i][1][afrnum])			#append it to the afrikaans phrase
			prevphrasenum = phrase_afr_arr[afrnum]
		entry = []
		entry.append(round(num/len(engstring_arr),1)) #eng phrase pos
		entry.append(round(phrasepos/len(engstring_arr),1)) #afr phrase pos
		
		for phr in afrphrase:   #add afr phrase
			entry.append(phr)
		beforenafter = ["",""]			#word before and after
		if len(engstring_arr)>1:		#if it's not  one word sentence
			if num > 1:					#if not first phrase in sentence
				beforenafter[0] = (engstring_arr[num-2][-1]) 		#get preceding word - last word of previous phrase
			if num < len(engstring_arr)-1:
				beforenafter[1] = (engstring_arr[num][0])		#get proceding word - first word of next phrase
		entry.append(beforenafter[0])
		entry.append(beforenafter[1])
		if tuple(engstring_arr[num-1]) not in phrase_table:			#add to phrasetable
			
			phrase_table[tuple(engstring_arr[num-1])] = []		#convert list to tuple because list is unhashable - cannot be used as key
			phrase_table[tuple(engstring_arr[num-1])].append(entry)
			engphrasecount[tuple(engstring_arr[num-1])] = 1
			targetlangentry = {}
			targetlangentry[tuple(entry[2:-2])] = 1
			phrasecounttracker[tuple(engstring_arr[num-1])] = targetlangentry
		else:
			engphrasecount[tuple(engstring_arr[num-1])] = engphrasecount[tuple(engstring_arr[num-1])] +1
			phrase_table[tuple(engstring_arr[num-1])].append(entry)
			if (tuple(entry[2:-2]) in phrasecounttracker[tuple(engstring_arr[num-1])] ):
				phrasecounttracker[tuple(engstring_arr[num-1])][tuple(entry[2:-2])] = phrasecounttracker[tuple(engstring_arr[num-1])][tuple(entry[2:-2])] +1
			else:
				phrasecounttracker[tuple(engstring_arr[num-1])][tuple(entry[2:-2])] = 1
	count = count+1
	if count%1000 == 0:
		print(count)

print("finished tokenising")	
sentenceinput = input("enter an english sentence: ")
#need to go through sentence and sort it into all possible phrases that exist in the phrase table
#scores need to be assigned to: the number of times this phrase has occurred, the words before and after and its position
trans_score = 1
dist_score = 1
ngram_score = 1
sentence_transandinfo = {}
while sentenceinput != 'exit':
	sentence = []
	sentence = nltk.word_tokenize(sentenceinput)
	outputsent = []
	phrase_array = []
	
	
	for start in range(len(sentence)):		#start point goes from beginning of sentence to end (phrase gets smaller)
		phrase = []							#reset phrase
		for w in range(start,len(sentence)):#go from start to end
			phrase.append(sentence[w])		#
			
			if tuple(phrase) in phrase_table:
				phrase_array.append(phrase[:])   #??????????????????????
				
			
	#construct the sentence in all the possible ways with all the different phrases
	possiblesentences = []   #[[[a],[bit],[of],[luck]],[[second],[sentence]]]
	print(phrase_array)
	count = 0
	for phr in phrase_array:
		newsentence = []
		if phr[0] == sentence[0]:
			newsentence.append(phr[:])
			possiblesentences.append(newsentence[:])
			
	count = 0
	while count < len(sentence)-1:
		for sent in range(len(possiblesentences)):					#go through sentences being built - these are 
			for phr in phrase_array:
				if possiblesentences[sent][-1][-1] in sentence[count:] and ((sentence[count:].index(possiblesentences[sent][-1][-1]))+count+1) <len(sentence) :
					print((sentence[count:].index(possiblesentences[sent][-1][-1]))+count+1)
					if phr[0] == sentence[(sentence[count:].index(possiblesentences[sent][-1][-1]))+count+1]:			#using indexing feature always finds first occurence
						possiblesentences[sent].append(phr[:])	
		count = count +1
	print("possible sentences")
	print("\n")
	for a in possiblesentences:
		print(a)
		print("\n")
	allpossibletranslations = []										#we also need to store phrase table entry information for later scoring
	alltranslationinfo = []
	phrase_transandinfo = {}
	for sent in possiblesentences:										#go through different sentences - [["the thing"],["is here"]]
		possibletranslations = []
		translationinfo = []
		counter = 0
		for phr in sent:												# ["the thing"]
			if (counter == 0):											#if it's the beginning of a sentence - first phrase
				for entry in phrase_table[tuple(phr)]:
					info_entry = []
					posstrans = []
					if (len(entry[2:-2])>1):
						posstrans.append(entry[2:-2])
						possibletranslations.append(posstrans)
						info_entry.append(entry[:])
						translationinfo.append(info_entry[:])
			else:
				newerinfo = []
				newerpossibilities = []
																			# all translation for this sentence thus far
				for m in range(len(possibletranslations)):	
					for entry in phrase_table[tuple(phr)]:					#for each possible sentence so far go through all possible translations of 'the thing'
						newinfo = translationinfo[m][:]
						newpossibility = possibletranslations[m][:]												#append all the translations to each of the possible sentences so far
						if (len(entry[2:-2])>1):													# make these the new possible sentences
							newinfo.append(entry[:])
							newerinfo.append(newinfo)
							newpossibility.append(entry[2:-2])
							newerpossibilities.append(newpossibility)
				translationinfo = newerinfo[:]	
				possibletranslations = newerpossibilities[:]
			counter = counter+1
		
		for b in range(len(possibletranslations)):
			anarray = []
			anarray.append(translationinfo[:])
			anarray.append(possibletranslations[:])
			#sentence_transandinfo[tuple(sent)] = tuple(anarray)
			#sentence_transandinfo[tuple(sent)] = [translationinfo,possibletranslations]   #corresponds to sentence
			alltranslationinfo.append(translationinfo)
			
			allpossibletranslations.append(possibletranslations[b][:])
			
	#print(len(allpossibletranslations))
	#print(len(alltranslationinfo))
	print(allpossibletranslations[0])
	#print(allpossibletranslations[0][1])  #the possible translation for phrase
	#print(engphrasecount[tuple()])   # the count for the english phrase
	#print(phrasecounttracker[allpossibletranslations[0][1]][tuple(alltranslationinfo[0][1][1][2:-2])]) #the count for the possible translation
	#print(alltranslationinfo[0][1][1])		#the information about the possible translation
	
	#translation model - need to look at count
	
	
	
	
	#go through allpossibletranslations
	
	#scoring
	
	
	#for sent in allpossibletranslations:
		
	#		print(sent)
	#		print("\n")
	#for sentences in allpossibletranslations:
	#	counter = 0
	#	for phr in sentences:
	#		lastword
						#thus sentence is shortened by count to also include later duplicate occurences
		#print(a)
		#print(phrasecounttracker[tuple(a)])
		#a1_sorted_keys = sorted(phrasecounttracker[tuple(a)], key=phrasecounttracker[tuple(a)].get, reverse=True)
		#print(a1_sorted_keys[:10])
		#for entry in phrase_table[tuple(a)]:
			
		#	print(phrase_table[tuple(a)])
			#print(phrasecounttracker[tuple(a)][tuple(entry[2:-2])])
	sentenceinput = input("enter an english sentence: ")
			
	#go through phrase matches and find best translated phrases
	#get all variations of the starting phrase
	
	buildphrases1 = []
	for phrase in phrase_array:
		if phrase[0] == sentence[0]:
			buildphrases1.append(phrase[:])
	
	
	buildphrases2 = []
	print(buildphrases1[0][-1])
	print(phrase_table[tuple(buildphrases1[1])][0][-2])
	
	
	for phrase in buildphrases1:			#go through starting phrases
		
		for p in phrase_array:				#go through all phrases gathered from input sentence
			
			for entries in phrase_table[tuple(p)]:			#go through
				temp = phrase
				temp.append(phrase[:])
				if phrase[-1] == entries[-2]:
					temp.append(p[:])
					buildphrases2.append[temp[:]]
					
					
			
	print(buildphrases2)
	
	print(outputsent)
	sentenceinput = input("enter an english sentence: ")
	
	
	

	
	
	
	
#can either use weight in the sense that the weight determines which quality is examined first, second and third when choosing phrases
#or a score can be assigned to the phrases based on the weights
#points for words before and after matching
#points for how close its position is to the position of the phrase in the sentence
#points for frequency of phrase




	
	
	'''
	
	
	
	
	
	
	
	
	
	