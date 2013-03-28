#!/usr/bin/env python

import vcf

class PerformOperations(object):
    """
    This class performs operations on files/datasets
    """




    # Creates three critical variables: datasets (in this case are files, in subsequent sets can be files or
    # datasets resulting from previous operations, and opsPerformed, a variable that stores a list of all the
    # operations performed
    def __init__(self, file1, file2):
        self.data1 = file1
        self.data2 = file2
        self.opsPerformed = ""

    def __str__(self):
        return "PerformOperations:\n\tData 1: " + self.data1 + "\n\t Data 2: " + self.data2 +\
            "\n\t Operations Performed: " + self.opsPerformed

