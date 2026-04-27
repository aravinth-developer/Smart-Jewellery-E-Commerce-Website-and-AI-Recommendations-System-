import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
    
# Load dataset
data = pd.read_excel("Wastage_Prediction_Dataset_600_Rows_Updated.xlsx")

# Feature Engineering
data["Weight_Difference"] = data["Gold_Given_Weight(g)"] - data["Final_Weight(g)"]

# Encode categorical
le_jewel = LabelEncoder()
le_design = LabelEncoder()
le_stone = LabelEncoder()

data["Jewel_Type"] = le_jewel.fit_transform(data["Jewel_Type"])
data["Design_Type"] = le_design.fit_transform(data["Design_Type"])
data["Stone_Included"] = le_stone.fit_transform(data["Stone_Included"])

# Features
X = data[[
    "Jewel_Type",
    "Karat",
    "Design_Type",
    "Stone_Included",
    "Gold_Given_Weight(g)",
    "Final_Weight(g)",
    "Weight_Difference"
]]

y = data["Wastage_Percentage(%)"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# Predictions
pred = model.predict(X_test)

# Accuracy
r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)

print("R2 Score:", r2)
print("Mean Absolute Error:", mae)

# Save everything
joblib.dump({
    "model": model,
    "le_jewel": le_jewel,
    "le_design": le_design,
    "le_stone": le_stone
}, "wastage_model.pkl")

print("Model Saved Successfully")