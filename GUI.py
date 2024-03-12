import tkinter as tk
from tkinter import messagebox
from pandastable import Table, TableModel
import os
import pandas as pd
from constants import USERNAME, PASSWORD
from encrypt_decrypt import encrypt_excel, decrypt_excel
import matplotlib.pyplot as plt


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def check_credentials(window, username, password):
    if username == USERNAME and password == PASSWORD:
        window.destroy()
        data_screen()
    else:
        messagebox.showerror('Error', 'Invalid credentials')


def login_screen():
    login_window = tk.Tk()
    login_window.title('Login')
    login_window.state('zoomed')
    login_window.geometry('1920x1080')
    login_window.lift()

    username_label = tk.Label(login_window, text='Username')
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text='Password')
    password_label.pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()

    submit_button = tk.Button(login_window, text='Submit',
                              command=lambda: check_credentials(login_window, username_entry.get(),
                                                                password_entry.get()))
    submit_button.pack()

    login_window.mainloop()


def data_screen():
    global data_window
    data_window = tk.Tk()
    data_window.title('Data')
    data_window.state('zoomed')
    data_window.geometry('1920x1080')

    subject_label = tk.Label(data_window, text='Subject')
    subject_label.pack()
    subject_entry = tk.Entry(data_window)
    subject_entry.pack()

    sem_label = tk.Label(data_window, text='Semester')
    sem_label.pack()
    sem_entry = tk.Entry(data_window)
    sem_entry.pack()

    year_label = tk.Label(data_window, text='Year')
    year_label.pack()
    year_entry = tk.Entry(data_window)
    year_entry.pack()

    button_frame = tk.Frame(data_window)
    button_frame.pack()

    # Create a frame for the buttons
    button_frame = tk.Frame(data_window)
    button_frame.pack()

    # Add the load button
    load_button = tk.Button(button_frame, text='Load',
                            command=lambda: load_data(subject_entry.get(), sem_entry.get(), year_entry.get()))
    load_button.pack(side='left', padx=5)  # Use side='left' to arrange the buttons side by side
    createToolTip(load_button, "Load the data from the specified Excel file")

    # Add the analyze button for the previous analysis
    analyze_button = tk.Button(button_frame, text='Analyze',
                               command=lambda: analyze_data(subject_entry.get(), sem_entry.get(), year_entry.get()))
    analyze_button.pack(side='left', padx=5)
    createToolTip(analyze_button, "Perform the analysis of getting average scores of each unit")

    # Add another button for the new analysis
    analyze_button_2 = tk.Button(button_frame, text='Analyze Difficulty',
                                 command=lambda: analyze_difficulty(subject_entry.get(), sem_entry.get(),
                                                                    year_entry.get()))
    analyze_button_2.pack(side='left', padx=5)
    createToolTip(analyze_button_2, "Perform the difficulty analysis on each question (question wise average)")

    analyze_button_3 = tk.Button(button_frame, text='Analyze Pass/Fail',
                                 command=lambda: analyze_pass_fail(subject_entry.get(), sem_entry.get(),
                                                                   year_entry.get()))
    analyze_button_3.pack(side='left', padx=5)
    createToolTip(analyze_button_3, "Perform the pass/fail analysis on the loaded data")

    data_window.mainloop()


# Define frame globally
frame = None


def load_data(subject, sem, year):
    global data_window, frame
    filename = f'C:\\major-version1.0\\Excels\\{subject}-{sem}-{year}.xlsx'
    if os.path.exists(filename):
        # Destroy the existing frame and create a new one
        if frame is not None:
            frame.destroy()
        # Decrypt here
        decrypt_excel(subject, sem, year, filename)
        data = pd.read_excel(filename)
        # Encrypt immediately
        encrypt_excel(subject, sem, year, filename)
        frame = tk.Frame(data_window)
        frame.pack(fill='both', expand=True)
        pt = Table(frame, dataframe=data, showtoolbar=False, showstatusbar=True)
        pt.show()
    else:
        messagebox.showerror('Error', 'File does not exist')


def analyze_data(subject, sem, year):
    filename = f'C:\\major-version1.0\\Excels\\{subject}-{sem}-{year}.xlsx'
    if os.path.exists(filename):
        decrypt_excel(subject, sem, year, filename)
        data = pd.read_excel(filename)
        encrypt_excel(subject, sem, year, filename)
        # Calculate the total for each question and the best total for each unit
        units = ['Unit1', 'Unit2', 'Unit3', 'Unit4', 'Unit5']
        best_scores = []
        for i in range(1, 11, 2):
            q1_total = data[[f'Q{i}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
            q2_total = data[[f'Q{i + 1}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
            best_scores.append(pd.concat([q1_total, q2_total], axis=1).max(axis=1))

        # Create a DataFrame from the best scores
        scores_df = pd.DataFrame(best_scores).T
        scores_df.columns = units

        # Calculate the average score for each unit
        avg_scores = scores_df.mean()

        # Create a bar chart of the average scores
        avg_scores.plot(kind='bar')
        plt.title('Average Scores by Unit')
        plt.xlabel('Unit')
        plt.ylabel('Average Score')
        plt.show()
    else:
        messagebox.showerror('Error', 'File does not exist')
    encrypt_excel(subject, sem, year, filename)


def analyze_difficulty(subject, sem, year):
    filename = f'C:\\major-version1.0\\Excels\\{subject}-{sem}-{year}.xlsx'
    if os.path.exists(filename):
        decrypt_excel(subject, sem, year, filename)
        data = pd.read_excel(filename)
        encrypt_excel(subject, sem, year, filename)
        # Calculate the total for each question
        question_totals = []
        for i in range(1, 11):
            question_cols = [f'Q{i}_Bit{j}' for j in range(1, 4)]
            question_totals.append(data[question_cols].sum(axis=1))

        # Create a DataFrame from the question totals
        totals_df = pd.DataFrame(question_totals).T

        # Calculate the average total for each question
        avg_totals = totals_df.mean()

        # Create a bar chart of the average totals
        avg_totals.plot(kind='bar')
        plt.title('Average Totals by Question')
        plt.xlabel('Question')
        plt.ylabel('Average Total')
        plt.show()
    else:
        messagebox.showerror('Error', 'File does not exist')


def analyze_pass_fail(subject, sem, year):
    filename = f'C:\\major-version1.0\\Excels\\{subject}-{sem}-{year}.xlsx'
    if os.path.exists(filename):
        decrypt_excel(subject, sem, year, filename)
        data = pd.read_excel(filename)
        encrypt_excel(subject, sem, year, filename)
        # Calculate the number of students who passed and failed
        pass_count = len(data[data['Sum'] >= 25])
        fail_count = len(data[data['Sum'] < 25])

        # Create a pie chart of the pass/fail counts
        plt.pie([pass_count, fail_count], labels=['Pass', 'Fail'], autopct='%1.1f%%')
        plt.title('Pass/Fail Analysis')
        plt.show()
# sample usage
# login_screen()
