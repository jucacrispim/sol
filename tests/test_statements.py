# -*- coding: utf-8 -*-

from unittest.mock import Mock

import pytest

from sol import statements


def test_statement():
    statement = statements.Statement()
    with pytest.raises(NotImplementedError):
        statement({})


def test_say(mocker):
    mocker.patch.object(statements, 'print', Mock(spec=print))
    say = statements.Say('hei')
    say({})

    assert statements.print.called


def test_say_context_var(mocker):
    mocker.patch.object(statements, 'print', Mock(spec=print))
    say = statements.Say('hei {oi}')
    say({'oi': 'ola'})

    assert statements.print.call_args[0][0] == 'hei ola'


def test_ask(mocker):
    mocker.patch.object(statements, 'print', Mock(spec=print))
    mocker.patch.object(statements, 'input', Mock(spec=input,
                                                  return_value='oi'))
    ask = statements.Ask('what?', 'oque')
    r = ask({})

    assert r == {'oque': 'oi'}


def test_if_true(mocker):
    mocker.patch.object(statements, 'print', Mock(spec=print))
    mocker.patch.object(statements, 'input', Mock(spec=input,
                                                  return_value='oi'))
    cond = 'a == 1'
    true_body = [('ask', 'ok?', 'ok')]
    false_body = [('say', 'ok!')]

    stmt = statements.If(cond, true_body, false_body)
    context = {'a': 1}
    stmt(context)

    assert statements.input.called


def test_if_false(mocker):
    mocker.patch.object(statements, 'print', Mock(spec=print))
    mocker.patch.object(statements, 'input', Mock(spec=input,
                                                  return_value='oi'))
    cond = 'a == 1'
    true_body = [('ask', 'ok?', 'ok')]
    false_body = [('say', 'ok!')]

    stmt = statements.If(cond, true_body, false_body)
    context = {'a': 2}
    stmt(context)

    assert not statements.input.called
