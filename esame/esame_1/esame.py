# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:59:38 2017

@author: domenico
"""
import random
import os
from codecs import open
name = os.getcwd().split('/')[-1]
data_esame = '21 gennaio 2019'
random.seed(data_esame)

def read_environment(data, environment, include=False):
# write list with '\begin{environment}...\end{environment}'
# that are found in the string data.
# If include=True \begin and \end are included
    if include:
        bo, eo = 0, len('\\end{}') + len(environment)
    else: 
        bo, eo = len('\\begin{}\n')  + len(environment), -1      
    x = []
    b = data.find(r'\begin{' + environment + '}')
    while b != -1:
        e =  data.find(r'\end{' + environment + '}',b) 
        x.append( data[b+bo : e+eo] ) 
        b = data.find(r'\begin{' + environment + '}',e)
    return x

def create_individual_exam(template,student):
# template is is between \begin{document} ... \end{document}
# the names with the files with be replaced with a question
# the command \student is replace with the name of a student
    x = read_environment(template, 'quesito', include=False)
    individual = template.replace( r'\student', student )
    for i in x:
        qname = random.choice( i.split('\n') ).strip()
        with open(qname + '.tex', 'r', encoding='utf-8') as f:
            qdata = f.read()
        j = random.choice( read_environment(qdata, 'question', include=False) ) 
        individual = individual.replace( i, j, 1 )
    return individual

with open(name + '.tex', 'r', encoding='utf-8') as f:
    data = f.read()
    f.closed

data = data.replace('data_esame', data_esame)

template = read_environment(data, 'document', include=False)
students = read_environment(data, 'students', include=False)[0].split('\n')


tutti = ''
i = 0
for student in students:
    i += 1
    tutti += create_individual_exam(template[0],student) + r'\clearpage'

data = data.replace(template[0],tutti)

name = name.replace('esame', 'domande')
with open(name + '.tex', 'w', encoding='utf-8') as f:
    f.write(data)
    f.closed
os.system('pdflatex '  + name + '.tex')
os.system('pythontex ' + name + '.tex')
os.system('pdflatex '  + name + '.tex')

name = name.replace('domande', 'risposte')
data = data.replace(r'\excludecomment{answer}', ' ')
with open(name + '.tex', 'w', encoding='utf-8') as f:
    f.write(data)
    f.closed
os.system('pdflatex '  + name + '.tex')
os.system('pythontex ' + name + '.tex')
os.system('pdflatex '  + name + '.tex')
   
