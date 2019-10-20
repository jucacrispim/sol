# -*- coding: utf-8 -*-

from .utils import eval_expr


class Statement:

    def __call__(self, context):
        raise NotImplementedError


class Say(Statement):

    def __init__(self, msg):
        self.msg = msg

    def __call__(self, context):
        print(self.msg.format(**context))
        return context

    def __str__(self):  # pragma no cover
        return 'say: {}'.format(self.msg)


class Ask(Statement):

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


class If(Statement):

    def __init__(self, cond, true_body, false_body):
        self.cond = cond
        self.true_body = [get_statement(stmt) for stmt in true_body]
        self.false_body = [get_statement(stmt) for stmt in false_body]

    def __call__(self, context):
        if eval_expr(self.cond, context):
            stmts = self.true_body
        else:
            stmts = self.false_body

        for stmt in stmts:
            context = stmt(context)
        return context

    def __str__(self):  # pragma no cover
        return 'if {}:'.format(self.cond)


def get_statement(parsed):
    stmts = {
        'say': Say,
        'ask': Ask,
        'if': If
    }
    stmt = parsed[0]
    rest = parsed[1:]
    cls = stmts.get(stmt)
    return cls(*rest)
