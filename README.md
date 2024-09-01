# Conversion of Marks into Digital Format Using Object Detection and Providing Analysis

## Project Overview

The primary objective of this project is to automate the process of converting manually entered marks into a digital format using object detection. This system not only digitizes the marks but also provides insightful analysis of student performance, making it a valuable tool for educational institutions. The project uses the YOLOv7 model for digit recognition, ensuring high accuracy and efficiency in detecting and converting marks. Additionally, the project implements robust security measures to protect sensitive student data.

## Key Objectives

- **Automation:** Eliminate manual data entry by automating the digitization of marks from scanned images.
- **Analysis:** Provide comprehensive analysis tools to evaluate student performance across various metrics.
- **Security:** Ensure the confidentiality and integrity of student data through encryption and secure storage mechanisms.

## Features

### 1. Digit Recognition

- Utilizes the YOLOv7 model to accurately detect and recognize digits from scanned images of mark sheets.
- Processes highly distorted and handwritten digits with high accuracy.

### 2. Data Digitization

- Converts recognized marks into a digital format, stored in Excel files for easy access and further analysis.
- Supports preprocessing of images to standardize input for better recognition accuracy.

### 3. Analysis Tools

- **Average Scores Analysis:** Calculates and visualizes average scores for each unit using bar charts.
- **Difficulty Analysis:** Assesses the difficulty of each question and visualizes the data.
- **Pass/Fail Analysis:** Determines the pass and fail rates and presents the results in a pie chart.

### 4. Graphical User Interface (GUI)

- Provides an intuitive GUI for users to interact with the system, including features for loading data, analyzing marks, and visualizing results.

### 5. Security

- **Implements two-layer security:** Cell Encryption and Folder Encryption.
  - **Cell Encryption:** Encrypts individual cells within Excel files using Fernet symmetric encryption.
  - **Folder Encryption:** Encrypts entire folders containing sensitive data using a combination of PBKDF2HMAC, SHA-256, and Fernet encryption.

## Project Structure

All project files are located in the home directory. Below is an overview of the key files:

- **app.bat:** The main executable file that initiates the entire process. Replace the paths in accordance to your system
- **requirements.txt:** Lists all dependencies required to run the project.
- **Python Source Files:** Contain the source code for digit recognition, data processing, GUI implementation, and data encryption.
- **Excel Data Files:** Store input scanned images and the output of the digit recognition and analysis processes.

## Installation

To set up and run the project on your local machine, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/CH-Sampath/digitization-and-analysis-of-marks
   ```

2. **Install Dependencies:** Ensure Python 3 is installed on your system. Then, install the necessary Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:** Execute the `app.bat` file to start the project:

   ```bash
   ./app.bat
   ```

## Usage

1. **Digit Recognition:**

   - Place scanned mark sheets in the appropriate directory.
   - The system will automatically process these images, recognize digits, and store the results in an Excel file.

2. **Analysis:**

   - Use the GUI to load the processed Excel files.
   - Choose from various analysis options (e.g., Average Scores, Difficulty Analysis, Pass/Fail Analysis).
   - Visualize the results in real-time through charts and graphs.

3. **Security:**

   - The data is securely encrypted both at the cell level (individual entries) and folder level (entire datasets).
   - Ensure that the encryption keys are safely stored and managed as they are required for decrypting the data.

## Contributing

Contributions are welcome! Please follow these steps if you wish to contribute:

1. **Fork the repository.**
2. **Create a feature branch for your changes:**

   ```bash
   git checkout -b feature_branch
   ```

3. **Commit your changes:**

   ```bash
   git commit -m "Your detailed description of the changes"
   ```

4. **Push to the branch:**

   ```bash
   git push origin feature_branch
   ```

5. **Create a pull request for review.**

## Acknowledgments

- **YOLOv7:** Used for the digit recognition model.
- **Python Libraries:** NumPy, Pandas, Matplotlib, Pytorch (CUDA enabled), Tkinter, Cryptography libraries (Fernet, PBKDF2HMAC, SHA-256).
- **Guidance:** Project developed under the guidance of Mr. M. Vamsi Krishna, Assistant Professor, MVGR College of Engineering.
