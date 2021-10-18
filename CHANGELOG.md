# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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
