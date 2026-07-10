# PDF Recovery

PDF over-compression recovery workspace from 2026-07-02 to 2026-07-03.

Tracked content:

- `recover_overcompressed_pdfs.py`
- `recover_overcompressed_browser.py`
- `pdf_compression*.tsv`
- `pdf_recovery*.tsv`
- `overcompressed_*_candidates.tsv`
- `sig_acm_*`

Ignored content:

- `_private/pdf_overcompressed_backup/`: large backup PDFs.
- `_private/pdf_recovery_work/`: scratch downloads and intermediate repair work.

The scripts were moved here during the 2026-07-09 cleanup. Future recovery logs
now write back into this directory.
