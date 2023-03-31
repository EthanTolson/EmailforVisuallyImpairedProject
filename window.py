import tkinter as tk
import math
from constants import FILEPATH, NUMBER_WORDS_CHANGE
from os import system
import mailing.mailing as mailing
import time
import voice.voice as voice

class Window():
    def __init__(self):
        # create tkinter object set the title
        self.window = tk.Tk()
        self.window.title("Email")
        self.window.state('zoomed')
        self.window.geometry("1000x500")
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.voice = voice.VoiceControl()
        self.vc = False

    def exit(self):
        # What happens when window is closed
        self.window.destroy()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def draw_interface(self):
        """
        draws the login interface to the screen should be called before the mainloop in main
        """
        # Buttons, entries, and labels that allow the user to create a connection
        self.loginbutton = tk.Button(text = "Login", background = "#259c45", activebackground = "#2621ad", font = 3, width = 10, height = 1, command = self.login)
        self.voice_control_button = tk.Button(text = "Voice Control", font = 3, width = 10, height = 1, command = self.prompt_voice_control)
        self.user = tk.Entry()
        self.label1 = tk.Label(text = "Username: ")

        self.password = tk.Entry()

        self.label4 = tk.Label(text = "Application Password: ")
        self.label5 = tk.Label(text = "Here is a link to find the application password: https://support.google.com/mail/answer/185833?hl=en")

        self.label3 = tk.Label(text = "")

        # Pack the buttons, labels and entries to the screen
        self.label1.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.user.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.label3.grid(row = 3, column = 1, columnspan = 2, padx = 10, pady = 10)
        self.label4.grid(row = 1, column = 3, padx = 10, pady = 10)
        self.password.grid(row = 1, column = 4, padx = 10, pady = 10)
        self.label5.grid(row = 2, column = 3, padx = 10, pady = 10)
        self.loginbutton.grid(row = 4, column = 1, columnspan = 2, padx = 10, pady = 10)
        self.voice_control_button.grid(row = 5, column = 1, columnspan = 2, padx = 10, pady = 10) 
        self.window.update()
        self.prompt_voice_control()

    def prompt_voice_control(self):
        """
        prompts the user to use voice control
        """
        system(f"{FILEPATH}prompts/voice_control_prompt.wav")
        response = self.voice.speech_to_text(10)
        if "yes" in response:
            self.label3.config(text = "Voice Control Active")
            self.window.update()
            self.vc = True
            self.voice_login()

    def voice_login(self):
        """
        allows the user to login with voice commands through prompts
        """
        self.password.delete(0, tk.END)
        self.user.delete(0, tk.END)
        self.window.update()
        print("Success")
        # prompt for user and password and attempt login
        system(f"{FILEPATH}prompts/user_prompt.wav")
        response = self.voice.speech_to_text(10)
        response = response.split(" ")
        username = ""
        for word in response:
            print(word)
            if word == "at":
                word = "@"
            if word in NUMBER_WORDS_CHANGE.keys():
                word = NUMBER_WORDS_CHANGE[word]
            username += word
        self.user.insert(tk.END, username.strip().replace(" ", ""))
        self.window.update()
        system(f"{FILEPATH}prompts/pass_prompt.wav")
        response = self.voice.speech_to_text(15)
        response = response.split(" ")
        password = ""
        for word in response:
            print(word)
            if word == "at":
                word = "@"
            password += word
        self.password.insert(tk.END, password.strip().replace(" ", ""))
        self.window.update()
        del username
        del password

        self.login()

    def bad_login_prompt(self):
        """
        if voice control is on then plays a message letting the user know that there was an issue
        """
        if self.vc:
            system(f"{FILEPATH}prompts/bad_user_pass_prompt.wav")
            response = self.voice.speech_to_text(10)
            if "yes" in response:
                self.voice_login()
            else:
                self.label3.config(text = "Voice Control Deactivated")
                self.vc = False

    def login(self):
        """
        Attempts to login to gmail server and update the view displays an error message if there was a problem
        """
        if self.user.get() == "" or self.password.get() =="":
            self.bad_login_prompt()
            self.label3.config(text = "Please enter an Username and/or Password.")
        elif self.user.get().strip()[-10:] != "@gmail.com":
            self.bad_login_prompt()
            self.label3.config(text = "Please enter a valid Gmail Email Address")

        self.mail = mailing.Mailing(self.user.get(), self.password.get())

        if not self.mail.try_login():
            self.bad_login_prompt()
            self.label3.config(text = "Please enter a valid Gmail Email Address/Check to make sure you are using the correct password")
        else:
            self.label3.config(text = "Success")
            if self.vc:
                system(f"{FILEPATH}prompts/login_success_prompt.wav")
            time.sleep(.5)
            self.email_interface()

    def email_interface(self):
        """
        draws the email interface after a successful login
        """
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


        self.email_one = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")
        self.email_two = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")
        self.email_three = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")
        self.email_four = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")
        self.email_five = tk.Button(text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")
        self.refresh_inbox = tk.Button(text = "Refresh Inbox", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")

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
        self.error_label.grid(column = 2, row = 9)

        self.get_recieved_emails()
        
    def get_text_from_speech(self, length):
        """
        used for testing get rid of it
        """
        self.body.insert(tk.END, self.voice.speech_to_text(length))

    def get_recieved_emails(self):
        """
        retrieves emails from google inbox and then displays them as buttons along the side of the screen
        """
        if self.mail.get_emails():
            if self.mail.messages_length == 1:
                self.email_one.config(text = self.mail.messages[0]["from"][0:14] + "\n" + self.mail.messages[0]["subj"][0:14], command = lambda: self.display_email(0))
                self.email_two.config(text = "")
                self.email_three.config(text = "")
                self.email_four.config(text = "")
                self.email_five.config(text = "")
            elif self.mail.messages_length == 2:
                self.email_one.config(text = self.mail.messages[0]["from"][0:14] + "\n" + self.mail.messages[0]["subj"][0:14], command = lambda: self.display_email(0))
                self.email_two.config(text = self.mail.messages[1]["from"][0:14] + "\n" + self.mail.messages[1]["subj"][0:14], command = lambda: self.display_email(1))
                self.email_three.config(text = "")
                self.email_four.config(text = "")
                self.email_five.config(text = "")
            elif self.mail.messages_length == 3:
                self.email_one.config(text = self.mail.messages[0]["from"][0:14] + "\n" + self.mail.messages[0]["subj"][0:14], command = lambda: self.display_email(0))
                self.email_two.config(text = self.mail.messages[1]["from"][0:14] + "\n" + self.mail.messages[1]["subj"][0:14], command = lambda: self.display_email(1))
                self.email_three.config(text = self.mail.messages[2]["from"][0:14] + "\n" + self.mail.messages[2]["subj"][0:14], command = lambda: self.display_email(2))
                self.email_four.config(text = "")
                self.email_five.config(text = "")
            elif self.mail.messages_length == 4:
                self.email_one.config(text = self.mail.messages[0]["from"][0:14] + "\n" + self.mail.messages[0]["subj"][0:14], command = lambda: self.display_email(0))
                self.email_two.config(text = self.mail.messages[1]["from"][0:14] + "\n" + self.mail.messages[1]["subj"][0:14], command = lambda: self.display_email(1))
                self.email_three.config(text = self.mail.messages[2]["from"][0:14] + "\n" + self.mail.messages[2]["subj"][0:14], command = lambda: self.display_email(2))
                self.email_four.config(text = self.mail.messages[3]["from"][0:14] + "\n" + self.mail.messages[3]["subj"][0:14], command = lambda: self.display_email(3))
                self.email_five.config(text = "")
            elif self.mail.messages_length == 0:
                self.email_one.config(text = "No Emails in Inbox")
                self.email_two.config(text = "No Emails in Inbox")
                self.email_three.config(text = "No Emails in Inbox")
                self.email_four.config(text = "No Emails in Inbox")
                self.email_five.config(text = "No Emails in Inbox")
            else:
                self.email_one.config(text = self.mail.messages[0]["from"][0:14] + "\n" + self.mail.messages[0]["subj"][0:14], command = lambda: self.display_email(0))
                self.email_two.config(text = self.mail.messages[1]["from"][0:14] + "\n" + self.mail.messages[1]["subj"][0:14], command = lambda: self.display_email(1))
                self.email_three.config(text = self.mail.messages[2]["from"][0:14] + "\n" + self.mail.messages[2]["subj"][0:14], command = lambda: self.display_email(2))
                self.email_four.config(text = self.mail.messages[3]["from"][0:14] + "\n" + self.mail.messages[3]["subj"][0:14], command = lambda: self.display_email(3))
                self.email_five.config(text = self.mail.messages[4]["from"][0:14] + "\n" + self.mail.messages[4]["subj"][0:14], command = lambda: self.display_email(4))
            self.error_label.config(text = "Emails Received")
        else:
            self.error_label.config(text = "There was an issue retrieving from your inbox.")

    def display_email(self, index):
        """"
        Displays the email that the user selects
        """
        self.reset_button_colors()

        self.body.delete("1.0", tk.END)
        self.user_from.config(text = self.mail.messages[index]['from'])
        self.user_to.delete(0, tk.END)
        self.user_to.insert(0, self.mail.user)
        self.subject.delete(0, tk.END)
        self.subject.insert(0, self.mail.messages[index]['subj'])
        self.body.insert("1.0", self.mail.messages[index]['body'])
        self.send_email_button.config(width = 20, text = "Return to Email View", command = self.email_interface)
        if index == 0:
            self.email_one.config(background = "#b4c0d6")
        elif index == 1:
            self.email_two.config(background = "#b4c0d6")
        elif index == 2:
            self.email_three.config(background = "#b4c0d6")
        elif index == 3:
            self.email_four.config(background = "#b4c0d6")
        elif index == 4:
            self.email_five.config(background = "#b4c0d6")

    def reset_button_colors(self):
        self.email_one.config(background = "#3474eb")
        self.email_two.config(background = "#3474eb")
        self.email_three.config(background = "#3474eb")
        self.email_four.config(background = "#3474eb")
        self.email_five.config(background = "#3474eb")

    def send_email(self):
        """
        attempts to send the email displays an error if it cannot
        """
        self.mail.create_message(self.user_to.get(), self.subject.get(), self.body.get("1.0", tk.END))
        if not self.mail.send_email():
            self.error_label.config(text = "Something went wrong check all the entry boxes.")
        else:
            self.error_label.config(text = "Email Sent Successfully!")
            self.user_to.delete(0, tk.END)
            self.subject.delete(0, tk.END)
            self.body.delete("1.0", tk.END)

    def read_email(self):
        """
        reads the selected email to the user
        """
        self.voice.text_to_speech(self.body.get("1.0", tk.END))