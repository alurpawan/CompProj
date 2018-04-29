'''
Author : Pawan Alur
What does this file do? : This file takes as input a filename, and then reads this file. 
It assumes that the file is a C file with a SINGLE loop(no nested loops), and then converts it to an expression as decided in the paper.


For every line : 
1. If not a for loop, there will be variables
2. If for loop, get the iterator, and the max . Check if line ends in a {
3. Inside for loop, store every line in list of loop body
4. Stop when you get to first }
5. Store return variable, and ensure Final }
For now : Print Loop body

Done : Obtain Loop Body.
Next task : Find SVar and IVar

TODO : Convert Loop body to expr(will have to read and understand for this to happen)  

'''

import sys

#Global lists..
expressions = []
SVar = []
IVar = []

#Function to get loop body
def get_loop_body(content):
	loop_body = []
	flag_is_loop_body = 0						#This is used to detect when we are in and out of loop body
	num_open_bracket = 0						#This is used to count all open {} so we dont exit loop body prematurely

	#Loop to check every line for for loop
	for i in range (0,len(content)):
		if (content[i] is not ''):
			if flag_is_loop_body == 1:
				#Check for all curly braces
				for j in range  (0,len(content[i])):
					if content[i][j] == '{':
						num_open_bracket = num_open_bracket+1
					if content[i][j] == '}':
						num_open_bracket = num_open_bracket-1

				#Get out of loop body
				if num_open_bracket <= 0:
					flag_is_loop_body = 2
					break
				else:
					#Adding to loop body if we still in it
					loop_body.append(content[i])

			#Assuming the only loop is for loop. Can add a while check, but that would be better done in a more efficient system...
			if (flag_is_loop_body == 0 and content[i][0] == 'f' and content[i][1] == 'o' and content[i][2] == 'r' and content[i][3] == '('):
				if (content[i][len(content[i]) - 1] == '{'):
					num_open_bracket = num_open_bracket+1
				flag_is_loop_body = 1
	return loop_body

#Function to get expressions, and get SVar and IVar values, It also get root expressions according to the given schema
def add_expr_and_var(express):
	'''
	1. = without anything else. The left side is an SVar, right side is an expression
	2. &&, || both sides are expressions
	3. >=, <=, == , != both sides are expressions
	'''

	#Remove all brackets cause not needed
	express = [x.strip('(') for x in express]
	express = [x.strip(')') for x in express]
	express = [x.strip(';') for x in express]
	express = [x.strip() for x in express]
	
	express = ''.join(express)
	#Checking for = signs
	for i in range(0,len(express)):
		if express[i] == '=':
			if (express[i-1] is not '<' and express[i-1] is not '>' and express[i-1] is not '!' and express[i-1] is not '=' and express[i+1] is not '='):
				temp = express[0:i].strip()
				if temp in IVar:
					IVar.remove(temp)
				SVar.append(temp)
				add_expr_and_var(express[i+1:len(express)])
				return 0

	#Checking for && and ||
	if "&&" in express:
		add_expr_and_var(express[0:express.index("&&")])
		add_expr_and_var(express[express.index("&&")+2:])
		return 0
	elif "||" in express:
		add_expr_and_var(express[0:express.index("||")])
		add_expr_and_var(express[express.index("||")+2:])
		return 0
	#Checking for >=,<=,!= and ==
	elif ">=" in express:
		add_expr_and_var(express[0:express.index(">=")])
		add_expr_and_var(express[express.index("<=")+2:])
		return 0
	elif "<=" in express:
		add_expr_and_var(express[0:express.index("<=")])
		add_expr_and_var(express[express.index("<=")+2:])
		return 0
	elif "!=" in express:
		add_expr_and_var(express[0:express.index("!=")])
		add_expr_and_var(express[express.index("!=")+2:])
		return 0
	elif "==" in express:
		add_expr_and_var(express[0:express.index("==")])
		add_expr_and_var(express[express.index("==")+2:])
		return 0
	else:
		if (express in SVar) == False : 
			IVar.append(express)

#Function called to simplify expressions, and filter out if statements
def get_expr(loop_body):
	for i in range(0,len(loop_body)):
		if ( loop_body[i] is not ''):
			if(loop_body[i][0] == 'i' ):
				if(loop_body[i][1] == 'f' and (loop_body[i][2] == '(') or (loop_body[i][2] == ' ')):
					to_stop = 0
					to_start = 0
					for j in range(0,len(loop_body[i])):
						if(loop_body[i][j] == ')'):
							to_stop = j
					for j in range(0,len(loop_body[i])):
						if(loop_body[i][j] == '('):
							to_start = j
							break
					add_expr_and_var(loop_body[i][to_start+1:to_stop])
			else:
				if(loop_body[i][0] == '{' or loop_body[i][0] == '}'):
					continue
				else:
					add_expr_and_var(loop_body[i])


#Function that adds else statements to the loop if they are missing
def add_else(loop_body):
	check = 1
	st = 0
	end = 0
	ret = 0
	for i in range(0,len(loop_body)):
		if check == 1:
			if loop_body[i][0] == 'i' and loop_body[i][1] == 'f' and (loop_body[i][2] == ' ' or loop_body[i][2] == '('):
				st = i+1
				check = 0;
				big_br = add_else(loopbody[st:])
				big_br = i+big_br

		if (check == 0  or check == 2) and i > big_br:
			if loop_body[i][0] == '}' or check == 2:
				check = 2
				if i < len(loop_body)-1:
					if loop_body[i+1] is not '':
						if loop_body[i+1][0] == 'e' and loop_body[i+1][0] == 'l' and loop_body[i+1][0] == 's' and loop_body[i+1][0] == 'e':
							big_br = add_else(loop_body[i+1:])
							big_br = i+big_br
							check = 3
						else:
							temp_array = loop_body[:i]
							temp_array.append("else{}")
							temp_array.apped(loop_body[i+1:])
							ret = i+1
				else:
					loop_body.append("else{}")
					ret = i+



'''	for i in range(len(loop_body),0):
		if check = 0:
			if loop_body[i][0] == '}':
				end = i;
				temp_array = loop_body[st:end]
				temp_array = add_else(temp_array)
'''
#Function which reads the file, and has the main goal of getting SVar
def get_SVar_from_File(name):
	#Get all contents of file
	with open(name) as f:
	    content = f.readlines()

	content = [x.strip() for x in content] 

	#Get Loop Body
	loopbody = get_loop_body(content)

	#Get Expressions,create SVar and IVar
	get_expr(loopbody)


#Get the filename from command line argument
fname = sys.argv[1]

get_SVar_from_File(fname,0)




