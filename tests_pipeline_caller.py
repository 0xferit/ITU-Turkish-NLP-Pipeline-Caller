#!/usr/bin/python3

import pipeline_caller
import unittest
import os
import re

class Test(unittest.TestCase):

    def module_exception_test(self):

        try:

            caller = pipeline_caller.PipelineCaller('pipelineNisy', 'test sentence', os.environ['pipeline_token'], 'whole')
            
            r = re.compile(r'(\d+)(\t.+?){7,}')
            
            response = caller.call()
            
            print(response)
            assert re.match(r, response)) != None
        except:
            self.fail('Exception thrown')
    
    def tool_exception_test(self):
        try:
            exec(open('./pipeline_caller.py').read())
        except:
            self.fail('Exception thrown')



if __name__ == '__main__':
    unittest.main()


