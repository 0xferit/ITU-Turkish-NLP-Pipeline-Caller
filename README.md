# ITU Turkish NLP Pipeline Caller [![Build Status](https://travis-ci.org/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller.svg?branch=master)](https://travis-ci.org/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller) [![Join the chat at https://gitter.im/freecodecamp/freecodecamp](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller)
 A Python3 wrapper tool to use [ITU Turkish NLP Pipeline API](http://tools.nlp.itu.edu.tr/)


For details of the pipeline, please check the pipeline page and the sources below.

[Eryigit, Gülsen. "ITU Turkish NLP Web Service." EACL. 2014.](http://web.itu.edu.tr/gulsenc/papers/itunlp.pdf)

[Gülşen Eryiğit, Joakim Nivre, and Kemal Oflazer. Dependency Parsing 
of Turkish. Computational Linguistics, 34 no.3, 2008.](http://www.mitpressjournals.org/doi/pdf/10.1162/coli.2008.07-017-R1-06-83)

## Usage
To be able to use the pipeline, you need an **authentication token** (details on API web page).
### Setup
Download the latest release, extract the archive and inside that directory simply run `python3 ./setup.py install` to install.
### As a Command Line Tool
The tool reads the token from `pipeline.token` file (under the same directory with the tool) by default.

Simply
`pipeline.caller.py <filename>`
reads the input file, prints the output under `./output/output<system_time>`

You can select the pipeline tool by using `-t` option
`pipeline.caller.py <filename> -t <tool_name>`
default is "pipelineNoisy"

You can force the encoding for I/O by using `-e` option
`pipeline.caller.py <filename> -e <encoding>`
default is your system locale

And you can change the output directory by using `-o` option
`pipeline.caller.py <filename> -o <another_directory>`
default is "output"

Also `pipeline.caller.py --help` shows the help menu.
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

`default_separator_char_class = "[\.\?:;!]"` for command line tool, to separate sentences and process sentence by sentence
## Special Thanks
Special thanks to [Asst. Prof. Dr. Peter Schüller](https://github.com/peschue) for his great suggestions!

## Author, Copyright & License
This work is a part of a [KnowLP](http://www.knowlp.com) research project.

Copyright 2015 Ferit Tunçer, <ferit.tuncer@autistici.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License version 2
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
