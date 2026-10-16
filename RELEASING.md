# Releasing bachs

Releases are published to PyPI by `.github/workflows/release.yml` when a version
tag is pushed. The workflow uses PyPI trusted publishing, so no PyPI token is
stored anywhere, and PyPI records which commit and workflow run built each file.

## One-time setup (an owner of the `bachs` project on PyPI)

1. On pypi.org, open the `bachs` project, then **Manage project** > **Publishing**.
2. Add a GitHub publisher:
   - Owner: `bachsdev`
   - Repository name: `bachs-python`
   - Workflow name: `release.yml`
   - Environment name: `pypi`
3. Optionally, in this repository's **Settings** > **Environments** > `pypi`,
   add required reviewers so each publish waits for an approval. GitHub creates
   the environment on the first release if it does not exist.

## Each release

1. Update `version` in `pyproject.toml` and `src/bachs/_version.py`, and add the
   version to `CHANGELOG.md`.
2. Merge to `main` with the **SDK checks** workflow passing.
3. Tag the merge commit and push the tag, with a `v` in front of the version:

   ```bash
   git tag v1.0.0a1
   git push origin v1.0.0a1
   ```

4. Watch the **Release** workflow. It checks that the tag matches
   `pyproject.toml`, runs lint, type checks and tests, builds the sdist and
   wheel, verifies their contents and publishes. Pre-release versions such as
   `1.0.0a1` or `1.0.0rc1` are only installed by `pip install --pre bachs` or an
   exact pin, so `pip install bachs` keeps resolving to the last stable release.
5. Confirm with `pip index versions bachs --pre`.

PyPI never accepts the same version twice, even after a file is deleted. If a
release is broken, fix it and release a new version.

## After the first real release

Yank the placeholder (needs a PyPI owner, once): on pypi.org, open `bachs` >
**Manage project** > **Releases** > `0.0.1` > **Options** > **Yank**, with the
reason "Placeholder. Install bachs 1.0.0a1 or later."
