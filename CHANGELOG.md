# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Component `Loader` interface which allows downstream libraries to implement
  their own Component save/load functionality.
- Support for Component `Loader` interface to CLI commands.
- `dataset-similarity` CLI command for generating program similarity datasets.
- Added explicit support for Python 3.11.
- Added explicit support for Python 3.12.

### Fixed
- Correct documentation for `verbose_name` - property not optional.
- Allow special characters (`=`, `:`) in quotes in CLI component parsing.

### Removed
- Removed explicit support for Python 3.5 (end-of-life).
- Removed explicit support for Python 3.6 (end-of-life).
- Removed explicit support for Python 3.7 (end-of-life).

## [1.2.0] - 2022-01-18
### Added
- GitHub Actions automated testing and deployment.
- `WindowsChocolateyDependency` for automatically installing dependencies from
  the Chocolatey package manager.
- Additional information, filtering, and search to the `list` command.
- Added explicit support for Python 3.10.

### Changed
- Renamed the `dependencies` command to `install` - changed the CLI slightly
  and added a few quality of life features.
- `LinuxAPTDependency` now automatically attempts to elevate if `apt update`
  fails.

### Removed
- Removed explicit support for Python 3.5 (end-of-life).

### Fixed
- Terminal colors are no longer used when they are not supported by `stdout`.

## [1.1.1] - 2021-09-14
### Added
- Initial public HELIX release.

[Unreleased]: https://github.com/helix-datasets/helix/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/helix-datasets/helix/releases/tag/v1.1.1
