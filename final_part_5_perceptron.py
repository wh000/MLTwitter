from math import *
import sys
import numpy
import copy

##########################################################################################
# Please change these variables to modify the files to train, write to, and to compare to!
train = 'train'
file_name = 'dev.in'
output_filename = 'dev.p5.out'


##########################################################################################
o = {}
bp = {}
bn = {}
bneg = {}
ip = {}
inn = {}
ineg = {}

op = {}
bpp = {}
bnp = {}
bnegp = {}
ipp = {}
innp = {}
inegp = {}

keys = {'O' : 0, 'B-pos' : 1, 'B-neu' : 2, 'B-neg' : 3, 'I-pos' : 4, 'I-neu' : 5, 'I-neg' : 6}
keys2 = {'O' : 0, 'B-positive' : 1, 'B-neutral' : 2, 'B-negative' : 3, 'I-positive' : 4, 'I-neutral' : 5, 'I-negative' : 6}
invkeys = {0 : 'O', 1 : 'B-positive', 2 : 'B-neutral', 3 : 'B-negative', 4: 'I-positive', 5 : 'I-neutral', 6 : 'I-negative'}

List = [o,bp,bn,bneg,ip,inn,ineg]
ListCount = [0,0,0,0,0,0,0]
Listp = [op,bpp,bnp,bnegp,ipp,innp,inegp]
    
ct={}
pt={}
twoback={}
nexttag={}
twoahead={}
bf1={}
bf2={}
bf3={}
bf4={}
tf1={}
tf2={}
tf3={}
    
fv_key = {1:ct, 2:pt, 3:twoback, 4:List, 5:bf1, 6:bf2, 7:tf1, 8:nexttag, 9:twoahead, 10:bf3, 11:bf4, 12:tf2, 13:tf3, 14:Listp}
#1 CURRENT TAG
#2 PREVIOUS TAG
#3 TAG TWO BACK
#4 EMISSION
#5 BI-GRAM FEATURE 1 (pi-2, pi-1)
#6 BI-GRAM FEATURE 2 (pi-1, pi)
#7 TRI-GRAM FEATURE 1 (pi-2, pi-1, pi)
#8 NEXTTAG 
#9 TWOAHEAD
#10 BI-GRAM FEATURE 3 (pi+1,pi+2)
#11 BI-GRAM FEATURE 4 (pi, pi+1)
#12 TRI-GRAM FEATURE 2 (pi-1, pi, pi+1)
#13 TRI-GRAM FEATURE 3 (pi, pi+1, pi+2)

include = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]


