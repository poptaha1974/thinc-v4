# THINC — Documented Release Package

> Distribution-level document. The current version lives in
> `src/thinc_v4/_version.py` (mirrored in `pyproject.toml`, enforced by a test);
> `<version>` below stands for it. Layer versions (4.0 framework, 4.2 engine,
> 4.1 calibration / Layer 8) are independent of the distribution version.

**Inventor / Author / Owner:** Dr. Ehab Taha (الدكتور إيهاب طه).

Every THINC release is produced by one script, `scripts/build_release.py`, so the
package, its checksums, its SBOM, and its provenance record are always generated
together and never drift apart.

## Build it

```bash
pip install -e '.[dev,release]'
python scripts/build_release.py
```

Or via Make:

```bash
make release
```

## What lands in `dist/`

| File | Purpose |
|---|---|
| `thinc_v4-<version>-py3-none-any.whl` | installable wheel |
| `thinc_v4-<version>.tar.gz` | source distribution |
| `SHA256SUMS` | SHA-256 for every artifact, `sha256sum -c` compatible |
| `sbom.cyclonedx.json` | CycloneDX 1.5 SBOM of the package and its resolved dependency environment |
| `RELEASE_MANIFEST.json` | machine-readable provenance: version, git commit and cleanliness, builder platform, quality-gate results, reproducibility proof, SBOM generator, artifact digests, THINC identity hash |
| `RELEASE_NOTES.md` | human-readable release record with the digest table and verification steps |

## Quality gates run before packaging

The build refuses to package unless all of these pass:

1. `ruff check .`
2. `mypy` (strict, over `src` + `services` + `tests` + `scripts`)
3. `pytest -q`
4. `python -m thinc_v4.v4_2.master_framework --test` (v4.2 self-test, 45 checks)
5. `pyproject.toml` version == `thinc_v4.__version__`
6. `verify_attribution()` — the build aborts if THINC attribution was modified

Use `--skip-gates` only for local experiments; CI never skips them for a tag.

## Reproducibility

`SOURCE_DATE_EPOCH` is pinned to the HEAD commit time, and the sdist is rewritten
with fixed member mtimes, ownership, and permissions plus a pinned gzip header.
Rebuilding the same commit with the same toolchain yields **identical** wheel and
sdist digests.

The proof runs *inside* the same invocation: the archives are rebuilt in a scratch
directory and their digests compared, and the result is recorded under
`reproducibility` in the manifest. This is deliberate — an external
"build again and diff" step would overwrite the gated manifest and notes with a
gate-skipping build, making the published record claim `SKIPPED`.
Use `--skip-reproducibility-check` only for fast local iterations.

The SBOM intentionally embeds a build timestamp, so only the archives are
compared for bit-for-bit equality.

## Verify a received package

```bash
cd dist
sha256sum -c SHA256SUMS

# provenance and identity
python -c "import json;m=json.load(open('RELEASE_MANIFEST.json'));print(m['version'],m['git']['commit'],m['identity']['identity_hash_sha256'])"

# SBOM sanity
python -c "import json;d=json.load(open('sbom.cyclonedx.json'));print(d['bomFormat'],d['specVersion'],len(d['components']),'components')"

# clean-room smoke test
python -m venv /tmp/verify && /tmp/verify/bin/pip install thinc_v4-*-py3-none-any.whl
/tmp/verify/bin/python -m thinc_v4.v4_2.master_framework --test
```

## SBOM generator

The `release` extra pins `cyclonedx-bom==7.3.1`, whose CLI provides the
`environment` subcommand used here (~75 components). The script keeps a minimal
built-in fallback, records which generator ran in `sbom.generator`, and the
release workflow **fails** if the fallback was used — so a tooling downgrade can
never ship a thin SBOM unnoticed.

## Publishing

Tagging `v<version>` triggers `.github/workflows/release.yml`, which rebuilds the
package, verifies checksums, proves reproducibility, installs the wheel in a
clean virtualenv, runs the v4.2 self-test against the installed wheel, and then
attaches all artifacts to the GitHub Release.

```bash
VERSION=$(python -c "import tomllib,pathlib;print(tomllib.loads(pathlib.Path('pyproject.toml').read_text())['project']['version'])")
git tag -a "v${VERSION}" -m "THINC v${VERSION}"
git push origin "v${VERSION}"
```

### Re-publishing an existing tag

Prefer a **new version** for new content: two different archives published under
one version number cannot be told apart by a consumer holding only the version.

If a tag must be moved anyway, note that deleting it turns its release into an
orphaned *draft* (GitHub renames the slug to `untagged-…`). The workflow now
detects that case, deletes the stale draft, recreates the release with
`--verify-tag --latest`, and then asserts that exactly one **published** release
exists for the tag — so a moved tag can no longer leave duplicate drafts behind.

---
THINC™ — Invented by Dr. Ehab Taha (الدكتور إيهاب طه). © 2026 all rights reserved.
