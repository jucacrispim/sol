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
        return (self.label, ' '.join(toks.msg))


class AskParser(MatchParser):

    label = 'ask'

    def parse(self, s, loc, toks):
        return (self.label, ' '.join(toks.msg), toks.var)


class SlangParser:
    """The sol language! :)"""

    # First the language rules.
    # This is the message we display to the user, eg, after a SAY or
    # an ASK.
    OUTPUTMSG = OneOrMore(
        Word(printables)
    ).setResultsName('msg')

    # SAY Hello, user!
    SAY = oneOf('say diga', caseless=True) + OUTPUTMSG
    SAY.setParseAction(SayParser())

    # answer = ASK What is your name?
    ASK = Word(alphanums + '_').setResultsName('var') + Literal('=') + \
        oneOf('ask pergunte', caseless=True) + OUTPUTMSG
    ASK.setParseAction(AskParser())

    GRAMMAR = SAY | ASK

    def __call__(self, text):
        return self.parse(text)

    def parse(self, text):
        return self._parse_lines(text.splitlines())

    def _parse_lines(self, lines):
        dialog = []
        for l in lines:
            if l.startswith('#') or not l.strip():
                continue

            try:
                r = self.GRAMMAR.parseString(l)
                parsed = r[0]
            except ParseException:
                logger.warning('Line {} could not be parsed'.format(l))
            else:
                dialog.append(parsed)

        return dialog
