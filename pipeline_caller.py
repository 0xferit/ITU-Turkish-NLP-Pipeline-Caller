#!/usr/bin/python3

name = "ITU Turkish NLP Pipeline Caller"
copyright = "Copyright 2015 Ferit Tunçer"

license = "This program is free software; you can redistribute it and/or \
modify it under the terms of the GNU General Public License version 2 \
as published by the Free Software Foundation. \
This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details. \
You should have received a copy of the GNU General Public License \
along with this program.  If not, see <http://www.gnu.org/licenses/>."

author = "Ferit Tunçer"
email = "ferit.tuncer@autistici.org"
website = "https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller"

version = "2.1.0"

import sys
import urllib.request
import urllib.parse
import time
import os.path
import argparse
import re
import locale

#++ DEFAULTS
token_path = "pipeline.token"
default_encoding = locale.getpreferredencoding(False)
default_sentence_split_delimiter_class = "[\.\?:;!]"
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


def __readInput(path, encoding):
    try:
        with open(path, encoding=encoding) as input_file:
            full_text = ""
            for line in input_file:
                full_text += line
        r = re.compile(r'(?<=(?:{}))\s+'.format(default_sentence_split_delimiter_class))
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

def __getOutputPath(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, "output{0}".format(str(time.time()).split('.')[0]))
        return filepath
    except:
        raise

def __conditional_info(to_be_printed, quiet):
    if quiet == 0:
        print(to_be_printed)

def __parseArguments():
    arg_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="ITU Turkish NLP Pipeline Caller v{}\n{} <{}>\n{}".format(version, author, email, website),
    epilog="TOOLS: ner, morphanalyzer, isturkish,  morphgenerator, tokenizer, normalize, deasciifier, Vowelizer, DepParserFormal, DepParserNoisy, spellcheck, disambiguator, pipelineFormal, pipelineNoisy",
    add_help=True)
    arg_parser.add_argument("filename", help="relative input filepath")
    arg_parser.add_argument('-s', '--sentence-by-sentence', dest="sentence_by_sentence", action="store_true", help="process sentence by sentence instead of all at once")
    arg_parser.add_argument('-w', '--word-by-word', dest="word_by_word", action="store_true", help="process word by word instead of all at once")
    arg_parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", help="no info during process")
    arg_parser.add_argument("-t", "--tool", metavar="T", dest="tool", default="pipelineNoisy", help="pipeline tool name, \"pipelineNoisy\" by default")
    arg_parser.add_argument("-e", "--encoding", dest="encoding", metavar="E", default=default_encoding, help="force I/O to use given encoding, instead of default locale")
    arg_parser.add_argument("-o", "--output", metavar="O", dest="output_dir", default=default_output_dir, help="change output directory, \"{}\" by default".format(default_output_dir))
    arg_parser.add_argument('--version', action='version', version='{} {}'.format(name, version), help="version information")
    arg_parser.add_argument('--license', action='version', version='{}'.format(license), help="license information")

    return arg_parser.parse_args()

def main(args=None):
    if args is None:
        args = sys.argv[1:]
        
    args = __parseArguments()
    full_text, sentences, sentence_count = __readInput(args.filename, args.encoding)
    output_path = __getOutputPath(args.output_dir)
    token = __readToken()
    __conditional_info("[INFO] Pipeline tool: {}".format(args.tool), args.quiet)
    __conditional_info("[INFO] File I/O encoding: {}".format(args.encoding), args.quiet)
    __conditional_info("[INFO] Output destination: .{}{}".format(os.sep, output_path), args.quiet)
    start_time = time.time()

    caller = PipelineCaller()
    if args.sentence_by_sentence == 1:
        __conditional_info("[INFO] Processing sentence by sentence", args.quiet)
        with open(output_path, 'w', encoding=args.encoding) as output_file:
            for sentence in sentences:
                output_file.write("{0}\n".format(caller.call(args.tool, sentence, token)))
        print("[DONE] It took {0} seconds to process all {1} sentences.".format(str(time.time()-start_time).split('.')[0], sentence_count))

    if args.word_by_word == 1:
        __conditional_info("[INFO] Processing word by word", args.quiet)
        word_count = 0
        with open(output_path, 'w', encoding=args.encoding) as output_file:
            for sentence in sentences:
                for word in sentence.split():
                    output_file.write("{0}\n".format(caller.call(args.tool, word, token)))
                    word_count += 1
        print("[DONE] It took {0} seconds to process all {1} words.".format(str(time.time()-start_time).split('.')[0], word_count))


    else:
        __conditional_info("[INFO] Processing all the text at once", args.quiet)
        with open(output_path, 'w', encoding=args.encoding) as output_file:
            output_file.write("{0}\n".format(caller.call(args.tool, full_text, token)))
        print("[DONE] It took {0} seconds to process whole text.".format(str(time.time()-start_time).split('.')[0]))

if __name__ == '__main__':
    main()

