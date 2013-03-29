#!/usr/bin/env python
import re
from collections import OrderedDict


class InputFiles(object):

    def __init__(self, args, prefix):
        self.parse(args, prefix)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self.files = ""
        self.count = 0
        for i, v in self.inputFiles.items():
            if self.count == 0:
                self.files += i + "=" + str(v)
            else:
                self.files += ", " + i + "=" + str(v)

            self.count += 1

        return self.files

    def parse(self, args, prefix):

        """
        Create an ordered dictionary using the user-defined file input name
        as the key and the actual file name as the value.
        :param args:
        :param prefix:
        :raise:
        """

        self.inputFiles = OrderedDict()
        for i, v in enumerate(args):
            info = v.split('=')

            # if len(v) == 1, user did not specify name
            if len(info) == 1:
                self.file_name = info[0]
                self.file_id = prefix + i
                self.inputFiles[self.file_id] = self.file_name

            elif len(info) > 2:
                raise InputFileParamError('Unexpected input file parameter: ' + info)

            else:
                self.file_id = info[0]
                self.file_name = info[1]
                self.inputFiles[self.file_id] = self.file_name


class OperationList(object):

    def __init__(self):
        self.operationList = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ''.join(self.operationList.__str__())

    def append(self, operation):
        self.operationList.append(operation)


class SetOperation(object):

    def __init__(self, count, operation):
        self.parse(count, operation)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.oper_id + "=" + self.operator + "[" +\
            str(self.print_file_samples()) + "]"

    def parse(self, count, operation):
        info = operation.split('=')

        if len(info) == 1:
            self.oper_id = 's' + str(count)
            self.operIndex = 0

        elif len(info) > 2:
            raise InputFileParamError('Unexpected input file parameter: ' + operation)

        else:
            self.oper_id = info[0]
            self.operIndex = 1

        # Get first character and everything in the main brackets
        self.match = re.search("^(\w)\[(.+)\]$", info[self.operIndex])

        matches = self.match.groups()
        self.operator = matches[0]

        self.file_sample_list = matches[1].split(":")
        self.file_and_samples_dict = OrderedDict()

        # For each input, get the specified samples
        for i in self.file_sample_list:
            self.extracted = re.match("^(\w+)(\[(.+)\])*$", i).groups()
            self.input_id = self.extracted[0]
            self.sample_list = self.extracted[2]

            if self.input_id == self.oper_id:
                raise InputFileParamError('The operation cannot be used in its own definition: ' + operation)

            # If user specified samples
            if self.sample_list is not None:
                self.samples = self.sample_list.split(",")

            # User did not specify samples (use all)
            else:
                self.samples = "All"

            self.file_and_samples_dict[self.input_id] = self.samples

    def print_file_samples(self):
        self.samples = ""
        self.count = 0
        for i, v in self.file_and_samples_dict.items():
            if self.count == 0:
                self.samples += i + str(v)
            else:
                self.samples += ":" + i + str(v)

            self.count += 1

        return self.samples



class InputFileParamError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
