from Model.model import get_session, face_embs
from View.CheckInOut import CheckInOut
import config
import tkinter as tk

session = get_session(config.SQLITE_DB_PATH)
root = tk.Tk()
root.geometry("1100x560")  
app = CheckInOut(root, session, face_embs, config.CAM_INDEX)
root.mainloop()