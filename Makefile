TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)
FLAKE8 := $(shell which flake8)

unittest:
	python3 -m unittest discover

unittest_verbose:
	python3 -m unittest discover -f -v

coverage:
	rm -rf cover/
	nosetests tests/Direct/*.py --with-coverage --cover-package=normalize-filename,tests --cover-erase --cover-html --cover-branches
	open cover/index.html

stylecheck:
	# Debian version is badly packaged, make sure we are using Python 3.
	/usr/bin/env python3 $(FLAKE8) --max-line-length=132 --max-complexity 10 .

alltests: unittest stylecheck