def ViterbiAlgorithm(sentence,TopParam=1):
	word = 'start'
	Counter = 0
	Nodes = []
	ActualParam = TopParam
	Nodes.append([SubNode('start',0,'nil','nil')])
	wordCounter = 0
	sentence = sentence.strip('\n').split(' ')
	
	for word in sentence:
		word.strip('\n')
		if len(keys)**Counter < TopParam:         ####Ensure that there are enough parents
			ActualParam = len(keys)**Counter
		else:
			ActualParam = TopParam
		SubNodePaths = []        
		

		#wordPresent = wordCheck(word)             ####Check to invoke unknownparamplaceholder
		#print('Current word is ' + word)

		for i in range(len(keys)):                 ####Iterate through 7 states
			Scores = []
			for z in range(len(Nodes[Counter])):         ####Getting scores of each subnode in the previous word
				CurrentNodeScore = Nodes[Counter][z].score
				
				for f in range(1,15):                     ####Backward feature initialization
					# if f == 1:
					# 	try:
					# 		CurrentNodeScore += fv_key[f][invkeys[i]]
							
					# 	except KeyError as ke:
					# 		#print f,CurrentNodeScore
					# 		pass
					# elif f == 2:
					# 	try:
					# 		CurrentNodeScore += fv_key[f][Nodes[Counter][z].state]
							
					# 	except KeyError as ke:
					# 		#print f,CurrentNodeScore
					# 		pass
					# elif f == 3 and Counter != 0:
					# 	try:
					# 		CurrentNodeScore += fv_key[f][Nodes[Counter][z].parent.state]
					# 	except KeyError as ke:
					# 		#print f,CurrentNodeScore
					# 		pass
					if f == 4:
						try:
							CurrentNodeScore += fv_key[f][i][word]
						except KeyError as ke:
							#print f,CurrentNodeScore
							pass
					# elif f == 5 and Counter != 0:
					# 	try:
					# 		Bigram = Nodes[Counter][z].parent.state + ' ' + Nodes[Counter][z].state
					# 		#print Bigram
					# 		#print '#####################'
					# 		CurrentNodeScore += fv_key[f][Bigram]
					# 		#print fv_key[f][Bigram]
					# 	except KeyError as ke:
					# 		#print f,CurrentNodeScore
					# 		pass
					elif f == 6:
						try:
							Bigram = Nodes[Counter][z].state + ' ' + invkeys[i]
							#print Bigram
							CurrentNodeScore += fv_key[f][Bigram]
							#print CurrentNodeScore
							#print 'yea'
						except KeyError as ke:
							#print f,CurrentNodeScore
							pass
					# elif f == 7 and Counter != 0: 
					# 	try:
					# 		Trigram = Nodes[Counter][z].parent.state + ' ' + Nodes[Counter][z].state + ' ' + invkeys[i]
					# 		CurrentNodeScore += fv_key[f][Trigram]
					# 	except KeyError as ke:
					# 		#print f,CurrentNodeScore
					# 		pass
					#elif f == 14 and Counter !=:

				Scores.append(CurrentNodeScore)

			Score_Alias = copy.deepcopy(Scores)
			BestParentsIndex = argMaxKBest(Score_Alias,ActualParam)
			
			for j in BestParentsIndex:
				SubNodePaths.append(SubNode(invkeys[i],Scores[j],Nodes[Counter][j],word))
		Nodes.append(SubNodePaths)
		Counter += 1
	Scores = []
	SubNodePaths = []
	for z in range(len(Nodes[Counter])):         ####Getting scores of each subnode in the previous word

		CurrentNodeScore = Nodes[Counter][z].score
		for f in range(1,9):                     ####Backward feature initialization
			if f == 1:
				pass
			# elif f == 2:
			# 	try:
			# 		CurrentNodeScore += fv_key[f][invkeys[Nodes[Counter][z].state]]
			# 	except KeyError as ke:
			# 		pass
			# elif f == 3:
			# 	try:
			# 		CurrentNodeScore += fv_key[f][invkeys[Nodes[Counter][z].parent.state]]
			# 	except KeyError as ke:
			# 		pass
			# elif f == 4:
			# 	pass
			# elif f == 5:
			# 	try:
			# 		Bigram = Nodes[Counter][z].parent.state + ' ' + Nodes[Counter][z].state
			# 		CurrentNodeScore += fv_key[f][Bigram]
			# 	except KeyError as ke:
			# 		pass
			elif f == 6:
				try:
					Bigram = Nodes[Counter][z].state + ' ' + 'stop'
					CurrentNodeScore += fv_key[f][Bigram]
				except KeyError as ke:
					pass
			# elif f == 7:
			# 	try:
			# 		Trigram = Nodes[Counter][z].parent.state + ' ' + Nodes[Counter][z].state + ' ' + 'stop'
			# 		CurrentNodeScore += fv_key[f][Trigram]
			# 	except KeyError as ke:
			# 		pass
		Scores.append(CurrentNodeScore)
	Score_Alias = copy.deepcopy(Scores)                         ####Avoid alias issue as Argmax alters input
	BestParentsIndex = argMaxKBest(Score_Alias,ActualParam)          ####Apply Argmax to find K-best indices
	for j in BestParentsIndex:
		SubNodePaths.append(SubNode('stop',Scores[j],Nodes[Counter][j],'nil'))            
	Nodes.append(SubNodePaths)

	
	return Nodes
	
def argMaxKBest(values,Params):
	Best = []
	for j in range(len(values)):
		if values[j] == -float('inf'):
			values[j] =-sys.maxint
	for i in range(Params):
		
		Best.append(numpy.argmax(values))
		values[Best[i]] = -float('inf')#-(10+i)*sys.maxint-1
	return Best
	
def wordCheck(word):
	Bit = 0
	counter = 0
	for i in range(len(keys)):
		
		try:
			Bit += List[i][word]
		except:
			counter += 1
 
	if counter == 7:
		return False
	else:
		return True
def merge_asst(f):
	fileopen = open(f,'r')
	old_list = []
	wholelist = []
	for lines in fileopen:
		lines = lines.split('\n')
		if lines == ['', '']:
			wholelist.append(old_list)
			old_list = []
		else:
			old_list.append(lines[0])
	return wholelist

