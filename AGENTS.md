# PyAutoCTI — Agent Instructions

Canonical, agent-agnostic instructions for this repo. `CLAUDE.md` imports this
file; any tool that does not process `@`-imports should read this directly.

## What this repo is

**PyAutoCTI** (package `autocti`) is a Bayesian library for calibrating and
modelling Charge Transfer Inefficiency (CTI) in CCD imaging: charge-injection
imaging (`ImagingCI`) and 1D datasets (`Dataset1D`), trap/CCD models clocked
through the C++ **arctic** code (`Clocker1D`/`Clocker2D` wrapping `arcticpy`),
FPR/EPER extraction (`autocti/extract/`), and per-dataset `Fit*`/`Analysis*`
classes. Heritage: Euclid VIS CTI calibration; also HST ACS
(`autocti/instruments/acs`).

Dependency direction: autocti may import **autoarray** (data structures),
**autofit** (model-fitting), and **autoconf** (config). Nothing in the PyAuto
stack imports autocti — it is a leaf like PyAutoLens.

## Resurrection status (2026-07)

This repo was unmaintained for ~2 years and is being brought back into the
ecosystem via the CTI resurrection epic
([PyAutoCTI#82](https://github.com/PyAutoLabs/PyAutoCTI/issues/82)). Phase 0
(importable + unit tests green on the current stack) and Phase 1 (the
visualization layer rewritten on the matplotlib **function API**, mirroring
PyAutoGalaxy: per-domain `plot/*_plots.py` function modules, config-gated
`model/plotter.py` orchestrators, `autocti/util/plot_utils.py` helpers) are
complete. Remaining: Phase 2 autofit sync (5 aggregator tests skipped pending
the `AnalysisFactor`/`FactorGraphModel` port), Phase 3 CI + ecosystem
plumbing, Phase 4 workspace update, Phase 5 workspace_test rebuild + release.

## arcticpy (read before installing)

`import autocti` requires **arcticpy** (pinned 2.6), which is deliberately not
a pip dependency:

- Its PyPI sdist is **source-only C++** — it needs `libgsl-dev` headers and a
  toolchain to build.
- Its own requirements **downgrade numpy below 2.0**, breaking a modern stack.

Install it after numpy is in place:

```bash
pip install arcticpy==2.6 --no-build-isolation --no-deps
```

If GSL headers are missing and you lack root, extract them locally
(`apt-get download libgsl-dev && dpkg -x ...`) and point `CPPFLAGS`/`LDFLAGS`
at them.

## Quick commands

```bash
pip install -e ".[dev]"                                  # install with dev/test extras
python -m pytest test_autocti/                           # full test suite
python -m pytest test_autocti/extract/                   # one focused directory
```

In a sandboxed / restricted environment, point numba and matplotlib at
writable caches:

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib python -m pytest test_autocti/
```

## Related repos

- **Source siblings:** PyAutoConf, PyAutoArray, PyAutoFit (upstream).
- **autocti_workspace** — runnable examples/tutorials (updated in epic Phase 4).
- **autocti_workspace_test** — regression scripts + Euclid tvac/temporal
  heritage (rebuilt in epic Phase 5).
- **Science context:** `PyAutoMemory/wiki/cti/` (trap physics, arctic
  algorithm, Euclid VIS / HST ACS heritage).

## Public API

The public surface is defined authoritatively in `autocti/__init__.py` — read
it rather than trusting a hand-maintained table. Canonical import:

```python
import autocti as ac
```

## Key rules / footguns

- Import direction: autoarray / autofit / autoconf only — never autogalaxy or
  autolens.
- Unit tests are numpy-only; there is no JAX in this library (arctic is C++).
- Slicing an autoarray `Mask2D` returns a plain ndarray — rebuild a `Mask2D`
  with the parent's `pixel_scales` before constructing an `Array2D` from it
  (see `autocti/extract/two_d/abstract.py`).
- Fits I/O goes through `autoconf.fitsable` (`ndarray_via_fits_from`,
  `output_to_fits`, `hdu_list_for_output_from`) — instance `.output_to_fits`
  methods no longer exist on autoarray structures.
- All files use Unix line endings (LF, `\n`) — never `\r\n`.

## Working on issues

1. Read the issue description and any linked plan.
2. Identify affected files and make the change.
3. Run the full suite: `python -m pytest test_autocti/`.
4. If you changed public API, say so explicitly — autocti_workspace may need
   updates.
5. Ensure all tests pass before opening a PR.

## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
