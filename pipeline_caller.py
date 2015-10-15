# -*- coding: windows-1254 -*-

##      This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##      This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##      You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##      Author: Ferit Tunçer, ferit.tuncer@autistici.org

version = 0.6

#++ Configuration block - EDIT HERE
tool = "pipelineFormal"
token = "Dfph8QwU3bSKvL7Fy8JFjYhuxZrul0Qw"
api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"
output_dir = "script_output"
encoding_code = "WINDOWS-1254"
#-- Configuration block

import xml.etree.ElementTree as etree
import sys
import urllib.request
import urllib.parse
import contextlib
import time
import os.path
import argparse

invalid_token_message = ""
invalid_param_message = ""
invalid_tool_message = ""

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
        return readed_result
    except KeyboardInterrupt:
        f.close()
        sys.exit("[FATAL]Terminated by keyboard interrupt.")
    except:
        f.close()
        warning("{0}\nDid you configure the configuration part of the source code properly?".format(sys.exc_info()[1]))
        print(invalid_param_message)
        sys.exit("[FATAL]Failed to connect pipeline! Terminated.")

def fetchInvalidMessages():
	dummy_params = urllib.parse.urlencode({'tool': tool, 'input': "dummy", 'token': "wrong_token"}).encode("UTF-8")
	invalid_token_message = urllib.request.urlopen(api_url, dummy_params).read().decode("UTF-8")
	dummy_params = urllib.parse.urlencode({'tool': "dummy", 'input': "dummy", 'token': token}).encode("UTF-8")
	invalid_tool_message = urllib.request.urlopen(api_url, dummy_params).read().decode("UTF-8")
	invalid_param_message = urllib.request.urlopen(api_url).read().decode("UTF-8")

def parseArgumentsAndGreet():
	option_parser = argparse.ArgumentParser(description="ITU Turkish NLP Pipeline Caller v{0}".format(version))
	option_parser.add_argument("filename", help="relative input filepath")
	option_parser.add_argument('-s', '--seperate', dest="seperate", action="store_true", help="process sentence-by-sentence instead of batch processing")
	option_parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="no info during process")
	print("{0}".format(option_parser.description))
	return option_parser.parse_args()


args = parseArgumentsAndGreet()
fetchInvalidMessages()

parser = etree.XMLParser(encoding=encoding_code)

#++ Input file block
try:
    tree = etree.parse(args.filename, parser=parser)
except:
    warning("{0}".format(sys.exc_info()[1]))
    sys.exit("[FATAL] Failed to read {0}. Terminated.".format(args.filename))
#-- Input file block


#++ Output file block
try:
    #filepath = ('{0}\output{1}').format(output_dir, str(time.time()).split('.')[0])
    filepath = os.path.join(output_dir, "output{0}".format(str(time.time()).split('.')[0]))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    f = open(filepath, 'w')
    conditional_info("[INFO] Writing destination: {0}".format(filepath))
except:
    warning("{0}".format(sys.exc_info()[1]))
    sys.exit("[FATAL] Error writing to {0}".format(filepath))
#-- Output file block

root = tree.getroot()

sentences = []
for sub_element_1 in root:
	temp_sentence = []
	for sub_element_2 in sub_element_1:
		temp_sentence.append(sub_element_2)
	sentences.append(temp_sentence)

full_text = "".join(str(e) for e in sentences)
full_text = full_text.replace('_', ' ')

##full_text = ""
##g = open(args.filename)
##for line in g:
##    full_text += line
##print(full_text)

start_time = time.time()

conditional_info("[INFO] Using {0} tool".format(tool))

if args.seperate == 0:
    conditional_info("[INFO] Batch processing started!")
    params = urllib.parse.urlencode({'tool': tool, 'input': full_text, 'token': token}).encode("UTF-8")
    f.write("{0}\n".format(request(params)))
    conditional_info("[DONE] It took {0} seconds to process all sentences".format(str(time.time()-start_time).split('.')[0]))


else:
    conditional_info("[INFO] Sentence-by-sentence processing started!")
    for sentence in sentences:
        plain_sentence = "".join(str(x.text) for x in sentence)
        params = urllib.parse.urlencode({'tool': tool, 'input': plain_sentence, 'token': token}).encode("UTF-8")
        f.write("{0}\n".format(request(params)))
        sentence_count = len(sentences)
        conditional_info("[INFO] Processing {0}".format(plain_sentence))
    conditional_info("[DONE] It took {0} seconds to process all {1} sentences.".format(str(time.time()-start_time).split('.')[0], sentence_count))


f.close()
