# AGENTS.md

This file contains public instructions for coding agents working on Erdem Office.
Human contributors should also read [CONTRIBUTING.md](CONTRIBUTING.md) before
making changes.

## Project

Erdem Office is a free, Mongolian-focused office suite from the American
University of Mongolia. It is based on LibreOffice and aims to improve
Mongolian localization, typography, accounting formats, templates, traditional
Mongolian script support, and assisted conversion between Cyrillic and
traditional Mongolian script.

This repository is a fork of `LibreOffice/core`. LibreOffice's GitHub
repository is a read-only mirror; generally useful LibreOffice changes are
submitted upstream through LibreOffice Gerrit. Erdem-specific integration and
packaging changes are reviewed in this repository.

## Before Making Changes

1. Read the relevant issue and confirm the requested scope and acceptance
   criteria.
2. Read the nearest module `README.md` and any more specific `AGENTS.md` in the
   directory being changed.
3. Check whether the work belongs in Erdem Office, an extension or template
   package, or upstream LibreOffice.
4. Identify the smallest relevant build and test commands from LibreOffice's
   current documentation. Do not invent commands or assume a full build is
   required.

If requirements are ambiguous, state the ambiguity and ask before making a
choice that would affect document compatibility, legal compliance, linguistic
correctness, or the long-term maintenance of the fork.

## Working Principles

- Keep the Erdem Office patch set small and easy to rebase onto LibreOffice.
- Prefer configuration, extensions, templates, and upstreamable fixes over
  permanent core divergence.
- Make surgical changes. Do not reformat, rename, or refactor unrelated code.
- Follow the style and conventions of the LibreOffice module being changed.
- Add or update focused tests when behavior changes.
- Preserve ODF behavior and test DOCX, XLSX, or PPTX interoperability whenever
  a change can affect Microsoft Office documents.
- Do not commit secrets, credentials, private documents, personal data, or
  unlicensed fonts and datasets.
- Use synthetic or explicitly redistributable documents for tests and examples.

## Mongolian-Specific Requirements

- Do not guess statutory accounting formats, tax rules, terminology, or
  official form requirements. Record the authoritative source and effective
  date, and require review by a qualified Mongolian subject-matter expert.
- Do not guess translations or traditional-script spellings. Mark uncertain
  language for review by a fluent Mongolian editor.
- Treat Cyrillic-to-traditional-script output as assisted conversion unless a
  reviewed benchmark establishes otherwise. Preserve the source text and make
  ambiguous or low-confidence output visible to users.
- Use Unicode text. Test the Mongolian Cyrillic letters `Ө ө Ү ү` and relevant
  traditional Mongolian characters explicitly.
- Traditional Mongolian layout must be tested vertically with columns
  progressing from left to right, including cursor movement, selection,
  punctuation, mixed-script text, printing, PDF export, and document reopening.
- Every bundled font must have a redistribution-compatible license committed or
  referenced alongside it. Font appearance alone is not sufficient; verify
  shaping, embedding, export, and fallback behavior.

## Verification and Handoff

Report:

- what changed and why;
- the issue or acceptance criterion addressed;
- the exact checks run and their results;
- formats and platforms tested;
- any remaining linguistic, accounting, compatibility, licensing, or upstream
  uncertainty.

Do not describe work as complete when required specialist review or document
compatibility testing is still pending.

