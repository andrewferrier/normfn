class NormFN < Formula
  desc "normfn --- filename normalizer"
  homepage "http://github.com/andrewferrier/normfn"
  url "https://github.com/andrewferrier/normfn/archive/X.Y.zip"
  version "X.Y"

  depends_on "python@3"

  def install
      bin.install "normfn"
      doc.install "README.md", "LICENSE.txt"
  end
end
