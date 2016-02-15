#!/usr/bin/python3

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

version = "1.0.0"

import sys
import urllib.request
import urllib.parse
import time
import os.path
import argparse
import re
import locale
import unittest

#++ DEFAULTS
token_path = "pipeline.token"
default_encoding = locale.getpreferredencoding(False)
default_separator_char_class = "[\.\?:;!]"
default_output_dir = "output"
api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"
pipeline_encoding = 'UTF-8'
#-- DEFAULTS


class PipelineCaller:

    def call(self, tool, text, token):
        params = urllib.parse.urlencode({'tool': tool, 'input': text, 'token': token}).encode(pipeline_encoding)
        try:
            result = urllib.request.urlopen(api_url, params)
            return result.read().decode(pipeline_encoding)
        except:
            raise


def __readInput(path):
    try:
        with open(path, encoding=args.encoding) as input_file:
            full_text = ""
            for line in input_file:
                full_text += line
        r = re.compile(r'(?<=(?:{}))\s+'.format(default_separator_char_class)) 
        sentences = r.split(full_text)
        sentence_count = len(sentences)
        if re.match("^\s*$", sentences[sentence_count-1]):
            sentences.pop(sentence_count-1)
        sentence_count = len(sentences)
        return full_text, sentences, sentence_count
    except:
        raise
        
def __readToken():
    try:
        token_file = open(token_path)
        token = token_file.readline().strip()
        return token    
    except:
        raise

def __getOutputPath():
    try:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        filepath = os.path.join(args.output_dir, "output{0}".format(str(time.time()).split('.')[0]))
        return filepath
    except:
        raise
        


def __conditional_info(to_be_printed):
    #
    if args.quiet == 0:
        print(to_be_printed)

def __parseArguments():
        arg_parser = argparse.ArgumentParser(
        description="ITU Turkish NLP Pipeline Caller v{}{}".format(version, author_copyright),
        epilog="TOOLS: ner, morphanalyzer, isturkish,  morphgenerator, tokenizer, normalize, deasciifier, Vowelizer, DepParserFormal, DepParserNoisy, spellcheck, disambiguator, pipelineFormal, pipelineNoisy",
        add_help=True)
        arg_parser.add_argument("filename", help="relative input filepath")
        arg_parser.add_argument('-s', '--separate', dest="separate", action="store_true", help="process sentence by sentence instead of all at once")
        arg_parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="no info during process")
        arg_parser.add_argument("-t", "--tool", metavar="T", dest="tool", default="pipelineNoisy", help="pipeline tool name, \"pipelineNoisy\" by default")
        arg_parser.add_argument("-e", "--encoding", dest="encoding", metavar="E", default=default_encoding, help="force I/O to use given encoding, instead of default locale")
        arg_parser.add_argument("-o", "--output", metavar="O", dest="output_dir", default=default_output_dir, help="change output directory, \"{}\" by default".format(default_output_dir))
        return arg_parser.parse_args()

if __name__ == '__main__':

    args = __parseArguments()
    full_text, sentences, sentence_count = __readInput(args.filename)
    output_path = __getOutputPath()
    token = __readToken()
    __conditional_info("[INFO] Pipeline tool: {}".format(args.tool))
    __conditional_info("[INFO] File I/O encoding: {}".format(args.encoding))
    __conditional_info("[INFO] Output destination: .{}{}".format(os.sep, output_path))
    start_time = time.time()

    caller = PipelineCaller()
    
    if args.separate == 0:
        __conditional_info("[INFO] Processing all the text at once")
        with open(output_path, 'w', encoding=args.encoding) as output_file:
            output_file.write("{0}\n".format(caller.call(args.tool, full_text, token)))
        
    else:
        __conditional_info("[INFO] Processing sentence by sentence")
        with open(output_path, 'w', encoding=args.encoding) as output_file:
            for sentence in sentences:
                output_file.write("{0}\n".format(caller.call(args.tool, sentence, token)))
    print("[DONE] It took {0} seconds to process all {1} sentences.".format(str(time.time()-start_time).split('.')[0], sentence_count))
    
    
    
