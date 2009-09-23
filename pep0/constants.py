# -*- coding: utf-8 -*-
title_length = 55
column_format = (u' %(type)1s%(status)1s %(number)4s  %(title)-' +
                    unicode(title_length) + u's %(authors)-s')

header = u"""PEP: 0
Title: Index of Python Enhancement Proposals (PEPs)
Version: $Revision$
Last-Modified: $Date$
Author: David Goodger <goodger@python.org>,
        Barry Warsaw <barry@python.org>
Status: Active
Type: Informational
Created: 13-Jul-2000
"""

intro = u"""
    The PEP contains the index of all Python Enhancement Proposals,
    known as PEPs.  PEP numbers are assigned by the PEP Editor, and
    once assigned are never changed.  The SVN history[1] of the PEP
    texts represent their historical record.
"""

references = u"""
    [1] View PEP history online
        http://svn.python.org/projects/peps/trunk/
"""

footer = u"""
Local Variables:
mode: indented-text
indent-tabs-mode: nil
sentence-end-double-space: t
fill-column: 70
coding: utf-8
End:"""
