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


class Call(Statement):

    def __init__(self, expr, variable=None):
        self.expr = expr
        self.variable = variable

    def __call__(self, context):
        r = eval_expr(self.expr, context)
        context[self.variable] = r
        return context

    def __str__(self):  # pragma no cover
        return 'call {}:'.format(self.expr)


class Exists(Statement):

    def __init__(self, expr, variable=None):
        self.expr = expr
        self.variable = variable

    def __call__(self, context):
        try:
            eval_expr(self.expr, context)
            r = True
        except NameError:
            r = False

        context[self.variable] = r
        return context

    def __str__(self):  # pragma no cover
        return 'exitsts {}:'.format(self.expr)


def get_statement(parsed):
    stmts = {
        'say': Say,
        'ask': Ask,
        'if': If,
        'call': Call,
        'exists': Exists
    }
    stmt = parsed[0]
    rest = parsed[1:]
    cls = stmts.get(stmt)
    return cls(*rest)
