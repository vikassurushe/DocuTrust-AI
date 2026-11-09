# DocuTrust AI
### AI-Powered Document Forensics & Contextual Intelligence System
**DataOps Innovation Hackathon 2026 — Problem Statement 2**

DocuTrust AI is a prototype for reviewing related digital and scanned documents. It extracts text, compares selected fields across documents, surfaces basic image-screening metrics, preserves source filenames and generates a PDF investigation dossier.

> **Safety note:** This project is a review assistant, not a fraud detector. A discrepancy or visual signal is not proof of manipulation. Use only synthetic or explicitly authorized documents. Do not upload real customer information without permission.

## Features implemented
- Upload multiple PDF, image, DOCX and TXT files.
- Extract text from text-based PDFs, DOCX and TXT.
- OCR for image uploads through Tesseract (when installed and configured).
- Pattern-based extraction of name, date of birth, ID/reference number, address, phone and email.
- Cross-document comparison for supported fields.
- Basic image statistics (brightness, contrast and edge intensity) for triage.
- SHA-256 file hashes for file identity / traceability.
- Human review notes.
- Download case JSON and PDF investigation dossier.

## Prototype limitations — disclose these in the hackathon
- This is a prototype, not a production forensic platform.
- OCR quality depends on image quality and Tesseract installation.
- Scanned/image-only PDFs are not OCR-processed in this version.
- Field extraction is pattern-based and may miss varied document layouts.
- Visual metrics are descriptive only; they do not detect or prove image tampering.
- No trained ML model, signature verification, handwriting recognition or LLM reasoning is implemented.
- No live cloud storage, access control or multi-user audit service is included.
- All findings require human verification.

## Architecture
```text
User uploads documents
        |
        v
File validation + SHA-256
        |
        v
Text extraction / OCR
        |
        v
Pattern-based field extraction
        |
        +------> Basic image statistics (image files)
        |
        v
Cross-document field comparison
        |
        v
Findings + source filenames + reviewer notes
        |
        v
JSON case export + PDF investigation dossier
```

## Requirements
- Python 3.10+
- Tesseract OCR installed separately for image OCR (optional but recommended)

### Install Tesseract
- Windows: Install the Tesseract OCR Windows package and add its installation folder to PATH.
- Ubuntu/Debian: `sudo apt install tesseract-ocr`
- macOS (Homebrew): `brew install tesseract`

## Run locally
```bash
git clone https://github.com/<your-username>/docutrust-ai.git
cd docutrust-ai

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```
Open the local Streamlit URL printed in the terminal.

## Safe demo dataset
Create two synthetic text files and upload both.

`sample_data/application_form.txt`
```text
Applicant Name: Asha Sharma
Date of Birth: 12-04-2002
ID Number: DEMO-1001
Address: 21 Sample Road, Pune
Phone: 9000000001
Email: asha.demo@example.com
```

`sample_data/address_proof.txt`
```text
Applicant Name: Asha Sharma
Date of Birth: 12-04-2002
ID Number: DEMO-1001
Address: 42 Example Avenue, Pune
Phone: 9000000001
Email: asha.demo@example.com
```

Expected result: the app should flag the different address values as a **potential discrepancy requiring human verification**. These are fictional records.

## Repository structure
```text
docutrust-ai/
├── app.py
├── docutrust/
│   ├── __init__.py
│   ├── analysis.py
│   ├── extractors.py
│   └── report.py
├── sample_data/
│   ├── application_form.txt
│   └── address_proof.txt
├── requirements.txt
├── .gitignore
└── README.md
```

## Integration status matrix
| Capability | Status | Notes |
|---|---|---|
| PDF text extraction | Implemented | Text-based PDFs |
| Image OCR | Implemented, environment-dependent | Requires Tesseract |
| DOCX/TXT extraction | Implemented | Paragraph/text extraction |
| Cross-document field comparison | Implemented | Supported fields only |
| Visual forensic analysis | Basic screening only | Image statistics; not manipulation detection |
| Layout analysis | Not implemented | Future work |
| Handwriting recognition | Not implemented | Future work |
| Signature verification | Not implemented | Future work |
| LLM contextual reasoning | Not implemented | Future work |
| Evidence-linked PDF dossier | Implemented, basic | Source filenames and field values |
| Human review notes | Implemented | Reviewer notes included in export |

## Team details
- Team name: **[Enter team name]**
- Team members: **[Enter names]**
- College: **[Enter college]**

## License
For hackathon demonstration and educational use. Add a license after confirming the terms appropriate for your team and all dependencies.
