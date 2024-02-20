from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from password_management import PasswordManagementApp
from database import DatabaseManager
from aes import AESCipher

class PasswordManagerAuthentication:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager Authentication")
        self.root.iconbitmap("images/password.ico")
        
        self.window_width = 700
        self.window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        self.database = DatabaseManager()
        self.database.create_table()

        self.aes_cipher = AESCipher(b'Sixteen byte key')

        self.radio_var = IntVar()
        login_radio = Radiobutton(root, text="Login", variable=self.radio_var, value=0, command=self.show_frame)
        signup_radio = Radiobutton(root, text="Sign Up", variable=self.radio_var, value=1, command=self.show_frame)

        login_radio.place(relx=0.4, rely=0.1)
        signup_radio.place(relx=0.5, rely=0.1)

        self.show_frame()

    def show_frame(self):
        selected = self.radio_var.get()
        if selected == 0:
            self.destroy_signup_frame()
            self.create_login_frame()
        elif selected == 1:
            self.destroy_login_frame()
            self.create_signup_frame()

    def create_login_frame(self):
        
        self.login_frame = Frame(self.root, bg="light blue", width=self.window_width, height=self.window_height)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        login_label = Label(self.login_frame, text="Login", bg="light blue")
        login_label.pack(pady=30,padx=50)

        login_username_label = Label(self.login_frame, text="Username:", bg="light blue")
        login_username_label.pack()

        self.login_username_entry = Entry(self.login_frame)
        self.login_username_entry.pack(padx=50)

        login_password_label = Label(self.login_frame, text="Master Password:", bg="light blue")
        login_password_label.pack()

        self.login_password_entry = Entry(self.login_frame, show="*")
        self.login_password_entry.pack()

        login_button = Button(self.login_frame, text="Login", command=self.login_user)
        login_button.pack(pady=30,padx=50)
        
        forget_password_button = Button(self.login_frame, text="Forget Password", command=self.show_forget_password_dialog)
        forget_password_button.pack(pady=10)
    
    def create_signup_frame(self):
        

        self.signup_frame = Frame(self.root, bg="light green", width=self.window_width, height=self.window_height)
        self.signup_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        signup_label = Label(self.signup_frame, text="Sign Up", bg="light green")
        signup_label.pack(pady=30,padx=100)

        reg_username_label = Label(self.signup_frame, text="Username:", bg="light green")
        reg_username_label.pack()

        self.reg_username_entry = Entry(self.signup_frame)
        self.reg_username_entry.pack()

        reg_password_label = Label(self.signup_frame, text="Master Password:", bg="light green")
        reg_password_label.pack()

        self.reg_password_entry = Entry(self.signup_frame, show="*")
        self.reg_password_entry.pack()

        confirm_password_label = Label(self.signup_frame, text="Confirm Master Password:", bg="light green")
        confirm_password_label.pack()

        self.confirm_password_entry = Entry(self.signup_frame, show="*")
        self.confirm_password_entry.pack()

        favourite_food_label = Label(self.signup_frame, text="Favourite Food:", bg="light green")
        favourite_food_label.pack()

        self.favourite_food_entry = Entry(self.signup_frame)
        self.favourite_food_entry.pack()

        signup_button = Button(self.signup_frame, text="Sign Up", command=self.register_user)
        signup_button.pack(pady=30,padx=100)
        
    def destroy_login_frame(self):
        if hasattr(self, 'login_frame'): # checks is loginframe present and destroyes it
            self.login_frame.destroy()

    def destroy_signup_frame(self):
        if hasattr(self, 'signup_frame'): # checks is signupframe present and destroyes it
            self.signup_frame.destroy()
            
    def login_user(self):
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get().strip()
        if username and password:
            hashed_password = self.database.get_password(username)
            if hashed_password and self.check_password(password, hashed_password):
                messagebox.showinfo("Success", "Login successful!")
                self.clear_entries()
                self.open_password_management_window(username)
                
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def register_user(self):
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        favourite_food=self.favourite_food_entry.get().strip()
        if username and password and confirm_password and favourite_food:
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
            elif self.database.username_exists(username):
                messagebox.showerror("Error", "Username already exists.")
            else:
                encrypted_password = self.aes_cipher.encrypt_password(password)
                self.database.register_user(username, encrypted_password,favourite_food)
                messagebox.showinfo("Success", "Registration successful!")
                self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter all fields.")

    def check_password(self, password, hashed_password):
        decrypted_password = self.aes_cipher.decrypt_password(hashed_password)
        return password == decrypted_password
    def forget_password(self):
        # Prompt the user for their favorite food
        username = simpledialog.askstring("Forget Password", "Enter your username:")
        favorite_food = simpledialog.askstring("Forget Password", "What is your favorite food?")
        if favorite_food and username:
            stored_favorite_food = self.database.get_favorite_food(username)
            if stored_favorite_food == favorite_food:
                hashed_password = self.database.get_password(username)
                password=self.aes_cipher.decrypt_password(hashed_password)
                if password:
                    messagebox.showinfo("Password Recovery", f"Your password is: {password}")
                else:
                    messagebox.showerror("Error", "Unable to retrieve password.")
            else:
                messagebox.showerror("Error", "Incorrect favorite food or username")
    
    def show_forget_password_dialog(self):
        forget_password_window = Toplevel(root)
        forget_password_window.title("Forget Password")

        Label(forget_password_window, text="Enter your username and favorite food:").pack(pady=10)

        username_label = Label(forget_password_window, text="Username:")
        username_label.pack()

        username_entry = Entry(forget_password_window)
        username_entry.pack()

        food_label = Label(forget_password_window, text="Favorite food:")
        food_label.pack()

        food_entry = Entry(forget_password_window)
        food_entry.pack()

        def check_and_show_password():
            username = username_entry.get()
            favorite_food = food_entry.get()
            if favorite_food and username:
                stored_favorite_food = self.database.get_favorite_food(username)
                if stored_favorite_food == favorite_food:
                    hashed_password = self.database.get_password(username)
                    password=self.aes_cipher.decrypt_password(hashed_password)
                    if password:
                        messagebox.showinfo("Password Recovery", f"Your password is: {password}")
                        forget_password_window.destroy()
                    else:
                        messagebox.showerror("Error", "Unable to retrieve password.")
                        
                else:
                    messagebox.showerror("Error", "Incorrect favorite food or username")
            else:
                 messagebox.showerror("Error", "Enter the values of username or password")
        Button(forget_password_window, text="Retrieve Password", command=check_and_show_password).pack(pady=10)
    
    
    def open_password_management_window(self,username):
        userid =self.database.get_userid(username)
        self.root.destroy()  # Close the current window
        password_management_app = PasswordManagementApp(userid,username)
        password_management_app.run()
    
    def clear_entries(self):
        selected = self.radio_var.get()
        if selected == 0:
            self.login_username_entry.delete(0, END)
            self.login_password_entry.delete(0, END)
        elif selected == 1:
            self.reg_username_entry.delete(0, END)
            self.reg_password_entry.delete(0, END)
            self.confirm_password_entry.delete(0, END)
            self.favourite_food_entry.delete(0,END)



if __name__ == "__main__":
    root = Tk()
    app = PasswordManagerAuthentication(root)
    root.mainloop()
