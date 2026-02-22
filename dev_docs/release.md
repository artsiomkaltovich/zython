# Release Process Documentation

This document describes the release process for the Zython project.

## 1. Preparation
- Ensure all tests pass locally and in CI (GitHub "Test on release" action should be run manually).
- Update the [changelog](../changelog.md).
- Update copyright year in [sphinx conf.py](../docs/source/conf.py).
- Update `target-version` in [pyproject.toml](../pyproject.toml).
- Update Python and MiniZinc versions in [README.md](../README.md)

## 2. Tagging the Release
- Create a new tag for the release:

    ```shell
        git tag vX.Y.Z
        git push --tags
    ```

## 3. GitHub Actions
- On tag push, the release-test workflow runs tests and builds for all supported Python and MiniZinc versions.
- The release workflow builds and publishes distributions (wheels, source) to PyPI and triggers documentation builds.

## 4. PyPI Publishing
- Check if the package was published to PyPI.

## 5. Documentation
- Read the Docs is configured to build documentation for every tag (using `*` as tag specifier).
- Ensure the documentation is up-to-date and builds without errors.
