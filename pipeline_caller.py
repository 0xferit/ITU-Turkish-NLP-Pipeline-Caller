#!/usr/bin/python3
#-*- coding: utf-8 -*-

name = 'ITU Turkish NLP Pipeline Caller' 

__copyright__ = '__copyright__ 2015-2017 Ferit Tunçer'

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
email = 'ferit@lavabit.com'
website = 'https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller'

version = '3.0.0'

import argparse
import locale
import os
import re
import time

import urllib.parse
import urllib.request

TOKEN_PATH = "pipeline.token"
TOKEN_ENVVAR = "pipeline_token"
DEFAULT_ENCODING = locale.getpreferredencoding(False)
DEFAULT_OUTPUT_DIR = 'output'


class PipelineCaller(object):
    API_URL = 'http://tools.nlp.itu.edu.tr/SimpleApi'
    PIPELINE_ENCODING = 'UTF-8'

    DEFAULT_SENTENCE_SPLIT_DELIMITER_CLASS = '[\.\?:;!]'

    def __init__(self, tool='pipelineNoisy', text='example', token='invalid', processing_type='whole'):
        self.tool = tool
        self.text = text
        self.token = token
        self.processing_type = processing_type

    def call(self):

        if self.processing_type == 'whole':
            params = self.encode_parameters(self.text)
            return self.request(params)

        if self.processing_type == 'sentence':
            results = []
            self.parse_sentences()

            for sentence in self.sentences:
                params = self.encode_parameters(sentence)
                results.append(self.request(params))

            return "\n".join(results)

        if self.processing_type == 'word':
            results = []
            self.parse_words()

            for word in self.words:
                params = self.encode_parameters(word)
                results.append(self.request(params))

            return "\n".join(results)


    def parse_sentences(self):
        r = re.compile(r'(?<=(?:{}))\s+'.format(PipelineCaller.DEFAULT_SENTENCE_SPLIT_DELIMITER_CLASS))
        self.sentences = r.split(self.text)
        sentence_count = len(self.sentences)

        if re.match('^\s*$', self.sentences[sentence_count-1]):
            self.sentences.pop(sentence_count-1)

        self.sentence_count = len(self.sentences)

    def parse_words(self):
        self.parse_sentences()
        self.words = []

        for sentence in self.sentences:
            for word in sentence.split():
                self.words.append(word)

        self.word_count = len(self.words)

    def encode_parameters(self, text):
        return urllib.parse.urlencode({'tool': self.tool, 'input': text, 'token': self.token}).encode(self.PIPELINE_ENCODING)
    
    def request(self, params):
        response = urllib.request.urlopen(self.API_URL, params)
        return response.read().decode(self.PIPELINE_ENCODING)


def get_token(filename=TOKEN_PATH, envvar=TOKEN_ENVVAR):
    """
    Returns pipeline_token for API

    Tries local file first, then env variable
    """
    if os.path.isfile(filename):
        with open(filename) as token_file:
            token = token_file.readline().strip()

    else:
        token = os.environ.get(envvar)

        if not token:
            raise ValueError("No token found.\n"
                             "{} file doesn't exist.\n{} environment variable is not set.".format(filename, envvar))

    return token


def get_output_path(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, 'output{0:.0f}'.format(time.time()))
    return filepath


def conditional_info(to_be_printed, quiet):
    if quiet == 0:
        print(to_be_printed)


def parse_arguments():
    # epilog section is free now
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='ITU Turkish NLP Pipeline Caller v{}\n{} <{}>\n{}'.format(version, author, email, website),
        add_help=True
    )
    parser.add_argument('filename', help='relative input filepath')
    parser.add_argument('-p', '--processing-type', dest='processing_type', choices=['word', 'sentence', 'whole'], default='whole', help='Switches processing type, default is whole text at once. Alternatively, word by word or sentence by sentence processing can be selected.')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='no info during process')
    parser.add_argument('--tool', dest='tool', default='pipelineNoisy', choices=['ner', 'morphanalyzer', 'isturkish',  'morphgenerator', 'tokenizer', 'normalize', 'deasciifier', 'Vowelizer', 'DepParserFormal', 'DepParserNoisy', 'spellcheck', 'disambiguator', 'pipelineFormal', 'pipelineNoisy'], help='Switches pipeline tool which is \'pipelineNoisy\' by default')
    parser.add_argument('-e', '--encoding', dest='encoding', metavar='E', default=DEFAULT_ENCODING, help='force I/O to use given encoding, instead of default locale')
    parser.add_argument('-o', '--output', metavar='O', dest='output_dir', default=DEFAULT_OUTPUT_DIR, help='change output directory, \'{}\' by default'.format(DEFAULT_OUTPUT_DIR))
    parser.add_argument('--version', action='version', version='{} {}'.format(name, version), help='version information')
    parser.add_argument('--license', action='version', version='{}'.format(__license__), help='license information')

    return parser.parse_args()


def main():
    args = parse_arguments()

    with open(args.filename, encoding=args.encoding) as input_file:
        text = input_file.read()

    output_path = get_output_path(args.output_dir)
    token = get_token()
    conditional_info('[INFO] Pipeline tool: {}'.format(args.tool), args.quiet)
    conditional_info('[INFO] File I/O encoding: {}'.format(args.encoding), args.quiet)
    conditional_info('[INFO] Output destination: .{}{}'.format(os.sep, output_path), args.quiet)

    start_time = time.time()

    caller = PipelineCaller(args.tool, text, token, args.processing_type)
    with open(output_path, 'w', encoding=args.encoding) as output_file:
        output_file.write('{}\n'.format(caller.call()))

    process_time = time.time() - start_time

    print("[DONE] It took {0:.0f} seconds to process whole text.".format(process_time))


if __name__ == '__main__':
    main()

