# -*- coding: utf-8 -*-

import sys

from sol.chatter import Chatter


def cli():
    chatter = Chatter()
    while True:
        text = input('>>> ')
        if text == 'q':
            sys.exit(0)

        chatter.respond_to(text)


if __name__ == '__main__':
    cli()
