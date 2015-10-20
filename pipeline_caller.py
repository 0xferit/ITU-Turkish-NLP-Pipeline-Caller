# -*- coding: windows-1254 -*-

##      ITU TURKISH NLP PIPELINE CALLER
##      Copyright 2015 Ferit Tunçer
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

author_copyright = "\nCopyright 2015 Ferit Tunçer ferit.tuncer@autistici.org"

version = 0.71

import sys
import urllib.request
import urllib.parse
import contextlib
import time
import os.path
import argparse
import re
import locale


#++ DEFAULTS
token_path = "pipeline.token"
api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"
default_encoding = locale.getpreferredencoding(False)
pipeline_encoding = 'UTF-8'
default_output_dir = "pipeline_caller_output"
default_seperator_class = "[\.\?:;!]"
#-- DEFAULTS

invalid_token_message = ""
invalid_param_message = ""
invalid_tool_message = ""
no_parameter_message = ""


#++ Utility Functions
def warning(*objs):
    print(*objs, file=sys.stderr)

def conditional_info(to_be_printed):
    #
    if args.quiet == 0:
        print(to_be_printed)
#--

#-- Functions
def request(params):
	try:
		result = urllib.request.urlopen(api_url, params)	
		readed_result = result.read().decode(pipeline_encoding)
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
		warning("{0}1".format(sys.exc_info()))
	except:
		raise

def fetchInvalidMessages():
	dummy_params = urllib.parse.urlencode({'tool': args.tool, 'input': "", 'token': token}).encode(pipeline_encoding)
	no_parameter_message = urllib.request.urlopen(api_url, dummy_params).read().decode("UTF-8")
	dummy_params = urllib.parse.urlencode({'tool': args.tool, 'input': "dummy", 'token': "wrong_token"}).encode(pipeline_encoding)
	invalid_token_message = urllib.request.urlopen(api_url, dummy_params).read().decode(pipeline_encoding)
	dummy_params = urllib.parse.urlencode({'tool': "dummy", 'input': "dummy", 'token': token}).encode(pipeline_encoding)
	invalid_tool_message = urllib.request.urlopen(api_url, dummy_params).read().decode(pipeline_encoding)
	invalid_param_message = urllib.request.urlopen(api_url).read().decode(pipeline_encoding)
	return no_parameter_message, invalid_token_message, invalid_tool_message, invalid_param_message

def parseArguments():
		arg_parser = argparse.ArgumentParser(
		description="ITU Turkish NLP Pipeline Caller v{}{}".format(version, author_copyright),
		epilog="TOOLS: ner, morphanalyzer, isturkish,  morphgenerator, tokenizer, normalize, deasciifier, Vowelizer, DepParserFormal, DepParserNoisy, spellcheck, disambiguator, pipelineFormal, pipelineNoisy",
		add_help=True)
		arg_parser.add_argument("filename", help="relative input filepath")
		arg_parser.add_argument('-s', '--seperate', dest="seperate", action="store_true", help="process sentence-by-sentence instead of batch processing")
		arg_parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="no info during process")
		arg_parser.add_argument("-t", "--tool", metavar="T", dest="tool", default="pipelineFormal", help="pipeline tool name, \"pipelineFormal\" by default")
		arg_parser.add_argument("-e", "--encoding", dest="encoding", metavar="E", default=default_encoding, help="force I/O to use given encoding, instead of default locale")
		arg_parser.add_argument("-o", "--output", metavar="O", dest="output_dir", default=default_output_dir, help="change output directory, \"pipeline_caller_output\" by default")
		return arg_parser.parse_args()

def readInput(path):
	try:
		with open(path, encoding=args.encoding) as input_file:
			full_text = ""
			for line in input_file:
				full_text += line
		r = re.compile(r'(?<=(?:{}))\s+'.format(default_seperator_class)) 
		sentences = r.split(full_text)
		sentence_count = len(sentences)
		if re.match("^\s*$", sentences[sentence_count-1]):
			sentences.pop(sentence_count-1)
		return full_text, sentences, sentence_count
	except:
		raise

def getOutputPath():
	try:
		if not os.path.exists(args.output_dir):
			os.makedirs(args.output_dir)	
		filepath = os.path.join(args.output_dir, "output{0}".format(str(time.time()).split('.')[0]))
		conditional_info("[INFO] Output destination: .{}{}".format(os.sep, filepath))
		return filepath
	except:
		raise
		
def readToken():
	try:
		token_file = open(token_path)
		token = token_file.readline()
		return token
	except:
		raise
		
def process():
	with open(output_path, 'w', encoding=args.encoding) as output_file:
		if args.seperate == 0:
			conditional_info("[INFO] Processing type: Batch")
			
			params = urllib.parse.urlencode({'tool': args.tool, 'input': full_text, 'token': token}).encode(pipeline_encoding)
			
			output_file.write("{0}\n".format(request(params)))
			print("[DONE] It took {0} seconds to process {1} sentences".format(str(time.time()-start_time).split('.')[0], sentence_count))
		else:
			conditional_info("[INFO] Processing type: Sentence-by-sentence")
			for sentence in sentences:
			
				params = urllib.parse.urlencode({'tool': args.tool, 'input': sentence, 'token': token}).encode(pipeline_encoding)
				
				output_file.write("{0}\n".format(request(params)))
				conditional_info("[INFO] Processing {0}".format(sentence))
			print("[DONE] It took {0} seconds to process all {1} sentences.".format(str(time.time()-start_time).split('.')[0], sentence_count))
#-- Functions

#++ Main Block
args = parseArguments()
try:
	full_text, sentences, sentence_count = readInput(args.filename)
	output_path = getOutputPath()
	token = readToken()
	conditional_info("[INFO] File I/O encoding: {}".format(args.encoding))
	no_parameter_message, invalid_token_message, invalid_tool_message, invalid_param_message = fetchInvalidMessages()
	start_time = time.time()
	conditional_info("[INFO] Pipeline tool: {}".format(args.tool))
	process()
except:
	warning("{0}".format(sys.exc_info()))
	sys.exit("[FATAL] Terminating.")

#-- Main Block