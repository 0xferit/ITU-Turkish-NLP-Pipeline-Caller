Under construction...

# ITU-Turkish-NLP-Pipeline-Caller
 A tool for using ITU Turkish NLP Pipeline API <http://tools.nlp.itu.edu.tr/>

## Configuration
### Token
You must provide an authentication token given by ITU-NLP staff(please visit the web page of the pipeline). Next, you have to write it down into `pipeline.token` file by default, under the same path with the program. You can change token file name in the source code if you like.
## Usage
`pipeline.caller.py filename`
reads input file <filename>, prints the output under `./script_output/output<%system_time>`

