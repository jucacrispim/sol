# -*- coding: utf-8 -*-

import random

from .actions import Say, Ask

actions = {
    'say': Say,
    'ask': Ask
}


class Dialog:

    def __init__(self, actions):
        self.actions = actions

    def __call__(self, context):
        return self.execute(context)

    @classmethod
    def from_parsed(cls, parsed):
        dialog_actions = []
        for action_conf in parsed:
            label = action_conf[0]
            rest = action_conf[1:]
            action_cls = actions[label]
            dialog_actions.append(action_cls(*rest))

        return cls(dialog_actions)

    def execute(self, context):
        for action in self.actions:
            context = action(context)
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
        self.actions = [Say(random.choice(self.sentences))]
        try:
            super().execute(context)
        finally:
            self.actions = []
