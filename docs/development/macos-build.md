# Native macOS build baseline

This procedure builds an unmodified Apple Silicon LibreOffice development app. It intentionally adds no Erdem Office branding or features; that clean baseline is the prerequisite for later work.

## Pinned source

| Item | Value |
| --- | --- |
| LibreOffice tag | `libreoffice-26.2.5.2` |
| Commit | `cd7284b4cbbfeb507e630c1aac019f4157393acb` |
| Architecture | Apple Silicon (`arm64`) |
| Minimum deployment target | macOS 11.0 |

Keep the source path short, without spaces. LibreOffice's macOS build currently requires a source path of no more than eight characters; this build uses `~/eo`. Allow at least 25 GB of free disk space.

## Prerequisites

LibreOffice's current build documentation requires macOS 13.3 or newer.

1. Install Xcode, launch it once, accept the licence, and make it the active developer directory.
2. Install [Homebrew](https://brew.sh/) if it is not already available.
3. Install JDK 17:

```sh
brew install openjdk@17
```

LODE supplies pinned private copies of the remaining build utilities. Set it up outside the source tree:

```sh
git clone https://gerrit.libreoffice.org/lode ~/lode
cd ~/lode
./setup --prereq
./setup
```

`./setup --prereq` reports unsupported host configuration. `./setup` downloads and builds the tools under `~/lode/opt`; it does not require modifying shell startup files.

## Source checkout

Clone the fork into the short path and detach at the pinned upstream tag:

```sh
git clone https://github.com/American-University-of-Mongolia/erdem-office.git ~/eo
cd ~/eo
git checkout --detach libreoffice-26.2.5.2
git rev-parse HEAD
```

The final command must print `cd7284b4cbbfeb507e630c1aac019f4157393acb`.

## Configure

The reference build is a developer build with assertions and ccache enabled. It uses LODE's tools, Homebrew's JDK 17, and a Python installed by `uv`:

```sh
cd ~/eo
export ERDEM_JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export ERDEM_PYTHON="$HOME/.local/share/uv/python/cpython-3.11-macos-aarch64-none/bin/python3.11"
export ERDEM_BUILD_PATH="$HOME/lode/opt/bin:$HOME/lode/opt/ant/bin:/opt/homebrew/opt/openjdk@17/bin:$(dirname "$ERDEM_PYTHON"):/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

set -o pipefail
env JAVA_HOME="$ERDEM_JAVA_HOME" PYTHON="$ERDEM_PYTHON" PATH="$ERDEM_BUILD_PATH" \
  ./autogen.sh \
  --enable-dbgutil \
  --enable-ccache \
  --with-jdk-home="$ERDEM_JAVA_HOME" \
  --with-junit="$HOME/lode/opt/share/java/junit.jar" \
  2>&1 | tee "$HOME/eo-autogen.log"
```

Configuration should report `CPUNAME=AARCH64`, `ENABLE_DBGUTIL=TRUE`, `VCLplugs=osx`, and `LibreOfficeDev 26.2.5.2`.

## Build

```sh
cd ~/eo
set -o pipefail
caffeinate -dimsu env \
  JAVA_HOME="$ERDEM_JAVA_HOME" \
  PYTHON="$ERDEM_PYTHON" \
  PATH="$ERDEM_BUILD_PATH" \
  "$HOME/lode/opt/bin/make" 2>&1 | tee "$HOME/eo-build.log"
```

LODE's GNU Make invokes a ten-job build automatically on the ten-core reference Mac. The resulting app is `~/eo/instdir/LibreOfficeDev.app`. Subsequent builds use the same environment and `make` command, and are incremental.

## Verify the app

Confirm that the executable is native Apple Silicon:

```sh
file ~/eo/instdir/LibreOfficeDev.app/Contents/MacOS/soffice
lipo -archs ~/eo/instdir/LibreOfficeDev.app/Contents/MacOS/soffice
~/eo/instdir/LibreOfficeDev.app/Contents/MacOS/soffice --version
```

Launch each main module and confirm that a new document appears:

```sh
open -n ~/eo/instdir/LibreOfficeDev.app --args --writer
open -n ~/eo/instdir/LibreOfficeDev.app --args --calc
open -n ~/eo/instdir/LibreOfficeDev.app --args --impress
```

Run the automated filter smoke test from a separate checkout of this repository (not the `~/eo` source worktree):

```sh
uv run python scripts/macos-format-smoke.py \
  ~/eo/instdir/LibreOfficeDev.app/Contents/MacOS/soffice
```

The test creates and opens Writer, Calc, and Impress documents; saves ODT/DOCX, ODS/XLSX, and ODP/PPTX; round-trips every saved file back through its module; and validates Writer PDF export. It uses a temporary isolated LibreOffice profile and removes its test files afterward.

## Confirm source cleanliness

Build output is ignored by the upstream repository. Confirm that the pinned source itself did not change:

```sh
cd ~/eo
git status --short --untracked-files=no
git diff --exit-code libreoffice-26.2.5.2 -- .
```

Both commands should produce no output.

## Expected configuration notes

- `.NET` support is disabled when the optional `dotnet` command is absent.
- Compiler plugins are disabled when the optional Clang plugin headers are absent.
- The legacy Bluetooth Impress Remote API is unavailable on current macOS and is disabled.
- Apple's linker can print non-fatal probe warnings for long placeholder response-file paths. A successful target immediately after the warning confirms that it was a capability probe, not a failed product link.

These notes describe the unmodified baseline. Do not suppress them with source changes.

## Verified reference run

Issue [#1](https://github.com/American-University-of-Mongolia/erdem-office/issues/1) was verified on 2026-08-23 with:

| Item | Result |
| --- | --- |
| Mac | `Mac17,3`, 10 CPU cores, 24 GB RAM |
| Host | macOS 26.6.2 (25G83) |
| Toolchain | Xcode 26.6 (17F113), macOS SDK 26.5 |
| Full configure and build | Passed; 1 hour 27 minutes including source-archive downloads |
| Product binary | Mach-O 64-bit `arm64`; `LibreOfficeDev 26.2.5.2 cd7284b...` |
| Visible module processes | Writer, Calc, and Impress each launched and registered with macOS, then exited cleanly |
| Format smoke test | Passed ODT, DOCX, PDF, ODS, XLSX, ODP, and PPTX creation and round trips |
| Source integrity | No tracked status or diff from `libreoffice-26.2.5.2` |
| Build storage | 11 GB `workdir`, 1.3 GB `instdir` |

The development app is ad-hoc signed with the upstream identifier `org.libreoffice.script`. Distribution signing, notarization, and release packaging are deliberately deferred to [#13](https://github.com/American-University-of-Mongolia/erdem-office/issues/13).
