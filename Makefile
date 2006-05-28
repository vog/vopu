#!/usr/bin/env make

MODULE = vopu
TMPFILES = *.pyc doc/

RM = rm -rf
EPYDOC = PYTHONVER=2.4 epydoc --no-frames
PYTHON = python2.4


default: test doc

test:
	$(PYTHON) $(MODULE).py

doc: doc/index.html
doc/index.html: $(MODULE).py
	$(EPYDOC) -o doc/ $(MODULE).py

clean:
	$(RM) $(wildcard $(TMPFILES))
