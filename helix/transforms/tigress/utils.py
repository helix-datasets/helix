import os
import re

from zipfile import ZipFile, ZipInfo


def extract_fnames(src):
    """Extracts function names out of function definitions on C source code.

    Args:
        src (str): C source code as a string.

    Returns:
        List of function names.

    RegEx patterns explained:
        //.*\n?                     : matches code formatted as single-line comments
        /*.*?*//n?                  : matches code formatted as multi-line comments
        char|signed char|...        : matches return types
        ( |\n)(*)( |\n)             : considers functions returning pointers
        [a-zA-Z_]+[a-zA-Z0-9_]*     : matches the function name
         ?                          : matches 0 or 1 whitespace
        ([^;]*?)                    : matches parameters inside parentheses
         ?                          : matches 0 or 1 whitespace
        ?:{|\n{                     : matches the start of the body of the function definition
    """

    singleline_pattern = r"\/\/.*\n?"
    multiline_pattern = r"\/\*.*?\*\/\n?"

    regex_singleline = re.compile(singleline_pattern)
    regex_multiline = re.compile(multiline_pattern, re.DOTALL)

    src = re.sub(regex_singleline, "", src)
    src = re.sub(regex_multiline, "", src)

    pattern = r"""(?:char|signed char|unsigned char|short|short int|signed short|signed short int|
    unsigned short|unsigned short int|int|signed|signed int|unsigned|unsigned int|long|long int|
    signed long|signed long int|unsigned long|unsigned long int|long long|long long int|
    signed long long|signed long long int|unsigned long long|unsigned long long int|float|double|
    long double|void|bool)(?: |\n)(?:\*)?(?: |\n)?([a-zA-Z_]+\w*) ?(?:\([^;]*?\)) ?(?:\{|\n\{)"""
    return re.findall(pattern, src)


class CustomZipFile(ZipFile):
    """Overriding ``_extract_member`` method to handle file permissions.

    This allows to take advantage of ZipInfo.external_attr that returns external
    file information in the form of 4 bytes. The high order two bytes represent
    file type bits and UNIX permission.

    Source: https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries
    """

    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)
        mode = member.external_attr >> 16

        if mode != 0:
            os.chmod(targetpath, mode)

        return targetpath
