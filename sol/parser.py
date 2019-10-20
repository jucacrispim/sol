# -*- coding: utf-8 -*-

# This module parses the contents of .slang files and returns
# a list of tupples with a dialog configuration

from pyparsing import (
    OneOrMore,
    oneOf,
    Word,
    alphanums,
    printables,
    ParseException,
    Literal
)

from .utils import logger


class MatchParser:
    """A match parser is called when a match occours within the source text
    """

    label = None

    def __call__(self, s, loc, toks):
        r = self.parse(s, loc, toks)
        logger.debug('line {} parsed with {}'.format(
            s, type(self).__name__))

        return r

    def parse(self, s, loc, toks):
        """Parses the match result from pyparsing.

        :param s: is the original parse string
        :param loc: is the location in the string where matching started
        :param toks: is the list of the matched tokens, packaged as a
          ParseResults object
        """
        raise NotImplementedError


class SayParser(MatchParser):

    label = 'say'

    def parse(self, s, loc, toks):
        return (self.label, ' '.join(toks.rest))


class AskParser(MatchParser):

    label = 'ask'

    def parse(self, s, loc, toks):
        return (self.label, ' '.join(toks.rest), toks.var)


class IfParser(MatchParser):

    label = 'if'

    def parse(self, s, loc, toks):
        # label, condition, true-block, false-block
        # true and false blocks will be analized later in
        # the parsing process.
        return (self.label, ' '.join(toks.rest), [], [])


class SlangParser:
    """The sol language! :)"""

    # First the language rules.
    # A pattern that matches everything
    SAY_KW = [
        'say',
        'diga'
    ]

    ASK_KW = [
        'ask',
        'pergunte'
    ]

    IF_KW = [
        'if',
        'se'
    ]

    # tokens that mark start of blocks related to ifs
    IF_CONT_KW = [
        'else',
        'senão'
    ]

    REST = OneOrMore(
        Word(printables)
    ).setResultsName('rest')

    # SAY Hello, user!
    SAY = oneOf(' '.join(SAY_KW), caseless=True) + REST
    SAY.setParseAction(SayParser())

    # answer = ASK What is your name?
    ASK = Word(alphanums + '_').setResultsName('var') + Literal('=') + \
        oneOf(' '.join(ASK_KW), caseless=True) + REST
    ASK.setParseAction(AskParser())

    # IF {bla} == "oi"
    IF = oneOf(' '.join(IF_KW), caseless=True) + REST
    IF.setParseAction(IfParser())

    GRAMMAR = SAY | ASK | IF

    def __call__(self, text):
        return self.parse(text)

    def parse(self, text):
        return self._parse_lines(text.splitlines())

    def _parse_lines(self, lines):
        dialog = []
        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1
            if line.startswith('#') or not line.strip():
                continue

            try:
                r = self.GRAMMAR.parseString(line)
                parsed = r[0]
            except ParseException:
                logger.warning('Line {} could not be parsed'.format(line))
                continue

            stmt = parsed[0]
            if stmt not in self.IF_KW:
                dialog.append(parsed)
                continue

            cond_true, cond_false, j = self._get_if_actions(lines[i:])

            parsed[-2].extend(self._parse_lines(cond_true))
            parsed[-1].extend(self._parse_lines(cond_false))
            i += j
            dialog.append(parsed)

        return dialog

    def _get_if_actions(self, lines):
        cond_true, i = self._get_nested_lines(lines)
        line = lines[i].lower()
        if self._is_else(line):
            cond_false, j = self._get_nested_lines(lines[i + 1:])
            i += j
        else:
            cond_false = []

        return cond_true, cond_false, i + 2

    def _is_else(self, line):
        for kw in self.IF_CONT_KW:
            if line.startswith(kw):
                return True

        return False

    def _get_nested_lines(self, lines):
        nested = []
        i = 0
        line = lines[i]
        if line and not line.startswith(' '):
            raise IndentationError(line)

        leading_spaces = len(line) - len(line.lstrip())
        nested.append(line[leading_spaces:])
        for i in range(1, len(lines)):
            line = lines[i]
            if line and not line.startswith(' '):
                break

            nested.append(line[leading_spaces:])

        return nested, i
