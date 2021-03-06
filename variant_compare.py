#!/usr/bin/env python
import argparse
import re
import sys

import param_structures
import plinkToVCFParser


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

    exampleOper = "Here is an example intersect on two unions:\n" +\
        "\'-s out1=u[fId1[sId1,sId2]:fId2[sId3]]\n" +\
        "out2=u[fId3[sId4,sId5]:fId4[sId6]] out3=i[out1,out2]\'."
    operFormat = "<oper_id>=<operator>[<input_id1>[<sample_id1>,<sample_id2>,etc.]:<input_id2>[<sample_id3>," +\
                 "<sample_id4>,etc.]:etc.]\n"
    operDesc = "where \'<oper_id>\' is a user provided ID of the operation\n" +\
        "(can be referenced in other operations), \'<operator>\'\n" +\
        "may be any of union ([uU]), intersect ([iI]), and\n" +\
        "complement ([cC]), \'<input_id>\' is a user-provided\n" +\
        "file input ID (see --input), and \'<sample_id>\' is a\n" +\
        "sample ID within an input file."
    inputRV = RegexValidator(
        "^((\w+)=)?([a-zA-Z0-9,\.'()_\s-]+\.*[a-zA-Z0-9,\s-]*)$",
        """Input files must conform to \'<fId>=<filename>\' or just
        \'<filename>\', where \'<fId>\' is a new ID for the input file to be
        used in \'--set-operation\'. See \'help\' for details.""")
    operatorRV = RegexValidator(
        "^((\w+)=)?[iIuUcC]\[(\w+(\[\w+(,\w+)*\])?)(:\w+(\[\w+(,\w+)*\])?)*\]$",
        "\nSet operations must conform to \n" + operFormat + operDesc + "\n" + exampleOper)

    parser = argparse.ArgumentParser(
        description='Compare variants across individuals',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-i', '--input', dest='VCF', nargs='+',
                        type=inputRV,
                        help="""Specify a VCF input file. Multiple files may be
                        specified at once. An ID may be provided for the input file
                        for use in --set-operation as follows \'--input
                        <fId>=<input.vcf> <fId2>=<input2.vcf>\', where
                        \'<fId>\' and \'<fId2>\' are the new IDs. If IDs
                        are excluded, IDs will be assigned as \'<i0>\',
                        \'<i1>\', etc. by default. The new ID may only
                        consist of letter, digits, and underscores.""")
    parser.add_argument('-p', '--pinput', dest='plink', nargs='+',
                        type=inputRV,
                        help="""Specify root file name for plink input (e.g.
                        \'myplink\' will expect \'myplink.ped\'
                        and \'myplink.map\'). Can be used repeatedly. IDs may also
                        be provided for plink input files (see
                        --input). If IDs are excluded, plink input files will
                        be given IDs as \'<p0>\', \'<p1>\', etc.""")
    parser.add_argument('-b', '--binput', dest='binary', nargs='+',
                        type=inputRV,
                        help="""Specify root file name for binary plink input
                        (e.g. \'myplink\' will expect \'myplink.bed\',
                        \'myplink.fam\', and \'smyplink.bim\').
                        Can be used repeatedly. IDs may also be provided for binary plink
                        input files IDs (see --input). If IDs are excluded, binary
                        plink input files will be given IDs as \'<b0>\', \'<b1>\',
                        etc.""")
    group.add_argument('-s', '--set-operation', dest='operation', nargs='+',
                       type=operatorRV,
                       help="""Specify a set operation between one or more
                        input files. Set operations are formatted as follows: """ +
                       operFormat + operDesc +
                       """ If only file IDs (i.e. \'<fId>\') are
                        provided in the operation, all samples within those
                        files will be used. If operation IDs (i.e. <oper_id>) are excluded, set
                        operations will be given IDs as \'<s0>\', \'<s1>\',
                        etc. """ + exampleOper + """An \'fId\' refers to a
                       file ID (see --input) and an \'sId\' refers to a
                       sample within that file.""")
    group.add_argument('-a', '--association', dest="phenotype_file",
                       help="""Perform an association study between phenotypes...""")
    parser.add_argument('-o', '--outfile', default="variant_list.vcf",
                        help="""Specify the final output file name.""")
    parser.add_argument('-I', '--intermediate-files', action="store_true",
                        help="""Print intermediate files such as when
                            performing multiple set operations. Intermediate
                            files will be named according to the --set-operation
                            IDs (e.g. \'out0.vcf\', \'out1.vcf\', etc.)""",)
    parser.add_argument('-k', '--keep-homozygotes', action="store_true",
                        help="""List homozygotes in output when both hetero-
                        and homozygotes are present for the same variant.""")

    return parser


def main():
    #parse command line args
    parser = create_options_parser()

    # Print help and exit if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    print args

    # Handle input files
    variant_sets = parse_input_files(args.VCF, args.plink, args.binary)

    print variant_sets;

    """nameToRecords = {};
    #	if (args.VCF is not None):
    #		associate each VCF file name with the list
    #		of records contained in the file
    if args.plink is not None:
        for input in plinkInputs:
            name = input.userFileName;
            fileName = input.fileName;
            records = plinkToVCFParser.doParse(fileName, False);
            nameToRecords[name] = records;
    if args.binary is not None:
        for input in binInputs:
            name = input.userFileName;
            fileName = input.fileName;
            records = plinkToVCFParser.doParse(fileName, True);
            nameToRecords[name] = records;
    print(str(nameToRecords));"""

    try:
        # Handle set operations
        operations = parse_operations(args.operation, variant_sets)
        print operations
    except param_structures.InputFileParamError as e:
        print >> sys.stderr, e.value
        exit(1)


def parse_input_files(vcf_args, plink_args, bin_args):
    variantSets = set()
    if vcf_args is not None:
        prefix = 'i'
        vcfInputs = param_structures.InputFiles(vcf_args, prefix)
        variantSets.update(vcfInputs.inputFiles.keys())

    if plink_args is not None:
        prefix = 'p'
        plinkInputs = param_structures.InputFiles(plink_args, prefix)
        variantSets.update(plinkInputs.inputFiles)

    if bin_args is not None:
        prefix = 'b'
        binInputs = param_structures.InputFiles(bin_args, prefix)
        variantSets.update(binInputs.inputFiles)

    return variantSets


def parse_operations(oper_args, variant_sets):

    operations = param_structures.OperationList()
    if oper_args is not None:
        invalidInputNames = set()
        for i, v in enumerate(oper_args):
            op = param_structures.SetOperation(i, v)
            operations.append(op)
            variant_sets.add(op.oper_id)

            # Test if input file names used in operation exist
            # in the input file parameters
            invalidInputNames.update(set(op.file_and_samples_dict) - variant_sets)

        if len(invalidInputNames) > 0:
            invalidStr = ", ".join(sorted(list(invalidInputNames)))
            raise param_structures.InputFileParamError("The following file input or operation ID(s) is/are not"
                    + " recognized: \'" + invalidStr + "\'. They must be defined in either an input or previous set"
                    + " operation parameter. See '--input' for details.")

    return operations


if __name__ == '__main__':
    main()
