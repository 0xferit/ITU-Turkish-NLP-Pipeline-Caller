#!/usr/bin/python3
#-*- coding: utf-8 -*-

import pipeline_caller
import unittest
import os
import re
import sys


import subprocess




KATANA = 'Katana\'yı saklarız, dedi Ramiz, ben giderim bahçeye, tüm yeşil erikleri toplar gelirim, sonra da erikleri komşuya götürür, ondan Katana\'yı ele vermemesini isterim.'
KELIME = 'kelime kelime gönderelim bakalım'
UCDORT = '    Üç   -      dört      kız      başı      göründü      .          Gülüşüp      itişiyorlar      . '


class Test(unittest.TestCase):
    def module_Vowelizer_word_test(self):
        caller = pipeline_caller.PipelineCaller('Vowelizer', KELIME, os.environ['pipeline_token'], 'word')

        r = re.compile(r'(.+?\n)', re.MULTILINE)

        response = caller.call()

        print(response)
        assert len(re.findall(r, response)) == 4

    def module_pipelineNoisy_sentence_test(self):
        caller = pipeline_caller.PipelineCaller('pipelineNoisy', UCDORT, os.environ['pipeline_token'], 'sentence')

        r1 = re.compile(r'(1)(\t.+?){7,}', re.MULTILINE)
        r2 = re.compile(r'(5)(\t.+?){7,}', re.MULTILINE)

        response = caller.call()

        print(response)
        assert len(re.findall(r1, response)) == 2 and len(re.findall(r2, response)) == 1

    def module_pipelineNoisy_whole_test(self):
        caller = pipeline_caller.PipelineCaller('pipelineNoisy', KATANA, os.environ['pipeline_token'], 'whole')

        r = re.compile(r'(\d+)(\t.+?){7,}', re.MULTILINE)

        response = caller.call()

        print(response)
        assert len(re.findall(r, response)) == 29

    def tool_exception_test(self):
        exec (open('./pipeline_caller.py').read())

    def tool_noisy_test(self):
        #subprocess.Popen("python3 pipeline_caller.py katana.txt")
        script_path = "./pipeline_caller.py"
        subprocess.check_call([sys.executable or 'python3', script_path, "test_inputs/katana.txt"],
                       cwd=os.path.dirname(script_path))


if __name__ == '__main__':
    unittest.main()
