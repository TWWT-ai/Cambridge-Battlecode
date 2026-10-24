"""Count 'bot error' lines that a bot printed in replay bundles.

Usage: python tools/errors.py <bot-name> [replay-dir]
"""
import collections
import re
import sys
import zipfile
from pathlib import Path

bot = sys.argv[1]
folder = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "matches" / "eval")
errors = collections.Counter()
for bundle in folder.glob("*.repl26a"):
    a, b = bundle.stem.rsplit("-", 1)[0].split("-vs-")
    sides = [s for s, name in (("team-a", a), ("team-b", b)) if name == bot]
    with zipfile.ZipFile(bundle) as z:
        for side in sides:
            text = z.read(f"{side}.stdout").decode("utf-8", "replace")
            for message in re.findall(r"bot error: ([^\n\x00-\x08]*)", text):
                errors[message.strip()] += 1
print(sum(errors.values()), "errors")
for message, count in errors.most_common(15):
    print(f"{count:6}  {message}")
