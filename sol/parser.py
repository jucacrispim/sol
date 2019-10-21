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
    Literal,
    Regex
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


class CallParser(MatchParser):

    label = 'call'

    def parse(self, s, loc, toks):
        return (self.label, toks.expr, toks.var)


class ExistsParser(MatchParser):

    label = 'exists'

    def parse(self, s, loc, toks):
        return (self.label, ' '.join(toks.rest), toks.var)


class SlangParser:
    """The sol language! :)"""

    # First the language rules.

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

    EXISTS_KW = [
        'exists',
        'existe'
    ]

    # A pattern that matches everything
    REST = OneOrMore(
        Word(printables)
    ).setResultsName('rest')

    # matches variable assignments like `var =`
    VAR = Word(alphanums + '_').setResultsName('var') + Literal('=')

    # SAY Hello, user!
    SAY = oneOf(' '.join(SAY_KW), caseless=True) + REST
    SAY.setParseAction(SayParser())

    # answer = ASK What is your name?
    # or ASK What is your name?
    ASK = oneOf(' '.join(ASK_KW), caseless=True) + REST
    ASK = (VAR + ASK) | ASK
    ASK.setParseAction(AskParser())

    # EXISTS {a_var}
    EXISTS = oneOf(' '.join(EXISTS_KW), caseless=True) + REST
    EXISTS = (VAR + EXISTS | EXISTS)
    EXISTS.setParseAction(ExistsParser())

    # IF {bla} == "oi"
    IF = oneOf(' '.join(IF_KW), caseless=True) + REST
    IF.setParseAction(IfParser())

    # r = fn() or fn()
    CALL = Regex(r'[\w|_]+\(.*?\)').setResultsName('expr')
    CALL = (VAR + CALL) | CALL
    CALL.setParseAction(CallParser())

    GRAMMAR = SAY | ASK | IF | CALL | EXISTS

    def __call__(self, text):
        return self.parse(text)

    def parse(self, text):
        """Parses the contents of a .slang file and returns a list of
        statement rules in the following format:

        [
            ('say', 'something'),
            ('say', 'What?', 'varname'),
            ('if', 'cond', TRUE_RULES, FALSE_RULES),
            ('call', 'expr', 'varname')
        ]
        """
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
        try:
            line = lines[i].lower()
        except IndexError:
            cond_false = []
        else:
            if self._is_else(line):
                cond_false, j = self._get_nested_lines(lines[i + 1:])
                i += j + 1
            else:
                cond_false = []

        return cond_true, cond_false, i

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
        i += 1
        while i < len(lines):
            line = lines[i]
            if line and not line.startswith(' '):
                break

            nested.append(line[leading_spaces:])
            i += 1

        return nested, i
