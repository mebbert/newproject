#!/usr/bin/env python
import argparse
import re

class RegexValidator(object): 
	""" 
	Performs regular expression match on value. 
	If match fails an ArgumentError is raised 
	""" 

	def __init__(self, pattern, statement=None): 
		self.pattern = re.compile(pattern) 
		self.statement = statement 
		if not self.statement: 
			self.statement = "must match pattern %s" % self.pattern 

	def __call__(self, string): 
		match = self.pattern.search(string) 
		if not match: 
			raise argparse.ArgumentError(None, self.statement)
		return string 

def create_options_parser():

	inputRV = RegexValidator("^((\w+)=)?[a-zA-Z0-9,\.'()_\s-]+\.*[a-zA-Z0-9,\s-]*$",
			"""Input files must conform to \'<fId>=<filename>\' or just \'<filename>\', where \'<fId>\' is a
			new name for the input file to be used in \'--set-operation\'. See \'help\' for
			details.""")
	parser = argparse.ArgumentParser(
			description='Compare variants across individuals')
	parser.add_argument('-i','--input',
			type=inputRV,
			help="""Specify a VCF input file. Can be used repeatedly. The input file can be named for use
			in --set-operation as follows \'--input <fId>=<input.vcf>\', where \'<fId>\' is the new name. If
			the name is excluded, input
			files will be named \'<f1>\', \'<f2>\', etc. by default. The new name may only consist of letter,
			digits, and underscores.""")
	parser.add_argument('-p','--pinput',
			type=inputRV,
			help="""Specify root file name for plink input (e.g. \'myplink\' will expect \'myplink.ped\'
			and \'myplink.map\'). Can be used repeatedly. These input files may also be named (see
			--input).""")
	parser.add_argument('-b','--binput',
			type=inputRV,
			help="""Specify root file name for binary plink input (e.g. \'myplink\' will expect
			\'myplink.bed\', \'myplink.fam\', and \'myplink.bim\'). Can be used repeatedly. These input
			files may also be named (see --input).""")
	parser.add_argument('-s','--set-operation',
			type=RegexValidator("^((\w+)=)?[iIuUcC]\[(\w+(:\w+)?)(,\w+(:\w+)?)*\]$",
			"""Set operations must conform to <name>=<operation>(<input_name>:<sample_id>,<input_name>:<sample_id>,etc.),
			where \'<name>\' is a user provided name of the operation that can be reused in other operations,
			\'<operation>\' may be any of union ([uU]), intersect ([iI]), and complement ([cC]), \'<input_name>\' is 
			a user-provided file input name (see --input in \'help\'), and \'<sample_id>\' is a sample id within an input
			file. Here is an example intersect on two unions:
			\'-s out1=u(fId1:sId1,fId1:sId2,fId2:sId3) -s out2=u(fId3:sId4,fId3:sId5) -s out3=i(out1,out2)\'."""),
			help="""Specify a set operation between one or more input files. Set operations are formatted as
			follows: <name>=<operation>(<input_name>:<sample_id>,<input_name>:<sample_id>,etc.), where \'<name>\' is a
			user provided name of the operation (can be referenced in other operations),
			\'<operation>\' may be any of union ([uU]), intersect ([iI]), and complement ([cC]), \'<input_name>\' is 
			a user-provided file input name (see --input), and \'<sample_id>\' is a sample id within an input
			file. If only file input names (\'<input_name>\') are provided in the operation, all samples within those
			files will be used.
			Here is an example intersect on two unions:
			\'-s out1=u(fId1:sId1,fId1:sId2,fId2:sId3) -s out2=u(fId3:sId4,fId3:sId5) -s out3=i(out1,out2)\'.
			An \'fId\' refers to a named file (see --input) and an \'sId\' refers to a sample within that file.""")
	parser.add_argument('-o','--outfile',
			help="""Specify the final output file name (default = variant_list.vcf).""")
	parser.add_argument('-t','--intermediate-files',action="store_true",
			help="""Print intermediate files such as when performing multiple set operations (default
			= false).""")

	return parser

def main():
	#parse command line args
	parser = create_options_parser()
	args = parser.parse_args()

if __name__ == '__main__': main()
