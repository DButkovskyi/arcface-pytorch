# save as make_tiny_faceset.py and run: python make_tiny_faceset.py
import os, shutil
from sklearn.datasets import fetch_lfw_people
from pathlib import Path

out = Path("data_lfw_tiny")
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True, exist_ok=True)

# min_faces_per_person controls class size; bump to 20 if you want even fewer, cleaner classes
lfw = fetch_lfw_people(color=True, resize=1.0, min_faces_per_person=15, funneled=True, download_if_missing=True)

# Build person -> list of indices
import numpy as np
names = lfw.target_names
for person_idx, person_name in enumerate(names):
    idxs = np.where(lfw.target == person_idx)[0]
    if len(idxs) < 2:  # need at least 2 images per identity
        continue
    person_dir = out / person_name.replace(" ", "_")
    person_dir.mkdir(parents=True, exist_ok=True)
    for k, i in enumerate(idxs):
        img = (lfw.images[i]).astype("uint8")
        # lfw.images is HxWx3 in RGB uint8 already
        from PIL import Image
        Image.fromarray(img).save(person_dir / f"img_{k:03d}.jpg")

print("Wrote dataset to:", out.resolve())
