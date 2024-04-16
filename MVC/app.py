from Model.model import get_session, face_embs
from View.CheckInOut import CheckInOut
import config
import tkinter as tk

session = get_session(config.SQLITE_DB_PATH)
root = tk.Tk()
app = CheckInOut(root, session, face_embs)
root.mainloop()