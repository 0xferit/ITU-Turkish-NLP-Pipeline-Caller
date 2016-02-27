#!/usr/bin/python3

name = 'ITU Turkish NLP Pipeline Caller'

__copyright__ = '__copyright__ 2015 Ferit Tunçer'

__license__ = 'GPLv2\n\
This program is free software; you can redistribute it and/or \
modify it under the terms of the GNU General Public license version 2 \
as published by the Free Software Foundation. \
This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public license for more details. \
You should have received a copy of the GNU General Public license \
along with this program.  If not, see <http://www.gnu.org/licenses/>.'

author = 'Ferit Tunçer'
email = 'ferit.tuncer@autistici.org'
website = 'https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller'

version = '3.0.0'

import sys
import urllib.request
import urllib.parse
import time
import os.path
import argparse
import re
import locale

TOKEN_PATH = 'pipeline.token'
DEFAULT_ENCODING = locale.getpreferredencoding(False)
DEFAULT_OUTPUT_DIR = 'output'

class PipelineCaller:

    API_URL = 'http://tools.nlp.itu.edu.tr/SimpleApi'
    PIPELINE_ENCODING = 'UTF-8'

    DEFAULT_SENTENCE_SPLIT_DELIMITER_CLASS = '[\.\?:;!]'


    def __init__(self, tool='pipelineNoisy', text ='example', token='invalid', processing_type='whole'):
        self.tool = tool
        self.text = text
        self.token = token
        self.processing_type = processing_type

    def call(self):

        if self.processing_type=='whole':
            params = self.encodeParams(self.tool, self.text, self.token)
            return self.request(params)

        if self.processing_type=='sentence':
            output = ''
            self.parseSentences()
            for sentence in self.sentences:
                params = self.encodeParams(self.tool, sentence, self.token)
                output += self.request(params) + '\n'
            return output

        if self.processing_type=='word':
            output = ''
            self.parseWords()
            for word in self.words:
                params = self.encodeParams(self.tool, word, self.token)
                output += self.request(params) + '\n'
            return output

    def parseSentences(self):
        r = re.compile(r'(?<=(?:{}))\s+'.format(PipelineCaller.DEFAULT_SENTENCE_SPLIT_DELIMITER_CLASS))
        self.sentences = r.split(self.text)
        sentence_count = len(self.sentences)
        if re.match('^\s*$', self.sentences[sentence_count-1]):
            self.sentences.pop(sentence_count-1)
        self.sentence_count = len(self.sentences)

    def parseWords(self):
        self.parseSentences()
        self.words = []
        for sentence in self.sentences:
            for word in sentence.split():
                self.words.append(word)
        self.word_count = len(self.words)

    def encodeParams(self, tool, text, token):
        return urllib.parse.urlencode({'tool': self.tool, 'input': text, 'token': self.token}).encode(self.PIPELINE_ENCODING)
    
    def request(self, params):
        try:
            response = urllib.request.urlopen(self.API_URL, params)
            return response.read().decode(self.PIPELINE_ENCODING)
        except:
            raise

def __readInput(path, encoding):
    try:
        with open(path, encoding=encoding) as input_file:
            text = ''
            for line in input_file:
                text += line
        return text
    except:
        raise

def __readToken():
    try:
        token_file = open(TOKEN_PATH)
        token = token_file.readline().strip()
        return token
    except:
        raise

def __getOutputPath(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, 'output{0}'.format(str(time.time()).split('.')[0]))
        return filepath
    except:
        raise

def __conditional_info(to_be_printed, quiet):
    if quiet == 0:
        print(to_be_printed)

def __parseArguments():
    #epilog section is free now
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='ITU Turkish NLP Pipeline Caller v{}\n{} <{}>\n{}'.format(version, __author__, email, website),
    add_help=True)
    parser.add_argument('filename', help='relative input filepath')
    parser.add_argument('-p', '--processing-type', dest='processing_type', choices=['word', 'sentence', 'whole'], default='whole', help='Switches processing type, default is whole text at once. Alternatively, word by word or sentence by sentence processing can be selected.')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='no info during process')
    parser.add_argument('--tool', dest='tool', default='pipelineNoisy', choices=['ner', 'morphanalyzer', 'isturkish',  'morphgenerator', 'tokenizer', 'normalize', 'deasciifier', 'Vowelizer', 'DepParserFormal', 'DepParserNoisy', 'spellcheck', 'disambiguator', 'pipelineFormal', 'pipelineNoisy'], help='Switches pipeline tool which is \'pipelineNoisy\' by default')
    parser.add_argument('-e', '--encoding', dest='encoding', metavar='E', default=DEFAULT_ENCODING, help='force I/O to use given encoding, instead of default locale')
    parser.add_argument('-o', '--output', metavar='O', dest='output_dir', default=DEFAULT_OUTPUT_DIR, help='change output directory, \'{}\' by default'.format(DEFAULT_OUTPUT_DIR))
    parser.add_argument('--version', action='version', version='{} {}'.format(name, version), help='version information')
    parser.add_argument('--license', action='version', version='{}'.format(__license__), help='license information')


    return parser.parse_args()

def main(args=None):
    if args is None:
        args = sys.argv[1:]
        
    args = __parseArguments()
    text = __readInput(args.filename, args.encoding)
    output_path = __getOutputPath(args.output_dir)
    token = __readToken()
    __conditional_info('[INFO] Pipeline tool: {}'.format(args.tool), args.quiet)
    __conditional_info('[INFO] File I/O encoding: {}'.format(args.encoding), args.quiet)
    __conditional_info('[INFO] Output destination: .{}{}'.format(os.sep, output_path), args.quiet)
    start_time = time.time()



    caller = PipelineCaller(args.tool, text, token, args.processing_type)
    with open(output_path, 'w', encoding=args.encoding) as output_file:
        output_file.write('{}\n'.format(caller.call()))
    
    if (args.tool == 'isturkish' or args.tool == 'Vowelizer') and args.processing_type != 'word':
        __conditional_info('[WARNING] ' +args.tool + ' accepts one word in a call, if you think the output is wrong, please try with `-p word` option.', args.quiet)
    
    if args.processing_type == 'whole':
        print('[DONE] It took {0} seconds to process whole text.'.format(str(time.time()-start_time).split('.')[0]))
    if args.processing_type == 'sentence':
        print('[DONE] It took {0} seconds to process whole text.'.format(str(time.time()-start_time).split('.')[0]))
    if args.processing_type == 'words':
        print('[DONE] It took {0} seconds to process whole text.'.format(str(time.time()-start_time).split('.')[0]))
    
    


if __name__ == '__main__':
    main()

