import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Create models folder if not exists
os.makedirs("models", exist_ok=True)

data = {
    "score":[40,50,60,70,80,90],
    "study_hours":[8,7,6,5,4,3]
}

df = pd.DataFrame(data)

X = df[['score']]
y = df['study_hours']

model = LinearRegression()
model.fit(X,y)

joblib.dump(
    model,
    "models/recommendation_model.pkl"
)

print("Model saved successfully")