"""Code to handle the output of PSEP 0."""
import sys
import unicodedata

from operator import attrgetter

from . import constants
from .psep import PSEP, PSEPError


indent = u' '

def write_column_headers(output):
    """Output the column headers for the PSEP indices."""
    column_headers = {'status': u'', 'type': u'', 'number': u'num',
                        'title': u'title', 'authors': u'owner'}
    print>>output, constants.column_format % column_headers
    underline_headers = {}
    for key, value in column_headers.items():
        underline_headers[key] = unicode(len(value) * '-')
    print>>output, constants.column_format % underline_headers


def sort_pseps(pseps):
    """Sort PSEPs into meta, informational, accepted, open, finished,
    and essentially dead."""
    meta = []
    info = []
    accepted = []
    open_ = []
    finished = []
    dead = []
    for psep in pseps:
        # Order of 'if' statement important.  Key Status values take precedence
        # over Type value, and vice-versa.
        if psep.type_ == 'Process':
            meta.append(psep)
        elif psep.status == 'Draft':
            open_.append(psep)
        elif psep.status in ('Rejected', 'Withdrawn', 'Deferred',
                'Incomplete', 'Replaced'):
            dead.append(psep)
        elif psep.type_ == 'Informational':
            info.append(psep)
        elif psep.status in ('Accepted', 'Active'):
            accepted.append(psep)
        elif psep.status == 'Final':
            finished.append(psep)
        else:
            raise PSEPError("unsorted (%s/%s)" %
                           (psep.type_, psep.status),
                           psep.filename, psep.number)
    return meta, info, accepted, open_, finished, dead


def verify_email_addresses(pseps):
    authors_dict = {}
    for psep in pseps:
        for author in psep.authors:
            # If this is the first time we have come across an author, add him.
            if author not in authors_dict:
                authors_dict[author] = [author.email]
            else:
                found_emails = authors_dict[author]
                # If no email exists for the author, use the new value.
                if not found_emails[0]:
                    authors_dict[author] = [author.email]
                # If the new email is an empty string, move on.
                elif not author.email:
                    continue
                # If the email has not been seen, add it to the list.
                elif author.email not in found_emails:
                    authors_dict[author].append(author.email)

    valid_authors_dict = {}
    too_many_emails = []
    for author, emails in authors_dict.items():
        if len(emails) > 1:
            too_many_emails.append((author.first_last, emails))
        else:
            valid_authors_dict[author] = emails[0]
    if too_many_emails:
        err_output = []
        for author, emails in too_many_emails:
            err_output.append("    %s: %r" % (author, emails))
        raise ValueError("some authors have more than one email address "
                         "listed:\n" + '\n'.join(err_output))

    return valid_authors_dict


def sort_authors(authors_dict):
    authors_list = authors_dict.keys()
    authors_list.sort(key=attrgetter('sort_by'))
    return authors_list

def normalized_last_first(name):
    return len(unicodedata.normalize('NFC', name.last_first))


def write_psep0(pseps, output=sys.stdout):
    print>>output, constants.header
    print>>output
    print>>output, u"Introduction"
    print>>output, constants.intro
    print>>output
    print>>output, u"Index by Category"
    print>>output
    write_column_headers(output)
    meta, info, accepted, open_, finished, dead = sort_pseps(pseps)
    print>>output
    print>>output, u" Meta-PSEPs (PSEPs about PSEPs or Processes)"
    print>>output
    for psep in meta:
        print>>output, unicode(psep)
    print>>output
    print>>output, u" Other Informational PSEPs"
    print>>output
    for psep in info:
        print>>output, unicode(psep)
    print>>output
    print>>output, u" Accepted PSEPs (accepted; may not be implemented yet)"
    print>>output
    for psep in accepted:
        print>>output, unicode(psep)
    print>>output
    print>>output, u" Open PSEPs (under consideration)"
    print>>output
    for psep in open_:
        print>>output, unicode(psep)
    print>>output
    print>>output, u" Finished PSEPs (done, implemented in code repository)"
    print>>output
    for psep in finished:
        print>>output, unicode(psep)
    print>>output
    print>>output, u" Deferred, Abandoned, Withdrawn, and Rejected PSEPs"
    print>>output
    for psep in dead:
        print>>output, unicode(psep)
    print>>output
    print>>output
    print>>output, u" Numerical Index"
    print>>output
    write_column_headers(output)
    prev_psep = 0
    for psep in pseps:
        if psep.number - prev_psep > 1:
            print>>output
        print>>output, unicode(psep)
        prev_psep = psep.number
    print>>output
    print>>output
    print>>output, u"Key"
    print>>output
    for type_ in PSEP.type_values:
        print>>output, u"    %s - %s PSEP" % (type_[0], type_)
    print>>output
    for status in PSEP.status_values:
        print>>output, u"    %s - %s proposal" % (status[0], status)

    print>>output
    print>>output
    print>>output, u"Owners"
    print>>output
    authors_dict = verify_email_addresses(pseps)
    max_name = max(authors_dict.keys(), key=normalized_last_first)
    max_name_len = len(max_name.last_first)
    print>>output, u"    %s  %s" % ('name'.ljust(max_name_len), 'email address')
    print>>output, u"    %s  %s" % ((len('name')*'-').ljust(max_name_len),
                                    len('email address')*'-')
    sorted_authors = sort_authors(authors_dict)
    for author in sorted_authors:
        # Use the email from authors_dict instead of the one from 'author' as
        # the author instance may have an empty email.
        print>>output, (u"    %s  %s" %
                (author.last_first.ljust(max_name_len), authors_dict[author]))
    print>>output
    print>>output
    print>>output, u"References"
    print>>output
    print>>output, constants.references
    print>>output, constants.footer
