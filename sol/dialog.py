# -*- coding: utf-8 -*-

import random


def say(msg):
    print(msg)


class Dialog:

    def __init__(self, actions):
        self.actions = actions

    def __call__(self, context):
        return self.execute(context)

    @classmethod
    def from_parsed(cls, parsed):
        actions = []
        for saying in parsed['sayings']:
            actions.append(lambda: say(saying))

        return cls(actions)

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    def execute(self, context):
        for action in self.actions:
            action()
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
        self.actions = [lambda: say(random.choice(self.sentences))]
        try:
            super().execute(context)
        finally:
            self.actions = []
