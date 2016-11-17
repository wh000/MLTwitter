
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
    for i in range(7):
        for a in List[i]:
            List[i][a] /= ListCount[i]

    #add 'unk' string for unknowns in every dictionary

def transmission(f):
    t_o = {}
    t_bn ={}
    t_bp = {}
    t_bne = {}
    t_ip = {}
    t_in = {}
    t_ine = {}
    start = {}
    t_keys = {'O' : t_o, 'B-positive' : t_bp, 'B-neutral' : t_bne, 'B-negative' : t_bn, 'I-positive' : t_ip, 'I-neutral' : t_ine, 'I-negative' : t_in, 'start' : start}
    totalCounts = {'O': ListCount[0],
                   'B-positive': ListCount[1],
                   'B-neutral': ListCount[2],
                   'B-negative' : ListCount[3],
                   'I-positive': ListCount[4],
                   'I-neutral': ListCount[5],
                   'I-negative': ListCount[6],
                   'start': 0}

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

    print t_o
    print t_bp
    print t_bne
    print t_bn

    
    

def countException(d,c,w):
    for a in d:
        d[a] *= c
    c+= 1
    d[w] = 1
    for b in d:
        d[b] /= c
    return c

def simplePredictor(f):
    counter = 0
    for lines in f:
        if counter <100:
            ListProb = [0,0,0,0,0,0,0]
            counter += 1
            lines = lines.strip('\n')
            if len(lines) > 0:
                for i in range(7):
                    try:
                        ListProb[i] = List[i][lines]
                    except:
                        ListCount[i] = countException(List[i],ListCount[i],lines)
                        ListProb[i] = List[i][lines]
            state = max(xrange(len(ListProb)), key=ListProb.__getitem__)
            print(lines+ " " + str(invkeys[state]))
        else:
            break
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
transmission(f)
f.close()



#for i in range(7):
#    print('###################################################################################################################################')
#    print(List[i])
#print ListCount

#simplePredictor(f2)
