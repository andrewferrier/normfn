# Changelog

## [3.1.0](https://github.com/andrewferrier/normfn/compare/v3.0.5...v3.1.0) (2026-04-28)


### Features

* Add support for completions - closes [#121](https://github.com/andrewferrier/normfn/issues/121) ([ccce5ce](https://github.com/andrewferrier/normfn/commit/ccce5cef99db25608776c3066688be50a5024fca))

## [3.0.5](https://github.com/andrewferrier/normfn/compare/v3.0.4...v3.0.5) (2026-03-31)


### Bug Fixes

* logo - displays consistently ([00292b9](https://github.com/andrewferrier/normfn/commit/00292b9ee5404d87f238ba243c7ceb548be85bf4))
* Standardize on AGENTS.md ([20223c6](https://github.com/andrewferrier/normfn/commit/20223c6b209fa64eb2d595d598534db49f8f2d26))
* Update copyright year in LICENSE file ([a2480bd](https://github.com/andrewferrier/normfn/commit/a2480bdbba0b0a29e0c035bd87139e8b65d85755))

## [3.0.4](https://github.com/andrewferrier/normfn/compare/v3.0.3...v3.0.4) (2026-03-28)


### Bug Fixes

* normfn --version in Debian package ([132e17e](https://github.com/andrewferrier/normfn/commit/132e17ef90b9cecedaded0c295b552c15dc2cfdf))

## [3.0.3](https://github.com/andrewferrier/normfn/compare/v3.0.2...v3.0.3) (2026-03-28)


### Bug Fixes

* Debian packaging issues ([139d602](https://github.com/andrewferrier/normfn/commit/139d60279c08ea17d0a559511318814fcd20ea37))

## [3.0.2](https://github.com/andrewferrier/normfn/compare/v3.0.1...v3.0.2) (2026-03-28)


### Bug Fixes

* Version matching logic for build ([5559339](https://github.com/andrewferrier/normfn/commit/5559339f5c58f0bb1962b79e0f1fac2f1ece4752))

## [3.0.1](https://github.com/andrewferrier/normfn/compare/v3.0.0...v3.0.1) (2026-03-28)


### Bug Fixes

* Further fix Debian build ([67bf03e](https://github.com/andrewferrier/normfn/commit/67bf03ed294a1fe238dc9b1903a42f195e9d3691))

## [3.0.0](https://github.com/andrewferrier/normfn/compare/v2.1.0...v3.0.0) (2026-03-28)


### ⚠ BREAKING CHANGES

* Move some lesser-used CLI options to config options - closes #104

### Features

* Move some lesser-used CLI options to config options - closes [#104](https://github.com/andrewferrier/normfn/issues/104) ([50dfb13](https://github.com/andrewferrier/normfn/commit/50dfb13dfe74ab317ef7f3d4fe31b529d3bfbdfc))


### Bug Fixes

* Improve Debian packaging ([3539993](https://github.com/andrewferrier/normfn/commit/3539993ac240504775d129d840ca876a6abe6b5b))
* Minor tweaks ([fa5928c](https://github.com/andrewferrier/normfn/commit/fa5928cfeae43bf9d39f2f4e0cd8b981cbe58339))
* Misc timezone issues - closes [#28](https://github.com/andrewferrier/normfn/issues/28) ([4034bf2](https://github.com/andrewferrier/normfn/commit/4034bf29b2343912c4c99d70b0eb036ce4243cc5))

## [2.1.0](https://github.com/andrewferrier/normfn/compare/v2.0.1...v2.1.0) (2026-03-24)


### Features

* Add --version - closes [#117](https://github.com/andrewferrier/normfn/issues/117) ([82c212d](https://github.com/andrewferrier/normfn/commit/82c212d83ea99251ec853d748bca440b4dd26b21))


### Bug Fixes

* Error handling for no args ([a37a22d](https://github.com/andrewferrier/normfn/commit/a37a22d408b52ad4319ad9148f66f6bda00e8c4b))


### Performance Improvements

* avoid double stat() call in get_timetouse() ([ace4eb0](https://github.com/andrewferrier/normfn/commit/ace4eb0dfd7d41929d596bafb92980acf248aa85))
* cache create_regex() ([d6d8c17](https://github.com/andrewferrier/normfn/commit/d6d8c1745fc76dc1c7ce866ed1526e8947d80e94))

## [2.0.1](https://github.com/andrewferrier/normfn/compare/v2.0.0...v2.0.1) (2026-03-16)


### Bug Fixes

* git ownership in Arch build ([5ee21a3](https://github.com/andrewferrier/normfn/commit/5ee21a3c890070b45d6aceccdb2881d4cc40b372))

## [2.0.0](https://github.com/andrewferrier/normfn/compare/v1.2.0...v2.0.0) (2026-03-16)


### ⚠ BREAKING CHANGES

* Reorganize normfn repo structure, change build system

### Features

* add .github/copilot-instructions.md and remove CONTRIBUTING.md ([289d4cd](https://github.com/andrewferrier/normfn/commit/289d4cd53d555fef3d03f851fe6bd49f92fe12b5))
* add demo scripts for normfn screencast ([875dc29](https://github.com/andrewferrier/normfn/commit/875dc298aad67456b4ccde26fa2cfbf0de6609e7))
* add support for ordinal date suffixes (1st, 2nd, 3rd, etc.) ([c202c6a](https://github.com/andrewferrier/normfn/commit/c202c6af8cdd4ee88cc7b8e00c3cb1b196cd6a64))
* support reading creation date from PDFs ([f7a97d6](https://github.com/andrewferrier/normfn/commit/f7a97d6457c354d8a20db212399f978239c60fe2))


### Bug Fixes

* Add missing permissions to GitHub workflows ([6272462](https://github.com/andrewferrier/normfn/commit/6272462e035239b1c51e049a655b7f4c99b8338d))
* Clean up imports ([80d6b3e](https://github.com/andrewferrier/normfn/commit/80d6b3ebd59ba07d1cc2bc80a87d01c1cb2eff4a))
* create parent directories for undo_log_file if missing ([ac6c630](https://github.com/andrewferrier/normfn/commit/ac6c630731472f11c9963c7e466398538937dc8d))
* Don't skip PDF tests ([0f732c3](https://github.com/andrewferrier/normfn/commit/0f732c3612e14bb20858db7c3db29f7848f79606))
* Handle dates like _18-Jun-25 - closes [#99](https://github.com/andrewferrier/normfn/issues/99) ([51f8ad9](https://github.com/andrewferrier/normfn/commit/51f8ad9568771678bb383db0574a543f0245a9e3))
* Ignore aider ([235407b](https://github.com/andrewferrier/normfn/commit/235407b8b669f1c79e866a14feed94ade40d3e9c))
* Python syntax issues ([c3b9435](https://github.com/andrewferrier/normfn/commit/c3b9435ffb37d6eafc1d1b2a89a6c4a36a59adfe))
* README update process ([0ddc500](https://github.com/andrewferrier/normfn/commit/0ddc500318864f3ab4bf8fe3e28817a833fd708d))
* remove traceback from user error messages ([3f07bc4](https://github.com/andrewferrier/normfn/commit/3f07bc4c8f93ae88d21897abbdf444f278650c9a))
* ruff issues ([767a29c](https://github.com/andrewferrier/normfn/commit/767a29c5d80a1378c0fc1535d2c74ea93a266895))
* shellcheck issue ([1d96bee](https://github.com/andrewferrier/normfn/commit/1d96bee959b8618c9ccbf667dba02c34312b84b5))
* Some typing issues ([e88d3ed](https://github.com/andrewferrier/normfn/commit/e88d3edc4e2d972f7b44421b28887a317d598151))
* Typing issues and warnings ([dc3c771](https://github.com/andrewferrier/normfn/commit/dc3c771f38e94d8a38b65ae2e528c3a5244cd7ee))


### Code Refactoring

* Reorganize normfn repo structure, change build system ([9566274](https://github.com/andrewferrier/normfn/commit/9566274bb9db86a23ea2ec77f6847bf756446441))

## [1.2.0](https://github.com/andrewferrier/normfn/compare/v1.1.9...v1.2.0) (2024-09-09)


### Features

* Add `install` target to Makefile ([ac82dea](https://github.com/andrewferrier/normfn/commit/ac82deaea6f9fd24ee989f4a86ce731ee72c1322))


### Bug Fixes

* Enforce python3 version ([595e3c3](https://github.com/andrewferrier/normfn/commit/595e3c34e3c3c7d47d39631b58d3810e7c7162a2))
* Remove unused hook ([50e93ab](https://github.com/andrewferrier/normfn/commit/50e93ab2dbbabe701277fc556b23907e74634c37))

## [1.1.9](https://github.com/andrewferrier/normfn/compare/v1.1.8...v1.1.9) (2024-08-14)


### Bug Fixes

* Switch Debian package section ([a94d3f1](https://github.com/andrewferrier/normfn/commit/a94d3f180bb047593da696ebd95af6988cdc6a6c))

## [1.1.8](https://github.com/andrewferrier/normfn/compare/v1.1.7...v1.1.8) (2024-08-11)


### Bug Fixes

* Disable Arch builds for now ([132be04](https://github.com/andrewferrier/normfn/commit/132be046a778bdb51f4304685ece1acde242af64))

## [1.1.7](https://github.com/andrewferrier/normfn/compare/v1.1.6...v1.1.7) (2024-08-11)


### Bug Fixes

* Upgrade Ubuntu ([cb50a77](https://github.com/andrewferrier/normfn/commit/cb50a779f71ce4a07688962931cc9daace73b629))

## [1.1.6](https://github.com/andrewferrier/normfn/compare/v1.1.5...v1.1.6) (2024-08-11)


### Bug Fixes

* Add universe repo ([182f33d](https://github.com/andrewferrier/normfn/commit/182f33db63dc9bb694e6d7d34c97554004458682))

## [1.1.5](https://github.com/andrewferrier/normfn/compare/v1.1.4...v1.1.5) (2024-08-11)


### Bug Fixes

* Build Arch package also ([0121761](https://github.com/andrewferrier/normfn/commit/012176133761c9539bd6d0e0042d4d246ba92551))

## [1.1.4](https://github.com/andrewferrier/normfn/compare/v1.1.3...v1.1.4) (2024-08-11)


### Bug Fixes

* Strip leading 'v' when building Debian ([33dc45a](https://github.com/andrewferrier/normfn/commit/33dc45a5bcb1a8166d42add000f6a8c444ed34df))

## [1.1.3](https://github.com/andrewferrier/normfn/compare/v1.1.2...v1.1.3) (2024-08-11)


### Bug Fixes

* 'git describe' ([565d3f1](https://github.com/andrewferrier/normfn/commit/565d3f1e66f4369b51a451aa8372461c2632e1e3))

## [1.1.2](https://github.com/andrewferrier/normfn/compare/v1.1.1...v1.1.2) (2024-08-11)


### Bug Fixes

* Check out before building ([7768bb8](https://github.com/andrewferrier/normfn/commit/7768bb8d769e4a6cb68cc12a3062d93f74ef5f4d))

## [1.1.1](https://github.com/andrewferrier/normfn/compare/v1.1.0...v1.1.1) (2024-08-11)


### Bug Fixes

* Correct ID ([f0f02f3](https://github.com/andrewferrier/normfn/commit/f0f02f30df174bbd4b3f9e936f9902ee4ae09570))

## [1.1.0](https://github.com/andrewferrier/normfn/compare/1.0.1...v1.1.0) (2024-08-11)


### Features

* Experiment with releasing Debian package ([54f11d5](https://github.com/andrewferrier/normfn/commit/54f11d5936a60f782fa514ae72bd3bfb5b4f7b5e))


### Bug Fixes

* Change to Python 3.10 from Ubuntu stable ([e753758](https://github.com/andrewferrier/normfn/commit/e753758ee4f4e2154ba9012ce02036cb55e08646))
* Try alternative approach to get normfn help ([3bdd1e1](https://github.com/andrewferrier/normfn/commit/3bdd1e106cfe6c7afb1e6dd75b58dc33b9c7a04b))

## [1.0.1](https://github.com/andrewferrier/normfn/compare/1.0.0...1.0.1) (2024-03-24)


### Bug Fixes

* Try using effective separator ([da2dba2](https://github.com/andrewferrier/normfn/commit/da2dba28da693037d1e417ed2dc99a46aef5de44))
* Update licence dates ([9184f82](https://github.com/andrewferrier/normfn/commit/9184f82124e0c595be4c9ebd1021939a3ac846b2))

## [1.0.0](https://github.com/andrewferrier/normfn/compare/0.8.1...1.0.0) (2023-11-25)


### ⚠ BREAKING CHANGES

* Remove --disable-datetime-prefixing

### Features

* Improve Arch package version ([27ea28d](https://github.com/andrewferrier/normfn/commit/27ea28db24eb4e49b6c5022d3979bbeb0be2d8a3))
* Remove --disable-datetime-prefixing ([bbdf200](https://github.com/andrewferrier/normfn/commit/bbdf200c3ec8e45aaff6414d229129b37bde228d))
* Update README with normfn --help ([e54fd7c](https://github.com/andrewferrier/normfn/commit/e54fd7ccf33024ff7ab9cb5987d0f72ed4678402))


### Bug Fixes

* Add backticks ([7f276b4](https://github.com/andrewferrier/normfn/commit/7f276b4d287bd6e09269eed73623824d5b98cbe0))
* Don't use Unix-like tmpdir ([d1a00a5](https://github.com/andrewferrier/normfn/commit/d1a00a52f7d552db61477ec84e01b75aba9c4f43))
* Enforce Python 3.8+ ([3dd98b7](https://github.com/andrewferrier/normfn/commit/3dd98b77aa0a73665f66cf57eb3c11a988cd1563))
* Ensure that a common separator is used for dates ([13d6b82](https://github.com/andrewferrier/normfn/commit/13d6b82fa1f07ab8183ace7926264f542dde2991))
* Ensure we use a common time separator ([0fb4c60](https://github.com/andrewferrier/normfn/commit/0fb4c6018460aca4b58444d5059600c6ca8a5fe1))
* Handle readchar() on Windows ([99b0c2c](https://github.com/andrewferrier/normfn/commit/99b0c2c94ae12eb896890abb3b2f7a80d55e1d0f))
* Handle readline on Windows ([849b7a8](https://github.com/andrewferrier/normfn/commit/849b7a8bdfc6338b24fec96f4bc5331dc8246b7a))
* Handle tty on Windows ([d590bd7](https://github.com/andrewferrier/normfn/commit/d590bd7b405c8bfbb94938f247be2d92c6e6a1eb))
* Handling of GITHUB_OUTPUT ([4a877a2](https://github.com/andrewferrier/normfn/commit/4a877a2c9a25b5ff68570b36a809eec63f44df18))
* Syntax for setting variable ([3255775](https://github.com/andrewferrier/normfn/commit/325577536ba7927166d486bfdd8adfa3e2a54dd4))
* Try command-output ([95b083c](https://github.com/andrewferrier/normfn/commit/95b083cc8e229f745b6363530e2cfb6b8618678c))
* Try syntax [#2](https://github.com/andrewferrier/normfn/issues/2) ([20b84c3](https://github.com/andrewferrier/normfn/commit/20b84c3dc7e31dd0ee2e16a8daf7c348bc3a76b0))
* Use --tags for 'git describe' ([7bc1538](https://github.com/andrewferrier/normfn/commit/7bc15381c73bac4682a99ef40b5c4af789d53d7d))
* Use os.sep for Windows excludes ([f5f8158](https://github.com/andrewferrier/normfn/commit/f5f8158b0df261866737487e14a8eacceeec38a9))
* Various aspects of README update ([85d77ca](https://github.com/andrewferrier/normfn/commit/85d77ca33dfc699ad0aac3477649f50a6f99cb95))

## [0.8.1](https://github.com/andrewferrier/normfn/compare/0.8.0...0.8.1) (2023-11-13)


### Bug Fixes

* Corner case where month was detected as 00 ([6aa39aa](https://github.com/andrewferrier/normfn/commit/6aa39aaf3e25bfd076c1cc81fa2b501a07fd51fa))

## [0.8.0](https://github.com/andrewferrier/normfn/compare/0.7.2...0.8.0) (2023-04-23)


### Features

* Add workflow to build Arch Linux ([6f5697f](https://github.com/andrewferrier/normfn/commit/6f5697fb8b4477bac2b51b4f933632725a558102))
* Check for conventional commits ([05f63d1](https://github.com/andrewferrier/normfn/commit/05f63d19cd5ba17a6db935695931d83d21d4c290))


### Bug Fixes

* Branch name ([47e92b0](https://github.com/andrewferrier/normfn/commit/47e92b0df19d6a45c8145f4670696c811b86d7b9))
* Install make ([d697994](https://github.com/andrewferrier/normfn/commit/d69799483f24eb004054f38e6703400092d67d97))
* Make pexpect a suggestion ([be482c2](https://github.com/andrewferrier/normfn/commit/be482c204cb96c10358922c90226f5c00ca17be9))
* Name of make command ([46ca2ec](https://github.com/andrewferrier/normfn/commit/46ca2ec5cb361b15ed15e1518e2aae84185500c4))
* Name of requirements file ([c6426f8](https://github.com/andrewferrier/normfn/commit/c6426f80cc2e82224e0677b5e3b80bf04812e787))
* Test commit ([be95809](https://github.com/andrewferrier/normfn/commit/be958099009b91d38dad4119476c338c3ed86e6d))
