# inventory/middleware.py
import redis
from django.conf import settings
from redis_cache import redis_client
from django.utils.deprecation import MiddlewareMixin

class RedisSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.session.get('user_id'):
            session_key = f"user:{request.session['user_id']}:session"
            session_data = redis_client.get(session_key)
            if session_data:
                print(f"Session data found for user {request.session['user_id']} in Redis.")
            else:
                print(f"No Redis session found for user {request.session['user_id']}")

    def process_response(self, request, response):
        if request.session.get('user_id'):
            session_key = f"user:{request.session['user_id']}:session"
            redis_client.set(session_key, request.session.session_key, ex=3600)  # 1 hour
            print(f"Session data stored in Redis for user {request.session['user_id']}")
        return response
