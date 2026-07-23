from pymongo import MongoClient
from config import MONGO_URI

DATABASE_NAME = "telecom_churn"

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client[DATABASE_NAME]

# Colecciones
predictions_collection = db["predictions"]
metrics_collection = db["metrics"]
confusion_matrix_collection = db["confusion_matrix"]
model_info_collection = db["model_info"]
logs_collection = db["logs"]
users_collection = db["users"]