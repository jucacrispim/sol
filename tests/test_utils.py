# -*- coding: utf-8 -*-

from sol import utils


def test_eval_expr_false():
    context = {'var': 'val'}
    r = utils.eval_expr('{var} == "other"', context)
    assert r is False


def test_eval_expr_true():
    context = {'var': 'val'}
    r = utils.eval_expr('{var} == "val"', context)
    assert r is True
