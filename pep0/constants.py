# -*- coding: utf-8 -*-
title_length = 55
column_format = (u' %(type)1s%(status)1s %(number)4s  %(title)-' +
                    unicode(title_length) + u's %(authors)-s')

header = u"""PSEP: 0
Title: Index of PySide Enhancement Proposals (PSEPs)
Version: $Revision$
Last-Modified: $Date$
Author: Matti Airas <matti.p.airas@nokia.com>,
Status: Active
Type: Informational
Created: 24-Sep-2009
"""

intro = u"""
    The PSEP contains the index of all PySide Enhancement Proposals,
    known as PSEPs.  PSEP numbers are assigned by the PSEP Editor, and
    once assigned are never changed.  The Git history[1] of the PSEP
    texts represent their historical record.
"""

references = u"""
    [1] View PSEP history online
        http://qt.gitorious.org/pyside/pseps/trees/master
"""

footer = u"""
Local Variables:
mode: indented-text
indent-tabs-mode: nil
sentence-end-double-space: t
fill-column: 70
coding: utf-8
End:"""
