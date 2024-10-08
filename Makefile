ROOTDIR :=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)
FLAKE8 := $(shell which flake8)
PYLINT := $(shell which pylint3 || which pylint)

ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

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

install:
	install -d $(DESTDIR)$(PREFIX)/bin
	install -d $(DESTDIR)$(PREFIX)/share/doc/normfn
	install -m 755 normfn $(DESTDIR)$(PREFIX)/bin
	install -m 644 README* $(DESTDIR)$(PREFIX)/share/doc/normfn
	install -m 644 LICENSE* $(DESTDIR)$(PREFIX)/share/doc/normfn

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

alltests: unittest
