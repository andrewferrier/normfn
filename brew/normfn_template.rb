class Normfn < Formula
  desc "normfn --- filename normalizer"
  homepage "http://github.com/andrewferrier/normfn"
  url "https://github.com/andrewferrier/normfn/archive/X.Y.tar.gz"
  version "X.Y"

  depends_on "python@3"

  def install
    system Formula["python@3"].opt_bin/"pip3", "install", "--prefix=#{prefix}", "."
    doc.install "README.md", "LICENSE.txt"
    (bash_completion/"normfn").write Utils.safe_popen_read(bin/"normfn", "--completions", "bash")
    (zsh_completion/"_normfn").write Utils.safe_popen_read(bin/"normfn", "--completions", "zsh")
  end

  test do
    system "#{bin}/normfn", "--help"
  end
end
