import math
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np


class AnthropometryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anthropometry Calculator")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Create and place labels and entry fields for user input
        ttk.Label(self.root, text="Gender (male or female):").pack(pady=10)
        self.gender_entry = ttk.Entry(self.root)
        self.gender_entry.pack(pady=5)

        ttk.Label(self.root, text="Height (in cm):").pack(pady=10)
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.pack(pady=5)

        ttk.Label(self.root, text="Weight (in kg):").pack(pady=10)
        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.pack(pady=5)

        ttk.Label(self.root, text="Wingspan (in cm):").pack(pady=10)
        self.wingspan_entry = ttk.Entry(self.root)
        self.wingspan_entry.pack(pady=5)

        ttk.Label(self.root, text="Waist size (in cm):").pack(pady=10)
        self.waist_entry = ttk.Entry(self.root)
        self.waist_entry.pack(pady=5)

        ttk.Label(self.root, text="Shoulder circumference (in cm):").pack(pady=10)
        self.shoulder_entry = ttk.Entry(self.root)
        self.shoulder_entry.pack(pady=5)

        ttk.Label(self.root, text="Neck circumference (in cm):").pack(pady=10)
        self.neck_entry = ttk.Entry(self.root)
        self.neck_entry.pack(pady=5)

        # Create and place the Calculate button
        ttk.Button(self.root, text="Calculate", command=self.calculate).pack(pady=20)

    def calculate(self):
        # Get the input values from the entry fields
        gender = self.gender_entry.get()
        height = float(self.height_entry.get())
        weight = float(self.weight_entry.get())
        wingspan = float(self.wingspan_entry.get())
        waist = float(self.waist_entry.get())
        shoulder_circum = float(self.shoulder_entry.get())
        neck_circum = float(self.neck_entry.get())

        # Calculate the results
        ape_result = self.ape_index(wingspan, height)
        whr_result = self.waist_to_height(waist, height)
        stw_result = self.shoulder_to_waist(shoulder_circum, waist)
        bmi_result = self.BMI(weight, height)
        bfp_result = self.body_fat_percentage(gender, waist, neck_circum, height)

        # Build the output string
        output = f"{ape_result}\n{whr_result}\n{stw_result}\n{bmi_result}\n{bfp_result}"

        # Display the output using a message box
        messagebox.showinfo("Results", output)
        filename = simpledialog.askstring("Save Results", "Enter a filename to save your results:")
        if filename:
            self.save_to_file(output, filename)
    def save_to_file(self, output, filename):
        with open(filename, "w") as file:
            file.write(output)
        messagebox.showinfo("File Saved", f"Results saved to {filename}")
        #if filename:
            #self.save_to_file(output, filename)
            #self.plot_bmi_range(weight, height, filename)
    def plot_bmi_range(self, weight, height, filename):
        bmi = self.calculate_BMI(weight, height)
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        ranges = [18.5, 24.9, 29.9, 40]
        colors = ['blue', 'green', 'yellow', 'red']

        plt.figure(figsize=(8, 6))
        plt.bar(categories, ranges, color=colors)
        plt.axhline(y=bmi, color='gray', linestyle='dashed', linewidth=2)
        plt.text(0.5, bmi + 1, f'Your BMI: {bmi:.2f}', ha='center', va='bottom', color='gray')
        plt.xlabel("BMI Categories")
        plt.ylabel("BMI Range")
        plt.title("BMI Range Categories")
        plt.ylim(0, 40)
        plt.tight_layout()

        graph_filename = filename.split('.')[0] + "_bmi_graph.png"
        plt.savefig(graph_filename)
        plt.close()

        messagebox.showinfo("Graph Saved", f"Graph saved to {graph_filename}")

    def ape_index(self, wingspan, height):
        if wingspan - height >= 6:
            return "Due to your longer arms, you should consider sports like basketball, boxing, MMA, or bouldering."
        elif wingspan - height < 6:
            return "You have an average reach."
        else:
            return ""

    def waist_to_height(self, waist, height):
        whr = waist / height
        if 0.43 <= whr <= 0.47:
            return "According to health standards, you have a good waist-to-height ratio."
        else:
            return f"Your waist-to-height ratio is {whr:.2f}. According to health standards, it should be between 0.43 and 0.47."

    def shoulder_to_waist(self, shoulder_circum, waist):
        stw = shoulder_circum / waist
        if stw >= 1.618:
            return "You have an impressive shoulder-to-waist ratio!"
        elif 1.4 <= stw < 1.618:
            return "You have an athletic shoulder-to-waist ratio."
        elif 1 <= stw < 1.4:
            return "You have an average male shoulder-to-waist ratio."
        elif stw < 1:
            return "Your shoulder-to-waist ratio is lower than average."

    def BMI(self, weight, height):
        if height == 0:
            return "Invalid height (height cannot be zero)."
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            return f"Your BMI is {bmi:.2f}. You are underweight."
        elif 18.5 <= bmi <= 25:
            return f"Your BMI is {bmi:.2f}. You have a normal BMI."
        elif 25 < bmi <= 30:
            return f"Your BMI is {bmi:.2f}. You are overweight."
        else:
            return f"Your BMI is {bmi:.2f}. You are obese."

    def body_fat_percentage(self, gender, waist, neck_circum, height):
        if gender == "male":
            bfp = 495 / (1.0324 - 0.19077 * math.log10(waist - neck_circum) + 0.15456 * math.log10(height)) - 450
        elif gender == "female":
            bfp = 495 / (1.29579 - 0.35004 * math.log10(waist + waist - neck_circum) + 0.22100 * math.log10(height)) - 450
        else:
            return "Invalid gender. Please enter 'male' or 'female'."
        
        if bfp < 2:
            return f"Your body fat percentage is {bfp:.2f}. You are extremely lean."
        elif 2 <= bfp < 5:
            return f"Your body fat percentage is {bfp:.2f}. You are very lean."
        elif 5 <= bfp < 13:
            return f"Your body fat percentage is {bfp:.2f}. You are an athlete."
        elif 13 <= bfp < 17:
            return f"Your body fat percentage is {bfp:.2f}. You are fit."
        elif 17 <= bfp < 24:
            return f"Your body fat percentage is {bfp:.2f}. You have an average body fat level."
        else:
            return f"Your body fat percentage is {bfp:.2f}. You are in the obese range."

if __name__ == "__main__":
    root = tk.Tk()
    app = AnthropometryApp(root)
    root.mainloop()
