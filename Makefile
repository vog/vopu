MODULE = vopu
TMPFILES = *.pyc doc/

RM = rm -rf
EPYDOC = epydoc --no-frames
PYTHON = python


default: test doc

test:
	$(PYTHON) $(MODULE).py

doc: doc/index.html
doc/index.html: $(MODULE).py
	$(EPYDOC) -o doc/ $(MODULE).py

clean:
	$(RM) $(wildcard $(TMPFILES))
