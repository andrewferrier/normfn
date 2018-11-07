class NormalizeFilename < Formula
  desc "Normalize Filename"
  homepage "http://github.com/andrewferrier/normalize-filename"
  url "https://github.com/andrewferrier/normalize-filename/archive/X.Y.zip"
  version "X.Y"

  depends_on "python@3"

  def install
      bin.install "normalize-filename"
      doc.install "README.md", "LICENSE.txt"
  end
end
