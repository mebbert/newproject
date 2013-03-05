import unittest
import doctest
import argparse
import re

import variantCompare


class TestParameters(unittest.TestCase):

	##########################
	# Test --input parameter #
	##########################
	def test_input_operation_parameter(self):
		parser = variantCompare.create_options_parser()

		###############
		# Should pass #
		###############
		try:
			# Named file with extension
			inargs = "-i f1=File.txt"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Named file without extension
			inargs = "-i f1=File"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		# Can't get this one to work
		#try:
			# Named file with space
			#inargs = "-i f1=File\ No.txt"
			#print inargs
			#patt = "(?<!\\\)\s"
			#args = parser.parse_args(re.split(pattern=patt,string=inargs,maxsplit=1,flags=re.DEBUG))
		#except:
			#print re.split(patt,inargs,maxsplit=1)
			#self.fail("Failed on: " + inargs)

		try:
			# Named file with parenthese
			inargs = "-i f1=FileNo(2).txt"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Named file with multiple periods
			inargs = "-i f1=FileNo.2a.txt"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Named file with comma
			inargs = "-i f1=FileNo,2a.txt"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)
	
		try:
			# Named file with all of the above except space
			inargs = "-i f1=FileNo(2a.).txt"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Unamed file
			inargs = "-i File.txt"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Unamed file without extension
			inargs = "-i File"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		#############################
		# Should fail, so pass them #
		#############################
		try:
			# No file
			inargs = "-i out="
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)



	##################################
	# Test --set-operation parameter #
	##################################
	def test_set_operation_parameter(self):
		parser = variantCompare.create_options_parser()

		###############
		# Should pass #
		###############
		try:
			# One sample and complete file
			inargs = "-s out1=i[one:id1,two]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# One complete file
			inargs = "-s out=i[one]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Two complete files
			inargs = "-s out=i[one,two]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Two samples
			inargs = "-s out=I[one:id1,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Three samples. Capital 'I'
			inargs = "-s out=I[one:id1,two:id2,f3:id98]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Two samples and a complete file
			inargs = "-s out=I[one:id1,two:id2,f3]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Check union operator
			inargs = "-s out=u[one:id1,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Check capital union operator
			inargs = "-s out=U[one:id1,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Check complement operator
			inargs = "-s out=c[one:id1,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Check capital complement operator
			inargs = "-s out=C[one:id1,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		try:
			# Check no operator name
			inargs = "-s U[one:id1,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.fail("Failed on: " + inargs)

		#############################
		# Should fail, so pass them #
		#############################
		try:
			# Ending comma
			inargs = "-s out=i[one:id1,]"
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)
		try:
			# Ending colon
			inargs = "-s out=i[one:id1,two:]"
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)
		try:
			# Leading colon
			inargs = "-s out=i[one:id1,:two]"
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)
		try:
			# Leading comma
			inargs = "-s out=C[,two:id2]"
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)
		try:
			# empty operation
			inargs = "-s out=C[]"
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)
		try:
			# Extra characters
			inargs = "-s out=C[one:id1,two:id2]sas"
			args = parser.parse_args(inargs.split())
		except:
			self.assertRaises(argparse.ArgumentError)

if __name__ == '__main__':
	unittest.main()
