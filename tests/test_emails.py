"""Every email address in the license files must be tested by hand before publishing.

Mail delivery cannot be verified automatically from a developer machine (outbound
SMTP on port 25 is blocked), so this test pins the addresses the published files
may contain. Before pushing or tagging a version, send a test message to each
address in MANUALLY_TESTED and confirm it was delivered without a bounce. A new
address fails this test until it has been tested by hand and added here.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = (ROOT / "LICENSE-PREVIEW.md", ROOT / "PREVIEW_LIMITS.md", ROOT / "README.md")
EMAIL_RE = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@(?:caber\.com|axotl\.ai)\b", re.IGNORECASE)

MANUALLY_TESTED = {"support@caber.com"}


def addresses():
    found = {}
    for path in PUBLISHED:
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            for match in EMAIL_RE.finditer(line):
                found.setdefault(match.group(0).lower(), []).append(f"{path.name}:{lineno}")
    return found


def test_no_retired_axotl_addresses():
    assert not [a for a in addresses() if a.endswith("@axotl.ai")]


def test_every_address_is_on_the_manually_tested_list():
    untested = {a: where for a, where in addresses().items() if a not in MANUALLY_TESTED}
    assert not untested, (
        f"test these by hand, then add them to MANUALLY_TESTED: {untested}"
    )


def test_manually_tested_list_has_no_stale_entries():
    assert MANUALLY_TESTED <= set(addresses()), "remove addresses the files no longer contain"
