from modules.Study_record import LearningTimerWindow
from SuffixModify_window import Wzapp

def open_learning_timer(app):
    app.learning_timer_window = LearningTimerWindow()
    app.learning_timer_window.show()

def wz_modi(app):
    dialog = Wzapp(app)
    dialog.show()