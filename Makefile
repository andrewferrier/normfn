ROOTDIR :=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

test:
	uv run pytest

DEB_SYSTEM_DEPS := debhelper dh-python python3-all python3-installer

builddeb:
	@missing=""; \
	for cmd in dpkg-buildpackage dh dh_python3 uv; do \
		command -v $$cmd > /dev/null 2>&1 || missing="$$missing $$cmd"; \
	done; \
	if [ -n "$$missing" ]; then \
		echo "ERROR: Missing commands:$$missing"; \
		echo "For system tools, install with: sudo apt-get install -y $(DEB_SYSTEM_DEPS)"; \
		echo "For uv, see: https://docs.astral.sh/uv/getting-started/installation/"; \
		exit 1; \
	fi
	uv sync
	$(ROOTDIR)/debian/gen-changelog
	dpkg-buildpackage --no-sign --build=binary
	mv -f $(ROOTDIR)/../normfn_*.deb $(ROOTDIR)/

buildarch:
	makepkg --noconfirm --skipinteg --nodeps

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
