import redis
import json
from datetime import datetime, timedelta

class ConversationMemory:
    def __init__(self, redis_url="redis://localhost:6379"):
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
        except:
            print("⚠️ Redis não disponível. Memória desativada.")
            self.redis_client = None
        self.ttl = timedelta(hours=1)
    
    def get_session(self, user_id):
        if not self.redis_client:
            return {"history": [], "context": {}}
        data = self.redis_client.get(f"session:{user_id}")
        return json.loads(data) if data else {"history": [], "context": {}}
    
    def save_session(self, user_id, session_data):
        if self.redis_client:
            self.redis_client.setex(
                f"session:{user_id}",
                self.ttl,
                json.dumps(session_data)
            )
    
    def add_message(self, user_id, role, content):
        session = self.get_session(user_id)
        session["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        session["history"] = session["history"][-10:]
        self.save_session(user_id, session)