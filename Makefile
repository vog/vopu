PACKAGE = vopu

SRCFILES = $(shell find -name '*.py')
PYCFILES = $(SRCFILES:.py=.pyc)
PYOFILES = $(SRCFILES:.py=.pyo)
TMPFILES = $(PYCFILES) $(PYOFILES) doc/

EPYDOC = epydoc --no-frames
PYTHON = python


default: test doc

test:
	$(PYTHON) $(PACKAGE).py

doc: doc/index.html
doc/index.html: $(SRCFILES)
	$(EPYDOC) -o doc -n "$(PACKAGE) API Documentation" $(SRCFILES)

clean:
	$(RM) -r $(wildcard $(TMPFILES))

.PHONY: default test doc clean
