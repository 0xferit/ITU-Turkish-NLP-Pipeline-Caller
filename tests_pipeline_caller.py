#!/usr/bin/python3

import pipeline_caller
import unittest
import nose.tools


class Test(unittest.TestCase):

	def __caller_exception_test():
		try:
			caller = pipeline_caller.PipelineCaller()
			caller.call("pipelineNoisy", "test sentence", "random token")
		except:
			self.fail("Exception thrown")

if __name__ == '__main__':
    unittest.main()


