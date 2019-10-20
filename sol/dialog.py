# -*- coding: utf-8 -*-

import random

from .statements import get_statement, Say


class Dialog:

    def __init__(self, statements):
        self.statements = statements

    def __call__(self, context):
        return self.execute(context)

    @classmethod
    def from_parsed(cls, parsed):
        dialog_actions = []
        for statement_decl in parsed:
            stmt = get_statement(statement_decl)
            dialog_actions.append(stmt)

        return cls(dialog_actions)

    def execute(self, context):
        for stmt in self.statements:
            context = stmt(context)
        return context


class Bollocks(Dialog):

    sentences = [
        'Olá, você!',
        'Hey, Jude',
        'Fala, fi.'
    ]

    def __init__(self):
        super().__init__([])

    def execute(self, context):
        self.statements = [Say(random.choice(self.sentences))]
        try:
            super().execute(context)
        finally:
            self.actions = []
