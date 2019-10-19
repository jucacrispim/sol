# -*- coding: utf-8 -*-


class Action:

    def __call__(self, context):
        raise NotImplementedError


class Say(Action):

    def __init__(self, msg):
        self.msg = msg

    def __call__(self, context):
        print(self.msg.format(**context))
        return context

    def __str__(self):  # pragma no cover
        return 'say: {}'.format(self.msg)


class Ask(Action):

    def __init__(self, msg, varname):
        self.msg = msg
        self.varname = varname

    def __call__(self, context):
        print(self.msg.format(**context))
        r = input('>>> ')
        context[self.varname] = r
        return context

    def __str__(self):  # pragma no cover
        return 'ask: {}'.format(self.msg)
