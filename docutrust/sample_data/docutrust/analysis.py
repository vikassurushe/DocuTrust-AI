from PIL import ImageStat, ImageFilter
import io

def compare_documents(docs):
    """Compare extracted values for common supported fields; retain source names."""
    fields = ["name", "date_of_birth", "id_number", "address", "phone", "email"]
    findings = []
    for field in fields:
        observed = []
        for doc in docs:
            value = (doc.get("fields") or {}).get(field)
            if value:
                observed.append((doc["filename"], str(value).strip()))
        distinct = sorted(set(v.lower() for _, v in observed))
        if len(distinct) > 1:
            findings.append({
                "Finding ID": f"CTX-{len(findings)+1:03d}",
                "Category": "Cross-document inconsistency",
                "Field": field,
                "Severity": "Review required",
                "Observed values": " | ".join(f"{name}: {value}" for name, value in observed),
                "Evidence sources": ", ".join(name for name, _ in observed),
                "Status": "Potential discrepancy — human verification required",
                "Confidence": "Rule-based match; not a probability"
            })
    return findings

def visual_screening(filename, image):
    """Basic image statistics for triage; not a manipulation detector."""
    gray = image.convert("L")
    stat = ImageStat.Stat(gray)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_mean = ImageStat.Stat(edges).mean[0]
    return [{
        "Document": filename,
        "Image width": image.width,
        "Image height": image.height,
        "Mean brightness (0-255)": round(stat.mean[0], 2),
        "Contrast (std dev)": round(stat.stddev[0], 2),
        "Edge intensity (mean)": round(edge_mean, 2),
        "Interpretation": "Descriptive screening metrics only; no tampering conclusion."
    }]
