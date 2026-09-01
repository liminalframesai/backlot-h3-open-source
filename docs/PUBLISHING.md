# Publishing checklist

The repository is initialized on branch `main` and all publishable files are staged, but
there is intentionally no commit, author identity, or remote. Add those only after choosing
the public account/identity.

## Before the first commit

```sh
python3 tools/verify_repo.py
shasum -a 256 -c checksums/SHA256SUMS
shasum -a 256 -c checksums/RELEASE-ASSETS.sha256
git status
```

The 1080p film is about 63 MiB. GitHub warns above 50 MiB but permits normal Git objects
below 100 MiB. The staged repository is about 261 MiB. The 4K master is ignored because it
is about 320 MiB and must not enter normal Git history.

## Commit and push

Set the repository-local public identity, create the remote repository, then:

```sh
git commit -m "Publish Backlot H3 production closure"
git remote add origin PUBLIC_REPOSITORY_URL
git push -u origin main
```

Do not use a private workstation identity by accident. Verify with
`git config --local --list` before committing.

## Publish the 4K master

With GitHub CLI authenticated to the public account:

```sh
gh release create v1.0.0 \
  release-assets/backlot-2160p-youtube.mp4 \
  --title "Backlot 1.0 — film and reproducibility package" \
  --notes "4K YouTube delivery master. Verify against checksums/RELEASE-ASSETS.sha256."
```

GitHub permits individual Release assets below 2 GiB. Confirm the uploaded asset's size and
hash, then replace the relative links in `docs/SUBMISSION-SUMMARY.md` with the public GitHub
URLs used in the contest form.
