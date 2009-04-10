#!/usr/bin/env python

import subprocess, sys
proc = subprocess.Popen(['python', 'launcher.py'] + sys.argv[1:], cwd='applauncher')
proc.wait()
