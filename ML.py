from math import *
import sys
import numpy
import copy
#f2 = open('C:/Users/Stanley Loh/Desktop/Term 6 EPD/Machine Learning/Project/EN/dev.in',"r")
o = {}
bp = {}
bn = {}
bne = {}
ip = {}
inn = {}
ine = {}
keys = {'O' : 0, 'B-pos' : 1, 'B-neu' : 2, 'B-neg' : 3, 'I-pos' : 4, 'I-neu' : 5, 'I-neg' : 6}
invkeys = {0 : 'O', 1 : 'B-positive', 2 : 'B-neutral', 3 : 'B-negative', 4: 'I-positive', 5 : 'I-neutral', 6 : 'I-negative'}
List = [o,bp,bn,bne,ip,inn,ine]
ListCount = [0,0,0,0,0,0,0]


t_o = {}
t_bn ={}
t_bp = {}
t_bne = {}
t_ip = {}
t_in = {}
t_ine = {}
start = {}
tpList = [t_o, t_bp, t_bn,t_bne, t_ip, t_in, t_ine]
t_keys = {'O' : t_o, 'B-positive' : t_bp, 'B-neutral' : t_bne, 'B-negative' : t_bn, 'I-positive' : t_ip, 'I-neutral' : t_ine, 'I-negative' : t_in, 'start' : start}

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

    for j in range(len(List)):
        List[j]['UnknownParamPlaceholder'] = 1
        ListCount[j] += 1
        for a in List[j]:
            List[j][a] /= ListCount[j]

    #add 'unk' string for unknowns in every dictionary

def transmission(f):


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
            dic[k] = v/float(totalCounts[label])




#takes in text file, returns open list of 
def simplePredictor(f):
    counter = 0
    StateList = []
    SubList = []
    for lines in f:
        ListProb = [0,0,0,0,0,0,0]
        lines = lines.strip('\n')
        lines = lines.split(' ')
        if lines[0] != '':
            for i in range(7):
                try:
                    ListProb[i] = List[i][lines[0]]
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
            
    return(StateList)

<<<<<<< HEAD
def ViterbiAlgorithm(f,TopParam = 1):
    word = 'start'
    counter = 0
    Paths = []
    flag = 0
    for x in List:
        for y in x:
            x[y] = log(x[y])
    for w in tpList:
        for v in w:
            w[v] = log(w[v])
    for s in start:
        start[s] = log(start[s])
        
    for lines in f:
        if counter < 2000:
 
            lines = lines.strip('\n')
            if lines != '':
                Column = []
                for i in range(7):
                    Column.append([])
                if word == 'start':
                    for i in range(len(Column)):
                            try:
                                Column[i].append([start[invkeys[i]],'start'])
                            except:
                                Column[i].append([-sys.maxint-1,'start'])

                else:
                    actualParam = TopParam
                    if len(keys)**counter < TopParam:
                        actualParam = len(keys)**counter
                    prevActualParam = TopParam if len(keys)**(counter-1)>TopParam else len(keys)**(counter-1)
                    values = []
                    for w in range(7):
                        for k in range(prevActualParam):
                            try:
                                values.append(Paths[counter-1][w][k][0]+List[w][word])
                            except:
                                values.append(Paths[counter-1][w][k][0]+List[w]['UnknownParamPlaceholder'])

                    for i in range(len(Column)):
                        transitionValues = []
                        for kthScore in range(len(values)):
                            try:
                                transitionValues.append(values[kthScore]+tpList[kthScore/prevActualParam][invkeys[i]])
                            except:
                                transitionValues.append(values[kthScore]-sys.maxint)
                        store = copy.deepcopy(transitionValues)             
                        BestIndex = argMaxKBest(store,actualParam)
                        for j in range(TopParam):
                            Column[i].append([transitionValues[BestIndex[j]],invkeys[BestIndex[j]/prevActualParam]])
                        
                        
                        if flag <7:
                            flag += 1
                    

                word = lines
                Paths.append(Column)
                counter += 1
                print(Column)
                print('#####################################################################################')

