# tools/make_lists.py
import argparse, os, random, json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True, help="Root folder with one subfolder per identity")
    ap.add_argument("--out-dir", required=True, help="Where to write the txt files")
    ap.add_argument("--val-perc", type=float, default=0.2, help="Fraction per identity for validation [0..1]")
    ap.add_argument("--min-train", type=int, default=1, help="Min train images per ID (if possible)")
    args = ap.parse_args()

    data_root = Path(args.data_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # deterministic split
    random.seed(1234)

    # map identity folder -> label id
    id_dirs = sorted([p for p in data_root.iterdir() if p.is_dir()])
    label_map = {p.name: i for i, p in enumerate(id_dirs)}

    train_lines, val_lines = [], []

    for name, label in label_map.items():
        imgs = sorted(
            [p for p in (data_root / name).iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
        )
        if not imgs:
            continue
        random.shuffle(imgs)

        # per-identity split
        n = len(imgs)
        n_val = max(1 if n >= 2 else 0, int(round(n * args.val_perc)))
        n_train = max(args.min_train, n - n_val) if n > 1 else n - n_val

        # guard rails
        n_val = max(0, min(n - n_train, n_val))
        train_imgs = imgs[: n - n_val]
        val_imgs   = imgs[n - n_val :]

        train_lines += [f"{str(p)} {label}\n" for p in train_imgs]
        val_lines   += [f"{str(p)} {label}\n" for p in val_imgs]

    # write files
    train_txt = out_dir / "train_data_generated.txt"
    val_txt   = out_dir / "val_data_generated.txt"
    with open(train_txt, "w", encoding="utf-8") as f:
        f.writelines(train_lines)
    with open(val_txt, "w", encoding="utf-8") as f:
        f.writelines(val_lines)

    # label map (for reference)
    with open(out_dir / "labels.json", "w", encoding="utf-8") as f:
        json.dump(label_map, f, indent=2)

    print(f"Wrote:\n  {train_txt}\n  {val_txt}")
    print(f"num_classes = {len(label_map)}")

if __name__ == "__main__":
    main()
