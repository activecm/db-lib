#!/usr/bin/env python3
"""Import pipe-separated key-value pairs and merge into the database specified on the command line."""

__version__ = '0.2.1'

__author__ = 'William Stearns'
__copyright__ = 'Copyright 2022, William Stearns'
__credits__ = ['William Stearns']
__email__ = 'william.l.stearns@gmail.com'
__license__ = 'GPL 3.0'
__maintainer__ = 'William Stearns'
__status__ = 'Production'				#Prototype, Development or Production

# pylint: disable=bad-indentation

import argparse
import json
import sys

import db_lib


default_max_adds = 100

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='merge_into_db version ' + str(__version__))
	parser.add_argument('-w', '--write', help='Database to write the records to', required=True, default='')
	parser.add_argument('-m', '--max', help='Maximum entries to write at a time', type=int, required=False, default=default_max_adds)
	(parsed, unparsed) = parser.parse_known_args()
	cl_args = vars(parsed)

	kv_list = []
	for one_line in sys.stdin:
		key, value = one_line.rstrip('\r\n').split('|', 1)
		val_list = json.loads(value)
		#print(key + '\t' + str(val_list) + '\t' + str(type(key)) + '\t' + str(len(val_list)))

		#This block submits key/val_list pairs to buffer_merges, which takes care of buffering for us
		db_lib.buffer_merges(cl_args['write'], key, val_list, cl_args['max'])

	#Flush out any remaining entries
	db_lib.buffer_merges("", "", [], 0)
