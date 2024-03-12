import os
import pandas as pd
from last_dir import navigate_to_last_directory
from constants import confidence_threshold, a, b, c
from encrypt_decrypt import encrypt_excel, decrypt_excel
from remove_cache import rmcache
from gui_entry_final import process_marks


def correct_marks(num):
    num = int(num)
    if num == 7 or num == 9:
        return 7
    if num == 2 or num == 10:
        return 2
    if num == 4 or num == 8:
        return 4
    else:
        return num
def give_max(bit):
    if bit == '1' or bit == 1:
        return a
    elif bit == '2' or bit == 2:
        return b
    elif bit == '3' or bit == 3:
        return c

def check3lines(lines, bit):
    line1= lines[0]
    line2 = lines[1]
    line3 = lines[2]
    conf1 = float(line1.split(" ")[5])
    conf2 = float(line2.split(" ")[5])
    conf3 = float(line3.split(" ")[5])
    num1 = correct_marks(line1.split(" ")[0])
    num2 = correct_marks(line2.split(" ")[0])
    num3 = correct_marks(line3.split(" ")[0])
    x_centre1 = line1.split(" ")[1]
    x_centre2 = line2.split(" ")[1]
    x_centre3 = line3.split(" ")[1]
    print(num1, num2, num3)
    print(bit)
    if num1 == num2:
        if conf1 > conf2:
            print(num1, "lol1", num2)
            return check_comb([line1, line3], bit)
        else:
            print(num1, "lol2", num2)
            return check_comb(lines[1:], bit)
    elif num2 == num3:
        if conf2 > conf3:
            return check_comb(lines[:2], bit)
        else:
            return check_comb([line1, line3], bit)
    elif num1 == num3:
        if conf1 > conf3:
            return check_comb(lines[:2], bit)
        else:
            return check_comb(lines[1:], bit)
    else:
        return -1

def check_comb(lines, bit):
    line1 = lines[0]
    line2 = lines[1]
    conf1 = float(line1.split(" ")[5])
    conf2 = float(line2.split(" ")[5])
    num1 = correct_marks(line1.split(" ")[0])
    num2 = correct_marks(line2.split(" ")[0])
    x_centre1 = line1.split(" ")[1]
    x_centre2 = line2.split(" ")[1]
    # check the major of the 2 confidence levels
    if conf1 > confidence_threshold and conf2 > confidence_threshold:
        if x_centre1 > x_centre2:
            num = int(num2) * 10 + int(num1)
            print(num)
            if num <= give_max(bit):
                print("--------------------", num)
                return num
            else:
                return -1
        elif x_centre2 > x_centre1:
            num = int(num1) * 10 + int(num2)
            if num <= give_max(bit):
                return num
            else:
                return -1
        else:
            return -1
    elif conf1 > confidence_threshold:
        return num1
    elif conf2 > confidence_threshold:
        return num2
    else:
        return -1


def check_same(lines):
    line1 = lines[0]
    line2 = lines[1]
    conf1 = float(line1.split(" ")[5])
    conf2 = conf = float(line2.split(" ")[5])
    num1 = line1.split(" ")[0]
    num2 = line2.split(" ")[0]
    if num1 == '2' and num2 == '10':
        return True, 2
    if num1 == '4' and num2 == '8':
        return True, 4
    if num1 == '7' and num2 == '9':
        return True, 7
    else:
        return False, -1


def fail_case(question, barcode, bit, df):
    # while True:
    print(f'Question {question} and Bit {bit} of barcode {barcode} are wrong!!!!')
    #     num = int(input("Enter the correct marks: "))
    #     user_input = input("Type OK to confirm.. ")
    #     if user_input == "OK":
    #         break
    if barcode in df['Barcode'].values:
        # If it is, update the corresponding cell with the confidence level
        df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = -1
    else:
        # If it's not, create a new row
        df._append({'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': -1},
                   ignore_index=True)


