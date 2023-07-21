#Author: Richjard Chang (Jerrr)
#Student ID: 0816125
#HW ID: HW1

#i use jupyternotebook while running code

# example dataset
import pandas as pd
import spacy

FP=0
FN=0

nlp = spacy.load('en_core_web_sm')
gt = 0
prd = 0

subs = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", 'conj']
objs = ["dobj", "attr","pobj"]
nouns = ["NOUN","PROPN","PRON"]

data = "example_with_answer.csv"
df = pd.read_csv(data,sep=',')
ans1 = []
for index,row in df.iterrows():
    sentence = row['Sentence']
    #print(sentence)
    doc = nlp(sentence)
    toks = [tok for tok in doc]
    
    verb = []
    subj = []
    obj = []
    for tok in toks:
        if tok.pos_ == 'VERB' or tok.pos_ == 'AUX':
            verb.append(str(tok))
    for tok in toks:
        if tok.dep_ in subs and tok.pos_ in nouns:
            subj.append(str(tok))
        if tok.dep_ in objs:
            obj.append(str(tok))
            
    S = [wd for wd in row['S'].split(' ')]
    O = [wd for wd in row['O'].split(' ')]
    V = [wd for wd in row['V'].split(' ')]
    
    sbool = 0
    for s in S:
        if s in subj:
            sbool = 1
            break

    obool = 0
    for o in O:
        if o in obj:
            obool = 1
            break
            
    vbool = 0
    for v in V:
        if v in verb:
            vbool = 1
            break
    pred = 0
    if vbool+obool+sbool == 3:
        pred = 1
        
    print(index,': ',pred,' / ',row['T/F'])
    if pred == row['T/F']:
        prd+=1
        
    else:
        if pred == 1 and row['T/F'] == 0:
            FP+=1
        else:
            FN+=1
    gt +=1
    
print(prd/gt)
print(FP)
print(FN)

#predict

import pandas as pd
import spacy
import numpy as np
import csv
from tqdm import tqdm

nlp = spacy.load('en_core_web_sm')

subs = ["nsubj", "nsubjpass", "csubj", "csubjpass",'conj','agent']
objs = [ "dobj","attr","pobj"]


data = "dataset.csv"
df = pd.read_csv(data,sep=',')
ans1 = []

vbools = []
obools = []
sbools = []

prediction = []

with open('0816125test11523.csv','a',newline = '') as fd:
    writer = csv.writer(fd)
    writer.writerow(['index','T/F'])
    
for index,row in tqdm(df.iterrows()):
    sentence = row['Sentence']
    doc = nlp(sentence)
    toks = [tok for tok in doc]
    
    verb = []
    subj = []
    obj = []
    for tok in toks:
        if tok.pos_ == 'VERB' or tok.pos_=='AUX':
            verb.append(str(tok))
    for tok in toks:
        if tok.dep_ in subs and tok.pos_ in nouns:
            subj.append(str(tok))
        if tok.dep_ in objs:
            obj.append(str(tok))
            
    S = [wd for wd in row['S'].split(' ')]
    O = [wd for wd in row['O'].split(' ')]
    V = [wd for wd in str(row['V']).split(' ')]
    
    sbool = 0
    for s in S:
        if s in subj:
            sbool = 1
            break
    sbools.append(sbool)
    obool = 0
    for o in O:
        if o in obj:
            obool = 1
            break
    obools.append(obool)
    vbool = 0
    for v in V:
        if v in verb:
            vbool = 1
            break
    vbools.append(vbool)
    if vbool+obool+sbool == 3:
        prediction.append(1)
    else:
        prediction.append(0)

for index,pred in enumerate(prediction):
    with open('0816125test11523.csv','a',newline = '') as fd:
        writer = csv.writer(fd)
        writer.writerow([index,pred])

#experience 
sentence = 'Following are excerpts from an interview with Sen. Richard C. Shelby , the Alabama Republican who is the ranking minority member of the Intelligence Committee : `` Maybe God just had a plan for me and wanted me to be around for a little while longer , '' said Johnson , who has a wife , Cookie , and three children .'
doc = nlp(sentence)
toks = [tok for tok in doc]
print(doc)
for i in toks:
    print(i,' ',i.dep_,' ',i.pos_)
verb = []
subj = []
obj = []
for tok in toks:
    if tok.pos_ == 'VERB' or tok.pos_ == 'AUX':
        verb.append(str(tok))
for tok in toks:
    if tok.dep_ in subs:
        subj.append(str(tok))
    if tok.dep_ in objs:
        obj.append(str(tok))
print(subj)      
print(verb)
print(obj)