# -*- coding: windows-1254 -*-

##      ITU TURKISH NLP PIPELINE CALLER
##      Copyright (C) 2015  Ferit Tunçer
##
##      This program is free software; you can redistribute it and/or
##  modify it under the terms of the GNU General Public License version 2
##  as published by the Free Software Foundation.
##
##      This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##      You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##      Author: Ferit Tunçer, ferit.tuncer@autistici.org

version = 0.63
##      Changes since 0.62
##			a big cleanup
##			token provided with token file(pipeline.token by default) now


##      TODOS
##			http://stackoverflow.com/questions/8763451/how-to-handle-urllibs-timeout-in-python-3 sentence-by-sentence performance improvement
##			cleanup on exceptions


#++ Configuration block - EDIT HERE
tool = "pipelineFormal"
token_path = "pipeline.token"
api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"
output_dir = "script_output"
encoding_code = "WINDOWS-1254"
#-- Configuration block

import sys
import urllib.request
import urllib.parse
import contextlib
import time
import os.path
import argparse
import re

invalid_token_message = ""
invalid_param_message = ""
invalid_tool_message = ""
no_parameter_message = ""
pipeline_encoding = 'UTF-8'

#++ Utility functions
def warning(*objs):
    print("[ERROR]:", *objs, file=sys.stderr)

def conditional_info(to_be_printed):
    #
    if args.quiet == 0:
        print(to_be_printed)
#--

def request(params):
	try:
		result = urllib.request.urlopen(api_url, params)
		readed_result = result.read().decode("UTF-8")
		if readed_result == invalid_token_message:
			sys.exit(invalid_token_message)
		elif readed_result == invalid_tool_message:
			sys.exit(invalid_tool_message)
		elif readed_result == invalid_param_message:
			sys.exit(invalid_param_message)
		elif readed_result == no_parameter_message:
			sys.exit(no_parameter_message)
		return readed_result
	except KeyboardInterrupt:
		sys.exit("[FATAL]Terminated by keyboard interrupt.")
	except:
		warning("{0}\nDid you configure the configuration part of the source code properly?".format(sys.exc_info()[1]))
		print(invalid_param_message)
		sys.exit("[FATAL]Failed to connect pipeline! Terminated.")

def fetchInvalidMessages():
	dummy_params = urllib.parse.urlencode({'tool': tool, 'input': "", 'token': token}).encode("UTF-8")
	no_parameter_message = urllib.request.urlopen(api_url, dummy_params).read().decode("UTF-8")
	dummy_params = urllib.parse.urlencode({'tool': tool, 'input': "dummy", 'token': "wrong_token"}).encode("UTF-8")
	invalid_token_message = urllib.request.urlopen(api_url, dummy_params).read().decode("UTF-8")
	dummy_params = urllib.parse.urlencode({'tool': "dummy", 'input': "dummy", 'token': token}).encode("UTF-8")
	invalid_tool_message = urllib.request.urlopen(api_url, dummy_params).read().decode("UTF-8")
	invalid_param_message = urllib.request.urlopen(api_url).read().decode("UTF-8")
	return no_parameter_message, invalid_token_message, invalid_tool_message, invalid_param_message

def parseArgumentsAndGreet():
        option_parser = argparse.ArgumentParser(description="ITU Turkish NLP Pipeline Caller v{0}".format(version))
        option_parser.add_argument("filename", help="relative input filepath")
        option_parser.add_argument('-s', '--seperate', dest="seperate", action="store_true", help="process sentence-by-sentence instead of batch processing")
        option_parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="no info during process")
        print("{0}".format(option_parser.description))
        return option_parser.parse_args()

def readInput(path):
	try:
		input_file = open(path)
		full_text = ""
		for line in input_file:
			full_text += line
		sentences = full_text.split('.')
		sentence_count = len(sentences)
		if re.match("^\s*$", sentences[sentence_count-1]):
			sentences.pop(sentence_count-1)
		return full_text, sentences, sentence_count
	except:
		pass

def getOutputPath():
	try:
		#filepath = ('{0}\output{1}').format(output_dir, str(time.time()).split('.')[0])
		filepath = os.path.join(output_dir, "output{0}".format(str(time.time()).split('.')[0]))
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		output_path = open(filepath, 'w')
		conditional_info("[INFO] Writing destination: {0}".format(filepath))
		return output_path
	except:
		pass
		
def readToken():
	try:
		token_file = open(token_path)
		token = token_file.readline()
		return token
	except:
		pass
		
def process():
	if args.seperate == 0:
		conditional_info("[INFO] Batch processing started!")
		params = urllib.parse.urlencode({'tool': tool, 'input': full_text, 'token': token}).encode("UTF-8")
		output_path.write("{0}\n".format(request(params)))
		conditional_info("[DONE] It took {0} seconds to process {1} sentences".format(str(time.time()-start_time).split('.')[0], sentence_count))
	else:
		conditional_info("[INFO] Sentence-by-sentence processing started!")
		for sentence in sentences:
			params = urllib.parse.urlencode({'tool': tool, 'input': sentence, 'token': token}).encode("UTF-8")
			output_path.write("{0}\n".format(request(params)))
			conditional_info("[INFO] Processing {0}".format(sentence))
		conditional_info("[DONE] It took {0} seconds to process all {1} sentences.".format(str(time.time()-start_time).split('.')[0], sentence_count))



args = parseArgumentsAndGreet()
try:
	full_text, sentences, sentence_count = readInput(args.filename)
	output_path = getOutputPath()
	token = readToken()
except:
	warning("{0}".format(sys.exc_info()[1]))
	output_path.close()
	sys.exit("[FATAL] I\O Exception")
no_parameter_message, invalid_token_message, invalid_tool_message, invalid_param_message = fetchInvalidMessages()
start_time = time.time()
conditional_info("[INFO] Using {0} tool".format(tool))
process()

output_path.close()