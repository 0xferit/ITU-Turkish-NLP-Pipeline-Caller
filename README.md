# ITU Turkish NLP Pipeline Caller
 A command-line tool for using [ITU Turkish NLP Pipeline API](http://tools.nlp.itu.edu.tr/)

For details of the pipeline, please check the pipeline page and the sources below.

[Gülşen Eryiğit . ITU Turkish NLP Web Service
In Proceedings of the Demonstrations at the 14th Conference
of the European Chapter of the Association for Computational Linguistics
(EACL 2014). Gothenburg, Sweden, April 2014.](http://web.itu.edu.tr/gulsenc/papers/itunlp.pdf)

[Gülşen Eryiğit, Joakim Nivre, and Kemal Oflazer. Dependency Parsing
of Turkish. Computational Linguistics, 34 no.3, 2008. ](http://www.mitpressjournals.org/doi/pdf/10.1162/coli.2008.07-017-R1-06-83)

## Usage
To be able to use the pipeline, you need an authentication token(details on API web page).
The tool reads the token from `pipeline.token` file(under the same directory with the tool) by default.

`pipeline.caller.py filename`
reads input file <filename>, prints the output under `./pipeline_caller_output/output<%system_time>`

You can select the pipeline tool by using -t option
`pipeline.caller.py filename -t pipelineFormal`
default is "pipelineNoisy"

You can force the encoding for I/O by using -e option
`pipeline.caller.py filename -e UTF-8`
default is your system locale

And you can change the output directory by using -o option
`pipeline.caller.py filename -o another_directory`
default is "pipeline_caller_output"

##  Defaults

Check DEFAULTS block in the source code if you need to change one of these:

`api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"` 

`pipeline_encoding = 'UTF-8'`

`token_path = "pipeline.token"`

## Author, Copyright & License

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
