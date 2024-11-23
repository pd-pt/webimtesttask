import tornado.gen

from auth import sessions

connected_clients = set()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if not self.get_secure_cookie("session_id") or self.get_secure_cookie("session_id").decode(
                'utf-8') not in sessions:
            self.close()
            return

        connected_clients.add(self)

    def on_close(self):
        connected_clients.remove(self)
