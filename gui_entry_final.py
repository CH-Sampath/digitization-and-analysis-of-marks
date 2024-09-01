import pandas as pd
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import PIL
from encrypt_decrypt import encrypt_excel, decrypt_excel
# Declare img as a global variable
img = None

def process_marks(name, sem, acyear, excel_path, folder_path):
    # Decrypt the excel data
    decrypt_excel(name, sem, acyear, excel_path)
    # Load the Excel data
    df = pd.read_excel(excel_path)

    encrypt_excel(name, sem, acyear, excel_path)

    # Function to find the most similar file
    def find_file(barcode, folder_path):
        # Get a list of all files in the folder
        files = os.listdir(folder_path)

        # Iterate over all files
        for file in files:
            # If the barcode is in the file name
            barcode_file = file[file.find("_") + 1: file.find(".")]
            if str(barcode_file) == str(barcode):
                # Return the full path to the file
                return os.path.join(folder_path, file)

        return None

    # Create the main window
    root = Tk()

    # Create a Frame for the Entry widgets
    frame = Frame(root)
    frame.grid(row=0, column=1)

    # Create a Canvas widget
    canvas = Canvas(root, width=1200, height=800)
    canvas.grid(row=0, column=0)

    # Create a list to store the Entry widgets
    entries = [[None]*3 for _ in range(10)]
    unit_sum_entries = [None]*5
    total_sum_entry = Entry(frame)
    total_sum_entry.grid(row=23, column=1)

    # Create labels for the columns and rows
    for i in range(1, 11):
        Label(frame, text=f"{i}.").grid(row=2*i-1, column=0)
    for i in range(1, 4):
        Label(frame, text=chr(64+i)).grid(row=0, column=i)
    Label(frame, text="Unit Sum").grid(row=0, column=4)  # Add this line
    Label(frame, text="Total Sum").grid(row=22, column=0)

    def calculate_unit_sum():
        # Calculate the unit sum
        for i in range(5):
            unit_sum = max(sum(int(entries[2*i+k][j].get()) for j in range(3)) for k in range(2))
            unit_sum_entries[i].delete(0, END)
            unit_sum_entries[i].insert(0, unit_sum)

    def calculate_total_sum():
        # Calculate the total sum
        total_sum = sum(int(unit_sum_entries[i].get()) for i in range(5))
        total_sum_entry.delete(0, END)
        total_sum_entry.insert(0, total_sum)

    def update_excel():
        # Iterate over the Entry widgets
        for i in range(10):
            for j in range(3):
                # Update the corresponding cell in the DataFrame
                df.at[index, f'Q{i+1}_Bit{j+1}'] = int(entries[i][j].get())

        # Update the total sum in the DataFrame
        calculate_total_sum()
        df.at[index, 'Sum'] = int(total_sum_entry.get())
        decrypt_excel(name, sem, acyear, excel_path)
        # Save the DataFrame to the Excel file
        df.to_excel(excel_path, index=False)
        encrypt_excel(name, sem, acyear, excel_path)

        # Go to the next row and update the image
        next_row()

    def go_back():
        nonlocal index
        global img
        index -= 1
        if index < 0:
            messagebox.showinfo("Information", "This is the first row.")
            index = 0
            return
        row = df.iloc[index]
        barcode = row['Barcode']
        file_path = find_file(barcode, folder_path)

        # Open the image file
        if file_path is None:
            messagebox.showinfo("Information", f"Barcode {barcode} is not present.")
            go_back()
        else:
            img = Image.open(file_path)
            img = img.resize((800, int(800 * img.height / img.width)), PIL.Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            # Add the image to the Canvas widget
            canvas.create_image(0, 0, anchor=NW, image=img)

            # Add the marks to the Canvas widget
            for i in range(1, 11):
                for j in range(1, 4):
                    mark = row[f'Q{i}_Bit{j}']
                    entries[i-1][j-1] = Entry(frame)
                    entries[i-1][j-1].insert(0, mark)
                    entries[i-1][j-1].grid(row=2*i-1, column=j)
                    if mark == -1:
                        entries[i-1][j-1].config({"background": "Red"})

            # Initialize the unit_sum_entries and calculate the unit sum
            for i in range(5):
                unit_sum_entries[i] = Entry(frame)
                unit_sum_entries[i].grid(row=2*i+1, column=4)
            calculate_unit_sum()

            # Calculate the total sum
            calculate_total_sum()

        # Update the window
        root.update()

    def next_row():
        nonlocal index
        global img
        index += 1
        if index >= len(df):
            messagebox.showinfo("Information", "All rows have been processed.")
            root.quit()
            return
        row = df.iloc[index]
        barcode = row['Barcode']
        file_path = find_file(barcode, folder_path)

        # Open the image file
        if file_path is None:
            messagebox.showinfo("Information", f"Barcode {barcode} is not present.")
            next_row()
        else:
            img = Image.open(file_path)
            img = img.resize((800, int(800 * img.height / img.width)), PIL.Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            # Add the image to the Canvas widget
            canvas.create_image(0, 0, anchor=NW, image=img)

            # Add the marks to the Canvas widget
            for i in range(1, 11):
                for j in range(1, 4):
                    mark = row[f'Q{i}_Bit{j}']
                    entries[i-1][j-1] = Entry(frame)
                    entries[i-1][j-1].insert(0, mark)
                    entries[i-1][j-1].grid(row=2*i-1, column=j)
                    if mark == -1:
                        entries[i-1][j-1].config({"background": "Red"})

            # Initialize the unit_sum_entries and calculate the unit sum
            for i in range(5):
                unit_sum_entries[i] = Entry(frame)
                unit_sum_entries[i].grid(row=2*i+1, column=4)
            calculate_unit_sum()

            # Calculate the total sum
            calculate_total_sum()

        # Update the window
        root.update()

    # Create an OK button
    ok_button = Button(root, text="OK", command=update_excel)
    ok_button.grid(row=1, column=0)

    # Create a BACK button
    back_button = Button(root, text="BACK", command=go_back)
    back_button.grid(row=1, column=1)

    index = -1
    next_row()

    # Start the main loop
    root.mainloop()

# Call the function with the path of the excel sheet and the folder with the marks sheets
# process_marks('C:\\major-version1.0\\Excels\\buhio1-4-2024.xlsx', 'C:\\major-version1.0\\dataset - 1100px')
