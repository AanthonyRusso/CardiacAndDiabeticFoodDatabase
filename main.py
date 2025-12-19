import db
from app import App
if __name__ == "__main__":
    db.init_db()
    App().mainloop()
