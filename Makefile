ROOTDIR :=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)
FLAKE8 := $(shell which flake8)
PYLINT := $(shell which pylint3 || which pylint)

determineversion:
	$(eval GITDESCRIBE_DEBIAN := $(shell git describe --tags --dirty | cut -c 2-))
	sed 's/Version: .*/Version: $(GITDESCRIBE_DEBIAN)/' debian/DEBIAN/control_template > debian/DEBIAN/control
	$(eval GITDESCRIBE_BREW := $(shell git describe --tags --abbrev=0))
	sed 's/X\.Y/$(GITDESCRIBE_BREW)/' brew/normfn_template.rb > brew/normfn.rb
	$(eval GITDESCRIBE_ARCH := $(shell git describe --tags | sed 's/-/_/g'))
	sed 's/pkgver=X/pkgver=$(GITDESCRIBE_ARCH)/' PKGBUILD_template > PKGBUILD

builddeb: determineversion builddeb_real

builddeb_real:
	sudo apt-get install build-essential
	cp -R debian/DEBIAN/ $(TEMPDIR)
	mkdir -p $(TEMPDIR)/usr/bin
	mkdir -p $(TEMPDIR)/usr/share/doc/normfn
	cp normfn $(TEMPDIR)/usr/bin
	cp README* $(TEMPDIR)/usr/share/doc/normfn
	cp LICENSE* $(TEMPDIR)/usr/share/doc/normfn
	fakeroot chmod -R u=rwX,go=rX $(TEMPDIR)
	fakeroot chmod -R u+x $(TEMPDIR)/usr/bin
	fakeroot dpkg-deb --build $(TEMPDIR) .

buildarch: determineversion
	makepkg --skipinteg

install_osx_finder:
	cp normfn osx/services/normfn-finder.workflow/Contents/
	rm -Rfv ~/Library/Services/normfn-finder.workflow/
	cp -R osx/services/normfn-finder.workflow ~/Library/Services
	# The following shortcut is Alt-Command-r
	defaults write com.apple.finder NSUserKeyEquivalents '{"Normalize Filename"="@~r";}'
	killall Finder

install_osx_brew: determineversion
	brew install -f file://$(ROOTDIR)/brew/normfn.rb

reinstall_osx_brew: determineversion
	brew reinstall file://$(ROOTDIR)/brew/normfn.rb

unittest:
	python3 -m unittest discover -s tests/

unittest_verbose:
	python3 -m unittest discover -s tests/ -f -v

analysis:
	pyflakes normfn
	# Debian version is badly packaged, make sure we are using Python 3.
	-/usr/bin/env python3 $(FLAKE8) --max-line-length=132 --max-complexity 10 normfn tests/
	$(PYLINT) --reports=n --disable=line-too-long --disable=missing-docstring --disable=locally-disabled normfn tests/

alltests: unittest analysis
