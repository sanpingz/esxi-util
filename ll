#!/usr/bin/env python

from os import system as run
from sys import argv

arg = argv[1]+'l' if len(argv)>1 else '-l'

run('ls %s' % arg)
