from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
NOTICE = ROOT / "LICENSE-PREVIEW.md"
LIMITS = ROOT / "PREVIEW_LIMITS.md"

def test_notice_is_version_1_2():
    text = NOTICE.read_text()
    assert text.splitlines()[0] == "# Caber Community Preview Edition License"
    assert "Version 1.2, November 12, 2026." in text.splitlines()[2]

def test_no_retired_urls_anywhere():
    for path in (NOTICE, LIMITS, ROOT / "README.md"):
        assert "axotl" not in path.read_text()
        assert "CaberSystemsPublic" not in path.read_text()

def test_every_github_url_points_at_caber_systems():
    urls = re.findall(r"https://github\.com/[^\s)]+", NOTICE.read_text() + LIMITS.read_text())
    assert urls, "expected at least the limits link"
    assert all(u.startswith("https://github.com/Caber-Systems/") for u in urls)

def test_limits_link_is_tagged_not_main():
    assert "/preview-license/blob/v1.2/PREVIEW_LIMITS.md" in NOTICE.read_text()
    assert "/blob/main/" not in NOTICE.read_text()

def test_limits_page_links_the_same_notice_version():
    assert "/preview-license/blob/v1.2/LICENSE-PREVIEW.md" in LIMITS.read_text()
    assert "/blob/main/" not in LIMITS.read_text()

def test_security_testing_does_not_survive_termination():
    text = NOTICE.read_text()
    assert "breach a condition in section 2." in text
    assert "except that the security testing authorization in section 4 ends with the license" in text

def test_files_end_with_single_newline():
    for path in (NOTICE, LIMITS):
        data = path.read_bytes()
        assert data.endswith(b"\n") and not data.endswith(b"\n\n")
