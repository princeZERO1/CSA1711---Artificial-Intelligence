# Deep Learning-Based Deepfake Detection for Social Media Content

AI Course Assignment (100% weightage) — submitted via GitHub + Google Classroom.

## Problem Statement
Build a deep learning system to distinguish real vs. deepfake (AI-manipulated) face
images/videos circulated on social media.

## Contents
- `train_demo.py` — runnable proof-of-concept: generates synthetic real/fake data,
  extracts frequency-domain forensic features, trains an MLP classifier, and outputs
  accuracy/precision/recall/F1/confusion-matrix/ROC results + plots (see `results/`).
- `results/` — output plots (sample_images.png, loss_curve.png, confusion_matrix.png,
  roc_curve.png) and results.txt from the demo run.
- `Deepfake_Detection_Assignment.docx` — full assignment report: problem statement,
  objectives, literature survey, dataset description, architecture, full CNN/EfficientNetB0
  implementation code (production pipeline for FaceForensics++/DFDC), and results.

## How to run the demo
```bash
pip install -r requirements.txt
python train_demo.py
```

## Production pipeline
See Section 8 of the report for the full CNN (EfficientNetB0 transfer learning) pipeline
intended for training on FaceForensics++ / Celeb-DF / DFDC with GPU.

## Results (demo run)
Accuracy: 0.985 | Precision: 0.971 | Recall: 1.000 | F1: 0.985