def txt2excel(name, sem, acyear, input_dir):
    # Define the path to the labels folder
    start_path = "C:\\major-version1.0\\runs"
    labels_folder = navigate_to_last_directory(start_path)

    # Create a DataFrame to hold the data
    df = pd.DataFrame(
        columns=['S. No', 'Barcode'] + [f'Q{i}_Bit{j}' for i in range(1, 11) for j in range(1, 4)] + ['Sum'])

    filenames = sorted(os.listdir(labels_folder))

    # Iterate over the files in the labels folder
    for filename in filenames:
        # print("iter")
        if filename.endswith(".txt"):
            # print("iter1")
            # Extract the barcode and question info from the filename
            barcode = filename.split('_')[1].split("-")[0]
            # print(barcode)
            question_bit = filename.split('_')[2:4]
            question = int(question_bit[0])
            bit = int(question_bit[1].split('.')[0])

            # Read the label file and extract the confidence level
            with open(os.path.join(labels_folder, filename), 'r') as file:
                lines = file.readlines()
                line_count = len(lines)

                if line_count == 1:
                    for line in lines:
                        conf = float(line.split(" ")[5])
                        if conf >= confidence_threshold:
                            num = int(line.split(" ")[0])
                            num = int(correct_marks(num=num))
                            print(f'{bit}-{question}-{num}')
                            # Check if the barcode is already in the DataFrame
                            if barcode in df['Barcode'].values:
                                # If it is, update the corresponding cell with the confidence level
                                df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = num
                            else:
                                # If it's not, create a new row
                                df = df._append(
                                    {'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': num},
                                    ignore_index=True)


                elif line_count == 2:
                    print("OMNGGGGGGG")
                    # initially check if the numbers are same i.e. two or 2, as so
                    chc, cnum = check_same(lines)
                    if chc == True:
                        num = int(cnum)
                        if barcode in df['Barcode'].values:
                            # If it is, update the corresponding cell with the confidence level
                            df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = num
                        else:
                            # If it's not, create a new row
                            df = df._append(
                                {'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': num},
                                ignore_index=True)
                    else:
                        # check if combination is correct ex: '0' '1' = 1
                        comb_num = check_comb(lines, bit=bit)
                        num = int(comb_num)
                        if barcode in df['Barcode'].values:
                            # If it is, update the corresponding cell with the confidence level
                            df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = num
                        else:
                            # If it's not, create a new row
                            df = df._append(
                                {'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': num},
                                ignore_index=True)

                elif line_count == 3:
                    num3 = check3lines(lines, bit)
                    if barcode in df['Barcode'].values:
                        # If it is, update the corresponding cell with the confidence level
                        df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = num3
                    else:
                        # If it's not, create a new row
                        df = df._append(
                            {'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': num3},
                            ignore_index=True)

                else:
                    fail_case(question, barcode, bit, df)

    df = df.fillna(0)
    # Calculate the sum for each row
    # for i in range(1, 11, 2):
    #     df['Sum'] = df[[f'Q{i}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
    #     df['Sum'] = df['Sum'].where(df['Sum'] > df[[f'Q{i+1}_Bit{j}' for j in range(1, 4)]].sum(axis=1), df[[f'Q{i+1}_Bit{j}' for j in range(1, 4)]].sum(axis=1))

    for i in range(1, 11, 2):
        sum1 = df[[f'Q{i}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
        sum2 = df[[f'Q{i + 1}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
        df['Sum'] += sum1.where(sum1 > sum2, sum2)
    print(df)

    # Save the DataFrame to an Excel file that is created with excel
    df.to_excel(f'C:\\major-version1.0\\Excels\\{name}-{sem}-{acyear}.xlsx', index=False)

    # encrypt the excel immediately
    encrypt_excel(name, sem, acyear, f'C:\\major-version1.0\\Excels\\{name}-{sem}-{acyear}.xlsx')

    process_marks(name, sem, acyear, f"C:\\major-version1.0\\Excels\\{name}-{sem}-{acyear}.xlsx", input_dir)
    # rmcache(labels_folder)

# txt2excel("test6", 4, 2024)
