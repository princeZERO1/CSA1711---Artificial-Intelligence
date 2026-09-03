"""
Deep Learning-Based Deepfake Detection - Proof-of-Concept Demonstration
-------------------------------------------------------------------------
NOTE: This script is a lightweight, fully-executable demonstration of the
detection pipeline. It runs on procedurally generated synthetic images
(since no GPU / internet access / real dataset such as FaceForensics++ or
DFDC is available in this sandbox) so that the assignment includes REAL,
reproducible output rather than fabricated numbers. The full production
pipeline (Section: Implementation) uses a CNN (EfficientNetB0 transfer
learning) trained on FaceForensics++ / DFDC frames.

The synthetic data is built to mimic a well-known real artifact used in
deepfake forensics: GAN-generated images exhibit periodic high-frequency
spectral artifacts (checkerboard patterns from transposed-convolution /
up-sampling layers) that are largely absent in camera-captured images.
We generate:
  - "REAL" images  -> smooth 2D Gaussian-blob faces + natural sensor noise
  - "FAKE" images  -> same base image + a faint periodic high-frequency
                      grid pattern (simulating GAN up-sampling artifacts)

Features extracted per image (classic forensic feature engineering):
  1. High-frequency FFT energy ratio
  2. Laplacian variance (edge/texture irregularity)
  3. Pixel intensity mean
  4. Pixel intensity std-dev
  5. Local noise residual variance

A small Multi-Layer Perceptron (a compact feed-forward deep neural
network) is trained on these features to classify REAL vs FAKE.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report,
                              roc_curve, auc)
from scipy.ndimage import gaussian_filter, laplace

RNG = np.random.default_rng(42)
IMG_SIZE = 64
N_PER_CLASS = 400


def make_base_face(size=IMG_SIZE):
    """Procedurally generate a smooth face-like intensity blob."""
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    xx, yy = np.meshgrid(x, y)
    base = np.exp(-(xx**2 + yy**2) * (2 + RNG.random()))
    base += 0.15 * RNG.random((size, size))
    base = gaussian_filter(base, sigma=1.2)
    base = (base - base.min()) / (base.max() - base.min() + 1e-8)
    return base


def make_real_image():
    img = make_base_face()
    img += RNG.normal(0, 0.02, img.shape)  # natural sensor noise
    return np.clip(img, 0, 1)


def make_fake_image():
    img = make_base_face()
    size = img.shape[0]
    # simulate GAN up-sampling checkerboard artifact (periodic high-freq grid)
    xv, yv = np.meshgrid(np.arange(size), np.arange(size))
    freq = 6 + RNG.integers(0, 3)
    artifact = 0.035 * np.sin(2 * np.pi * xv / freq) * np.sin(2 * np.pi * yv / freq)
    img = img + artifact
    img += RNG.normal(0, 0.015, img.shape)
    return np.clip(img, 0, 1)


def extract_features(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    mag = np.abs(fshift)
    h, w = mag.shape
    cy, cx = h // 2, w // 2
    low_mask = np.zeros_like(mag, dtype=bool)
    r = h // 6
    low_mask[cy - r:cy + r, cx - r:cx + r] = True
    low_energy = mag[low_mask].sum()
    high_energy = mag[~low_mask].sum()
    hf_ratio = high_energy / (low_energy + 1e-8)

    lap = laplace(img)
    lap_var = lap.var()

    mean_i = img.mean()
    std_i = img.std()

    residual = img - gaussian_filter(img, sigma=2)
    noise_var = residual.var()

    return [hf_ratio, lap_var, mean_i, std_i, noise_var]


def build_dataset():
    X, y, imgs = [], [], []
    for _ in range(N_PER_CLASS):
        ri = make_real_image()
        fi = make_fake_image()
        X.append(extract_features(ri)); y.append(0); imgs.append(ri)
        X.append(extract_features(fi)); y.append(1); imgs.append(fi)
    return np.array(X), np.array(y), imgs


def main():
    print("Generating synthetic REAL/FAKE dataset ...")
    X, y, imgs = build_dataset()
    print(f"Dataset shape: {X.shape}, Labels: {np.bincount(y)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)

    # normalize
    mu, sigma = X_train.mean(axis=0), X_train.std(axis=0) + 1e-8
    X_train_n = (X_train - mu) / sigma
    X_test_n = (X_test - mu) / sigma

    clf = MLPClassifier(hidden_layer_sizes=(32, 16), activation="relu",
                         solver="adam", max_iter=400, random_state=42,
                         early_stopping=True, validation_fraction=0.15)
    clf.fit(X_train_n, y_train)

    y_pred = clf.predict(X_test_n)
    y_proba = clf.predict_proba(X_test_n)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["REAL", "FAKE"])

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    print(report)

    with open("results.txt", "w") as f:
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall: {rec:.4f}\n")
        f.write(f"F1-score: {f1:.4f}\n")
        f.write("Confusion Matrix:\n")
        f.write(str(cm) + "\n\n")
        f.write(report)

    # --- Plot 1: Sample images ---
    fig, axes = plt.subplots(2, 4, figsize=(10, 5.2))
    real_idx = [i for i, lbl in enumerate(y) if lbl == 0][:4]
    fake_idx = [i for i, lbl in enumerate(y) if lbl == 1][:4]
    for k, idx in enumerate(real_idx):
        axes[0, k].imshow(imgs[idx], cmap="gray")
        axes[0, k].set_title("REAL", fontsize=10)
        axes[0, k].axis("off")
    for k, idx in enumerate(fake_idx):
        axes[1, k].imshow(imgs[idx], cmap="gray")
        axes[1, k].set_title("FAKE", fontsize=10)
        axes[1, k].axis("off")
    plt.suptitle("Sample Synthetic Frames used for the Proof-of-Concept Demo")
    plt.tight_layout()
    plt.savefig("sample_images.png", dpi=150)
    plt.close()

    # --- Plot 2: Confusion matrix ---
    fig, ax = plt.subplots(figsize=(4.5, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["REAL", "FAKE"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["REAL", "FAKE"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=14)
    fig.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=150)
    plt.close()

    # --- Plot 3: Training loss curve ---
    plt.figure(figsize=(5.5, 4))
    plt.plot(clf.loss_curve_, label="Training loss", color="#c0392b")
    plt.xlabel("Iteration"); plt.ylabel("Loss")
    plt.title("Model Training Loss Curve")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("loss_curve.png", dpi=150)
    plt.close()

    # --- Plot 4: ROC curve ---
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(5, 4.5))
    plt.plot(fpr, tpr, color="#2980b9", label=f"ROC curve (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate"); plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - Deepfake Detector")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("roc_curve.png", dpi=150)
    plt.close()

    print("\nSaved: sample_images.png, confusion_matrix.png, loss_curve.png, roc_curve.png, results.txt")
    return acc, prec, rec, f1, roc_auc


if __name__ == "__main__":
    main()
