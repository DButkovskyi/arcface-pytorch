from pathlib import Path
import random

ROOT = Path("data_lfw_tiny").resolve()   # your lfw_root
OUT  = Path("tiny_pairs.txt") # new pairs file expected by your test.py
SEED = 0
random.seed(SEED)

def lfw_files(person_dir: Path):
    name = person_dir.name
    return sorted([f for f in person_dir.glob(f"{name}_*.jpg")])

people = [d for d in sorted(ROOT.iterdir()) if d.is_dir()]
people = [(d.name, d, lfw_files(d)) for d in people]
people = [(n, d, fs) for (n,d,fs) in people if len(fs) >= 1]

if not people:
    raise SystemExit(f"No LFW-style files found under {ROOT}")

lines = []

# positives
for name, d, fs in people:
    if len(fs) < 2:
        continue
    a, b = random.sample(fs, 2)
    rel_a = f"{name}/{a.name}"
    rel_b = f"{name}/{b.name}"
    lines.append(f"{rel_a} {rel_b} 1\n")

# negatives (same count as positives)
pos_count = sum(1 for _ in lines)
while sum(1 for L in lines if L.endswith(" 0\n")) < pos_count:
    (n1, d1, f1s), (n2, d2, f2s) = random.sample(people, 2)
    a = random.choice(f1s)
    b = random.choice(f2s)
    lines.append(f"{n1}/{a.name} {n2}/{b.name} 0\n")

OUT.write_text("".join(lines), encoding="utf-8")
print(f"Wrote {OUT} with {pos_count} positive and {pos_count} negative pairs")
print("Example:", lines[0].strip())
