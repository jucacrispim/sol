# -*- coding: utf-8 -*-

# This module parses the contents of .slang files and returns
# a dictionary with a dialog configuration

from pyparsing import (
    CaselessLiteral,
    OneOrMore,
    Word,
    alphas,
    alphanums,
    ParseException,
    Literal
)

from .utils import logger


msg = OneOrMore(Word(alphas + alphanums + '{},!?.:')).setResultsName('msg')


class LineParser:

    label = None
    pattern = None

    def __call__(self, line):
        r = self.parse(line)
        logger.debug('line {} parsed with {}'.format(
            line, type(self).__name__))

        return r

    def parse(self, line):
        raise NotImplementedError


class SayParser(LineParser):

    label = 'say'
    pattern = CaselessLiteral('diga') + msg

    def parse(self, line):
        info = self.pattern.parseString(line)
        return (self.label, ' '.join(info.msg))


class AskParser(LineParser):

    label = 'ask'
    pattern = Word(alphas).setResultsName('var') + Literal('=') + \
        CaselessLiteral('pergunte') + msg

    def parse(self, line):
        info = self.pattern.parseString(line)
        return (self.label, ' '.join(info.msg), info.var)


parsers = [
    SayParser(),
    AskParser()
]


def parse_slang(slang):
    dialog = []
    for l in slang.splitlines():
        if l.startswith('#'):
            continue
        line_parsed = False
        for parser in parsers:
            try:
                dialog.append(parser(l))
            except ParseException:
                continue
            else:
                line_parsed = True
                break
        if not line_parsed:
            logger.warning('Line {} could not be parsed'.format(l))

    return dialog
