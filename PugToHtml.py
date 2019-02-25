#!/usr/bin/env python
# coding: utf-8

import re
from argparse import ArgumentParser
import os.path

#This function removes multiline attributes and converts them into single line
def removeMultilineAttr(block):
    attributes = re.findall(r"\(([^\)]+)\)", block)	
    for i in range(0,len(attributes)):
        attribute = attributes[i].replace("\n", "").strip()
        attribute = attribute.replace("\t", "  ").strip()
        attribute = re.sub("\s+", " ", attribute)
        block = block.replace(attributes[i],attribute)
    return block
#Removes | sign
def handlePalochki(block):
    return block.replace("|","")
#Replace \t by standard pug indentation
def handleTabs(block):
    return block.replace("\t","  ")	

#This function searchs for lines with Block Expansion.
#If it contains Block Expnasion, searchs the line where it is and lines affected by Block Expnasion
def handleBlockExpansion(block):
	def findWhereBlockExpansionEnds(lines):
		tab_number_of_line_where_blockExp_starts = len(lines[0]) - len(lines[0].lstrip())
		for i in range(1,len(lines)):
			if(tab_number_of_line_where_blockExp_starts >= len(lines[i]) - len(lines[i].lstrip())):
				index_of_end_block_expansion = i
				break
		return index_of_end_block_expansion  

	def handleLinesWithBlockExpansion(lines_with_be):
		line_where_be_starts, lines__affected_by_be = lines_with_be[0],lines_with_be[1:]
		leading_space_count = len(line_where_be_starts) - len(line_where_be_starts.lstrip())
		space = ""
		for i in range(0,leading_space_count):
			space = space+" "
		line_where_be_starts = line_where_be_starts.replace(": ","\n"+space+"  ").split("\n")
		
		for i in range(0,len(lines__affected_by_be)):
			if (lines__affected_by_be[i]!=''):
				lines__affected_by_be[i] = "  " + lines__affected_by_be[i]
		new_lines = line_where_be_starts+lines__affected_by_be
		return new_lines

	if ": " in block:
		lines = block.split("\n")
		lines_before_be = []
		lines_with_be =[]
		lines_after_be = []
		new_lines = []
		for i in range(0,len(lines)):
			if ": " in lines[i]:
				index_where_be_starts = i
				index_where_be_ends = index_where_be_starts+findWhereBlockExpansionEnds(lines[i:])
				lines_before_be = lines[:index_where_be_starts]
				lines_with_be = lines[index_where_be_starts:index_where_be_ends]
				lines_after_be = lines[index_where_be_ends:]
				lines_with_handled_be = handleLinesWithBlockExpansion(lines_with_be)
				new_lines = lines_before_be+lines_with_handled_be+lines_after_be
				new_block = "\n".join(new_lines)
				break
		return handleBlockExpansion(new_block)
	else:
		return block

#The final function which converts preprocessed text in pug format to html format
def convertToHtml(block):

	def convertBlockToHtml(block):
		html = ""
		for i in block:
			html = html + i["close_tag"]+"<"+i["tag"]+" "+i["attribute"]+">"+i["tag_text"]
		html = html.replace("< >", "")
		html = html.replace("</>", "")
		return html
	#This function makes a decision where to locate closing tag
	def findWhereToCloseTag(block,line):
		
		def checkForNestedOfSelfClosingElements(block,self_closing_line):
			for line in block:
				if (self_closing_line["tab"]<line["tab"] and line["tab"]!=0):
					print("Syntax ERROR: <"+self_closing_line["tag"] + "/> is a self closing element, it cannot have nested content, please move "+ line["tag"]+" tag in line " +  str(line["index"]+1)+"\n"+
						 "->"+ line["tag"] +"("+line["attribute"]+")")
					break
				elif(self_closing_line["tab"]>=line["tab"] and line["tab"]!=0):
					break

		if (line["self_closing"] == True):
			line["attribute"] = line["attribute"] + "/"
			checkForNestedOfSelfClosingElements(block,line)
		else:
			for i in block:
				if (line["tab"]>=i["tab"]):
					i["close_tag"] = "</" + line["tag"] + ">"+i["close_tag"]
					break
		return line
	#Parsing pug text line by line
	def handleByLine(line,index):
		
		def checkForSelfClosingSyntaxError(line, attribute,index):
			if(attribute != ""):
				if ("/(" in line):
					print("Unexpected token: \"start_attributes\" - line "+ str(index+1))
		#This function checks if the tag selfclosing or not
		def checkIfSelfClosingTag(tag):
			if (tag in list_of_self_closing_elements):
				return tag,True
			else:
				if "/" in tag:
					return tag.replace("/",""),True
				else:
					return tag,False

		attribute = re.search(r"\(([^\)]+)\)", line)#Extracting attributes

		if (attribute != None):#
			attribute = attribute.group(1)
		else:
			attribute = ""
		
		checkForSelfClosingSyntaxError(line, attribute,index)
		
		attributless_line = line.replace("("+attribute+")","")							#This block of code counts indentation
		leading_space_count = len(attributless_line) - len(attributless_line.lstrip())	#thus, further it will
		leading_spaceless_line = attributless_line.lstrip()								#be used in hierarchy tagging
		
		intag_text = leading_spaceless_line.split(" ",1)	#Text wrapped by tag
		tag = intag_text[0]	#The tag itself
		if (tag ==""):
			leading_space_count = 0	# Handling lines without any tag
		
		tag,self_closing = checkIfSelfClosingTag(tag)
		
		if 1 < len(intag_text):
			intag_text = intag_text[1]		#Tag text handling
		else:
			intag_text = ""
		
		return {
			"index": index,
			"tab" : leading_space_count,
			"tag" : tag,
			"attribute": attribute,
			"tag_text": intag_text,
			"self_closing": self_closing,
			"close_tag": ""
		}

		
	lines = block.split("\n") 
	line_info = []
	block_with_closed_tags = []
	for i in range(0,len(lines)):
		line_info.append(handleByLine(lines[i],i))	#Appending information about each line as dictionary

	for i in range(0,len(line_info)):
		line_with_closed_tags = findWhereToCloseTag(line_info[i+1:],line_info[i]) 
		block_with_closed_tags.append(line_with_closed_tags) 	#Here we have a dictionary with all the info, like where to close a tag, if it is self closing or not etc
	return convertBlockToHtml(block_with_closed_tags)


parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="myFile", help="Open specified file")
parser.add_argument("-o", "--output", help="Directs the output to a name of your choice")
args = parser.parse_args()
myFile = args.myFile
pugfile = open(myFile,'r')

PugAsText = pugfile.read()


list_of_self_closing_elements = ["img","input"]

PugAsText = handlePalochki(PugAsText)
PugAsText = handleTabs(PugAsText)
PugAsText = removeMultilineAttr(PugAsText)
PugAsText = handleBlockExpansion(PugAsText)
html = convertToHtml(PugAsText)

with open(args.output, 'w') as output_file:
    output_file.write("%s\n" % html)