def merge(f_dev_in,outputfilename,b):
	a=merge_asst(f_dev_in)
	filename=outputfilename
	ff=open(filename,'w')
	for i in range(len(a)):
		for j in range(len(a[i])):
			merge_ab = str(a[i][j]) + " " + str(b[i][j+1])
			ff.write(merge_ab)
			ff.write("\n")
		ff.write("\n")

	ff.close()

class SubNode:
	def __init__(self,state,score,parent,word):
		self.state = state
		self.score = score
		self.parent = parent
		self.word = word

class Sentence:

	def __init__(self, file_name):
		self.file_name = file_name
		self.counter = 0
		self.counter_true = 0
		self.list_of_sentences = []
		self.list_of_sentences_true = []

	def get_next(self):
		self.counter +=1
		
		return (self.list_of_sentences[self.counter-1])

	def get_next_true(self):
		self.counter_true +=1
		return (self.list_of_sentences_true[self.counter_true-1])

	def splitsentence_true(self):
		f = self.open_file(self.file_name)
		l = [['start','start']]
		for line in f:
			line = line.strip().split(' ')
			if len(line)>1:
				l.append(line)
			else:
				l.append(['stop','stop'])
				self.list_of_sentences_true.append(l)
				l = [['start','start']]
		self.close_file()

	def splitsentence(self):
		f = self.open_file(self.file_name)
		s = ''
		for line in f:
			line = line.strip().split(' ')
			
			if len(line[0]) >0 :
				s += line[0] + ' '
			else:
				s = s[:-1]
				self.list_of_sentences.append(s)
				s = ''
		self.close_file()

	def close_file(self):
		self.file.close()

	def open_file(self, file_name):
		#s = 'C:\\Users\\User\\Documents\\School\\SUTD\\term6\\ML\\Project\\Results\\'+file_name
		self.file = open(self.file_name,"r")
		return self.file
	def counter_reset(self):
		self.counter = 0
		self.counter_true = 0



