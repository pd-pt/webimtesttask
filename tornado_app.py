import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.websocket
import tornado.gen
import requests
import json
import uuid
from tornado.ioloop import IOLoop, PeriodicCallback
from auth import GitHubLoginHandler, GitHubCallbackHandler, LogoutHandler, BaseHandler, COOKIE_SECRET, WEBSOCKET_ENDPOINT
from websocket import connected_clients, WebSocketHandler
import random

RANDOM_NUMBER_INTERVAL = 5000

class MainHandler(BaseHandler):
    def get(self):
        if not self.get_current_user():
            self.render("login.html")
        else:
            self.render("index.html", user=self.get_current_user(), WEBSOCKET_ENDPOINT=WEBSOCKET_ENDPOINT)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/auth/login", GitHubLoginHandler),
        (r"/auth/callback", GitHubCallbackHandler),
        (r"/auth/logout", LogoutHandler),
        (r"/websocket", WebSocketHandler),
    ], cookie_secret=COOKIE_SECRET, debug=True, template_path="templates")


def update_random_number():
    random_number = random.randint(0, 100)
    for client in connected_clients:
        client.write_message(f"{random_number}")

def start_periodic_job():
    interval = RANDOM_NUMBER_INTERVAL 
    periodic_callback = PeriodicCallback(update_random_number, interval)
    periodic_callback.start()

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    start_periodic_job()
    tornado.ioloop.IOLoop.current().start()