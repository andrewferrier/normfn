# Changelog

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
