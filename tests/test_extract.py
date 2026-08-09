from cardtrack.extract import extract_text, fingerprint_text, sniff_kind


def test_html_extraction_and_fingerprint_stability():
    """Two HTML variants differing only in script nonces and whitespace must
    produce the same fingerprint (spec §5: change detection on text, not bytes)."""
    html_a = b"""<!DOCTYPE html><html><head><title>Card</title>
<script>var nonce="abc123";</script></head>
<body><main><h1>Card</h1><p>The model was evaluated on autonomy tasks.</p></main></body></html>"""
    html_b = b"""<!DOCTYPE html><html><head><title>Card</title>
<script>var nonce="zzz999";</script></head>
<body><main><h1>Card</h1>\n\n<p>The   model was evaluated
on autonomy tasks.</p></main></body></html>"""
    text_a, method_a = extract_text(html_a, "text/html")
    text_b, _ = extract_text(html_b, "text/html")
    assert method_a == "html"
    assert text_a and "autonomy tasks" in text_a
    assert "nonce" not in text_a
    assert fingerprint_text(text_a) == fingerprint_text(text_b)


def test_real_content_change_changes_fingerprint():
    a, _ = extract_text(b"<html><body><p>Version one of the card.</p></body></html>", "text/html")
    b, _ = extract_text(b"<html><body><p>Version two of the card.</p></body></html>", "text/html")
    assert a and b
    assert fingerprint_text(a) != fingerprint_text(b)


def test_pdf_extraction(pdf_bytes):
    assert sniff_kind(pdf_bytes, None) == "pdf"
    text, method = extract_text(pdf_bytes, "application/pdf")
    assert method == "pdf"
    assert text and "cardtrack PDF fixture" in text


def test_pdf_magic_beats_wrong_content_type(pdf_bytes):
    assert sniff_kind(pdf_bytes, "text/html") == "pdf"


def test_binary_garbage_fails_gracefully():
    text, method = extract_text(b"\x00\x01\x02\x03" * 100, "application/octet-stream")
    assert text is None
    assert method == "binary"
