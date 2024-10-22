# main.py

from ui import Win as MainWin
from controller import Controller
app = MainWin(Controller())

if __name__ == "__main__":
    app.mainloop()