def argMaxKBest(values,Params):
    Best = []
    for i in range(Params):
        Best.append(numpy.argmax(values))
        values[Best[i]] = -(2+i)*sys.maxint-1
    return Best
f = open('C:/Users/Stanley Loh/Desktop/Term 6 EPD/Machine Learning/Project/gitML/train.txt',"r")
emission(f)
f.close()
f = open('C:/Users/Stanley Loh/Desktop/Term 6 EPD/Machine Learning/Project/gitML/dev.in',"r")
#print(simplePredictor(f))
f.close()
totalCounts = {'O': ListCount[0],
               'B-positive': ListCount[1],
               'B-neutral': ListCount[2],
               'B-negative' : ListCount[3],
               'I-positive': ListCount[4],
               'I-neutral': ListCount[5],
               'I-negative': ListCount[6],
               'start': 0}
               
f = open('C:/Users/Stanley Loh/Desktop/Term 6 EPD/Machine Learning/Project/gitML/train.txt',"r")
transmission(f)
=======
#takes in file, returns nested list of sentence states
def get_gold_from_file(f):
    total = []
    sentence = []
    for line in f:
        if line == '\n':
            total.append(sentence)
            sentence = []
            
        else:
            line = line.strip('\n')
            tList = line.split(" ")
            sentence.append(tList[1])
    return total

#takes in 2 nested lists, outputs the total precision and recall value
def get_f(gold, predicted):
    total_precision = 0
    total_recall = 0

    for i in range(len(gold)):
        ith_gold = 0
        entities_predicted = 0
        correctly_predicted = 0
        prev_state = 'O'
        c_state = 0
        for j in range(len(gold[i])):
            #c_state 0: default/no match
            #c_state 1: comparing entity
            #c_state 2: entity comparison done, successful match

            #gold entities in the sentence
            if gold[i][j][0] == 'B':
               ith_gold += 1 
            #predicted entities
            if (prev_state == 'O' and predicted[i][j][0] != 'O'):
                entities_predicted += 1
                c_state = 1
            if c_state == 1:
                #comparison successful, go to c_state 2
                if (predicted[i][j][0] == 'O' and gold[i][j][0] == 'O'):
                    c_state = 2
                #comparing
                else:
                    #if its wrong, go back to c_state 0
                    try:
                        if gold[i][j][2:5] != predicted[i][j][2:5]:
                            c_state = 0
                    except:
                        c_state = 0
            if c_state == 2:
                correctly_predicted += 1
                c_state = 0
                
            prev_state = predicted[i][j][0]
            
            #if the entity is at the end of the sentence and is correct
            if j == len(gold[i])-1 and c_state == 1:
                correctly_predicted += 1
        print 'total_predicted: ' + str(entities_predicted)
        print 'correctly_predicted: ' + str(correctly_predicted)
        print 'gold: ' + str(ith_gold)
        print gold[i]
        print predicted[i]
        if entities_predicted >0:        
            total_precision += correctly_predicted/float(entities_predicted)
        if ith_gold > 0:
            total_recall += correctly_predicted/float(ith_gold)

    return total_precision, total_recall

        

#testd = {'tt' : 10,'ttt':20,'tttt':30}
#count = 60.0
#for i in testd:
#    testd[i] /= count   
#count = countException(testd,count,'t')
#print testd
#print count
f = open('train.txt',"r")
emission(f)
f.close()
f = open('train.txt',"r")
gold = get_gold_from_file(f)
f.close()
f = open('train.txt',"r")
predicted = simplePredictor(f)
print get_f(gold, predicted)
>>>>>>> a25c6cf1cb9fbcb4815624bcfe4e777537b1b248
f.close()
#f = open('train.txt',"r")
#transmission(f)
#f.close()

f = open('C:/Users/Stanley Loh/Desktop/Term 6 EPD/Machine Learning/Project/gitML/dev.in',"r")

ViterbiAlgorithm(f,5)

#for i in range(7):
#    print('###################################################################################################################################')
#    print(List[i])
#print ListCount

#simplePredictor(f2)
