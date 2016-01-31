#!/usr/bin/env python

import re
import sys

def task_list():
    for line in sys.stdin:
        match = re.match(r'^([a-z\-]*):(?:.*)#\s*(.*)$', line)
        if match:
            print match.group(1).ljust(32) + '....... ' +match.group(2)