class VPerceptron:
	keys = {'O' : 0, 'B-positive' : 1, 'B-neutral' : 2, 'B-negative' : 3, 'I-positive' : 4, 'I-neutral' : 5, 'I-negative' : 6}
	def __init__(self, sentences):
		self.sentences = sentences

	def train(self, num_iter):
		print "Perceptron training..."
		for i in range(num_iter):
			check_file_end = True
			check_iteration_correct = True
			count = 0
			#print self.sentences.counter, self.sentences.counter_true
			while check_file_end:
				#count +=1
				#print count
				try:
					s = self.sentences.get_next()
				except IndexError as e:
					print "file ended"
					self.sentences.counter_reset()
					break
				
				pred_tags = self.bestPaths(s)
				pred_tags.append('stop')
				#print pred_tags
				true_tags = self.sentences.get_next_true()
				#print (len(pred_tags)==len(true_tags))
				check_iteration_correct = self.train_compare(pred_tags,true_tags)


			print "iteration finished"

		#Normalize FVs to prevent overfitting on training set
		for dic in fv_key.values():
			if isinstance(dic, dict):
				for k,v in dic.iteritems():
					dic[k] = v/float(num_iter)
			else:
				for d in dic:
					for k,v in d.iteritems():
						d[k] = v/float(num_iter)

	def train_compare(self, pred_tags, true_tags):
		check = True
		# print pred_tags
		# print true_tags
		correction = 1
		correction2=3
		correction3=WeightChosen  #change this
		for i in range(len(pred_tags)):
			p_tag = pred_tags[i]
			t_tag = true_tags[i][1]
			word = true_tags[i][0]

			#emission
			if p_tag != t_tag:
				check = False
				try:
					List[keys2[t_tag]][word] += correction3
				except KeyError as ke:
					List[keys2[t_tag]][word] = +correction3
				try:
					List[keys2[p_tag]][word] -= correction3
				except KeyError as ke:
					List[keys2[p_tag]][word] = -correction3
			#ct
			if p_tag != t_tag:
				check = False
				try:
					ct[true_tags[i][1]] += correction
				except KeyError as ke:
					ct[true_tags[i][1]] = correction
				try:
					ct[pred_tags[i]] -= correction
				except KeyError as ke:
					ct[pred_tags[i]] = -correction
			#pt
			if i>0:
				check = False
				if pred_tags[i-1]!=true_tags[i-1][1]:
					try:
						pt[true_tags[i-1][1]] += correction
					except KeyError as ke:
						pt[true_tags[i-1][1]] = correction
					try:
						pt[pred_tags[i-1]] -= correction
					except KeyError as ke:
						pt[pred_tags[i-1]] = -correction
			#twoback
			if i>1:
				if pred_tags[i-2] != true_tags[i-2][1]:
					try:
						twoback[true_tags[i-2][1]] += correction
					except KeyError as ke:
						twoback[true_tags[i-2][1]] = correction
					try:
						twoback[pred_tags[i-2]] -= correction
					except KeyError as ke:
						twoback[pred_tags[i-2]] = -correction
			#nexttag
			if i<len(pred_tags)-1:
				if pred_tags[i+1] != true_tags[i+1][1]:
					try:
						nexttag[true_tags[i+1][1]] += correction
					except KeyError as ke:
						nexttag[true_tags[i+1][1]] = correction
					try:
						nexttag[pred_tags[i+1]] -= correction
					except KeyError as ke:
						nexttag[pred_tags[i+1]] = -correction
			#twoahead
			if i<len(pred_tags)-2:
				if pred_tags[i+2] != true_tags[i+2][1]:
					try:
						twoahead[true_tags[i+2][1]] += correction
					except KeyError as ke:
						twoahead[true_tags[i+2][1]] = correction
					try:
						twoahead[pred_tags[i+2]] -= correction
					except KeyError as ke:
						twoahead[pred_tags[i+2]] = -correction

			#bi-gram feature 1 (pi-2, pi-1)
			if i > 1:
				if pred_tags[i-2]+' '+pred_tags[i-1] != true_tags[i-2][1]+' '+true_tags[i-1][1]:
					check = False
					try:
						bf1[true_tags[i-2][1]+' '+true_tags[i-1][1]] += correction
					except KeyError as ke:
						bf1[true_tags[i-2][1]+' '+true_tags[i-1][1]] = correction
					try:
						bf1[pred_tags[i-2]+' '+pred_tags[i-1]] -= correction
					except KeyError as ke:
						bf1[pred_tags[i-2]+' '+pred_tags[i-1]] = -correction
			#bi-gram feature 2 (pi-1, pi)
			if i > 0:
				if pred_tags[i-1]+' '+pred_tags[i] != true_tags[i-1][1]+' '+true_tags[i][1]:

					check = False
					try:
						bf2[true_tags[i-1][1]+' '+true_tags[i][1]] += correction
						#print bf2[true_tags[i-1][1]+' '+true_tags[i][1]]
					except KeyError as ke:
						bf2[true_tags[i-1][1]+' '+true_tags[i][1]] = correction
					try:
						bf2[pred_tags[i-1]+' '+pred_tags[i]] -= correction
					except KeyError as ke:
						bf2[pred_tags[i-1]+' '+pred_tags[i]] = -correction
			#bi-gram feature 3 (pi, pi+1)
			if i < len(pred_tags)-1:
				if pred_tags[i]+' '+pred_tags[i+1] != true_tags[i][1]+' '+true_tags[i+1][1]:
					check = False
					try:
						bf3[true_tags[i][1]+' '+true_tags[i+1][1]] += correction
					except KeyError as ke:
						bf3[true_tags[i][1]+' '+true_tags[i+1][1]] = correction
					try:
						bf3[pred_tags[i]+' '+pred_tags[i+1]] -= correction
					except KeyError as ke:
						bf3[pred_tags[i]+' '+pred_tags[i+1]] = -correction
			#bi-gram feature 4 (pi+1, pi+2)
			if i < len(pred_tags)-2:
				if pred_tags[i+1]+' '+pred_tags[i+2] != true_tags[i+1][1]+' '+true_tags[i+2][1]:
					check = False
					try:
						bf4[true_tags[i+1][1]+' '+true_tags[i+2][1]] += correction
					except KeyError as ke:
						bf4[true_tags[i+1][1]+' '+true_tags[i+2][1]] = correction
					try:
						bf4[pred_tags[i+1]+' '+pred_tags[i+2]] -= correction
					except KeyError as ke:
						bf4[pred_tags[i+1]+' '+pred_tags[i+2]] = -correction


			#tri-gram feature 1 (pi-2, pi-1,pi)
			if i > 1:
				if pred_tags[i-2]+' '+pred_tags[i-1]+' '+pred_tags[i] != true_tags[i-2][1]+' '+true_tags[i-1][1]+' '+true_tags[i][1]:
					check = False
					try:
						tf1[true_tags[i-2][1]+' '+true_tags[i-1][1]+' '+true_tags[i][1]] += correction2
					except KeyError as ke:
						tf1[true_tags[i-2][1]+' '+true_tags[i-1][1]+' '+true_tags[i][1]] = correction2
					try:
						tf1[pred_tags[i-2]+' '+pred_tags[i-1]+' '+pred_tags[i]] -= correction2
					except KeyError as ke:
						tf1[pred_tags[i-2]+' '+pred_tags[i-1]+' '+pred_tags[i]] = -correction2
			#tri-gram feature 2 (pi-1, pi, pi+1)
			if 0<i<len(pred_tags)-1:
				if pred_tags[i-1]+' '+pred_tags[i]+' '+pred_tags[i+1] != true_tags[i-1][1]+' '+true_tags[i][1]+' '+true_tags[i+1][1]:
					check = False
					try:
						tf2[true_tags[i-1][1]+' '+true_tags[i][1]+' '+true_tags[i+1][1]] += correction
					except KeyError as ke:
						tf2[true_tags[i-1][1]+' '+true_tags[i][1]+' '+true_tags[i+1][1]] = correction
					try:
						tf2[pred_tags[i-1]+' '+pred_tags[i]+' '+pred_tags[i+1]] -= correction
					except KeyError as ke:
						tf2[pred_tags[i-1]+' '+pred_tags[i]+' '+pred_tags[i+1]] = -correction

			#tri-gram feature 1 (pi, pi+1,pi+2)
			if i<len(pred_tags)-2:
				if pred_tags[i]+' '+pred_tags[i+1]+' '+pred_tags[i+2] != true_tags[i][1]+' '+true_tags[i+1][1]+' '+true_tags[i+2][1]:
					check = False
					try:
						tf3[true_tags[i][1]+' '+true_tags[i+1][1]+' '+true_tags[i+2][1]] += correction
					except KeyError as ke:
						tf3[true_tags[i][1]+' '+true_tags[i+1][1]+' '+true_tags[i+2][1]] = correction
					try:
						tf3[pred_tags[i]+' '+pred_tags[i+1]+' '+pred_tags[i+2]] -= correction
					except KeyError as ke:
						tf3[pred_tags[i]+' '+pred_tags[i+1]+' '+pred_tags[i+2]] = -correction
		#print "1"	
		return check



	def bestPaths(self, sen, TopParam = 1, writescore = 1):
		try:
			
			BestPath = ViterbiAlgorithm(sen,TopParam)
			OptimalPath = []
			OptimalParents = []
			bestindex = []
			Count = 0
			PathOutput=[]

			for j in range(len(BestPath)-1,0,-1):
				
				if j == len(BestPath)-1:
		
					for z in BestPath[j]:
						bestindex.append(z.score)
					bestcopy = copy.deepcopy(bestindex)
					kscore = argMaxKBest(bestcopy,writescore)
					OptimalParents = [BestPath[j][kscore[writescore-1]].parent]+OptimalParents
					OptimalPath = [BestPath[j][kscore[writescore-1]].parent.state]+OptimalPath 
					Count += 1
					
				else:
					OptimalPath = [OptimalParents[0].parent.state]+OptimalPath 
					OptimalParents = [OptimalParents[0].parent]+OptimalParents
					Count += 1
				
			PathOutput.append(OptimalPath)
		except:
			print('END')
		   
		# print 'Path Output:'   
		# print OptimalPath
		return OptimalPath

	def predict(self, sentences):
		output = []
		while True:
			try:
				#list of tags for one sentence	
				pred_tags = self.bestPaths(sentences.get_next()) 
				output.append(pred_tags)
			except:
				break
		
		return output


################################################################
################ Running Code ##################################
################################################################


WeightChosen = 30 #weightage

s = Sentence(train)
s.splitsentence()
s.splitsentence_true()

v = VPerceptron(s)
v.train(8)

s2 = Sentence(file_name)
s2.splitsentence()

A=v.predict(s2)
merge(file_name,output_filename,A)
