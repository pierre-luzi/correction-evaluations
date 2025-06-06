#!/usr/bin/env python3
from gui.app import Application
from database.connection import init_db

if __name__ == "__main__":
    init_db()
    app = Application()
    app.mainloop()