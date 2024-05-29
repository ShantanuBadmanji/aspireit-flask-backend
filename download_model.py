# Use a pipeline as a high-level helper
from transformers import pipeline
import joblib

pipe = pipeline(
    "text-classification",
    model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
)

model1 = joblib.dump(pipe, "ml-model/sentement_analysis_joblib")
