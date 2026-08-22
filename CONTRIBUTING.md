# Contributing to Erdem Office

Thank you for helping build a free office suite for Mongolia. Contributions are
welcome from developers, translators, designers, accountants, educators,
typographers, traditional Mongolian script specialists, testers, and template
authors.

Erdem Office is at an early stage. Please use GitHub Issues to discuss a
substantial change before investing significant work.

## Find or Open an Issue

Search existing issues before opening a new one. A useful issue explains:

- the problem and who encounters it;
- the desired outcome;
- the affected Erdem Office or LibreOffice version and operating system;
- a minimal example or reproducible document, when applicable;
- any authoritative linguistic, accounting, legal, or technical source;
- whether the work appears Erdem-specific or generally useful to LibreOffice.

Never attach confidential business records or documents containing personal
data. Replace them with synthetic examples that reproduce the behavior.

## Choose the Right Contribution Path

Erdem Office intends to remain close to LibreOffice.

- Erdem branding, packaging, Mongolian templates, and Erdem-specific
  integration belong in this repository.
- Generally useful LibreOffice fixes should be proposed through
  [LibreOffice Gerrit](https://gerrit.libreoffice.org/) and tracked here with a
  link when they block Erdem Office.
- Mongolian LibreOffice interface translations should normally be contributed
  through [The Document Foundation's translation
  service](https://translations.documentfoundation.org/).

If the correct path is unclear, open an issue before writing code.

## Submit a Change

1. Fork this repository and create a focused branch from `master`.
2. Make the smallest change that resolves the linked issue.
3. Follow the relevant module documentation and existing LibreOffice style.
4. Add or update focused tests and test assets.
5. Run the relevant checks and record the exact commands and results.
6. Open a pull request that links the issue and explains any compatibility or
   specialist-review requirements.

Pull requests should not contain unrelated cleanup or generated files unless
the build process explicitly requires them. Keep commit messages concise and
describe the reason for the change, not only the files modified.

LibreOffice's platform build instructions are maintained in the
[LibreOffice development wiki](https://wiki.documentfoundation.org/Development/How_to_build).
Individual modules also contain `README.md` files with more specific guidance.

## Testing Expectations

Testing should be proportional to the change. In the pull request, identify:

- the operating systems tested;
- the focused automated tests run;
- any manual Writer, Calc, Impress, or installer checks;
- the document formats tested, including ODF and applicable Microsoft Office
  formats;
- PDF or print checks when layout, fonts, or vertical writing are affected.

Test documents and datasets must be synthetic, public domain, or licensed for
redistribution. Include their provenance and license.

## Subject-Matter Review

Some contributions cannot be accepted on automated tests alone.

- Accounting and statutory templates require an authoritative source, its
  effective date, and review by a qualified Mongolian accountant or relevant
  specialist.
- Mongolian translations require review by a fluent editor familiar with the
  product context.
- Traditional Mongolian script and conversion changes require native or expert
  review with representative text, documented ambiguities, and preserved
  Cyrillic source text.
- Fonts require license verification and rendering tests for Mongolian
  Cyrillic, traditional Mongolian shaping, export, and fallback.

Pull requests should state clearly when a required review remains outstanding.

## Licensing

LibreOffice source files retain their existing license notices and licensing
terms. New source files intended for the LibreOffice codebase should follow the
project's applicable MPL 2.0 and LGPLv3+ licensing conventions. Templates,
fonts, translations, documentation, datasets, and other assets may have
different compatible licenses; record the license and provenance with each
contribution.

By submitting a contribution, you confirm that you have the right to provide it
under the licenses identified in the repository and the contribution itself.

For public coding-agent instructions, see [AGENTS.md](AGENTS.md).
