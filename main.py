from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pswd():
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    upper_letters = [i.upper() for i in letters]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    password_letters = [choice(letters) for i in range(randint(4, 6))]
    password_upper_letters = [choice(upper_letters) for i in range(randint(4, 6))]
    password_symbols = [choice(symbols) for i in range(randint(2, 4))]
    password_numbers = [choice(numbers) for i in range(randint(2, 4))]

    password = (
        password_letters + password_symbols + password_numbers + password_upper_letters
    )
    shuffle(password)
    hard_password = "".join(password)
    pyperclip.copy(hard_password)
    pass_entry.insert(0, hard_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_data():
    websitee = web_entry.get()
    emaill = email_entry.get()
    passw = pass_entry.get()

    data = {
        websitee: {
            "email": emaill,
            "password": passw,
        }
    }

    if len(websitee) == 0 or len(emaill) == 0 or len(passw) == 0:
        messagebox.showinfo(
            title="Oops", message="Please don't leave any fields empty!"
        )
    else:
        try:
            with open(file="data.json", mode="r") as f:
                old_data = json.load(fp=f)
                old_data.update(data)
        except FileNotFoundError:
            old_data = data
        finally:
            with open(file="data.json", mode="w") as f:
                json.dump(old_data, f, indent=4)
            web_entry.delete(0, END)
            pass_entry.delete(0, END)
            messagebox.showinfo(message="Data added successfully!")


# ---------------------------- Search Password ------------------------------- #
def search_pass():
    try:
        with open(file="data.json", mode="r") as f:
            data = json.load(fp=f)
            website_name = web_entry.get()
            email = data[website_name]["email"]
            password = data[website_name]["password"]
    except KeyError:
        messagebox.showerror(
            title="Error", message=f"No Details found about '{website_name}'"
        )
    except FileNotFoundError as msg:
        messagebox.showerror(title="Error", message=f"No data file found!")
    else:
        messagebox.showinfo(
            title="Account Details",
            message=f"Email: {email}\nPassword: '{password}'",
        )
    finally:
        web_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg="white")

canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

# Labels
website = Label(text="Website:", bg="white")
website.grid(row=1, column=0)
email = Label(text="Email/Username:", bg="white")
email.grid(row=2, column=0)
password = Label(text="Password:", bg="white")
password.grid(row=3, column=0)

# Entries
web_entry = Entry(width=32, justify="left")
web_entry.grid(row=1, column=1, pady=5)
web_entry.focus()
email_entry = Entry(width=50, justify="left")
email_entry.insert(0, "john564@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, pady=5)
pass_entry = Entry(width=32, justify="left")
pass_entry.grid(row=3, column=1, pady=5)

# Buttons
search = Button(
    text="            Search           ",
    bg="white",
    command=search_pass,
    justify="left",
)
search.grid(row=1, column=2)
gen_pass = Button(text="Generate Password", justify="left", bg="white", command=pswd)
gen_pass.grid(row=3, column=2)
add_pass = Button(text="Add", justify="center", width=42, command=add_data, bg="white")
add_pass.grid(row=4, column=1, columnspan=2, pady=5)

window.mainloop()
