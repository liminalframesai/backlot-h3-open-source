# Public-package sanitization

The public repository is derived from a larger private production/evidence package. It
intentionally excludes:

- workstation usernames and absolute local paths;
- private hostnames, addresses, credentials, and network topology;
- internal queue/conductor deployment details;
- Resolve project databases and opaque project exports;
- unused generations and their metadata;
- the nearly 2 GiB uncompressed finishing source.

The public FCPXML uses a `file:///RELINK/` placeholder. Audit CSV paths are repository
relative. Two input filenames containing personal initials/names and one Comfy output
selector were normalized; the mapping itself is not published because it is unnecessary
for reuse. Exact private originals and their hashes remain in the non-public evidence
package.

Prompts, seeds, model filenames, workflow topology, and final-used audiovisual media are
preserved. Run `python3 tools/verify_repo.py` before publication; it scans text and binary
metadata for known private-path/name/network patterns.
