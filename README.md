# ITU Turkish NLP Pipeline Caller
 A tool for using ITU Turkish NLP Pipeline API <http://tools.nlp.itu.edu.tr/>
 

## Usage
To be able to use the pipeline, you need an authentication token(details on API web page).
The tool reads the token from `pipeline.token` file(under the same directory with the tool) by default.

`pipeline.caller.py filename`
reads input file <filename>, prints the output under `./script_output/output<%system_time>`

You can select the pipeline tool by using -t option
`pipeline.caller.py filename -t PipelineNoisy`
default is "PipelineFormal"

You can force the encoding for I/O by using -e option
`pipeline.caller.py filename -e UTF-8`
default is your system locale

And you can change the output directory by using -o option
`pipeline.caller.py filename -o another_directory`
default is "pipeline_caller_output"

##  Defaults

Check DEFAULTS block in the source code if you need to change one of these:

`api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"` 

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
