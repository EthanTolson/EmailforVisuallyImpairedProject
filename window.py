import tkinter as tk
import math
import constants
import mailing.mailing
import time
import voice.voice


class Window():
    def __init__(self):
        # create tkinter object set the title
        self.window = tk.Tk()
        self.window.title("Email")
        self.window.state('zoomed')
        self.window.geometry("1000x500")
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.voice = voice.voice.VoiceControl()

    def exit(self):
        # What happens when window is closed
        self.window.destroy()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def draw_interface(self):
            # Buttons, entries, and labels that allow the user to create a connection
            self.loginbutton = tk.Button(text = "Login", background = "#259c45", activebackground = "#2621ad", font = 3, width = 10, height = 1, command = self.login)
            self.user = tk.Entry()
            self.label1 = tk.Label(text = "Username: ")

            self.password = tk.Entry()

            self.label4 = tk.Label(text = "Application Password: ")
            self.label5 = tk.Label(text = "Here is a link to find the application password: PLACEHOLDER")

            self.label3 = tk.Label(text = "")

            # Pack the buttons, labels and entries to the screen
            self.label1.grid(row = 1, column = 1, padx = 10, pady = 10)
            self.user.grid(row = 1, column = 2, padx = 10, pady = 10)
            self.label3.grid(row = 3, column = 1, columnspan = 2, padx = 10, pady = 10)
            self.label4.grid(row = 1, column = 3, padx = 10, pady = 10)
            self.password.grid(row = 1, column = 4, padx = 10, pady = 10)
            self.label5.grid(row = 2, column = 3, padx = 10, pady = 10)
            self.loginbutton.grid(row = 4, column = 1, columnspan = 2, padx = 10, pady = 10)

    def login(self):
        if self.user.get() == "" or self.password.get() =="":
            self.label3.config(text = "Please enter an Username and/or Password.")
        elif self.user.get().strip()[-10:] != "@gmail.com":
            self.label3.config(text = "Please enter a valid Gmail Email Address")

        self.mail = mailing.mailing.Mailing(self.user.get(), self.password.get())

        if not self.mail.try_login():
            self.label3.config(text = "Please enter a valid Gmail Email Address/Check to make sure you are using the correct password")
        else:
            self.label3.config(text = "Success")
            time.sleep(.5)
            self.email_interface()

    def email_interface(self):
        self.clear_window()

        self.send_email_button = tk.Button(text = "Send Email", background = "#259c45", activebackground = "#2621ad", font = 3, width = 10, height = 1, command = self.send_email)
        self.user_from = tk.Label(text = self.mail.user)
        self.user_from_label = tk.Label(text = "From: ")
        self.user_to = tk.Entry()
        self.user_to_label = tk.Label(text = "To: ")
        self.subject = tk.Entry()
        self.subject_label = tk.Label(text = "Subject: ")
        self.body = tk.Text(width = 100, height = 10, border = 10, font = "Calibri")
        self.body_label = tk.Label(text = "Body: ")
        self.error_label = tk.Label(text = "")


        """TESTING PURPOSES REMOVE"""
        self.speech_button = tk.Button(text = "Speech to Text (Body) (10 secs)", command = lambda: self.get_text_from_speech(10))
        self.speech_button.grid(column = 1, row = 8)


        """TESTING PURPOSES REMOVE"""


        self.email_one = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails)
        self.email_two = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails)
        self.email_three = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails)
        self.email_four = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails)
        self.email_five = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails)
        self.refresh_inbox = tk.Button(text = "Refresh Inbox", command = self.get_recieved_emails)

        self.email_one.grid(column = 1, row = 2, pady = 10, padx = 10)
        self.email_two.grid(column = 1, row = 3, pady = 10, padx = 10)
        self.email_three.grid(column = 1, row = 4, pady = 10, padx = 10)
        self.email_four.grid(column = 1, row = 5, pady = 10, padx = 10)
        self.email_five.grid(column = 1, row = 6, pady = 10, padx = 10)
        self.refresh_inbox.grid(column = 1, row = 7)

        self.send_email_button.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.user_from.grid(column = 3, row = 1, padx = 1, pady = 2)
        self.user_to.grid(column = 3, row = 2, padx = 1, pady = 2)
        self.subject.grid(column = 3, row = 3, padx = 1, pady = 2)
        self.user_from_label.grid(column = 2, row = 1, padx = 1, pady = 2)
        self.user_to_label.grid(column = 2, row = 2, padx = 1, pady = 2)
        self.subject_label.grid(column = 2, row = 3, padx = 1, pady = 2)
        self.body_label.grid(column = 2, row = 4, padx = 1, pady = 2)
        self.body.grid(column = 2, columnspan = 4, row = 5, rowspan = 4, padx = 1, pady = 2)
        self.error_label.grid(column = 1, row = 2)

        self.get_recieved_emails()

    def get_text_from_speech(self, length):
        self.body.config(text = self.voice.speech_to_text(length))

    def get_recieved_emails(self):
        if self.mail.get_emails():
            if self.mail.messages_length < 5:
                for i in range(0, self.mail.messages_length):
                    pass
            else:
                self.email_one.config(text = self.mail.messages[0]["from"] + "\n" + self.mail.messages[0]["subj"], command = lambda: self.display_email(0))
                self.email_two.config(text = self.mail.messages[1]["from"] + "\n" + self.mail.messages[1]["subj"], command = lambda: self.display_email(1))
                self.email_three.config(text = self.mail.messages[2]["from"] + "\n" + self.mail.messages[2]["subj"], command = lambda: self.display_email(2))
                self.email_four.config(text = self.mail.messages[3]["from"] + "\n" + self.mail.messages[3]["subj"], command = lambda: self.display_email(3))
                self.email_five.config(text = self.mail.messages[4]["from"] + "\n" + self.mail.messages[4]["subj"], command = lambda: self.display_email(4))
        else:
            self.error_label.config(text = "There was an issue retrieving from your inbox.")

        


    def display_email(self, index):
        """"
        Displays the email that the user selects
        """
        self.clear_window()
        # self.send_email_button.destroy()
        # self.user_from.destroy()
        # self.user_from_label.destroy()
        # self.user_to.destroy()
        # self.user_to_label.destroy()
        # self.subject.destroy()
        # self.subject_label.destroy()
        # self.body.destroy()
        # self.body_label.destroy()
        # self.error_label.destroy()
        

    def send_email(self):
        self.mail.create_message(self.user_to.get(), self.subject.get(), self.body.get("1.0", tk.END))
        if not self.mail.send_email():
            self.error_label.config(text = "Something went wrong check all the entry boxes.")
        else:
            self.error_label.config(text = "Email Sent Successfully!")
            self.user_to.delete(0, tk.END)
            self.subject.delete(0, tk.END)
            self.body.delete("1.0", tk.END)

