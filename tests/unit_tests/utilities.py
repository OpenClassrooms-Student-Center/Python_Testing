import inspect
import logging

def disp_log(response, assert_code):
	func_name = inspect.currentframe().f_back.f_code.co_name
	if response == assert_code:
		return logging.info(f'\n{func_name} => assert value = {assert_code} : PASSED')
	