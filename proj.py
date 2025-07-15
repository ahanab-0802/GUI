import tkinter as tk
from tkinter import messagebox,PhotoImage
from PIL import Image, ImageTk
import os
import hashlib

# ---------------------8
# Password Hashing Utility
# ---------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------
# Product and Cart Classes
# ---------------------
class Product:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product):
        if product.name in self.items:
            self.items[product.name]['quantity'] += 1
        else:
            self.items[product.name] = {'product': product, 'quantity': 1}

    def get_total(self):
        return sum(item['product'].price * item['quantity'] for item in self.items.values())

    def clear(self):
        self.items.clear()

# ---------------------
# Shopping GUI Class
# ---------------------
class ShoppingApp:
    def __init__(self, master, username):
        self.master = master
        self.master.title(f"ShopSmart - Welcome {username}")
        self.master.geometry("600x600")
        self.master.config(bg="pink")

        self.cart = Cart()
        self.products = [
            Product("Bag", 60000, "images/bag.png"),
            Product("Headphones", 1500, "images/headphones.png"),
            Product("Smartphone", 25000, "images/smartphone.png"),
            Product("Backpack", 1200, "images/backpack.png"),
            Product("Smartwatch", 5000, "images/smartwatch.png"),
            Product("Shoes", 2500, "images/shoes.png")
        ]

        self.product_images = {}  # To hold loaded PhotoImages
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="ShopSmart - OOP Edition", font=("Arial", 18, "bold"), bg="white", fg="green").pack(pady=10)

        product_frame = tk.Frame(self.master, bg="white")
        product_frame.pack(pady=10)

        for idx, product in enumerate(self.products):
            img = Image.open(product.image_path)
            img = img.resize((60, 60))
            photo = ImageTk.PhotoImage(img)
            self.product_images[product.name] = photo  # Store reference to prevent garbage collection

            row = tk.Frame(product_frame, bg="white")
            row.pack(fill="x", pady=5)

            tk.Label(row, image=photo, bg="white").pack(side="left", padx=10)
            tk.Label(row, text=f"{product.name} - ₹{product.price}", bg="white", font=("Arial", 12)).pack(side="left", padx=10)
            tk.Button(row, text="Add to Cart", command=lambda p=product: self.add_to_cart(p)).pack(side="right", padx=10)

        tk.Label(self.master, text="Your Cart:", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        self.cart_list = tk.Listbox(self.master, width=60, height=7)
        self.cart_list.pack()

        self.total_label = tk.Label(self.master, text="Total: ₹0", font=("Arial", 12, "bold"), bg="white", fg="blue")
        self.total_label.pack(pady=5)

        tk.Button(self.master, text="Checkout", font=("Arial", 12), bg="green", fg="white", command=self.checkout).pack(pady=10)

    def add_to_cart(self, product):
        self.cart.add(product)
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_list.delete(0, tk.END)
        for item_name, item_info in self.cart.items.items():
            qty = item_info['quantity']
            price = item_info['product'].price * qty
            self.cart_list.insert(tk.END, f"{item_name} x{qty} - ₹{price}")
        self.total_label.config(text=f"Total: ₹{self.cart.get_total()}")

    def checkout(self):
        if not self.cart.items:
            messagebox.showinfo("Checkout", "Your cart is empty!")
            return
        messagebox.showinfo("Checkout", f"Thank you for your purchase!\nTotal: ₹{self.cart.get_total()}")
        self.cart.clear()
        self.update_cart_display()

# ---------------------
# Login/Signup Class
# ---------------------
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login to ShopSmart")
        self.root.geometry("400x300")
        self.root.config(bg="lightblue")

        self.username_var = tk.StringVar() #username
        self.password_var = tk.StringVar() #password holder

        tk.Label(root, text="Welcome to ShopSmart!", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=10)
        tk.Label(root, text="Username:", font=("Arial", 12), bg="lightblue").pack()
        self.username_entry = tk.Entry(root, textvariable=self.username_var)
        self.username_entry.pack()

        tk.Label(root, text="Password:", font=("Arial", 12), bg="lightblue").pack()
        self.password_entry = tk.Entry(root, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", bg="green", fg="white", command=self.login).pack(pady=10)
        tk.Button(root, text="Signup", bg="blue", fg="white", command=self.signup).pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        hashed_input = hash_password(password)

        if not os.path.exists("users.txt"):
            messagebox.showerror("Login Failed", "No users registered yet!")
            return

        with open("users.txt", "r") as file:
            users = file.readlines()
            for user in users:
                u, p_hash = user.strip().split(",")
                if u == username and p_hash == hashed_input:
                    messagebox.showinfo("Login Success", f"Welcome {username}!")
                    self.root.destroy()
                    self.launch_shopping_app(username)
                    return

        messagebox.showerror("Login Failed", "Incorrect username or password")

    def signup(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return

        hashed = hash_password(password)
        with open("users.txt", "a") as file:
            file.write(f"{username},{hashed}\n")
        messagebox.showinfo("Signup Success", "User registered successfully!")

    def launch_shopping_app(self, username):
        shopping_window = tk.Tk()
        ShoppingApp(shopping_window, username)
        shopping_window.mainloop()

# ---------------------
# Run the App
# ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()