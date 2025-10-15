from pathlib import Path
import random
import re

# --- CONFIG ---
ROOT = Path("data_lfw_tiny").resolve()   # your dataset root
OUT  = Path("tiny_pairs.txt")            # pairs file expected by test.py
SEED = 0
PAD  = 4                                 # zero-pad width -> 0001, 0002, ...
EXT  = ".jpg"                            # output extension for renamed files
random.seed(SEED)

# ---------- 1) RENAME TO Name/Name_0001.jpg, Name_0002.jpg, ... ----------
def rename_person_dir(person_dir: Path, pad: int = PAD, ext: str = EXT):
    """Rename files inside person_dir to the format: <Name>_<NNNN>.jpg"""
    name = person_dir.name
    # Collect image files (you can add more suffixes if needed)
    files = sorted([f for f in person_dir.iterdir() if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    if not files:
        return

    # If they are already in the correct format, do nothing
    desired_re = re.compile(rf"^{re.escape(name)}_\d+{re.escape(ext)}$", re.IGNORECASE)
    already_ok = all(desired_re.match(f.name) for f in files)
    if already_ok:
        return

    # To avoid collisions, rename in two passes via temporary names
    tmp_files = []
    for i, f in enumerate(files, start=1):
        tmp = f.with_name(f"__tmp__{i:08d}{f.suffix.lower()}")
        f.rename(tmp)
        tmp_files.append(tmp)

    for i, tmp in enumerate(sorted(tmp_files), start=1):
        new_name = f"{name}_{i:0{pad}d}{ext}"
        tmp.rename(person_dir / new_name)

# Run renaming for every person folder
for d in sorted(ROOT.iterdir()):
    if d.is_dir():
        rename_person_dir(d)

# ---------- 2) CREATE PAIRS ON THE NEW NAMES ----------
def lfw_files(person_dir: Path):
    """Return sorted list of <Name>_<NNNN>.jpg files inside a person's folder."""
    name = person_dir.name
    return sorted(person_dir.glob(f"{name}_*.jpg"))

people = [(d.name, d, lfw_files(d)) for d in sorted(ROOT.iterdir()) if d.is_dir()]
people = [(n, d, fs) for (n, d, fs) in people if len(fs) >= 1]

if not people:
    raise SystemExit(f"No LFW-style files found under {ROOT}")

lines = []

# positives
for name, d, fs in people:
    if len(fs) < 2:
        continue
    a, b = random.sample(fs, 2)
    lines.append(f"{name}/{a.name} {name}/{b.name} 1\n")

# negatives (same count as positives)
pos_count = sum(1 for _ in lines)
neg_needed = pos_count
while sum(1 for L in lines if L.endswith(" 0\n")) < neg_needed:
    (n1, d1, f1s), (n2, d2, f2s) = random.sample(people, 2)
    a = random.choice(f1s)
    b = random.choice(f2s)
    lines.append(f"{n1}/{a.name} {n2}/{b.name} 0\n")

OUT.write_text("".join(lines), encoding="utf-8")
print(f"Wrote {OUT} with {pos_count} positive and {pos_count} negative pairs")
print("Example:", lines[0].strip())
