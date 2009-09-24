# Rules to only make the required HTML versions, not all of them,
# without the user having to keep track of which.
#
# Not really important, but convenient.

PEP2HTML=pep2html.py

PYTHON=python

.SUFFIXES: .txt .html

.txt.html:
	@$(PYTHON) $(PEP2HTML) $<

TARGETS=$(patsubst %.txt,%.html,$(wildcard psep-????.txt)) psep-0000.html

all: psep-0000.txt $(TARGETS)

$(TARGETS): pep2html.py

psep-0000.txt: $(wildcard psep-????.txt)
	$(PYTHON) genpepindex.py .

install:
	echo "Installing is not necessary anymore. It will be done in post-commit."

clean:
	-rm psep-0000.txt
	-rm *.html

update:
	git pull
