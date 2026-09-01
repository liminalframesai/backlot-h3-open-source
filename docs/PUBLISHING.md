# Publishing checklist

The repository is committed on `main`, attributed to the public `slogonomo` GitHub
identity through its noreply address, and pushed to
`liminalframesai/backlot-h3-open-source`. It remains **private until the contest
submission is timestamped**.

## Before publishing

```sh
python3 tools/verify_repo.py
shasum -a 256 -c checksums/SHA256SUMS
shasum -a 256 -c checksums/RELEASE-ASSETS.sha256
git status --short
```

The 1080p film is about 63 MiB. GitHub warns above 50 MiB but permits normal Git objects
below 100 MiB. The 4K master is ignored because it is about 320 MiB and must not enter
normal Git history.

## Publish the 4K master

With GitHub CLI authenticated to the public account:

```sh
gh release create v1.0.0 \
  release-assets/backlot-2160p-youtube.mp4 \
  --title "Backlot 1.0 — film and reproducibility package" \
  --notes "4K YouTube delivery master. Verify against checksums/RELEASE-ASSETS.sha256."
```

GitHub permits individual Release assets below 2 GiB. Confirm the uploaded asset's size and
hash, then replace the relative links in `docs/SUBMISSION-SUMMARY.md` with the GitHub URLs
used in the contest form.

## Submission-safe publication order

1. Keep the repository private while uploading and verifying the release asset.
2. Upload the film and workflow to the contest destinations and submit the official form.
3. Change the repository to public immediately afterward:

   ```sh
   gh repo edit liminalframesai/backlot-h3-open-source \
     --visibility public \
     --accept-visibility-change-consequences
   ```

4. Open the repository in a signed-out browser and verify the README, film, workflow, and
   release asset.
