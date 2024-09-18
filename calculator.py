import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator with Voice Assistant")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        self.create_widgets()
        self.setup_voice_assistant()

    def create_widgets(self):
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        input_field = ttk.Entry(input_frame, textvariable=self.input_text, font=('Arial', 18), justify='right', width=25)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=10)

        btns_frame = ttk.Frame(self.root)
        btns_frame.pack()

        self.create_button(btns_frame, '7', 1, 0)
        self.create_button(btns_frame, '8', 1, 1)
        self.create_button(btns_frame, '9', 1, 2)
        self.create_button(btns_frame, '/', 1, 3)

        self.create_button(btns_frame, '4', 2, 0)
        self.create_button(btns_frame, '5', 2, 1)
        self.create_button(btns_frame, '6', 2, 2)
        self.create_button(btns_frame, '*', 2, 3)

     
        self.create_button(btns_frame, '1', 3, 0)
        self.create_button(btns_frame, '2', 3, 1)
        self.create_button(btns_frame, '3', 3, 2)
        self.create_button(btns_frame, '-', 3, 3)

        self.create_button(btns_frame, 'C', 4, 0)
        self.create_button(btns_frame, '0', 4, 1)
        self.create_button(btns_frame, '=', 4, 2)
        self.create_button(btns_frame, '+', 4, 3)

        voice_btn_frame = ttk.Frame(self.root)
        voice_btn_frame.pack(pady=10)
        voice_btn = ttk.Button(voice_btn_frame, text="Voice Command", command=self.voice_command)
        voice_btn.pack(ipadx=10, ipady=10)

    def create_button(self, frame, text, row, column):
        button = ttk.Button(frame, text=text, command=lambda: self.on_button_click(text))
        button.grid(row=row, column=column, ipadx=10, ipady=10, padx=5, pady=5)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                self.expression = str(eval(self.expression))
                self.speak(f"The result is {self.expression}")
            except Exception as e:
                self.expression = "Error"
                self.speak("Error")
        else:
            self.expression += str(char)
        self.input_text.set(self.expression)

    def setup_voice_assistant(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def voice_command(self):
        with sr.Microphone() as source:
            self.speak("Listening for command")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                self.speak(f"You said: {command}")
                self.process_voice_command(command)
            except sr.UnknownValueError:
                self.speak("Sorry, I did not understand that")
            except sr.RequestError:
                self.speak("Sorry, my speech service is down")

    def process_voice_command(self, command):
        command = command.lower()
        if "plus" in command:
            command = command.replace("plus", "+")
        if "minus" in command:
            command = command.replace("minus", "-")
        if "times" in command or "multiplied by" in command:
            command = command.replace("times", "*").replace("multiplied by", "*")
        if "divided by" in command:
            command = command.replace("divided by", "/")
        if "clear" in command:
            self.on_button_click('C')
            return
        if "equals" in command or "result" in command:
            self.on_button_click('=')
            return

        for char in command:
            if char in "0123456789+-*/":
                self.on_button_click(char)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
