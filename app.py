import io
import json
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image
from docx import Document as DocxDocument

from docutrust.extractors import extract_document
from docutrust.analysis import compare_documents, visual_screening
from docutrust.report import build_pdf_report

st.set_page_config(page_title="DocuTrust AI", page_icon="🔎", layout="wide")

st.title("🔎 DocuTrust AI")
st.caption("AI-assisted document forensics and contextual intelligence — prototype")
st.warning(
    "Use synthetic or explicitly authorized documents only. Findings are screening signals, "
    "not proof of fraud or document manipulation. A human reviewer must verify every finding."
)

with st.sidebar:
    st.header("Investigation")
    case_name = st.text_input("Case name", "Sample document review")
    reviewer = st.text_input("Reviewer", "Analyst")
    st.markdown("---")
    st.write("**Prototype capabilities**")
    st.write("• PDF/image/DOCX/TXT ingestion")
    st.write("• OCR/text extraction")
    st.write("• Cross-document field comparison")
    st.write("• Basic image screening signals")
    st.write("• Evidence-linked PDF dossier")

uploaded = st.file_uploader(
    "Upload related documents",
    type=["pdf", "png", "jpg", "jpeg", "tif", "tiff", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded:
    docs = []
    visual_rows = []
    progress = st.progress(0, text="Processing documents...")
    for idx, f in enumerate(uploaded):
        raw = f.getvalue()
        digest = hashlib.sha256(raw).hexdigest()
        try:
            result = extract_document(f.name, raw)
            result["sha256"] = digest
            result["size_bytes"] = len(raw)
            docs.append(result)
            if result.get("image"):
                visual_rows.extend(visual_screening(f.name, result["image"]))
        except Exception as exc:
            docs.append({
                "filename": f.name,
                "text": "",
                "pages": [],
                "fields": {},
                "error": str(exc),
                "sha256": digest,
                "size_bytes": len(raw),
            })
        progress.progress((idx + 1) / len(uploaded), text=f"Processed {idx+1}/{len(uploaded)}")
    progress.empty()

    st.subheader("1. Document processing")
    overview = []
    for d in docs:
        overview.append({
            "Document": d["filename"],
            "Pages": len(d.get("pages", [])),
            "Extracted characters": len(d.get("text", "")),
            "SHA-256 (first 12)": d.get("sha256", "")[:12],
            "Status": "Error: " + d["error"] if d.get("error") else "Processed"
        })
    st.dataframe(pd.DataFrame(overview), use_container_width=True)

    st.subheader("2. Extracted information")
    for d in docs:
        with st.expander(f"{d['filename']} — extracted fields"):
            st.json(d.get("fields", {}))
            st.text_area("Extracted text (preview)", d.get("text", "")[:6000], height=160, key=f"text_{d['filename']}")

    st.subheader("3. Contextual / cross-document analysis")
    findings = compare_documents(docs)
    if findings:
        fdf = pd.DataFrame(findings)
        st.dataframe(fdf, use_container_width=True)
    else:
        st.success("No cross-document field conflicts were detected in the supported fields. This does not establish document authenticity.")

    st.subheader("4. Visual screening signals")
    if visual_rows:
        st.dataframe(pd.DataFrame(visual_rows), use_container_width=True)
        st.caption("These are simple image-level screening metrics only; this prototype does not prove image tampering.")
    else:
        st.info("No standalone image page was available for the visual screening module.")

    st.subheader("5. Human review")
    st.write("Review each potential discrepancy against the original source document before drawing a conclusion.")
    review_note = st.text_area("Analyst review notes", "Pending manual verification.")
    reviewed_by = st.text_input("Reviewed by", reviewer)

    st.subheader("6. Download investigation dossier")
    case = {
        "case_name": case_name,
        "reviewer": reviewed_by,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "documents": [
            {k: v for k, v in d.items() if k not in ("image",)}
            for d in docs
        ],
        "findings": findings,
        "visual_screening": visual_rows,
        "review_notes": review_note,
        "limitations": [
            "OCR output may contain errors and is not verified ground truth.",
            "Field extraction uses transparent pattern matching, not a trained fraud model.",
            "Visual screening uses basic image statistics and does not establish manipulation.",
            "A detected discrepancy is not a fraud determination.",
            "Only the displayed file formats and fields are supported by this prototype."
        ]
    }
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download case data (JSON)",
            data=json.dumps(case, indent=2, ensure_ascii=False),
            file_name="docutrust_case.json",
            mime="application/json"
        )
    with c2:
        pdf_bytes = build_pdf_report(case)
        st.download_button(
            "Download investigation dossier (PDF)",
            data=pdf_bytes,
            file_name="docutrust_investigation_dossier.pdf",
            mime="application/pdf"
        )
else:
    st.info("Upload two or more related sample documents to demonstrate cross-document comparison.")
    st.markdown("### Suggested safe demo")
    st.markdown(
        "Create two synthetic documents with the same applicant name and ID but different dates "
        "or addresses. Upload both and show how DocuTrust AI records the conflicting values and "
        "their source document names."
    )
