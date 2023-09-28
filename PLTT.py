import matplotlib.pyplot as plt

# Input BMI value
bmi = float(input("Enter your BMI: "))

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
plt.show()


