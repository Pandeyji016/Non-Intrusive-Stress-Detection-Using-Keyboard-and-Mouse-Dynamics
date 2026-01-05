import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/stress_data.csv")

# Feature names (VERY IMPORTANT FOR EXAMINER)
feature_names = [
    'typing_speed',
    'avg_key_delay',
    'mouse_speed',
    'mouse_jitter',
    'click_rate',
    'idle_time'
]

X = df[feature_names]
y = df['stress']

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# Save model
joblib.dump(model, "model/stress_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

# FEATURE IMPORTANCE
importances = model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values(by="Importance", ascending=False)

# Save importance for Streamlit
importance_df.to_csv("model/feature_importance.csv", index=False)

print("\nFeature Importance:")
print(importance_df)

print("\nModel and feature importance saved")
