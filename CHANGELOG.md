# Changelog
All notable changes will be documented in this file.

## [Unreleased]
### Added
- Added sps User-Agent
### Changed
- fixed bug [23](https://github.com/SweBarre/sps/issues/23), error thrown when cache file lacked information while running completion bash
- upgraded PyYaml to >= 5.4
### Removed

## [0.2.0]
### Added
- patchproduct search functionality
- patch search functionality
### Changed
- completion for bash
### Removed
- removed --short option for product

## [0.1.1]
### Added
- added helpers print_err and print_warn
- cache age check
- --sort-table/-S option to product/package output
- --no-header/-H option to product/package output
- CHANGELOG.md
- --no-borders/-n option to product/package output
- --exact-match/-e option to product search
- --version/-v option

### Changed
- changed default cache file name to ~/.cache/sps_cache.json
- Product/Package headings in README.rst
- description of sps in README.rst
- typo i README.rst
- typos in cli help texts
- help text for package --short/-s option

## [0.1.0] - 2020-06-04
### Changed
- total refactor of code

## [0.0.1] - 2019-03-06
