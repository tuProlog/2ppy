## [1.7.4](https://github.com/tuProlog/2ppy/compare/1.7.3...1.7.4) (2026-10-22)

### Bug Fixes

* **deps:** update tuprolog to v3.0.4 ([#113](https://github.com/tuProlog/2ppy/issues/113)) ([4f6df15](https://github.com/tuProlog/2ppy/commit/4f6df1545c6a41b0328011ca195bac5de04e4d2a))

## [1.7.3](https://github.com/tuProlog/2ppy/compare/1.7.2...1.7.3) (2026-10-21)

### Dependency updates

* **deps:** update gradle to v9.8.2 ([#112](https://github.com/tuProlog/2ppy/issues/112)) ([2667883](https://github.com/tuProlog/2ppy/commit/2667883753e27ad973ac7d7ae6319d8a91875ec8))

### Bug Fixes

* **deps:** update dependency org.junit:junit-bom to v6 ([#111](https://github.com/tuProlog/2ppy/issues/111)) ([d486a11](https://github.com/tuProlog/2ppy/commit/d486a11c5f0d9c85d35c11f4979fb8f905ec7ca1))

### Build and continuous integration

* **deps:** update docker/setup-buildx-action action to v4 ([#109](https://github.com/tuProlog/2ppy/issues/109)) ([0e3ab40](https://github.com/tuProlog/2ppy/commit/0e3ab40118112fb5675485e79de1531045f3aa0c))
* **deps:** update docker/setup-qemu-action action to v4 ([#110](https://github.com/tuProlog/2ppy/issues/110)) ([7f28c53](https://github.com/tuProlog/2ppy/commit/7f28c53b8bfbdd255d75afb73421118949e98e96))

## [1.7.2](https://github.com/tuProlog/2ppy/compare/1.7.1...1.7.2) (2026-10-21)

### Bug Fixes

* **deps:** update dependency org.junit:junit-bom to v5.14.4 ([#107](https://github.com/tuProlog/2ppy/issues/107)) ([064a7c8](https://github.com/tuProlog/2ppy/commit/064a7c8710f41b72c52940d5dac8597699fa42de))

### Build and continuous integration

* **deps:** update docker/login-action action to v4 ([#108](https://github.com/tuProlog/2ppy/issues/108)) ([5995615](https://github.com/tuProlog/2ppy/commit/59956157bb325a91802da534f236b03494d9baa5))

## [1.7.1](https://github.com/tuProlog/2ppy/compare/1.7.0...1.7.1) (2026-10-19)

### Documentation

* **readme:** explain what to expect from 2PPy, the terminal IDE, and how to install it from PyPI ([76f1459](https://github.com/tuProlog/2ppy/commit/76f1459043663f6a57b5ebadcd86dc149fcb1cc0))

## [1.7.0](https://github.com/tuProlog/2ppy/compare/1.6.0...1.7.0) (2026-10-19)

### Features

* Textual terminal IDE backed by 2P-Kt's GUI core ([#103](https://github.com/tuProlog/2ppy/issues/103)) ([0026da0](https://github.com/tuProlog/2ppy/commit/0026da005b3bb1a1405d9e18d0a8816f19d5e8d8))

## [1.6.0](https://github.com/tuProlog/2ppy/compare/1.5.0...1.6.0) (2026-10-18)

### Features

* **solve.library:** runtime - library removes libraries, by library, alias, or aliases ([e6f4797](https://github.com/tuProlog/2ppy/commit/e6f479726994d841a87da0c9ae6a8ab934f7f2e0))

### Bug Fixes

* check arguments with exceptions instead of assert, which python -O strips ([e960207](https://github.com/tuProlog/2ppy/commit/e9602076fdf51aebb076f84146e7d77370fbd235))
* classes implementing JVM interfaces keep their docstrings, module and name ([32c08e4](https://github.com/tuProlog/2ppy/commit/32c08e47330cd8e3e4f10dbd6fdd96b0f398f523))
* **core:** numeric normalizes reals parsed from strings, e.g. "1e3" is 1000.0, not the unparsable 1E+3.0 ([f0de996](https://github.com/tuProlog/2ppy/commit/f0de9961d9e1e9f32de9c2d7e6393c193b3911b8))
* **core:** substitutions, set_args and insert_at convert Python values into terms ([45503c8](https://github.com/tuProlog/2ppy/commit/45503c8aa2df006b60218477a2e7cc7d66b5c6ae))
* **errors:** let help() and doc tools read the docstrings of tuprolog.errors' classes ([b252f59](https://github.com/tuProlog/2ppy/commit/b252f599dbd3067f17b0e4e1157f7e6705519a6c))
* **errors:** the repr of errors without a message shows their error term, instead of None ([6c34028](https://github.com/tuProlog/2ppy/commit/6c34028657ef48d24210af1322bad44fc1e3464a))
* **repl:** no whitespace-only line after solutions without bindings ([0c508d9](https://github.com/tuProlog/2ppy/commit/0c508d9bc665d4db4a7418296484424fe0c50a0c))
* **solve.flags:** flag stores convert the Python values added as dicts, and raise KeyError for missing flags ([2694320](https://github.com/tuProlog/2ppy/commit/26943209f71cd0366571f621ba96597fac001253))
* **solve.function:** exceptions raised by Python functions become logic errors, as in primitives ([7ec19ed](https://github.com/tuProlog/2ppy/commit/7ec19ed0d115e198a851056b9de02cc389f91652))
* **solve.library:** library accepts any iterable of clauses, e.g. the lazy sequences of parse_clauses ([ad0a6f1](https://github.com/tuProlog/2ppy/commit/ad0a6f1b50caaf5768a6fd3e4c261ee331a4d451))
* **solve.libs:** OOPLib calls method-wrappers named by atoms on Python 3.10 too ([43ffced](https://github.com/tuProlog/2ppy/commit/43ffced4791e857155a65d5f6307eb2dfadd5bae))
* **theory:** abolish accepts "name/arity" strings, and explains that a bare name lacks an arity ([0328b30](https://github.com/tuProlog/2ppy/commit/0328b30fc094693f826965bed4d3eae1aa18d8da))
* **typing:** correct the annotations of term_reader, fact and halt_solution, and make optional parameters explicit ([94e631d](https://github.com/tuProlog/2ppy/commit/94e631d87c91abfe1378cf6ac44aa61d6ca05c07))

### Documentation

* a concise README, and a documentation site organized as 2P-Kt's ([4eaf9f1](https://github.com/tuProlog/2ppy/commit/4eaf9f1d536fd76a53404d428e75ef03c16e5f70))
* document primitives, IOLib and OOPLib (with a user guide), and logic errors ([6973078](https://github.com/tuProlog/2ppy/commit/69730788faa9a75c39e4973852af385a6b0e4a80))
* document the solver API, Prolog and ProbLog solvers, flags, channels, side effects, libraries and the standard library ([710f6cb](https://github.com/tuProlog/2ppy/commit/710f6cbea007f6844519e8d776c373790906bc8f))
* document the tuprolog package, core (terms, operators, parsing), math and utils ([bdf17d4](https://github.com/tuProlog/2ppy/commit/bdf17d4f6e96065ecc0e1d6f7b91dba6464cbdb1))
* document unify, theory, collections, errors, the JVM/IO bridges and the REPLs ([5f4c213](https://github.com/tuProlog/2ppy/commit/5f4c21372d6a60431cdfd296c7fed48ae865ad44))
* example Jupyter notebooks, from terms to probabilistic logic programming ([94549d4](https://github.com/tuProlog/2ppy/commit/94549d4738df1e6352757f29737f54afbfd63f24))
* **examples:** open files by URI in the IOLib example, as Windows paths are not URIs ([8461911](https://github.com/tuProlog/2ppy/commit/8461911662c2379142625e8f7324b9d36057051c))
* **jvmioutils:** annotate the returns of the stream adapters, which griffe requires for Returns sections ([cdd70e8](https://github.com/tuProlog/2ppy/commit/cdd70e87667bbc11e3089929bd6b05856b97fa18))
* publish a documentation site on GitHub Pages, with the API reference generated from the docstrings ([87300f6](https://github.com/tuProlog/2ppy/commit/87300f66e4448732387b5072e12f51b2701e25cb))
* render the example notebooks in the documentation site, and link them from the guides ([9824295](https://github.com/tuProlog/2ppy/commit/9824295b01157effed016e0cee547409f5d2b3f6))
* rewrite the README as a guide with tested examples, and set the docstring conventions ([29c6acf](https://github.com/tuProlog/2ppy/commit/29c6acf2a19013a490c58d62fcbec71cad5ee1f5))

### Refactoring

* use ensure_input_stream instead of its misspelled alias ensure_input_steam, kept for compatibility ([02dcd4d](https://github.com/tuProlog/2ppy/commit/02dcd4d2fba59ed45c535b75cdd930b4f7410179))

## [1.5.0](https://github.com/tuProlog/2ppy/compare/1.4.0...1.5.0) (2026-10-18)

### Features

* **solve.libs:** OOPLib's Prolog API over Python objects ([#102](https://github.com/tuProlog/2ppy/issues/102)) ([5a5df20](https://github.com/tuProlog/2ppy/commit/5a5df206f18586f36a2bfbccac58a8cb7e94d32f))

## [1.4.0](https://github.com/tuProlog/2ppy/compare/1.3.0...1.4.0) (2026-10-18)

### Features

* **typing:** ship py.typed and fully annotate the Python API ([#100](https://github.com/tuProlog/2ppy/issues/100)) ([88410c5](https://github.com/tuProlog/2ppy/commit/88410c549cb6fd6b7d5ab8e229c974eed97906b6))

## [1.3.0](https://github.com/tuProlog/2ppy/compare/1.2.0...1.3.0) (2026-10-18)

### Features

* **errors:** classify 2P-Kt's exceptions with Python exception classes ([#98](https://github.com/tuProlog/2ppy/issues/98)) ([105c62f](https://github.com/tuProlog/2ppy/commit/105c62fef7b3bff972373a3cd4ce7869706a17fd))
* **solve:** Pythonic querying and Python-defined predicates and functions ([#99](https://github.com/tuProlog/2ppy/issues/99)) ([9c9711d](https://github.com/tuProlog/2ppy/commit/9c9711d07ca53d6b175b2178ff225ecd4418bc03))

## [1.2.0](https://github.com/tuProlog/2ppy/compare/1.1.1...1.2.0) (2026-10-18)

### Features

* **io:** wrap IOLib, and adapt 2ppy to accept Python streams wherever 2P-Kt reads or writes ([#97](https://github.com/tuProlog/2ppy/issues/97)) ([4e79c8d](https://github.com/tuProlog/2ppy/commit/4e79c8d096a819f9888e35d3245a9a60a19d6396))

## [1.1.1](https://github.com/tuProlog/2ppy/compare/1.1.0...1.1.1) (2026-10-18)

### Bug Fixes

* **deps:** update dependency it.unibo.tuprolog:solve-problog-jvm to v3.0.3 ([#94](https://github.com/tuProlog/2ppy/issues/94)) ([649cc34](https://github.com/tuProlog/2ppy/commit/649cc34af6eae96e76a6668e1f1cd331520bbe99))

## [1.1.0](https://github.com/tuProlog/2ppy/compare/1.0.0...1.1.0) (2026-10-18)

### Features

* **collections:** wrap it.unibo.tuprolog.collections ([5fdf5c0](https://github.com/tuProlog/2ppy/commit/5fdf5c07fc2ef30ec301f90fe44cbbbffd235379)), closes [#14](https://github.com/tuProlog/2ppy/issues/14)

## [1.0.0](https://github.com/tuProlog/2ppy/compare/0.4.1...1.0.0) (2026-10-18)

### ⚠ BREAKING CHANGES

* star-imports export only __all__; domain(), type() and
permission() are renamed; tuprolog.solve.plp.solve_options takes
probabilistic as a keyword argument only.
* requires 2P-Kt 3.x; Scope.empty_list is now
Scope.empty_logic_list; FlagStore.DEFAULT holds 8 notable flags; parse
error messages changed.

### Features

* align with 2P-Kt 3.0.1 ([8292528](https://github.com/tuProlog/2ppy/commit/8292528ddfb25b99107d4aeb5dc26239b833bc35)), closes [tuProlog/2p-kt#859](https://github.com/tuProlog/2p-kt/issues/859) [tuProlog/2p-kt#242](https://github.com/tuProlog/2p-kt/issues/242)
* convert Python values at the API boundary, iterate anonymous JVM iterables ([458fb00](https://github.com/tuProlog/2ppy/commit/458fb002358e5ecc7f37b79a7fb4ba6453f64f12))
* declare __all__ everywhere, stop shadowing builtins and subpackages ([a49df7d](https://github.com/tuProlog/2ppy/commit/a49df7de5c024ceda17b9491230d3c6aaa6a51a3))
* REPL directives and probabilities, PLP decision diagrams, type_error_for_term ([c469126](https://github.com/tuProlog/2ppy/commit/c469126bfefe4a7b637830aa20efca7965097c2c))

### Dependency updates

* **deps:** update dependency coverage to v7.3.4 ([#54](https://github.com/tuProlog/2ppy/issues/54)) ([6b7a2e0](https://github.com/tuProlog/2ppy/commit/6b7a2e0d3610c4d863d5226ed7e93f84eb2e90f4))
* **deps:** update dependency it.unibo.tuprolog:repl-jvm to v0.31.21 ([#59](https://github.com/tuProlog/2ppy/issues/59)) ([ad278d8](https://github.com/tuProlog/2ppy/commit/ad278d808c02f0d7917e311ea321b56fcf54d6ad))
* **deps:** update dependency it.unibo.tuprolog:solve-problog-jvm to v0.31.21 ([#63](https://github.com/tuProlog/2ppy/issues/63)) ([b730113](https://github.com/tuProlog/2ppy/commit/b730113766c0f2a8c45b6cd14c2ea47f498bbf9d))
* **deps:** update dependency jdk4py to v17.0.9.2 ([#65](https://github.com/tuProlog/2ppy/issues/65)) ([1567fd4](https://github.com/tuProlog/2ppy/commit/1567fd4d2be47449a715b328917116ac72889b85))
* **deps:** update dependency org.jetbrains.kotlin:kotlin-bom to v1.9.25 ([#66](https://github.com/tuProlog/2ppy/issues/66)) ([0434e8a](https://github.com/tuProlog/2ppy/commit/0434e8a0dbea7667d6f2c0cf5963f22fba6ede38))

### Bug Fixes

* apply interface customizers to the classes redeclaring their methods ([98173de](https://github.com/tuProlog/2ppy/commit/98173de9af832a7fcb57d017e0de60605a8de13c))
* **channel:** honour output_store(channels=...) without standard channels ([7dded59](https://github.com/tuProlog/2ppy/commit/7dded5909e42daef9c61cf30522f6d26bbe25d14))
* **channel:** make listener() return a Listener ([af7a82e](https://github.com/tuProlog/2ppy/commit/af7a82e5ce80b948188a74c6ca1d151cb1386121))
* **channel:** pass Python strings to output_channel consumers ([41f0c3d](https://github.com/tuProlog/2ppy/commit/41f0c3df3fbfeb3f5da5afdcbfff8d83c6309951))
* **core:** accept mixed Python/term arguments in indicator ([a15c4b5](https://github.com/tuProlog/2ppy/commit/a15c4b556e54096681e6652dcc78ba9094f3de8f))
* **core:** call the vararg-only Scope.clauseOf/directiveOf/ruleOf with unpacked items ([c5b2451](https://github.com/tuProlog/2ppy/commit/c5b2451ff29884966a34c3ee6b18df6ba65c6ccb))
* **core:** default_formatter shows tags by default, like 2P-Kt's TermFormatter.default ([fac3dff](https://github.com/tuProlog/2ppy/commit/fac3dff0bcf4be0d48c89f796a8c033af2b352b2))
* **core:** drop the shadowed and broken Substitution.filter override ([95fa1d3](https://github.com/tuProlog/2ppy/commit/95fa1d3d6c70590f46cbf0b8592835bb135d912f))
* **core:** forward the collection in set_args, set_head_args and set_body_items ([28c1397](https://github.com/tuProlog/2ppy/commit/28c13977dc47e1f4893895a07b6757891a176e40))
* **core:** make Clause.insert_head_arg call the existing insertHeadArg ([20bb6b6](https://github.com/tuProlog/2ppy/commit/20bb6b6b9580952643e3da2279e1ae397addc548))
* **core:** make Recursive.__len__ a method, so that len() works on lists, tuples, blocks ([b229c8b](https://github.com/tuProlog/2ppy/commit/b229c8b7be762488386c2a9dc0d5e9bae5d03af3))
* **core:** make Scope.real build reals and Scope.numeric support big numbers ([85619a4](https://github.com/tuProlog/2ppy/commit/85619a45644fd03697074433c198a23b805f6b9e))
* **core:** make Struct.insert_at call insertAt instead of addFirst ([d70f90f](https://github.com/tuProlog/2ppy/commit/d70f90f9ec6cbd6da013f34faa556b690895f3b8))
* **core:** raise TypeError from specifier on non-string, non-term arguments ([c599d84](https://github.com/tuProlog/2ppy/commit/c599d8496a47c19cf27277ca494bf85a4bd0fa4e))
* **core:** support tuple indices in Term.__getitem__ ([1755e18](https://github.com/tuProlog/2ppy/commit/1755e18840602054deeb33d7bbb9bafee8ac1513))
* **data:** make EMPTY_DATA an immutable empty map ([18c0334](https://github.com/tuProlog/2ppy/commit/18c03345c05445ad3a324e5cc0b4150e1915b18c))
* **deps:** update dependency it.unibo.tuprolog:repl-jvm to v3.0.3 ([#93](https://github.com/tuProlog/2ppy/issues/93)) ([249004e](https://github.com/tuProlog/2ppy/commit/249004ef21b5719b826aef367bce976e19469ba5))
* **exception:** accept lower-case names in error_type() ([06f0a5f](https://github.com/tuProlog/2ppy/commit/06f0a5f85dc49dc46032ddacca97277daab2fb4a))
* **exception:** alias SystemError to the JVM SystemError, not SyntaxError ([52beda8](https://github.com/tuProlog/2ppy/commit/52beda8788e0276a11e8efb00bc1c7a5c244920d))
* **exception:** box the optional index of error factories as java.lang.Integer ([8c8373a](https://github.com/tuProlog/2ppy/commit/8c8373a4106edcea5b874dcac11edd267bae55f1))
* **exception:** call MessageError's companion of() in message_error ([cd2980f](https://github.com/tuProlog/2ppy/commit/cd2980ff256f7c932c0d94fc1dad2f857a40512d))
* **exception:** make system_error call the existing SystemError factories ([358c65c](https://github.com/tuProlog/2ppy/commit/358c65ce8636f787d4888da29d056c3e3df39550))
* **exception:** make type() look up TypeError.Expected, not TypeError ([243daae](https://github.com/tuProlog/2ppy/commit/243daae3d614efa3be016dadf7f955bfcb8a359f))
* **exception:** name DOMAIN_ATOM_PROPERTY and DOMAIN_DIRECTIVE consistently ([1e99461](https://github.com/tuProlog/2ppy/commit/1e994616f74e4c54beef1ecc3a570bea9cbe2e95))
* **exception:** replace broken type_error_for_flag_values with type_error ([9d156fe](https://github.com/tuProlog/2ppy/commit/9d156fe46820d1b16520f2d0e955d8b3c5ac8dc9))
* **flags:** let 'in' look up notable flags in a FlagStore ([58914ce](https://github.com/tuProlog/2ppy/commit/58914ce70082725551f70851228e0d59de51f6df))
* **flags:** let FlagStore + accept Python dicts ([eebd9cf](https://github.com/tuProlog/2ppy/commit/eebd9cf66f7b2364dd52f308ebe3db5c282aa8b5))
* **flags:** merge flag_store() arguments in order, accepting dicts ([e732da3](https://github.com/tuProlog/2ppy/commit/e732da37784ca8e39cf7e75e15a61d437e658a75))
* **flags:** validate the (name, value) pairs given to flag() ([e7b5194](https://github.com/tuProlog/2ppy/commit/e7b5194015286a5e26c18d2290b16eb574273a9b))
* **function:** alias ComputeResponse to Compute.Response ([34a8909](https://github.com/tuProlog/2ppy/commit/34a8909639f18918308eebf183c830cf94db3e39))
* **function:** box the argument index of eval_as_expression ([5e00663](https://github.com/tuProlog/2ppy/commit/5e00663ddd7088087acfe9b98f35bfa05a3fd77d))
* **function:** convert compute_request arguments to a JVM list ([1f9033e](https://github.com/tuProlog/2ppy/commit/1f9033e9a2afbd7de67b8cb3390d598f93aa2a66))
* **function:** make logic_function() return a LogicFunction ([f587e75](https://github.com/tuProlog/2ppy/commit/f587e75fbe9681f40e069a0d008dc32f6b1b7bb7))
* input/output stores with channels, compute_request default, system_error ([78cf01a](https://github.com/tuProlog/2ppy/commit/78cf01a9cbae46bc157f2cc458b4ea943d3245be))
* **jvmioutils:** accept the lines argument in InputStream.writelines ([34c20ca](https://github.com/tuProlog/2ppy/commit/34c20ca0e6def3e0ad9ac9cdc24921baef398d37))
* **jvmioutils:** build the TypeError message of ensure_input_steam correctly ([b2de366](https://github.com/tuProlog/2ppy/commit/b2de366ea914e1b3615e23392071b9f46482c3da))
* **jvmioutils:** combine UTF-16 surrogate pairs in InputStream.readline ([fb4fd70](https://github.com/tuProlog/2ppy/commit/fb4fd704da7e6e825e7849e46be28c06712bc603))
* **jvmioutils:** implement readline, readlines and iteration on InputStream ([d41a153](https://github.com/tuProlog/2ppy/commit/d41a153ae19f5434c4fb65321da814bd789e939f))
* **jvmutils:** make automatic snake_case accessors virtual and non-shadowing ([b04df92](https://github.com/tuProlog/2ppy/commit/b04df9264af60cfa8f6456efae0e0ad50e880145))
* **jvmutils:** make jiterable re-iterable for one-shot iterators ([66d1fbc](https://github.com/tuProlog/2ppy/commit/66d1fbc512a60c69cc70b76e8f9e99d69700f21a))
* **jvmutils:** raise ValueError from kpair/ktriple on wrong-sized iterables ([67492a2](https://github.com/tuProlog/2ppy/commit/67492a245dee29d0ab9a714ffe31b3a518d2c418))
* library aggregation, side effects, solve adapters and REPL on 0.31.16 ([2df74b0](https://github.com/tuProlog/2ppy/commit/2df74b027c6827303176a53a85d7250c156290c7))
* **library:** accept any iterable of operators in library() ([6d89145](https://github.com/tuProlog/2ppy/commit/6d891456c2da568806b25f01ffaa21184258ff9d))
* **library:** preserve the order of libraries given to libraries() ([a5c328f](https://github.com/tuProlog/2ppy/commit/a5c328f2fa206a38229259f5302c580c3ef6396a))
* **library:** validate the arguments of libraries() and accept runtimes ([a409331](https://github.com/tuProlog/2ppy/commit/a409331d4bead413ce52cc7cb29e7222ea6d4885))
* **libs:** actually check that the JVM library found in JAVA_HOME exists ([80ba6b7](https://github.com/tuProlog/2ppy/commit/80ba6b7f46b142de1d4336a628776efb43f84915))
* **math:** accept BigInteger and bool values in big_integer ([15df818](https://github.com/tuProlog/2ppy/commit/15df818770382379f147afd80f8fee8da0b31d1e))
* **math:** avoid negative scales in big_decimal ([da5d679](https://github.com/tuProlog/2ppy/commit/da5d679c58d4a3c8eb0120d9bcd4a9d07a9b4a25))
* **math:** raise TypeError instead of AssertionError on invalid arguments ([0e7e844](https://github.com/tuProlog/2ppy/commit/0e7e84499a1696ffd7789e1f3ed9f333793e4787))
* **primitive:** compute solve_request's default issuing instant at call time ([1e034e4](https://github.com/tuProlog/2ppy/commit/1e034e4cf4ecd9abafb8285366803684f0f09ed7))
* **primitive:** convert solve_request arguments to a JVM list ([032cbb5](https://github.com/tuProlog/2ppy/commit/032cbb513d5ae36aab35465702c08e34f5c6e7fd))
* **primitive:** let request.solve() default to the request's remaining time ([f687943](https://github.com/tuProlog/2ppy/commit/f6879438366ca60f92bd4e574987c3e820ed56d7))
* **primitive:** make primitive() return a Primitive ([0fad155](https://github.com/tuProlog/2ppy/commit/0fad15571739b4ae181545f168a6c8990b8ec6e2))
* **primitive:** make Solve.Request replies usable from Python ([5cb1e0c](https://github.com/tuProlog/2ppy/commit/5cb1e0c2de33048dbc54db7e94e8092a8b7a5fcc))
* **primitive:** wrap PrimitiveWrapper.ensuringArgumentIsWellFormedList ([1c273cb](https://github.com/tuProlog/2ppy/commit/1c273cb6f4152a7e1b59f55c04208a3cd021f327))
* **pyutils:** do not split a single string argument in iterable_or_varargs ([11949d2](https://github.com/tuProlog/2ppy/commit/11949d2036bb02c8afba3a39766c17164db2b252))
* **repl:** accept whitespace after the final full stop ([ecd3e99](https://github.com/tuProlog/2ppy/commit/ecd3e9931b4554b982925ea4d375d5c335622ad3))
* **repl:** exit on halt/0 and halt/1, as 2P-Kt's REPL does ([a0793b7](https://github.com/tuProlog/2ppy/commit/a0793b7759d8b6dd84818fd7546cdb27eb07eb3e))
* **repl:** ignore blank lines outside multi-line input ([9f1874f](https://github.com/tuProlog/2ppy/commit/9f1874f04bcf175c345b7e4ac06f936ecdc7fec3))
* **repl:** parse and format with the solver's current operators ([dd74f28](https://github.com/tuProlog/2ppy/commit/dd74f28b8e6c62815f3e9a615f628eb08f04f067))
* **repl:** report clauses the solver rejects instead of crashing ([7c304a6](https://github.com/tuProlog/2ppy/commit/7c304a6e51137bc5fc6a1c8f38fc025c130c80fc))
* **shell:** drop the input() call after the interactive console exits ([156de04](https://github.com/tuProlog/2ppy/commit/156de04b78744de8fa68063c11c1ba5cb2ce10ff))
* **shell:** expose the core Atom, Var, Integer, Clause, rule and primitive ([7e25cf4](https://github.com/tuProlog/2ppy/commit/7e25cf45f5f140a6ef42f3dda412497e88ab0faa))
* **sideffects:** pass on_top to AddStaticClauses and AddDynamicClauses ([09fe271](https://github.com/tuProlog/2ppy/commit/09fe271dbdb09d80e8a9682e59cf03e0e7068c5e))
* **solve.flags:** flag_store materializes one-shot iterators once ([59ecbc4](https://github.com/tuProlog/2ppy/commit/59ecbc4ab7c400306681d7c1e1891bd96a470b5f))
* **solve:** add the missing value parameter to plp.set_probability ([79f3232](https://github.com/tuProlog/2ppy/commit/79f32322d075d1de185dbf0dcd7e94761a435ae9))
* **solve:** build signatures from indicators and signature terms ([916a39c](https://github.com/tuProlog/2ppy/commit/916a39c6895cb14e891b8b3caa06f382dbf643c1))
* **solve:** complete the SolveOptions mapping protocol ([e295fff](https://github.com/tuProlog/2ppy/commit/e295fff9f002efc644d00193b89a376b2955a0f9))
* **solve:** make load_static_clauses/load_dynamic_clauses work with varargs and iterables ([2dc0826](https://github.com/tuProlog/2ppy/commit/2dc0826c517b64759dac552468fc3a25ec76e06f))
* **theory:** default operators to None in ClausesParser/ClausesReader adapters ([6dc0c0e](https://github.com/tuProlog/2ppy/commit/6dc0c0e9d7b5a055e699f00837c3f7e8c260e60c))
* **theory:** keep mutable theories unhashable ([c8f993e](https://github.com/tuProlog/2ppy/commit/c8f993e190105ca75a61a505227a2c92d86107e6))
* **theory:** make assert_a/assert_z return the resulting theory and accept any iterable ([3b3897a](https://github.com/tuProlog/2ppy/commit/3b3897ad38154f1ed6d76d7d12c34a4115876d39))
* **theory:** make theories hashable ([b2ff830](https://github.com/tuProlog/2ppy/commit/b2ff830ff8b5f433bd25407aa3b89dcd4fee5435))

### Tests

* **channel:** cover Python-backed channels plugged into solvers ([2a0fa02](https://github.com/tuProlog/2ppy/commit/2a0fa026ade830773ea4723a0a037ce2bb834a23))
* **core:** cover operators and parsing APIs and adapters ([c8f9206](https://github.com/tuProlog/2ppy/commit/c8f920695d7d5cb6647aa66ca0f0143efb243650))
* **core:** cover the factory functions, adapters and re-exported definitions ([a754315](https://github.com/tuProlog/2ppy/commit/a754315820cbeea14a816a5172f044f07653db67))
* cover jvmutils, pyutils, jvmioutils, libs and package metadata ([9990ce3](https://github.com/tuProlog/2ppy/commit/9990ce3680fb6a5f5836a2391986ba64a457a0c8))
* drop the xfail marks of defects fixed by other merged fixes ([63f8448](https://github.com/tuProlog/2ppy/commit/63f84487f84ddf7deb7f759e777f5e61b5291f21))
* drop xfails fixed by merged fixes; run pytest without faulthandler ([77f8760](https://github.com/tuProlog/2ppy/commit/77f8760f87f91684caeff76b186bf9da717ef17a))
* **exception:** cover logic errors, warnings, base and library/unify exceptions ([07cb580](https://github.com/tuProlog/2ppy/commit/07cb580f0553c499f02732ef2deaa6e8866a49be))
* **flags:** cover flag stores given to solvers and the unknown flag ([6fd58d7](https://github.com/tuProlog/2ppy/commit/6fd58d7fa9c34bf24b40c28a9362e89cd156cb37))
* import every tuprolog module and check star-import collisions ([6c65b5d](https://github.com/tuProlog/2ppy/commit/6c65b5db1f0bbf1830456564df376e7e30272014))
* **jvmioutils:** write the fixture file with LF line endings on every OS ([cf4bb90](https://github.com/tuProlog/2ppy/commit/cf4bb902045fb9993aa9aff6f5d15713aab51741))
* **library:** cover library(), Library/Runtime customizers and libraries in solvers ([3f47a84](https://github.com/tuProlog/2ppy/commit/3f47a84b3370c9396f2e510c517f86f0ea3fb47d))
* **math:** cover big number conversions, rounding modes and error paths ([b8c290e](https://github.com/tuProlog/2ppy/commit/b8c290e2f082bda07b6d3c11e7affc5baa6bb400))
* merge the core/unify/math/utils test suite ([ce78891](https://github.com/tuProlog/2ppy/commit/ce788914030b5d83b96b4ccb50ce3c6765a718c3))
* merge the exception/repl/import-surface test suite ([b6177b6](https://github.com/tuProlog/2ppy/commit/b6177b686ba7ee8b1b31ef2e31ab6cce36686d53))
* merge the solver-extension test suite ([ffa7094](https://github.com/tuProlog/2ppy/commit/ffa7094ba01fb6e0f7f85613fe521a12b5bcf221))
* merge the theory/solve test suite ([a4b43bd](https://github.com/tuProlog/2ppy/commit/a4b43bde2b25a4f288f1108dd58b7fadf4f23917))
* **primitive:** cover ensuring_* checks, permissions and their end-to-end errors ([cbfa7bc](https://github.com/tuProlog/2ppy/commit/cbfa7bcb6cfb5604cf1e7ab45b7d02be9b8748ae))
* **repl:** check the python -m entry points of the shell and the REPLs ([5eefc4c](https://github.com/tuProlog/2ppy/commit/5eefc4c3c7cf839cf5016011818efd1acf71c9c5))
* **repl:** drive PrologREPL with scripted input ([9929c1d](https://github.com/tuProlog/2ppy/commit/9929c1d0c7e46d85f52af801adf9399d53d264e8))
* **sideffects:** cover flag, data, library, operator and channel side effects end to end ([1f83547](https://github.com/tuProlog/2ppy/commit/1f835471a1ae2c51f5e9e3f9d1b1a91bec312945))
* **solve:** cover Prolog solving end to end ([54406b6](https://github.com/tuProlog/2ppy/commit/54406b6d3ca17539495dc682e7c95df7b499f52a))
* **solve:** cover the solve API, solver adapters, solutions, ProbLog and PLP ([4b86e06](https://github.com/tuProlog/2ppy/commit/4b86e06ad502266c36cbe44feaecb01d0e2273c2))
* **solve:** cover the stdlib primitive, function, rule and magic singletons ([4f90a57](https://github.com/tuProlog/2ppy/commit/4f90a576aaf12af15f041ebc8d6c1f15b63394be))
* **theory:** cover the theory factories, adapters and parsing API ([7cc3298](https://github.com/tuProlog/2ppy/commit/7cc32980a0428e2c3d68e4b9104e1c0c7231c4b7))
* **theory:** do not depend on variable numbering in theory string checks ([545854b](https://github.com/tuProlog/2ppy/commit/545854b89b82a75e68682ca677cea84a85f49385))
* **unify:** cover unification API, unificators and exceptions ([0665a0b](https://github.com/tuProlog/2ppy/commit/0665a0bd067724fc8dd6e99e3ba296bc4eaad8eb))

### Build and continuous integration

* adopt template-python-project-uv ([45e84b3](https://github.com/tuProlog/2ppy/commit/45e84b3a5644677fb938d393d2695c2db5fd48f6))
* bump retired GitHub Actions versions ([6111cb9](https://github.com/tuProlog/2ppy/commit/6111cb98204c3e18200c2fc94237442db460f01c))
* **deps:** update actions/setup-java action to v6 ([#83](https://github.com/tuProlog/2ppy/issues/83)) ([6418454](https://github.com/tuProlog/2ppy/commit/64184542f5dc61d2cbd67e94ed11c26a2976ae92))
* **deps:** update dependency java-jdk to v25 ([#84](https://github.com/tuProlog/2ppy/issues/84)) ([136eb9f](https://github.com/tuProlog/2ppy/commit/136eb9fd3a32624391b976259444a14b10dc1f58))
* **release:** make semantic-release itself dry-run when RELEASE_DRY_RUN is set ([073cfdd](https://github.com/tuProlog/2ppy/commit/073cfdda825521267e3c4cbf9ac83da3b05957dc))

### Style improvements

* **jvmutils:** sort imports ([d50f51c](https://github.com/tuProlog/2ppy/commit/d50f51cbb140ef0a73b43b5a5b74244a6502dbbb))
* **solve:** satisfy ruff SIM401 in SolveOptions.get ([0597510](https://github.com/tuProlog/2ppy/commit/0597510e633173e6c7534ab29ffd80ba2d30913a))

### Refactoring

* make the static checks pass (ruff, ruff format, mypy) ([4fa814a](https://github.com/tuProlog/2ppy/commit/4fa814a7410fe8b2cfef70801435f79713062188))
