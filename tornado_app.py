import os
import random

import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.websocket
from dotenv import load_dotenv
from tornado.ioloop import PeriodicCallback

from auth import GitHubLoginHandler, GitHubCallbackHandler, LogoutHandler, BaseHandler, COOKIE_SECRET, \
    WEBSOCKET_ENDPOINT
from websocket import connected_clients, WebSocketHandler

load_dotenv('.env')
RANDOM_NUMBER_INTERVAL = int(os.environ["RANDOM_NUMBER_INTERVAL"])
DEBUG = os.environ["DEBUG"]


def get_random_number():
    random_number = random.randint(0, 100)
    return random_number


class MainHandler(BaseHandler):
    def get(self):
        if not self.get_current_user():
            self.render("login.html")
        else:
            random_number = get_random_number()
            self.render("index.html", initial_number=random_number, user=self.get_current_user(),
                        WEBSOCKET_ENDPOINT=WEBSOCKET_ENDPOINT)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/auth/login", GitHubLoginHandler),
        (r"/auth/callback", GitHubCallbackHandler),
        (r"/auth/logout", LogoutHandler),
        (r"/websocket", WebSocketHandler),
    ], cookie_secret=COOKIE_SECRET, debug=DEBUG, template_path="templates")


def update_random_number():
    random_number = get_random_number()
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
