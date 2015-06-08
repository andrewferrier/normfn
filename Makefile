TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)
FLAKE8 := $(shell which flake8)

builddeb:
	sudo apt-get install build-essential
	cp -R debian/DEBIAN/ $(TEMPDIR)
	mkdir -p $(TEMPDIR)/usr/bin
	mkdir -p $(TEMPDIR)/usr/share/doc/normalize-filename
	cp normalize-filename $(TEMPDIR)/usr/bin
	cp README* $(TEMPDIR)/usr/share/doc/normalize-filename
	cp LICENSE* $(TEMPDIR)/usr/share/doc/normalize-filename
	fakeroot chmod -R u=rwX,go=rX $(TEMPDIR)
	fakeroot chmod -R u+x $(TEMPDIR)/usr/bin
	fakeroot dpkg-deb --build $(TEMPDIR) .

builddocker:
	docker build -t andrewferrier/normalize-filename .

rundocker_testing: builddocker
	docker run -t andrewferrier/normalize-filename /sbin/my_init -- bash -c 'cd /tmp/normalize-filename && make unittest && make stylecheck'

rundocker_interactive: builddocker
	docker run -i -t andrewferrier/normalize-filename /sbin/my_init -- bash -l

unittest:
	python3 -m unittest discover

unittest_verbose:
	python3 -m unittest discover -f -v

coverage:
	rm -rf cover/
	nosetests tests/Direct/*.py --with-coverage --cover-package=normalize-filename,tests --cover-erase --cover-html --cover-branches
	open cover/index.html

analysis:
	pyflakes normalize-filename
	# Debian version is badly packaged, make sure we are using Python 3.
	/usr/bin/env python3 $(FLAKE8) --max-line-length=132 --max-complexity 10 .

alltests: unittest analysis
