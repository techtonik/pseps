#!/usr/bin/env python2
"""Auto-generate PSEP 0 (PSEP index).

Generating the PSEP index is a multi-step process.  To begin, you must first
parse the PSEP files themselves, which in and of itself takes a couple of steps:

    1. Parse metadata.
    2. Validate metadata.

With the PSEP information collected, to create the index itself you must:

    1. Output static text.
    2. Format an entry for the PSEP.
    3. Output the PSEP (both by category and numerical index).

"""
from __future__ import absolute_import, with_statement

import sys
import os
import codecs

from operator import attrgetter

from psep0.output import write_psep0
from psep0.psep import PSEP, PSEPError


def main(argv):
    if not argv[1:]:
        path = '.'
    else:
        path = argv[1]

    pseps = []
    if os.path.isdir(path):
        for file_path in os.listdir(path):
            abs_file_path = os.path.join(path, file_path)
            if not os.path.isfile(abs_file_path):
                continue
            if file_path.startswith("psep-") and file_path.endswith(".txt"):
                with codecs.open(abs_file_path, 'r', encoding='UTF-8') as psep_file:
                    try:
                        pseps.append(PSEP(psep_file))
                    except PSEPError, e:
                        errmsg = "Error processing PSEP %s, excluding:" % \
                            (e.number,)
                        print >>sys.stderr, errmsg, e
                        sys.exit(1)
        pseps.sort(key=attrgetter('number'))
    elif os.path.isfile(path):
        with open(path, 'r') as psep_file:
            pseps.append(PSEP(psep_file))
    else:
        raise ValueError("argument must be a directory or file path")

    with codecs.open('psep-0000.txt', 'w', encoding='UTF-8') as psep0_file:
        write_psep0(pseps, psep0_file)

if __name__ == "__main__":
    main(sys.argv)
