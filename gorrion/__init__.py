from Framework.gorrion_framework import App
import pyautogui


if __name__=='__main__':
    app=App(pyautogui.size().width,pyautogui.size().height)
    app.mainloop()
