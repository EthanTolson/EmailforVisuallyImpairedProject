import tkinter as tk
from constants import FILEPATH, NUMBER_WORDS_CHANGE
import mailing.mailing as mailing
import database.database as db
import time
import voice.voice as voice
from playsound import playsound # needs to be version 1.2.2 1.3.x has issues
import language_tool_python

class Window():
    def __init__(self):
        # create tkinter object set the title
        self.window = tk.Tk()
        self.window.title("Email")
        self.window.state('zoomed')
        self.window.geometry("1000x500")
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.window.configure(bg = "#34ebb1")
        self.voice = voice.VoiceControl()
        self.vc = False
        self.not_in_voice = True

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
        self.label1 = tk.Label(text = "Username: ", bg = "#34ebb1")

        self.password = tk.Entry()

        self.label4 = tk.Label(text = "Application Password: ", bg = "#34ebb1")
        self.label5 = tk.Label(text = "Here is a link to find the application password: https://support.google.com/mail/answer/185833?hl=en", bg = "#34ebb1")

        self.label3 = tk.Label(text = "", bg = "#34ebb1")

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
        playsound(f'{FILEPATH}prompts/voice_control_prompt1.wav', block = True)
        # playsound(f"{FILEPATH}prompts/voice_control_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(4)
        playsound(f"{FILEPATH}prompts/ding.wav")
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
        # prompt for user and password and attempt login
        playsound(f"{FILEPATH}prompts/user_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(10)
        playsound(f"{FILEPATH}prompts/ding.wav")
        response = response.split(" ")
        username = ""
        for word in response:
            if word == "at":
                word = "@"
            if word in NUMBER_WORDS_CHANGE.keys():
                word = NUMBER_WORDS_CHANGE[word]
            username += word
        self.user.insert(tk.END, username.strip().replace(" ", ""))
        self.window.update()
        playsound(f"{FILEPATH}prompts/pass_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(15)
        playsound(f"{FILEPATH}prompts/ding.wav")
        response = response.split(" ")
        password = ""
        for word in response:
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
            playsound(f"{FILEPATH}prompts/bad_user_pass_prompt.wav")
            playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
            response = self.voice.speech_to_text(4)
            playsound(f"{FILEPATH}prompts/ding.wav")
            if "yes" in response:
                self.voice_login()
            else:
                self.label3.config(text = "Voice Control Deactivated")
                self.vc = False

    def login(self):
        """
        Attempts to login to gmail server and update the view displays an error message if there was a problem
        """
        if self.user.get() == "" or self.password.get() == "":
            self.bad_login_prompt()
            self.label3.config(text = "Please enter an Username and/or Password.")
        elif self.user.get().strip()[-10:] != "@gmail.com":
            self.bad_login_prompt()
            self.label3.config(text = "Please enter a valid Gmail Email Address")

        self.mail = mailing.Mailing(self.user.get(), self.password.get())

        if not self.mail.try_login():
            self.label3.config(text = "Please enter a valid Gmail Email Address/Check to make sure you are using the correct password")
            self.bad_login_prompt()
            self.window.update()
        else:
            self.label3.config(text = "Success")
            try:
                self.db = db.DB_query(self.user.get().lower())
            except:
                self.label3.config(text = "MongoDB issue Connecting")
                time.sleep(.5)
            self.window.update()
            if self.vc:
                playsound(f"{FILEPATH}prompts/login_success_prompt.wav")
            time.sleep(.5)
            self.email_interface()

    def prompt_read_compose(self):
        self.not_in_voice = False
        self.email_interface()
        self.vc = True
        playsound(f"{FILEPATH}prompts/read_compose_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(5)
        playsound(f"{FILEPATH}prompts/ding.wav")
        if "compose" in response:
            self.window.update()
            self.voice_compose()
        elif "read" in response:
            self.window.update()
            self.prompt_email_read()
        elif "disable" in response:
            self.error_label.config(text = "Voice Control Deactivated")
            self.vc = False
            self.not_in_voice = True
        else:
            playsound(f"{FILEPATH}prompts/issue_with_response_prompt.wav")
            self.window.update()
            self.prompt_read_compose()

    def prompt_email_read(self):
        """
        prompts the user for what email they want to read then reads that email
        """
        playsound(f"{FILEPATH}prompts/which_read_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(5)
        if "one" in response:
            self.display_email(0)
        elif "two" in response:
            self.display_email(1)
        elif "three" in response:
            self.display_email(2)
        elif "four" in response:
            self.display_email(3)
        elif "five" in response:
            self.display_email(4)
        else:
            playsound(f"{FILEPATH}prompts/read_error_prompt.wav")
        self.prompt_read_compose()

    def voice_compose(self):
        self.prompt_to()
        self.prompt_subject()
        self.prompt_body()

    def prompt_to(self):
        playsound(f"{FILEPATH}prompts/to_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(15)
        playsound(f"{FILEPATH}prompts/ding.wav")
        response = response.split(" ")
        username = ""
        for word in response:
            if word.lower() == "at":
                word = "@"
            if word.lower() in NUMBER_WORDS_CHANGE.keys():
                word = NUMBER_WORDS_CHANGE[word]
            username += word
        self.user_to.delete(0, tk.END)
        self.user_to.insert(0, username.strip().replace(" ", "").lower())
        self.window.update()

    def prompt_subject(self):
        playsound(f"{FILEPATH}prompts/subject_prompt.wav")
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(15)
        playsound(f"{FILEPATH}prompts/ding.wav")
        self.subject.delete(0, tk.END)
        self.subject.insert(0, response)
        self.window.update()

    def prompt_body(self, replace = False):
        if replace:
            self.body.delete("1.0", tk.END)
        playsound(f"{FILEPATH}prompts/body_prompt.wav")
        response = "continue"
        while "stop" not in response and "continue" in response:
            playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
            self.body.insert(tk.END, self.voice.speech_to_text(15))
            playsound(f"{FILEPATH}prompts/ding.wav")
            response = self.voice.speech_to_text(5)
            self.window.update()
        
        self.fix_grammar()

        self.read_message_contents()

    def fix_grammar(self):
        """
        Fixes grammar from speech to text.
        """
        # fix grammar mistakes
        tool = language_tool_python.LanguageTool('en-US')

        text = self.body.get("1.0", tk.END)

        # get the matches
        matches = tool.check(text)

        my_mistakes = []
        my_corrections = []
        start_positions = []
        end_positions = []

        for rules in matches:
            if len(rules.replacements) > 0:
                start_positions.append(rules.offset)
                end_positions.append(rules.errorLength + rules.offset)
                my_mistakes.append(text[rules.offset : rules.errorLength + rules.offset])
                my_corrections.append(rules.replacements[0])

        my_new_text = list(text)

        for m in range(len(start_positions)):
            for i in range(len(text)):
                my_new_text[start_positions[m]] = my_corrections[m]
                if (i > start_positions[m] and i < end_positions[m]):
                    my_new_text[i]=""

        my_new_text = "".join(my_new_text)
        self.body.delete("1.0", tk.END)
        self.window.update()
        self.body.insert("1.0", my_new_text)
        self.window.update()

    def read_message_contents(self):
        playsound(f"{FILEPATH}prompts/check_input_prompt.wav")
        self.voice.text_to_speech(self.user_to.get())
        response = self.voice.speech_to_text(5)
        while "incorrect" in response:
            self.prompt_to()
            playsound(f"{FILEPATH}prompts/user_to_check_prompt.wav")
            self.voice.text_to_speech(self.user_to.get())
            playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
            response = self.voice.speech_to_text(5)                
        
        playsound(f"{FILEPATH}prompts/subject_check_prompt.wav")
        self.voice.text_to_speech(self.subject.get())
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(5)
        while "incorrect" in response:
            self.prompt_subject()
            playsound(f"{FILEPATH}prompts/subject_check_prompt.wav")
            self.voice.text_to_speech(self.user_to.get())
            playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
            response = self.voice.speech_to_text(5)

        playsound(f"{FILEPATH}prompts/body_check_prompt.wav")
        self.voice.text_to_speech(self.body.get("1.0", tk.END))
        playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
        response = self.voice.speech_to_text(5)
        while "incorrect" in response:
            self.prompt_body(True)
            playsound(f"{FILEPATH}prompts/body_check_prompt.wav")
            self.voice.text_to_speech(self.user_to.get())
            playsound(f"{FILEPATH}prompts/beginspeakingprompt.wav")
            response = self.voice.speech_to_text(5)

        playsound(f"{FILEPATH}prompts/final_check_prompt.wav")

        self.send_email()

        if self.error_label.cget("text") == "Something went wrong check all the entry boxes.":
            self.voice_compose()
        else:
            self.prompt_read_compose()

    def save_as_draft(self):
        try:
            self.db.save_draft(self.user_to.get().lower().strip(), self.subject.get().strip(), self.body.get("1.0", tk.END))
            self.user_to.delete(0, tk.END)
            self.subject.delete(0, tk.END)
            self.body.delete("1.0", tk.END)
        except:
            self.error_label.config(text = "Error saving Draft")
    
    def open_draft(self):
        subj = self.clicked2.get()
        for draft in self.drafts:
            if subj == draft[1]:
                self.user_to.delete(0, tk.END)
                self.subject.delete(0, tk.END)
                self.body.delete("1.0", tk.END)
                self.user_to.insert(0, draft[0])
                self.subject.insert(0, draft[1])
                self.body.insert("1.0", draft[2])
                break

    def email_interface(self):
        """
        draws the email interface after a successful login
        """
        self.clear_window()

        self.send_email_button = tk.Button(text = "Send Email", background = "#259c45", activebackground = "#2621ad", font = 3, width = 30, height = 5, command = self.send_email)
        self.user_from = tk.Label(text = self.mail.user)
        self.user_from_label = tk.Label(text = "From: ", bg = "#34ebb1")
        self.user_to = tk.Entry()
        self.user_to_label = tk.Label(text = "To: ", bg = "#34ebb1")
        self.subject = tk.Entry()
        self.subject_label = tk.Label(text = "Subject: ", bg = "#34ebb1")
        self.body = tk.Text(width = 100, height = 10, border = 10, font = "Calibri")
        self.body_label = tk.Label(text = "Body: ", bg = "#34ebb1")
        self.error_label = tk.Label(text = "", bg = "#34ebb1")


        self.draft_frame = tk.Frame(bg = "#34ebb1")
        self.save_draft = tk.Button(self.draft_frame, text = "Save as Draft", command = self.save_as_draft, width = 10, height = 2, background = "#3474eb")
        self.open_drafts = tk.Button(self.draft_frame, text = "Open a Draft", command = self.open_draft, width = 10, height = 2, background = "#3474eb")
        self.clicked2 = tk.StringVar()
        self.clicked2.set("")
        try:
            self.drafts = self.db.get_drafts()
            draft_names = [""]
            for item in self.drafts:
                draft_names.append(item[1])
        except:
            draft_names = [""]
            self.error_label.config(text = "Database Error")
        self.draft = tk.OptionMenu(self.draft_frame, self.clicked2, *draft_names)
        self.drafts_label = tk.Label(self.draft_frame, text = "Drop Down Menu for Drafts", bg = "#34ebb1")
        self.drafts_label.grid(column = 2, row = 1, pady = 10, padx = 10)
        self.draft.grid(column = 2, row = 2, pady = 10, padx = 10)
        self.open_drafts.grid(column = 3, row = 1, rowspan = 2, pady = 10, padx = 10)
        self.save_draft.grid(column = 1, row = 1, rowspan = 2, pady = 10, padx = 10)

        self.draft_frame.grid(column = 4, row = 3)


        self.contact_frame = tk.Frame(bg = "#34ebb1")
        self.contact_frame.grid(column = 4, row = 2)
        self.clicked1 = tk.StringVar()
        self.clicked1.set("")
        try:
            contacts = self.db.get_addresses()
        except:
            contacts = [""]
            self.error_label.config(text = "Database Error")
        self.contacts = tk.OptionMenu(self.contact_frame, self.clicked1, *contacts)
        self.contacts_label = tk.Label(self.contact_frame, text = "Drop Down Menu for Contacts", bg = "#34ebb1")
        self.contacts_label.grid(column = 1, row = 1, pady = 10, padx = 10)
        self.contacts.grid(column = 1, row = 2, pady = 10, padx = 10)

        self.add_to_contacts_button = tk.Button(self.contact_frame, text = "Add to Contacts", command = self.add_contact, background = "#3474eb")
        self.add_to_contacts_button.grid(column = 2, row = 2, pady = 10, padx = 10)

        self.speech_button = tk.Button(text = "Voice Control", command = self.prompt_read_compose)
        self.speech_button.grid(column = 1, row = 8)

        self.inbox = tk.Frame(bg = "#767a79", height = 24, width = 30)
        self.inbox_label = tk.Label(self.inbox, text = "Inbox", bg = "#767a79", font = ("Calibri", 20))

        self.email_one = tk.Button(self.inbox, text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 25, height = 3, background = "#3474eb")
        self.email_two = tk.Button(self.inbox,text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 25, height = 3, background = "#3474eb")
        self.email_three = tk.Button(self.inbox,text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 25, height = 3, background = "#3474eb")
        self.email_four = tk.Button(self.inbox,text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 25, height = 3, background = "#3474eb")
        self.email_five = tk.Button(self.inbox,text = "REFRESH EMAILS", command = self.get_recieved_emails, width = 25, height = 3, background = "#3474eb")
        self.refresh_inbox = tk.Button(self.inbox,text = "Refresh Inbox", command = self.get_recieved_emails, width = 15, height = 3, background = "#3474eb")

        self.inbox_label.grid(column = 1, row = 1)
        self.email_one.grid(column = 1, row = 2, pady = 10, padx = 10)
        self.email_two.grid(column = 1, row = 3, pady = 10, padx = 10)
        self.email_three.grid(column = 1, row = 4, pady = 10, padx = 10)
        self.email_four.grid(column = 1, row = 5, pady = 10, padx = 10)
        self.email_five.grid(column = 1, row = 6, pady = 10, padx = 10)
        self.refresh_inbox.grid(column = 1, row = 7)

        self.inbox.grid(column = 1, row = 2, rowspan = 6, padx = 10, pady = 10)

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

        self.window.update()

        if self.vc and self.not_in_voice:
            self.prompt_read_compose()

    def add_contact(self):
        user = self.user_to.get().lower()
        if user == "":
            self.error_label.config(text = "Error Adding to Addressbook")
        elif self.db.add_to_address_book(user):
            self.error_label.config(text = "Added to AddressBook")
        else:
            self.error_label.config(text = "Error Adding to Addressbook")

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
        if self.mail.messages_length < index:
            playsound(f"{FILEPATH}prompts/error_read_prompt.wav")
            self.error_label.config(text = "There is no Email.")
        else:
            self.body.delete("1.0", tk.END)
            self.user_from.config(text = self.mail.messages[index]['from'])
            self.user_to.delete(0, tk.END)
            self.user_to.insert(0, self.mail.user)
            self.subject.delete(0, tk.END)
            self.subject.insert(0, self.mail.messages[index]['subj'])
            self.body.insert("1.0", self.mail.messages[index]['body'])
            self.send_email_button.config(width = 20, text = "Return to Email View", command = self.email_interface)
            self.window.update()
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
            self.window.update()
            if self.vc:
                self.voice.text_to_speech(f"Now reading email from {self.mail.messages[index]['from']}, Subject, {self.mail.messages[index]['subj']}, Body, {self.mail.messages[index]['body']}")

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
        if self.user_to.get() == "" and self.clicked1.get() != "":
            self.mail.create_message(self.clicked1.get(), self.subject.get(), self.body.get("1.0", tk.END))
        else:
            self.mail.create_message(self.user_to.get(), self.subject.get(), self.body.get("1.0", tk.END))
        if not self.mail.send_email():
            if self.vc:
                playsound(f"{FILEPATH}prompts/email_fail_prompt.wav")
            self.error_label.config(text = "Something went wrong check all the entry boxes.")
        else:
            if self.vc:
                playsound(f"{FILEPATH}prompts/email_success_prompt.wav")
            self.error_label.config(text = "Email Sent Successfully!")
            self.user_to.delete(0, tk.END)
            self.subject.delete(0, tk.END)
            self.body.delete("1.0", tk.END)

    def read_email(self):
        """
        reads the selected email to the user
        """
        self.voice.text_to_speech(self.body.get("1.0", tk.END))