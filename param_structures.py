#!/usr/bin/env python
import re


class InputFileInfo(object):

    def __init__(self, count, fileinfo, prefix):
        self.parse(count, fileinfo, prefix)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.userFileName + '=' + self.fileName

    def parse(self, count, fileinfo, prefix):
        info = fileinfo.split('=')

        # if len(info) == 1, user did not specify name
        if (len(info) == 1):
            self.fileName = info[0]
            self.userFileName = prefix + count

        elif (len(info) > 2):
            raise InputFileParamError('Unexpected input file parameter: ', fileinfo)

        else:
            self.userFileName = info[0]
            self.fileName = info[1]


class SetOperation(object):

    def __init__(self, count, operation):
        self.parse(count, operation)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        None

    def parse(self, count, operation):
        info = operation.split('=')

        if (len(info) == 1):
            self.operName = 's' + str(count)
            self.operIndex = 0

        elif (len(info) > 2):
            raise InputFileParamError('Unexpected input file parameter: ', operation)

        else:
            self.operName = info[0]
            self.operIndex = 1

        self.operator = re.match("\d", info[self.operIndex])  # take the first character


class InputFileParamError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
