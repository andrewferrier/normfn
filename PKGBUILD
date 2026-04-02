pkgname=normfn
pkgdesc="Normalizes filenames by prefixing a date to them"
pkgver=1.2.0.81.g6d407fd
pkgrel=1
arch=(any)
url="https://github.com/andrewferrier/normfn"
license=(MIT)
depends=(python python-shtab)
makedepends=(git python-build python-installer python-hatchling python-hatch-vcs)
replaces=(normalize-filename)
source=()
sha256sums=()

pkgver() {
    git -C "$startdir" describe --tags | sed 's/^v//; s/-/./g'
}

build() {
    cd "$startdir"
    python -m build --wheel --no-isolation
    PYTHONPATH="$startdir/src" python -m shtab --shell bash normfn.args.get_parser \
        > "$startdir/_completion_bash"
    PYTHONPATH="$startdir/src" python -m shtab --shell zsh normfn.args.get_parser \
        > "$startdir/_completion_zsh"
}

package() {
    cd "$startdir"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 LICENSE.txt "$pkgdir/usr/share/licenses/$pkgname/LICENSE.txt"
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    install -Dm644 _completion_bash \
        "$pkgdir/usr/share/bash-completion/completions/$pkgname"
    install -Dm644 _completion_zsh \
        "$pkgdir/usr/share/zsh/site-functions/_$pkgname"
}
