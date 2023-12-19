import tkinter as tk
from tkinter import ttk  # Import themed tkinter module
from PIL import Image, ImageTk
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

# Dictionary to store employee information (ID: Employee object)
employee_info = {}

# Creating employee objects
class Employee:
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department

    def get_info(self):
        return f"Name: {self.name}, Age: {self.age}, Department: {self.department}"

# Populate employee information dictionary
employee1 = Employee("Malik Shah", 30, "Sales")
employee2 = Employee("Areeba Haq", 35, "Marketing")

employee_info["1"] = employee1
employee_info["2"] = employee2

# Function to decode barcode
def decode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = pyzbar.decode(gray)
    if results:
        return results[0].data.decode('utf-8')
    return None

# Function to retrieve employee information based on decoded barcode
def retrieve_info():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        decoded_data = decode(frame)
        if decoded_data is not None:
            cap.release()
            cv2.destroyAllWindows()
            employee_id = decoded_data.strip()  # Get the decoded employee ID
            if employee_id in employee_info:
                employee = employee_info[employee_id]
                result_label.config(text=employee.get_info())
            else:
                result_label.config(text="Invalid employee ID")
            break

        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Creating the main application window
root = tk.Tk()
root.title("Employee Information Retrieval")

# Styling the GUI elements using ttk
style = ttk.Style()
style.theme_use('clam')  # Change theme to 'clam' for a different look

# Creating UI elements with improved styling
retrieve_button = ttk.Button(root, text="Scan Barcode", command=retrieve_info)
retrieve_button.pack(pady=20)

result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

# Running the application
root.mainloop()
