import numpy as np
from scripts.feature_extractor import extract_features

def calibrate_user():
    baseline_features = []

    print("Calibration started. Please work normally for 3 sessions.")

    for i in range(3):
        print(f"Session {i+1}/3")
        features = extract_features()
        baseline_features.append(features)

    baseline = np.mean(baseline_features, axis=0)
    np.save("model/user_baseline.npy", baseline)

    print("Calibration completed and saved.")
