import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = {
    "score":[40,50,60,70,80,90],
    "study_hours":[8,7,6,5,4,3]
}

df=pd.DataFrame(data)

X=df[['score']]
y=df['study_hours']

model=LinearRegression()
model.fit(X,y)

joblib.dump(model,"recommendation_model.pkl")

print("Model Trained Successfully")