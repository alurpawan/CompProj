#Assuming that the squence iterator is i in the input c program :

import Loop_To_Expression
from Loop_To_Expression import Var
import re

#Get file name
file_name = input("Enter name of File : ")
SVar = Loop_To_Expression.Main(file_name)


#Create Correctness Specification :


#Global Variables defined here
max_depth = 5
f1_final = []
f2_final = []
ft_final = []
semantic_Var = []
allowed_ip = []

#Functions defined here
def change_SVar(num):
    to_replace = '[\[\s]+i[\]\s]+'
    tempSVar = []
    for j in SVar:
        #print(r'\1'+str(num))
        search_res = re.search(to_replace, j.CurrVal)
        tempVal = j.CurrVal
        if search_res:
            if '[' in search_res.group():
                tempVal = re.sub(to_replace,'[%d]' %(num),j.CurrVal)
            else:
                tempVal = re.sub(to_replace,' %d ' %(num),j.CurrVal)
        #print (j.name)
        tempVar = Var(j.name,tempVal)
        tempSVar.append(tempVar)
    return tempSVar

def print_val(double_list):
    for i in double_list:
        for j in i:
            print(j.name + " = " + j.CurrVal)
            if i.index(j) != len(i)-1:
                print("and")
        if(double_list.index(i) != len(double_list)-1):
            print("and")
        else:
            print(" ")

def calc_func():
    for depth in range(0,max_depth):
        max_calc = pow(2,depth)
        f1 = []
        f2 = []
        ft = []
        #print(depth)
        #print(max_calc)


        for i in range(0,max_calc):
            f1.append(change_SVar(i))
            f2.append(change_SVar(max_calc+i))
            #print(max_calc+i)

        for i in range(0,2*max_calc):
            ft.append(change_SVar(i))

        
        
        f1_final.append(f1)
        f2_final.append(f2)
        ft_final.append(ft)

def calc_semantic():
    names = []
    for j in SVar:
        names.append(j.name)
    banned_words = ['if','else','then','{','}','(',')','==','<=','>=','<','>','+','-','/','*','||','&&']
    for j in SVar: 
        wordlist = j.CurrVal.split()
        #print(wordlist)
        
        for ind,k in enumerate(wordlist):
            if not(k in banned_words):
                #print("here" + k)
                if k in names:
                    wordlist[ind] = '?LR'
                else:
                    wordlist[ind] = '?R'
        tempVal = " ".join(wordlist)
        tempName = j.name
        tempVar = Var(tempName,tempVal)
        semantic_Var.append(tempVar)
        #print(wordlist)

def get_allowed_words(depth):
    allowed_ip = []
    for i in Loop_To_Expression.Variable:

        allowed_ip.append(i.name +'L')
        allowed_ip.append(i.name + 'R')
    for i in range(2*pow(2,depth)):
        allowed_ip.append(i)
        
        allowed_ip.append("a[" + str(i) + ']')
       
    return allowed_ip


max_depth = int(input("Enter maximum depth : "))
calc_semantic()
calc_func()


print("The operator is of the form : ")
for j in semantic_Var:
    print (j.name + " = " + j.CurrVal)

print(" ")
for j in range(max_depth):
    allowed_ip = []
    print("For depth "+ str(j) + " ,the syntax function is of the form : ")
    print_val(f1_final[j]) 
    print( "operator")
    print("")
    print_val(f2_final[j]) 
    print("equals")
    print("")
    print_val(ft_final[j])
    print(" ")
    print("And the allowed inputs in the spaces are : ")
    allowed_ip = get_allowed_words(j)
    for k in allowed_ip:
        print(k)
    print("")
    print("")
    print("")
    print("")
    print("")   

#Now we assert that ft = f1 op f2, where we do not know op and want SyGuS to find it.
              
