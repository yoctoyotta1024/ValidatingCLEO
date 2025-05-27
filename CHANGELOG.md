# Changelog
All notable changes to this project will be documented in this file. See [conventional commits](https://www.conventionalcommits.org/) for commit guidelines.

- - -
## [v0.4.1](https://github.com/yoctoyotta1024/ValidatingCLEO/compare/0fb8c23a63331656457ab8465da85f09ab6e1685..v0.4.1) - 2025-05-27
#### Bug Fixes
- correct axis label - ([ae33bf7](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/ae33bf7286e7c363cee83f8a640ae50daf99ed05)) - clara.bayley
#### Refactoring
- beautify plots for motion test case - ([86072d0](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/86072d012c2894beba7fbd6481c4f3ea5b508003)) - clara.bayley
- beautify labels on collisions plot - ([ba094d8](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/ba094d8f1a90b471a3475022f9bca0349c285584)) - clara.bayley
- beautify labels on condensation/evaporation plot - ([0fb8c23](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/0fb8c23a63331656457ab8465da85f09ab6e1685)) - clara.bayley

- - -

## [v0.4.0](https://github.com/yoctoyotta1024/ValidatingCLEO/compare/00adb435122f6fd8e1cfa98fdc9723d5690b0eb9..v0.4.0) - 2025-04-25
#### Bug Fixes
- wrong order of setups - ([5827771](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/582777174b8d7574eb4d27b06b7bba1ce040421c)) - clara.bayley
- sbatch-able paths in scripts - ([b4e77d5](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/b4e77d51da795e098c4ff7354c4223adc645bf04)) - clara.bayley
#### Documentation
- document describing motion 2-D test-case - ([7234cb1](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/7234cb1017d2daba3b84722bf972d933e98d1ce2)) - clara.bayley
#### Features
- plotting script for 2d motion test case - ([b0d6a6c](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/b0d6a6c9b8efefcce99ba88f6a396e0e2848add8)) - clara.bayley
- source files for 2-D motion test case - ([d287973](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/d2879734838f7e7f0995600f4f3b668e2fb009bd)) - clara.bayley
- scripts to run motion 2-D test case - ([0e6dfba](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/0e6dfba32a5f45c1cfb548e51f2cb973c5f1412c)) - clara.bayley
#### Miscellaneous Chores
- update CLEO version for bug fixes: - ([fc5d130](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/fc5d130e89b9514067a8ba60fb993a398be94093)) - clara.bayley
- update CLEO version - ([81b7d88](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/81b7d88f7d403f0081249c2bfb7b3583071ababe)) - clara.bayley
- update CLEO version - ([00adb43](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/00adb435122f6fd8e1cfa98fdc9723d5690b0eb9)) - clara.bayley
#### Performance Improvements
- delete unused variables - ([064b387](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/064b3871add86045f30344dea3775b41c5f3f2b5)) - clara.bayley
- don't include cvode unneeded - ([4b2e89a](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/4b2e89a34dc13fbee01c972453b43180a9b97a59)) - clara.bayley
- remove unneeded comment - ([11a7916](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/11a7916434f9bba666d5ecec7c78d8e00ee64255)) - clara.bayley
#### Refactoring
- print total water mass as sanity check on distribution for collisions - ([06d16e8](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/06d16e8c3465ee44f76d5985859013f8df693950)) - clara.bayley
- remove rspan from initial collisions conditions - ([5408b26](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/5408b26908f583ac865fc9cebfebfd059b51ff65)) - clara.bayley

- - -

## [v0.3.0](https://github.com/yoctoyotta1024/ValidatingCLEO/compare/a8ac779a9a7e605bfdb41df18aa102d82cdf6217..v0.3.0) - 2025-04-17
#### Bug Fixes
- correct name and range of plotting script - ([4591115](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/4591115dfc346cfd37bec030d72545b98f5ac40b)) - clara.bayley
#### Documentation
- doc to explain collisions test case - ([5340cfe](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/5340cfeade5ca28b983f44c1dd2b2776dd504789)) - clara.bayley
- cite arabas and shima 2017 - ([7e3cef2](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/7e3cef2d6276777b02f0fd13b75ffa1388fc4a87)) - clara.bayley
#### Features
- collisions run scripts - ([a7da945](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/a7da945393d8989cf152013707e956db26e1bca2)) - clara.bayley
- source files for collisions test case - ([cf4b3c1](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/cf4b3c176c9179235a854812e5330b13e11dd3b7)) - clara.bayley
#### Miscellaneous Chores
- rename for consistency - ([92901cc](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/92901cc47574ecf14a6636475e0e20337b4addf1)) - clara.bayley
#### Performance Improvements
- correct comment - ([6c5089b](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/6c5089b97661fceadc83a184f1a07df1a5818a8c)) - clara.bayley
#### Refactoring
- edit initconds and add plotting functions for collisions - ([a4f5cee](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/a4f5cee8e718fc20c225b66aff1ba2155fbf8074)) - clara.bayley
- change initial conditions - ([a8ac779](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/a8ac779a9a7e605bfdb41df18aa102d82cdf6217)) - clara.bayley

- - -

## [v0.2.0](https://github.com/yoctoyotta1024/ValidatingCLEO/compare/fca018398bd526034bd4e0e90d794e9b758af992..v0.2.0) - 2025-04-16
#### Bug Fixes
- include observers in cond/evap run - ([a834bed](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/a834bed37dd34c2fcf61d0f8b5d2348182e5f518)) - clara.bayley
- correct typo on zarr base dir param - ([1395fcb](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/1395fcb260bd2682ad2133da63a48e1c3ad27d2a)) - clara.bayley
#### Documentation
- new documentation for cond/evap example - ([be64eeb](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/be64eeb352472d5c65163bd4cd0916a05ea0cc8c)) - clara.bayley
#### Features
- new script to plot results of cond/evap example - ([1e62e77](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/1e62e777f39a9073a073602ca65c7bd037788cb9)) - clara.bayley
- source files for cond/evap test case - ([717e607](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/717e607900a3cb678062e396caede7516e114e32)) - clara.bayley
- new bash scripts to build compile and run test cases - ([64e625e](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/64e625e5038390b5e3bc069ba12dac00bd3ced14)) - clara.bayley
- copy bash scripts from scripts/levante/bash directory in CLEO - ([fca0183](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/fca018398bd526034bd4e0e90d794e9b758af992)) - clara.bayley
#### Miscellaneous Chores
- formatting - ([a74ca60](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/a74ca6041f1cafe6f1bdd9ee92f6f98693838b56)) - clara.bayley
#### Refactoring
- move main program part of initial conditions generation from source into scripts dir - ([78decbf](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/78decbf01584ff5a216e385235d1c51d3867a12b)) - clara.bayley

- - -

## [v0.1.0](https://github.com/yoctoyotta1024/ValidatingCLEO/compare/0e2bbdc2f17d39e210f4714de18bc7d61692ac12..v0.1.0) - 2025-04-11
#### Features
- initial base repository - ([0e2bbdc](https://github.com/yoctoyotta1024/ValidatingCLEO/commit/0e2bbdc2f17d39e210f4714de18bc7d61692ac12)) - clara.bayley

- - -

Changelog generated by [cocogitto](https://github.com/cocogitto/cocogitto).
