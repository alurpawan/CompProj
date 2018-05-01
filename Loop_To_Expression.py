'''
Author : Pawan Alur
What does this file do? : This file takes as input a filename, and then reads this file. 
It assumes that the file is a C file with a SINGLE loop(no nested loops), and then converts it to an expression as decided in the paper.
'''


#Imports
import sys
import string
import re


#Global Variables
Variable = []						#This contains a list of all variables
SVar = []							#This contains a list of all SVar
if_Cond = []						#This contains a list of all if conditions to add to variables


#Classes
class Loop:							#Contains information about the loop
	def __init__(self):
		self.iter_var = "a"
		self.limit = 0
		self.loop_body = []

	def get_loop_info(self,loop):
		for_syntax = 'for\(([\w\d_ ]+)=[ \d]+;[ \w\d]+[ <>=]+([ \w\d_]+)'
		match = re.search(for_syntax,loop[0])
		if match:
			self.iter_var = match.group(1)
			self.limit = match.group(2)
			self.loop_body = loop[2:len(loop) - 1]
		else:
			print("Error : For loop not found in loop body")

	def print_loop_body(self):
		for i in self.loop_body:
			print(i)

	def get_SVar(self):
		match_equals = '([\w\d_ ]+)='
		for i in self.loop_body:
			match = re.search(match_equals,i)
			
			if match:
				var_name = match.group(1)
				var_name = var_name.strip()
				add_var_to_S(var_name)
			

	'''
	Algorithm to calculate expression : 
	For every line of code:
	 - if loop
	 - openging brace
	 - else
	 - closing brace of if loop
	 - closing brace of else loop
	 - assignment

	 Else flag
	 0 : Outside all conditionals
	 1 : Inside an if
	 2 : Inside an else

	 1)If it's an if condition:set old_loc = curr_loc. curr_loc = 1. Store the conditional to be used. 
	 2)If it's an opening bracket, add 1 to curr_place. 
	 3)If it's an else, set curr_loc = 2.
	 4)If it's a }, its super complicated and I'll comment the code line by line

	'''	
	def create_Expression(self):
		old_flag = []
		else_flag = 0
		loc = -1
		for i in self.loop_body:
			loc+=1
			if i.startswith("if(") or i.startswith("if "):		#If condition
				old_flag.append(else_flag)
				else_flag=1
				#print(old_flag)
				push_CV()
				match_if = 'if[ ]*\(([\w\d<>=|&\(\)\[\]! ]+)\)'
				match = re.search(match_if,i)
				#print(match)
				if match:
					
					cond = match.group(1)
					#print(cond)
					if_Cond.append(cond)
				else:
					print("Error in if loop")
			
			elif i.startswith("else"):						#Else condition
									
				else_flag = 2

 
			elif i == '}':
				if else_flag == 1:
					change_if_val()
					#print(self.loop_body[loc+1])
					#print(loc == len(self.loop_body)-1)
					#print(self.loop_body[loc+1].strip() != 'else')
					
					if loc == len(self.loop_body)-1 or self.loop_body[loc + 1].strip() != 'else':			#i is last line or next line IS NOT else:
						#print("Here")		
						create_CV()
						else_flag = old_flag.pop()
				if else_flag == 2:
					#print(loc)
					#print("Here")	
					change_else_val()
					create_CV()
					#for i in SVar:
					#	print(i.CurrVal)
					else_flag = old_flag.pop()
					#print(else_flag)
			
			else:												#Assignmnent
				match_equals = '([\w\d_ ]+)=([\w\d<>=|&\(\)\[\]!+-/\* ]+)'
				match = re.search(match_equals,i)
				if match:
					var_name = match.group(1)
					var_name = var_name.strip()
					var_val = match.group(2)
					change_val(var_name,var_val)
					
class Var:							#Contains information about a variable. This is used to get an expression. 
	def __init__(self,name,init_val):
		self.name = name
		self.CurrVal = init_val
		self.if_loop = []
		self.else_loop = []

	def print_Val(self):
		print(self.name + " = " + self.CurrVal)

	def same_name(self,name):
		if self.name == name:
			return True
		return False
		


#Functions not belonging to class
def get_loop_and_vars(content):		#Gets loop and also gets list of all variables
	loop_flag = 0
	loop = []

	for i in content:	
		if (i.startswith('int ') or i.startswith('float ') or i.startswith('bool ') or i.startswith('char ')) and i is not content[0]:
			tempvar = i[i.find(' ')+1:i.find('=')-1]
			tempval = str(i[i.find('=')+2:i.find(';')])
			new_var = Var(tempvar,tempvar)
			Variable.append(new_var)

		if i.startswith("for(") or i.startswith("for ("):	#To get loop
			loop_flag = 1

		if loop_flag >= 1:
			loop.append(i)
			if i == '{':
				loop_flag = loop_flag+1
			if i == '}':
				loop_flag = loop_flag-1

		if loop_flag == 1 and i == '}':
			loop_flag = 0 

	return loop

def get_data_from_file(fname):
	content = []


	with open(fname) as f:				#Get lines from file, removing all blank lines
		for line in f:
			if not line.isspace():
				content.append(line)

	#Remove starting spaces
	content = [x.strip() for x in content] 	
	return content	#Get the whole program from the file

def add_var_to_S(name):
	for i in Variable:
		if i.same_name(name) and i not in SVar:
			SVar.append(i)			 #Checks the whole loop for System Variables and adds them to a list

def push_CV():
	for j in SVar:
		j.if_loop.append(j.CurrVal)
		j.else_loop.append(j.CurrVal)					 #Called in case of if statements, to push the Current Value to if_loop and else_loop variables

def change_if_val():				#Called whenever an if loop ends, to save value from CV to if_loop 
	for i in SVar:
		#print(i.CurrVal)
		i.if_loop.pop()
		i.if_loop.append(i.CurrVal)

def create_CV():					#Used to convert if and else values to an if then else statement and store it in CV
	cond = if_Cond.pop()
	#print(cond)
	for i in SVar:
		if_val = i.if_loop.pop()
		else_val = i.else_loop.pop()
		#print(if_val)
		#print(else_val)
		if if_val is not else_val:
			final_cv = 'if ( '+ cond + ' ) then { ' + if_val + ' } else { ' + else_val + ' }'
			#print(final_cv)
			i.CurrVal = final_cv
			#print(i.CurrVal)
		else:
			i.CurrVal = if_val							 

def change_else_val():				#Called whenever an else loop ends, to save value from CV to else_loop 
	for i in SVar:
		i.else_loop.pop()
		i.else_loop.append(i.CurrVal)
		#print (i.CurrVal)			

def change_val(var_name,var_val):	#Called whenver a value of SVar is changed, used to store new value
	for i in SVar:
		if i.name == var_name:
			i.CurrVal = var_val
			break

#Main Starts here
def Main(arg1):
	fname = arg1
	content = get_data_from_file(fname)
	loop = get_loop_and_vars(content)
	
	main_loop = Loop()
	main_loop.get_loop_info(loop)
	#main_loop.print_loop_body()
	main_loop.get_SVar()
	#print(len(SVar))
	main_loop.create_Expression()
	for i in SVar:
		i.print_Val()
	return SVar

