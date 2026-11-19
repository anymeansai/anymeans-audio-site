# Drafts

Full product pages for plug-ins that aren't out yet. They use the same template as `artfreq.html`, so on
launch day they drop in and match the rest of the site.

Nothing in this folder is deployed: `drafts` is listed in `.vercelignore`, and each draft also has
`<meta name="robots" content="noindex">` as a backup.

| Draft | Replaces | Price | Stripe link |
| --- | --- | --- | --- |
| `creme.html` | `/creme` (coming-soon page) | $19 | https://buy.stripe.com/dRm9AU7ZyfkobateXhfYY05 |
| `vocalyst.html` | `/vocalyst` (coming-soon page) | $39 | https://buy.stripe.com/8x24gA6Vu1ty6Ud2avfYY07 |

Both Stripe links are live, one-time USD payments.

## Preview a draft

Any static server that maps `/creme` to `creme.html` works. Without one, open the file straight in a
browser: the fonts and images use root paths (`/assets/...`), so serve the repo root, for example:

```sh
npx serve .            # then open http://localhost:3000/drafts/creme
```

## Launch checklist

Search the draft for `TODO` first. Each one is something to confirm or a screenshot to drop in.

1. **Screenshots.** Export real screenshots, convert them to WebP (about 1600 px wide), put them in
   `assets/img/` and point the `TODO screenshot` frames at them. If the draft uses images from
   `drafts/img/`, move those to `assets/img/` and change `/drafts/img/` to `/assets/img/` in the page.
2. **Facts.** Confirm the price, the Stripe link and the number of machines per key (the plug-in READMEs
   say 2 computers, the ArtFreq page says one machine per key).
3. **Swap the page in.** Replace the coming-soon page with the draft, e.g. `git mv -f drafts/creme.html creme.html`.
   Then delete the DRAFT comment at the top and the `<meta name="robots" content="noindex">` line.
4. **Menu and footer.** The header menu and the footer are the same on every page. Edit them once in
   `index.html` (change `Soon` to `Out now`, add `menu__status--live`), then run
   `python3 tools/sync-shared.py` to copy them, and the shared CSS, to every page.
5. **Home page.** Move the plug-in out of the "Coming soon" grid in `index.html`. Copy the ArtFreq
   `feature-card` block for it, with its screenshot and price.
6. **Share image.** `assets/og/<name>.png` still says "Coming soon". Make a new 1200 x 630 image.
7. **Sitemap.** Bump `<lastmod>` for the page in `sitemap.xml`.
8. Push to a branch, check the Vercel preview on a phone and a laptop, then merge to `main`.
