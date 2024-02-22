from collections import defaultdict, deque
from datetime import datetime, timedelta

from flask import jsonify, request

from server import LOGGER, app


class RequestRateLimiterMiddleware:
    def __init__(self, cr_app, limit=500, period=10, cooldown=60):
        self.app = cr_app
        self.limit = limit
        self.period = period
        self.cooldown = cooldown

        self.cache = defaultdict(lambda: defaultdict(deque))

        self.app.before_request(self.check_rate_limit)

    def check_rate_limit(self):
        ip_address = request.remote_addr
        endpoint = request.endpoint

        current_time = datetime.now()
        window_start = current_time - timedelta(seconds=self.period)

        request_queue = self.cache[ip_address][endpoint]

        # Remove requests that are outside the current window
        while request_queue and request_queue[0] < window_start:
            request_queue.popleft()

        if len(request_queue) >= self.limit:
            last_request_time = request_queue[-1]
            time_since_last_request = current_time - last_request_time

            if time_since_last_request.total_seconds() < self.cooldown:
                return jsonify(error="Too Many Requests, Please Try Again Later"), 429
            self.cache[ip_address][endpoint].clear()

        request_queue.append(current_time)


RequestRateLimiterMiddleware(cr_app=app)


@app.before_request
def authorize_request():
    auth_key = request.headers.get('Authorization')
    if not auth_key or auth_key != app.config['AUTHORIZATION']:
        return jsonify(error="Unauthorized Session Request"), 404


@app.errorhandler(404)
def no_route_found(error):
    LOGGER.error(f"API Not Found: {error}")
    return jsonify(error="No Route Found...!"), 404


@app.errorhandler(405)
def incorrect_methods(error):
    LOGGER.error(f"Method Not Allowed: {error}")
    return jsonify(errors="Method Not Allowed...!"), 400


@app.errorhandler(Exception)
def python_exception(error):
    LOGGER.error(f"Python Error: {error}")
    return jsonify(errors="Something Went Wrong...!"), 400
