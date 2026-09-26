from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://nikitakangude12_db_user:<db_password>@cluster0.xg0ch5m.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

try:
    print(client.admin.command("ping"))
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:")
    print(e)