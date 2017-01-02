from math import *
import sys
import numpy
import copy


#For Part 3, uncomment the following section:
# Part = 3
# Path = 1

###For Part 4, uncomment the following section:
Part = 4
Path = 5


o = {}
bp = {}
bn = {}
bneg = {}
ip = {}
inn = {}
ineg = {}
keys = {'O' : 0, 'B-pos' : 1, 'B-neu' : 2, 'B-neg' : 3, 'I-pos' : 4, 'I-neu' : 5, 'I-neg' : 6}
keys2 = {'O' : 0, 'B-positive' : 1, 'B-neutral' : 2, 'B-negative' : 3, 'I-positive' : 4, 'I-neutral' : 5, 'I-negative' : 6}
invkeys = {0 : 'O', 1 : 'B-positive', 2 : 'B-neutral', 3 : 'B-negative', 4: 'I-positive', 5 : 'I-neutral', 6 : 'I-negative'}
List = [o,bp,bn,bneg,ip,inn,ineg]
ListCount = [0,0,0,0,0,0,0]


t_o = {}
t_bn ={}
t_bp = {}
t_bneg = {}
t_ip = {}
t_in = {}
t_ineg = {}
start = {}
tpList = [t_o, t_bp, t_bn,t_bneg, t_ip, t_in, t_ineg]
t_keys = {'O' : t_o, 'B-positive' : t_bp, 'B-neutral' : t_bn, 'B-negative' : t_bneg, 'I-positive' : t_ip, 'I-neutral' : t_in, 'I-negative' : t_ineg, 'start' : start}

#modifies above dictionaries
def emission(f):
    for lines in f:
        lines = lines.strip('\n')
        tList = lines.split(" ")
        if len(tList) > 1:
            if len(tList[1]) == 1:
                ListCount[0] += 1.0
                try:
                    o[tList[0]] += 1
                except:
                    o[tList[0]] = 1
            else:
                ListCount[keys[tList[1][0:5]]] += 1.0
                try:
                    List[keys[tList[1][0:5]]][tList[0]] += 1
                except:
                    List[keys[tList[1][0:5]]][tList[0]] = 1

  #  for j in range(len(List)):                             
		#List[j]['UnknownParamPlaceholder'] = 1
		#ListCount[j] += 1

    for j in range(len(List)):                              #for Part 1
        List[j]['UnknownParamPlaceholder'] = 1
        ListCount[j] += 1
        for a in List[j]:
            List[j][a] /= ListCount[j]

    #add 'unk' string for unknowns in every dictionary
    
    #for j in range(len(List)):                             ###For Part 5
    #     List[j]['UnknownParamPlaceholder'] = 1
    #     ListCount[j] += 1
    #     for a in List[j]:
    #         if a == 'UnknownParamPlaceholder':
    #             List[j][a] = ListCount[j]/float(sum(ListCount))
    #         else:
    #             List[j][a] /= ListCount[j]

def transition(f):

    t_keys = {'O' : t_o, 'B-positive' : t_bp, 'B-neutral' : t_bn, 'B-negative' : t_bneg, 'I-positive' : t_ip, 'I-neutral' : t_in, 'I-negative' : t_ineg, 'start' : start}
    totalCounts = {'O': ListCount[0], 'B-positive': ListCount[1], 'B-neutral': ListCount[2],'B-negative' : ListCount[3],'I-positive': ListCount[4],'I-neutral': ListCount[5],'I-negative': ListCount[6],'start': 0}

    prevline = 's start'
    for line in f:
        prevline_list = prevline.strip().split(" ")

        line = line.strip()
        tList = line.split(" ")
        if prevline == 's start':
            totalCounts['start'] += 1
        if len(tList) > 1:  
            try:
                t_keys[prevline_list[1]][tList[1]] += 1
            except:
                t_keys[prevline_list[1]][tList[1]] = 1
            prevline = line
    
        else:
            try:
                t_keys[prevline_list[1]]['stop'] += 1
            except:
                t_keys[prevline_list[1]]['stop'] = 1
    
            prevline = 's start'
    
    for label, dic in t_keys.iteritems():
        for k,v in dic.iteritems():
            dic[k] = v/float(totalCounts[label]-1)



def simplePredictor(f):
    counter = 0
    StateList = []
    SubList = []
    for lines in f:
        ListProb = [0,0,0,0,0,0,0]
        lines = lines.strip('\n')
        if lines != '':
            for i in range(7):
                try:
                    ListProb[i] = List[i][lines]
                except:
                    pass
            if sum(ListProb) == 0:
                for i in range(7):
                    ListProb[i] = List[i]['UnknownParamPlaceholder']       
            state = max(xrange(len(ListProb)), key=ListProb.__getitem__)
            SubList.append(str(invkeys[state]))
            #print(lines+ " " + str(invkeys[state]))
        else:
            StateList.append(SubList)
            SubList = []
    #print len(StateList)       
    return(StateList)

class SubNode:
    def __init__(self,state,score,parent,word):
        self.state = state
        self.score = score
        self.parent = parent
        self.word = word
        
class Sentence:

	def __init__(self, f):
		self.f = f
		self.counter = 0
		self.list_of_sentences = []

	def get_next(self):
		self.counter +=1
		return self.list_of_sentences[self.counter-1]

	def splitsentence(self):
		s = ''
		for line in self.f:
			
			line = line.strip().split(' ')
			
			if len(line[0]) >0 :
				s += line[0] + ' '
			else:
				s = s[:-1]
				self.list_of_sentences.append(s)
				s = ''        
				
