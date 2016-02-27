#!/usr/bin/python3

import pipeline_caller
import unittest
import os
import re

KATANA = 'Katana\'yı saklarız, dedi Ramiz, ben giderim bahçeye, tüm yeşil erikleri toplar gelirim, sonra da erikleri komşuya götürür, ondan Katana\'yı ele vermemesini isterim.'

class Test(unittest.TestCase):

    def module_pipelineNoisy_test(self):

        try:

            caller = pipeline_caller.PipelineCaller('pipelineNoisy', KATANA, os.environ['pipeline_token'], 'whole')
            
            r = re.compile(r'(\d+)(\t.+?){7,}', re.MULTILINE)
            
            response = caller.call()
            
            print(response)
            assert len(re.findall(r, response)) == 29
        except:
            self.fail('Exception thrown')
    

            
    def tool_exception_test(self):
        try:
            exec(open('./pipeline_caller.py').read())
        except:
            self.fail('Exception thrown')



if __name__ == '__main__':
    unittest.main()


