#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os, sys

quiet = False
if '--list' in sys.argv:
  quiet = True
  
def qprint(text):
  if quiet:
    sys.stderr.write(text + '\n')
    sys.stderr.flush()
    return
  print text
  
def dumb(cmd):
  if quiet:
    return cmd + ' 1>&2'
  else:
    return cmd

walkres = os.walk('.')
pos = []

for path, dirs, files in walkres:
  for file in files:
    p = os.path.join(path, file)
    if p.endswith(".po"):
      pos.append(p)
  

qprint("Generating .pot file")
cmd = "xgettext -d command-not-found -o command-not-found.pot -c --no-wrap command-not-found.py"
os.system(dumb(cmd))
  
LIST_OUT = []
for po in pos:
  qprint("Updating " + po)
  LIST_OUT.append(po.split('/')[2])
  
  cmd = "msgmerge --no-wrap -U  " + po + ' command-not-found.pot'
  os.system(dumb(cmd))
  mo = po[:-2] + 'mo'
  qprint ("Compiling " + po)
  cmd = "msgfmt -o " + mo + ' ' + po
  os.system(dumb(cmd))
  
os.remove('command-not-found.pot')

if quiet:
  print ' '.join(LIST_OUT)
  