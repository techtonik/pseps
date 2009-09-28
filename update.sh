#! /bin/sh

# This script is meant to be run by cron regularly on the
# www.python.org server to avoid letting the online PEPs get stale.
# Before using it, the user whose account it is run under needs to use
# the "cvs login" command to log into the Python CVS server as
# anonymous.

TMPDIR="/tmp"
WORKDIR="peps-$$"

AUXFILES="pep.css style.css index.html"

TARGETDIR='/tmp/www.pyside.org/docs/pseps/luck'

GITROOT='git://gitorious.org/pyside/pseps.git'
#CVSROOT=':pserver:anonymous@cvs.python.sourceforge.net:/cvsroot/python'
#export CVSROOT

cd "$TMPDIR" || exit $?
#cvs -Q checkout -d "$WORKDIR" python/nondist/peps || exit $?
git clone --depth 1 $GITROOT "$WORKDIR"

cd "$WORKDIR" || exit $?
#python ./pep2html.py -q || exit $?
make -s all || exit $?

# This loop avoids modifying the files for an unchanged PEP.
# The HTML file is treated a little strangely since it contains the
# (pseudo-)random selection of the corner logo.

for FILE in psep-*.txt ; do
    HTML="${FILE%txt}html"
    ATT="${FILE%.txt}-*"
    if [ -e "$TARGETDIR/$FILE" ] ; then
        if cmp -s "$FILE" "$TARGETDIR/$FILE" ; then
            true
        else
            cp "$FILE" "$TARGETDIR/" || exit $?
            cp "$HTML" "$TARGETDIR/" || exit $?
        fi
    else
        cp "$HTML" "$TARGETDIR/" || exit $?
    fi
    for N in "$ATT"; do
        if [ -e "$N" ] ; then
            if cmp -s "$N" "$TARGETDIR/$N" ; then
                true
            else
                cp "$N" "$TARGETDIR/" || exit $?
            fi
        fi
    done
done

for FILE in $AUXFILES; do
    if [ -e "$FILE" ] ; then
        if [ -e "$TARGETDIR/$FILE" ] ; then
            if cmp -s "$FILE" "$TARGETDIR/$FILE" ; then
                true
            else
                cp -d "$FILE" "$TARGETDIR/" || exit $?
            fi
        else
            cp -d "$FILE" "$TARGETDIR/" || exit $?
        fi
    fi
done

cd "$TMPDIR" || exit $?
rm -rf "$WORKDIR" || exit $?
