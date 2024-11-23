import json
import os
import uuid

import requests
import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.web
from dotenv import load_dotenv

sessions = {}

load_dotenv('.env')

# GitHub OAuth configuration
GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
GITHUB_CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]
GITHUB_REDIRECT_URI = os.environ["GITHUB_REDIRECT_URI"]
COOKIE_SECRET = os.environ["COOKIE_SECRET"]
WEBSOCKET_ENDPOINT = os.environ["WEBSOCKET_ENDPOINT"]


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session_id = self.get_secure_cookie("session_id")
        if session_id and session_id.decode('utf-8') in sessions:
            return sessions[session_id.decode('utf-8')]
        return None


class GitHubLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(
            f"https://github.com/login/oauth/authorize"
            f"?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email"
        )


class GitHubCallbackHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument('code')
        http_client = tornado.httpclient.AsyncHTTPClient()

        # Step 1: Exchange the code for an access token
        response = yield http_client.fetch(
            f"https://github.com/login/oauth/access_token",
            method="POST",
            headers={'Accept': 'application/json'},
            body=f"client_id={GITHUB_CLIENT_ID}&client_secret={GITHUB_CLIENT_SECRET}&code={code}&redirect_uri={GITHUB_REDIRECT_URI}"
        )

        access_token = json.loads(response.body)['access_token']

        # Step 2: Use the access token to fetch user data
        user_response = requests.get(
            "https://api.github.com/user",
            headers={'Authorization': f'token {access_token}'}
        )
        user_data = user_response.json()

        # Step 3: Store user data in memory with a session ID
        session_id = str(uuid.uuid4())
        sessions[session_id] = user_data

        # Step 4: Set a secure cookie with the session ID
        self.set_secure_cookie("session_id", session_id)

        # Redirect to the home page
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        session_id = self.get_secure_cookie("session_id")
        if session_id:
            sessions.pop(session_id.decode('utf-8'), None)
        self.clear_cookie("session_id")
        self.redirect("/")
