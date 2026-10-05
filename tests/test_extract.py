from cardtrack.extract import extract_text, fingerprint_text, sniff_kind


def test_html_extraction_and_fingerprint_stability():
    """Two HTML variants differing only in script nonces and whitespace must
    produce the same fingerprint (change detection runs on text, never bytes)."""
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


def test_footnotes_survive_a_footer_classed_wrapper():
    """Anthropic (Aug 2026) wrapped its footnote block in a "...postFooter" container;
    trafilatura discards anything classed "footer", so three documents' footnotes
    vanished from extracted text while the raw HTML still held them."""
    from cardtrack.extract import extract_text

    body = " ".join(["This model was evaluated on a benchmark suite with many tasks."] * 12)
    footnote = "We routinely test internal research prototypes like this one."
    html = f"""<!DOCTYPE html><html><head><title>Post</title></head><body>
    <nav><a href="/">Home</a><a href="/news">News</a></nav>
    <article><h1>A post</h1><p>{body}</p><p>{body}</p>
    <div class="page-wrapper PostDetail-module__postFooter">
      <div class="PostDetail-module__footnotes"><h4>Footnotes</h4>
      <ol><li id="footnote-1">{footnote}</li></ol></div>
    </div></article>
    <footer><a href="/privacy">Privacy</a></footer>
    </body></html>""".encode()
    text, method = extract_text(html, "text/html", "https://example.com/post")
    assert method == "html"
    assert footnote in text


def test_related_content_block_is_stripped_wherever_it_sits():
    """Short Anthropic posts (an 18-line access policy) carry the rotating "Related
    content" block well before the last quarter; its rotation must not change the
    fingerprint. A same-named heading followed by real content must still count."""
    from cardtrack.extract import normalize_for_fingerprint

    pats = ("^Read more$",)
    doc = ["Access policy.", "Researchers may apply.", "Related content",
           "Title one", "Blurb one.", "Read more", "Title two", "Read more"]
    rotated = doc[:3] + ["Title three", "Blurb three.", "Read more", "Title four", "Read more"]
    assert (normalize_for_fingerprint("\n".join(doc), pats)
            == normalize_for_fingerprint("\n".join(rotated), pats)
            == "Access policy. Researchers may apply.")
    real = doc[:3] + ["A real paragraph under a heading that shares the name."] + doc[3:]
    assert "real paragraph" in normalize_for_fingerprint("\n".join(real), pats)
    # a single group is not a teaser block, however it is shaped: the heading rule
    # must not fire (the trailing-pair rule still takes the last sentence + marker)
    probe = ["Intro.", "Related content", "Real section heading",
             "Real paragraph with 42%.", "Read more"]
    assert "Real section heading" in normalize_for_fingerprint("\n".join(probe), pats)


def test_date_line_pattern_matches_whole_line_dates_only():
    import re

    from cardtrack.extract import DATE_LINE_PATTERN

    rx = re.compile(DATE_LINE_PATTERN)
    for line in ["Jan 14, 2026", "05 July 2026", "2026-09-03", "Updated: March 6, 2026",
                 "August 3, 2026."]:
        assert rx.search(line), line
    for line in ["As of June 5, 2026, the bug bounty received ~100,000 attempts",
                 "Edited February 6, 2026:", "- Updated the author list", "2026",
                 "14 Maybe 2026", "| 2026-09-03 |", "2026-09-03:", "  date = {2026-07-13},"]:
        assert not rx.search(line), line
