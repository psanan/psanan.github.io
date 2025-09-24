# Source for patricksanan.org

Source for my "fun" website, [patricksanan.org](https://patricksanan.org).

It tries to avoid abstraction and complication beyond
[basic HTML and CSS](https://developer.mozilla.org). It prioritizes
simplicity.

It's non-scalable. It's "fun" iff it's small and simple.
It's only directly useful to me, though I hope it demonstrates
that you can and should build your own site in a simple way.

HTML files live directly in `site/`. A CSS stylesheet and other
resources are in subdirectories of `site/`.

There is no "build"! Clone this repository and open `site/index.html` with a
web browser. Edit the files in a text editor and reload the browser page.

You can deploy by uploading the contents of `site/` (including
hidden files) to your web server (probably to `$HOME/public_html`). Currently,
I'm deploying by pushing the `site/` subtree to a branch set up for GitHub
Pages. See `deploy.sh`.

Python scripts in `scripts/` (using only standard modules) help with feed generation
and bulk formatting operations on the HTML.


Scripts depend on some command line tools:

* [rsync](https://en.wikipedia.org/wiki/Rsync) to upload
* [ImageMagick](https://imagemagick.org/index.php) to shrink images

[Git](https://git-scm.com/) is practically essential, to track changes.
