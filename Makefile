ROOTDIR :=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)

ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

unittest:
	uv run -- python -m unittest discover -s tests -p "*.py"

unittest_verbose:
	uv run -- python -m unittest discover -s tests -p "*.py" -f -v

builddeb:
	sudo apt-get install build-essential fakeroot dpkg-dev
	mkdir -p $(TEMPDIR)/DEBIAN
	sed 's/Version: .*/Version: $(shell git describe --tags --dirty | cut -c 2-)/' debian/DEBIAN/control_template > $(TEMPDIR)/DEBIAN/control
	pip install --prefix=/usr --root=$(TEMPDIR) --no-deps .
	mkdir -p $(TEMPDIR)/usr/share/doc/normfn
	cp README* $(TEMPDIR)/usr/share/doc/normfn
	cp LICENSE* $(TEMPDIR)/usr/share/doc/normfn
	fakeroot chmod -R u=rwX,go=rX $(TEMPDIR)
	fakeroot dpkg-deb --build $(TEMPDIR) .

buildarch:
	makepkg --skipinteg --nodeps

install_osx_finder:
	cp src/normfn/__main__.py osx/services/normfn-finder.workflow/Contents/
	rm -Rfv ~/Library/Services/normfn-finder.workflow/
	cp -R osx/services/normfn-finder.workflow ~/Library/Services
	# The following shortcut is Alt-Command-r
	defaults write com.apple.finder NSUserKeyEquivalents '{"Normalize Filename"="@~r";}'
	killall Finder

install_osx_brew:
	$(eval GITDESCRIBE_BREW := $(shell git describe --tags --abbrev=0))
	sed 's/X\.Y/$(GITDESCRIBE_BREW)/' brew/normfn_template.rb > brew/normfn.rb
	brew install -f file://$(ROOTDIR)/brew/normfn.rb

reinstall_osx_brew:
	$(eval GITDESCRIBE_BREW := $(shell git describe --tags --abbrev=0))
	sed 's/X\.Y/$(GITDESCRIBE_BREW)/' brew/normfn_template.rb > brew/normfn.rb
	brew reinstall file://$(ROOTDIR)/brew/normfn.rb
