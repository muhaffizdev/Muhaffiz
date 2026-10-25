# Muhaffiz (formerly Hifazat)

Final Year Project, BS Software Engineering, Air University Islamabad: an offline-first safety app for women and children.

## Layout

```
Documents/
├── SRS/                  The SRS & SDS deliverable
│   ├── Muhaffiz-SRS-SDS.docx    generated: edit the build scripts, not this file
│   ├── Muhaffiz-SRS-SDS.pdf
│   ├── build/            Python scripts that generate the .docx (one ch*.py per chapter)
│   └── diagrams/         SVG + PNG figures produced by the build scripts
├── Audit/                Independent audit of the SRS (start with audit-summary.md)
├── Notes/                Working notes: project-context.md, progress.md, SRS-Checklist.md
├── Reference/            Inputs: university SRS template, scope document, feature document, chat record
└── Archive/              Superseded builds kept for reference
Source-Code/              Application code (not started yet)
```

## Rebuilding the SRS

```bash
cd Documents/SRS/build && SRS_WORK=/tmp/srs_work SRS_RENDER=/tmp/srs_render python3 build.py
```

The build reads `Documents/Reference/SRS-Template.docx` and writes `Documents/SRS/Muhaffiz-SRS-SDS.docx`. The PDF render step currently calls a LibreOffice helper at a hard-coded path in `build.py` (`render()`). See `Documents/Notes/progress.md` for build details.
