# ITU Turkish NLP Pipeline Caller 
[![Build Status](https://travis-ci.org/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller.svg?branch=master)](https://travis-ci.org/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller) [![PyPI version](https://badge.fury.io/py/ITU-Turkish-NLP-Pipeline-Caller.svg)](https://badge.fury.io/py/ITU-Turkish-NLP-Pipeline-Caller) [![Join the chat at https://gitter.im/freecodecamp/freecodecamp](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller)   [![Codacy Badge](https://api.codacy.com/project/badge/grade/6368b6f3c39d4199b2ed162b79944a27)](https://www.codacy.com/app/ferit-tuncer/ITU-Turkish-NLP-Pipeline-Caller)

<a target='_blank' rel='nofollow' href='https://app.codesponsor.io/link/Pg82rgFKnc4g5VxAT8KqaP8d/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller'>
  <img alt='Sponsor' width='888' height='68' src='https://app.codesponsor.io/embed/Pg82rgFKnc4g5VxAT8KqaP8d/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller.svg' />
</a>

 A Python3 wrapper tool to help using [ITU Turkish NLP Pipeline API](http://tools.nlp.itu.edu.tr/)



For details of the pipeline, please check the pipeline page and the sources below.

[Eryigit, Gülsen. "ITU Turkish NLP Web Service." EACL. 2014.](http://web.itu.edu.tr/gulsenc/papers/itunlp.pdf)

[Gülşen Eryiğit, Joakim Nivre, and Kemal Oflazer. Dependency Parsing 
of Turkish. Computational Linguistics, 34 no.3, 2008.](http://www.mitpressjournals.org/doi/pdf/10.1162/coli.2008.07-017-R1-06-83)

## Usage
To be able to use the pipeline, you need an **authentication token** (details on [API web page](http://tools.nlp.itu.edu.tr/)).

If you experience any problem please contact with me via email (see author section), or preferably via the [gitter chat room](https://gitter.im/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller).
### Setup
#### Recommended way
Using [PyPI](https://pypi.python.org/pypi) just run `pip3 install ITU-Turkish-NLP-Pipeline-Caller`

#### Alternative way
Download the latest [release](https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller/releases), extract the archive and inside that directory simply run `python3 ./setup.py install` to install.

### As a Command Line Tool
The tool reads the token from `pipeline.token` file (under the same directory with the tool) by default.

Simply
`pipeline_caller <filename>`
reads the input file, prints the output under `./output/output<system_time>`

You can select the pipeline tool by using `-t` option
`pipeline_caller <filename> --tool <tool_name>`
default is "pipelineNoisy"

You can force the encoding for I/O by using `-e` option
`pipeline_caller <filename> -e <encoding>`
default is your system locale

You can switch processing type using `-p` option. Input text can be processed whole at once, sentence by sentence or word by word. For some tools (`isturkish` for example) in the Pipeline, word by word processing is necessary at the moment. Default type is whole at once.
Example: `pipeline_caller <filename> --tool isturkish -p word` sends input text to `isturkish` tool, word by word.

And you can change the output directory by using `-o` option
`pipeline_caller <filename> -o <another_directory>`
default is "output"

Also `pipeline_caller --help` shows the help menu.
### Using As a Module

`import pipeline_caller`

`caller = pipeline_caller.PipelineCaller()`

`result = caller.call(<tool_name>, <text>, <api_token>)`

##  Defaults (Optional)

Check DEFAULTS block in the source code if you need (generally, you don't) to change one of these:

`api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"` 

`pipeline_encoding = 'UTF-8'`

`token_path = "pipeline.token"` for command line tool

`default_output_dir = "output"`

`default_enconding = locale.getpreferredencoding(False)` default encoding in your OS, for I/O operations in command line tool

`default_sentence_split_delimiter_class = "[\.\?:;!]"` for command line tool, to separate sentences and process sentence by sentence
## Special Thanks
Special thanks to [Asst. Prof. Dr. Peter Schüller](https://github.com/peschue) for his great suggestions!

## Author, Copyright & License
This work is a part of a [KnowLP](http://www.knowlp.com) research project.

Copyright 2015-2017 Ferit Tunçer, <ferit@lavabit.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License version 2
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


