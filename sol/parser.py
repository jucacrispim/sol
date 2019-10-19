# -*- coding: utf-8 -*-

# This module parses the contents of .slang files and returns
# a dictionary with a dialog configuration

from collections import defaultdict

from pyparsing import (
    CaselessLiteral,
    OneOrMore,
    Word,
    alphas,
    alphanums,
    ParseException
)


say_kw = CaselessLiteral('diga')
ask_kw = CaselessLiteral('pergunte')

say = say_kw + OneOrMore(
    Word(alphas, alphanums + ',!?.:')).setResultsName('msg')


def parse_slang(slang):
    dialog = defaultdict(list)
    for l in slang.splitlines():
        try:
            info = say.parseString(l)
        except ParseException:
            continue

        dialog['sayings'].append(' '.join(info.msg))

    return dialog
