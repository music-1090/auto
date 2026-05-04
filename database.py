import os
from pymongo import MongoClient

# Environment variable ကနေ Mongo URI ကို ယူမယ် (Docker အတွက်)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client['bot_database']
brain_collection = db['brain']

def init_db():
    # MongoDB က table (collection) ဆောက်စရာမလိုပါ၊ ဒေတာထည့်ရင် အလိုအလျောက် ဆောက်သွားပါလိမ့်မယ်။
    print("✅ MongoDB Connected")

def save_to_brain(q, a):
    if not q or not a: return
    brain_collection.insert_one({
        "input_text": q.lower().strip(),
        "reply_text": a,
        "sticker_id": None
    })

def get_reply(text):
    user_input = text.lower().strip()
    # Exact match သို့မဟုတ် regex word boundary နဲ့ ရှာမယ်
    query = {
        "$or": [
            {"input_text": user_input},
            {"input_text": {"$regex": f"\\b{user_input}\\b"}}
        ]
    }
    match = brain_collection.find_one(query)
    if match:
        return match.get('reply_text'), match.get('sticker_id')
    return None, None
