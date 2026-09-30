import matplotlib.pyplot as plt

categories = ["Acne", "Oily Skin", "Dry Skin", "Sensitive Skin", "Hyperpigmentation"]
counts = [32, 20, 15, 10, 8]  # dummy data

plt.figure(figsize=(8,5))
plt.bar(categories, counts)
plt.title("Distribution of Skincare Queries")
plt.xlabel("Category")
plt.ylabel("Number of Queries")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
