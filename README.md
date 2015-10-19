Under construction...

# ITU Turkish NLP Pipeline Caller
 A tool for using ITU Turkish NLP Pipeline API <http://tools.nlp.itu.edu.tr/>

## Usage
To be able to use the pipeline, you need an authentication token(details on API web page).
The tool reads the token from `pipeline.token` file(under the same directory with the tool) by default.

`pipeline.caller.py filename`
reads input file <filename>, prints the output under `./script_output/output<%system_time>`

and you can select the pipeline tool by using 
`pipeline.caller.py filename -t PipelineNoisy`
-t option, default is PipelineFormal

### Other Optional Configurations and Defaults
`++ Configuration block - EDIT HERE` part in the source code.

`api_url = "http://tools.nlp.itu.edu.tr/SimpleApi"` in case the API url changes:

`output_dir = "script_output"` you can change the output directory if you want

`encoding_code = "WINDOWS-1254"` and the file encoding for reading input and writing output
