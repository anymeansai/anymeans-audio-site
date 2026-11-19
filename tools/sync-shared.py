#!/usr/bin/env python3
"""Keep the shared parts of every page identical.

The site has no build step: each page is a self-contained HTML file with its own
<style> and <script>. To keep them consistent, the shared parts are marked with
comments and copied from one "source" page into the rest:

  @shared   CSS for the whole site (fonts, colours, header, menu, footer, buttons...)  source: index.html
  @menu     the header menu script                                                    source: index.html
  @video    autoplaying demo videos and their Sound button                             source: index.html
  @product  CSS for full product pages (hero, features, pricing, buy bar...)           source: artfreq.html
  @buy      the buy bar script                                                         source: artfreq.html
  @soon     CSS for the "coming soon" pages                                            source: creme.html
  @header   the site header and plug-in menu (HTML)                                    source: index.html
  @footer   the site footer (HTML)                                                     source: index.html

The header and footer links to the page itself get aria-current="page" automatically
(artfreq.html and drafts/artfreq.html both count as /artfreq).

Edit the block in its source page, then run:  python3 tools/sync-shared.py
Pages in drafts/ are synced too, so they match the live site on launch day.
To sync just some pages:                       python3 tools/sync-shared.py drafts/creme.html
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCKS = {
    "shared": "index.html",
    "menu": "index.html",
    "video": "index.html",
    "product": "artfreq.html",
    "buy": "artfreq.html",
    "soon": "creme.html",
    "header": "index.html",
    "footer": "index.html",
}
HTML_BLOCKS = {"header", "footer"}


def pattern(name):
    if name in HTML_BLOCKS:
        return re.compile(r"<!-- @%s:start -->.*?<!-- @%s:end -->" % (name, name), re.S)
    return re.compile(r"/\* @%s:start.*?/\* @%s:end \*/" % (name, name), re.S)


def for_page(name, block, page):
    """Mark the page's own links in the header/footer with aria-current."""
    if name not in HTML_BLOCKS:
        return block
    block = block.replace(' aria-current="page"', "")
    own = '<a href="/%s"' % page.stem
    return block.replace(own + ">", own + ' aria-current="page">')


def main():
    if len(sys.argv) > 1:  # sync only the pages given, e.g. drafts/creme.html
        pages = [pathlib.Path(p).resolve() for p in sys.argv[1:]]
    else:
        pages = sorted(ROOT.glob("*.html")) + sorted((ROOT / "drafts").glob("*.html"))
    sources = {}
    for name, src in BLOCKS.items():
        m = pattern(name).search((ROOT / src).read_text(encoding="utf-8"))
        if not m:
            sys.exit("missing @%s block in %s" % (name, src))
        sources[name] = m.group(0)

    for page in pages:
        text = page.read_text(encoding="utf-8")
        new = text
        done = []
        for name, block in sources.items():
            if page.name == BLOCKS[name] and page.parent == ROOT:
                continue
            if pattern(name).search(new):
                fitted = for_page(name, block, page)
                new = pattern(name).sub(lambda _m: fitted, new)
                done.append(name)
        if new != text:
            page.write_text(new, encoding="utf-8")
            print("updated %s (%s)" % (page.relative_to(ROOT), ", ".join(done)))
        else:
            print("ok      %s" % page.relative_to(ROOT))


if __name__ == "__main__":
    main()