def ViterbiAlgorithm(sentence,TopParam=1):
    word = 'start'
    counter = 0
    Nodes = []
    ActualParam = TopParam
    Nodes.append([SubNode('start',0,'nil','nil')])
        
    sentence = sentence.strip('\n').split(' ')
    
    for word in sentence:
        word.strip('\n')
        if len(keys)**counter < TopParam:         ####Ensure that there are enough parents
            ActualParam = len(keys)**counter
        else:
            ActualParam = TopParam
        SubNodePaths = []        
        

        wordPresent = wordCheck(word)             ####Check to invoke unknownparamplaceholder
            
        for i in range(len(keys)):                 ####Iterate through 7 states

            Scores = []
            
            
            for z in range(len(Nodes[counter])):         ####Getting scores of each subnode in the previous word
                
                if counter == 0:
                    try:    
                        Scores.append(Nodes[counter][z].score+start[invkeys[i]])
                    except:
                        Scores.append(-float('inf'))
                else:
                
                    try:
                        Scores.append(Nodes[counter][z].score+tpList[keys2[Nodes[counter][z].state]][invkeys[i]])
                    except:
                        Scores.append(-float('inf'))
                
                if wordPresent == True:                         ####Check word presence
                    try:
                        Scores[z] += List[i][word]
                    except:

                        Scores[z] = (-float('inf'))                    
                else:
                    Scores[z] += List[i]['UnknownParamPlaceholder']

            Score_Alias = copy.deepcopy(Scores)                         ####Avoid alias issue as Argmax alters input
            BestParentsIndex = argMaxKBest(Score_Alias,ActualParam)          ####Apply Argmax to find K-best indices
            
            
            for j in BestParentsIndex:
                SubNodePaths.append(SubNode(invkeys[i],Scores[j],Nodes[counter][j],word))
        Nodes.append(SubNodePaths)
        counter += 1
        
    Scores = []    
    SubNodePaths = []
    for z in range(len(Nodes[counter])):         ####Getting scores of each subnode in the previous word
        try:
            Scores.append(Nodes[counter][z].score)
        except:
            Scores.append(-float('inf'))    
                    
            Score_Alias = copy.deepcopy(Scores)                         ####Avoid alias issue as Argmax alters input
            BestParentsIndex = argMaxKBest(Score_Alias,ActualParam)          ####Apply Argmax to find K-best indices
    for j in BestParentsIndex:
        SubNodePaths.append(SubNode('stop',Scores[j],Nodes[counter][j],'nil'))            
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
        
def BestPaths(f,w,TopParam = 1, writescore = 1):
    print ("Calculating best paths...")
    sen = Sentence(f)    
    sen.splitsentence()
    PathOutput = []
    while True:
    #for z in range(1):
        try:
            BestPath = ViterbiAlgorithm(sen.get_next(),TopParam)
            OptimalPath = []
            OptimalParents = []
            bestindex = []
            Count = 0
            #for j in BestPath:
            #    print(j[0].word)
            #    for z in j:
            #        try:
            #            print(z.score,z.parent.state,z.state)
            #        except:
            #            print(z.score,'nil',z.state)  

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
            #print('END')
            break
        
    #print PathOutput
    return PathOutput    
    f.close()        


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

def mergeSimPre_Devin(f_dev_in,b):
    a=merge_asst(f_dev_in)
    ff=open('dev.p2.out','w')       
    for i in range(len(a)):
        for j in range(len(a[i])):
            merge_ab = str(a[i][j]) + " " + str(b[i][j])
            ff.write(merge_ab)
            ff.write("\n")
        ff.write("\n")
    ff.close()

def mergeVit_Devin(f_dev_in,x,b):
    a=merge_asst(f_dev_in)
    filename = 'dev.p' + str(x) + '.out'
    ff=open(filename,'w')        
    for i in range(len(a)):
        for j in range(len(a[i])):
            merge_ab = str(a[i][j]) + " " + str(b[i][j+1])
            ff.write(merge_ab)
            ff.write("\n")
        ff.write("\n")
    ff.close()

def mergeVit_Devin4(f_dev_in,x,b):
    a=merge_asst(f_dev_in)
    #filename = 'dev.p' + str(x) + '.out'
    ff=open('dev.p4.out','w')        
    for i in range(len(a)):
        for j in range(len(a[i])):
            merge_ab = str(a[i][j]) + " " + str(b[i][j+1])
            ff.write(merge_ab)
            ff.write("\n")
        ff.write("\n")
    ff.close()

f = open('train',"r")
emission(f)
f.close()
f = open('dev.in',"r")


################################################################
########### Part II ############################################
################################################################

SimPre=(simplePredictor(f))
mergeSimPre_Devin('dev.in',SimPre)  
f.close()
totalCounts = {'O': ListCount[0],
               'B-positive': ListCount[1],
               'B-neutral': ListCount[2],
               'B-negative' : ListCount[3],
               'I-positive': ListCount[4],
               'I-neutral': ListCount[5],
               'I-negative': ListCount[6],
               'start': 0}
f = open('train',"r")
transition(f)
f.close()

f = open('dev.in',"r")

for x in List:
    for y in x:
        x[y] = log(x[y])
        
for w in tpList:
    for v in w:
        w[v] = log(w[v])
        
for s in start:
    start[s] = log(start[s])



################################################################
########### Part III & IV  #####################################
################################################################


A=BestPaths(f,w,5,Path)   
mergeVit_Devin('dev.in', Part , A)     

      
f.close()