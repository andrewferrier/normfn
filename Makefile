ROOTDIR :=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)
FLAKE8 := $(shell which flake8)
PYLINT := $(shell which pylint3 || which pylint)

determineversion:
	$(eval GITDESCRIBE_DIRTY := $(shell git describe --dirty))
	sed 's/Version: .*/Version: $(GITDESCRIBE_DIRTY)/' debian/DEBIAN/control_template > debian/DEBIAN/control
	$(eval GITDESCRIBE_ABBREV := $(shell git describe --abbrev=0))
	sed 's/X\.Y/$(GITDESCRIBE_ABBREV)/' brew/normalize-filename_template.rb > brew/normalize-filename.rb
	sed 's/pkgver=X/pkgver=$(GITDESCRIBE_ABBREV)/' PKGBUILD_template > PKGBUILD

builddeb: determineversion builddeb_real

builddeb_real:
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

buildarch: determineversion
	makepkg --skipinteg

install_osx_finder:
	cp normalize-filename osx/services/normalize-filename-finder.workflow/Contents/
	rm -Rfv ~/Library/Services/normalize-filename-finder.workflow/
	cp -R osx/services/normalize-filename-finder.workflow ~/Library/Services
	# The following shortcut is Alt-Command-r
	defaults write com.apple.finder NSUserKeyEquivalents '{"Normalize Filename"="@~r";}'
	killall Finder

install_osx_brew: determineversion
	brew install -f file://$(ROOTDIR)/brew/normalize-filename.rb

reinstall_osx_brew: determineversion
	brew reinstall file://$(ROOTDIR)/brew/normalize-filename.rb

unittest:
	python3 -m unittest discover -s tests/

unittest_verbose:
	python3 -m unittest discover -s tests/ -f -v

coverage:
	rm -rf cover/
	nosetests tests/Direct/*.py --with-coverage --cover-package=normalize-filename,tests --cover-erase --cover-html --cover-branches
	open cover/index.html

analysis:
	pyflakes normalize-filename
	# Debian version is badly packaged, make sure we are using Python 3.
	-/usr/bin/env python3 $(FLAKE8) --max-line-length=132 --max-complexity 10 normalize-filename tests/
	$(PYLINT) --reports=n --disable=line-too-long --disable=missing-docstring --disable=locally-disabled normalize-filename tests/

alltests: unittest analysis
