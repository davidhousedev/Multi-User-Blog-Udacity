""" Clears authentication cookie """

import handler as handler

class LogOut(handler.Handler):
    def get(self):
        self.logout()
        self.redirect("/")