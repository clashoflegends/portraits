# Clash of Legends — character portraits

Character portrait images for *Clash of Legends*. **Counselor downloads these on demand** (they are
deliberately kept out of the Counselor download). Public so the client can fetch them anonymously —
the same images were already served publicly from `clashlegends.com/portraits/`.

## Layout
- `Pers/` — character portraits, each named exactly as the character's `personagem.nm_filename`
  in the game DB (e.g. `Aegon II Targaryen.jpg`). The client flattens the zip on extract, so the
  folder split here is just for tidiness — only the filenames matter.
- `Teasers/` — teaser / splash images.

## Publishing a new pack (how Counselor picks it up)
1. Add or replace images under `Pers/` (or `Teasers/`), commit, and push to `main`.
2. Tag a release: `git tag portraits-YYYY.MM.DD && git push origin portraits-YYYY.MM.DD`.
3. CI (`.github/workflows/build.yml`) zips **all** image content into `portraits.zip` and publishes it
   as the GitHub Release asset for that tag.

Counselor downloads the **stable latest URL**
`https://github.com/clashoflegends/portraits/releases/latest/download/portraits.zip`
and compares the latest release `tag_name` against its stored `PortraitsVersion` to detect a newer
pack — no server-side manifest needed.
