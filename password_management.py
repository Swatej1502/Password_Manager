from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from database import DatabaseManager
from aes import AESCipher
from generate_password import strongpassword



class PasswordManagementApp:
    def __init__(self,userid,username): #(self,username)
        
        self.username = username
        self.userid=userid
        self.password_management_window = Tk()
        self.password_management_window.title("Password Management")
        self.password_management_window.iconbitmap("images/password.ico")
        self.db = DatabaseManager()
        self.aes_cipher = AESCipher(b'Sixteen byte key')
        self.window_width = 700
        self.window_height = 500
        self.folder=[]
       

        # Set the window position
        self.password_management_window.geometry("1400x900+30+30")

        Label(self.password_management_window, text=f"Welcome, {self.username}!", font=("Arial", 14)).place(relx=0.5, rely=0.1)
        
        self.radio_var = IntVar()
        add_password_button = Radiobutton(self.password_management_window, text="Add Account", variable=self.radio_var, value=0, command=self.show_frame)
        search_password_button = Radiobutton(self.password_management_window, text="Search", variable=self.radio_var, value=1,command=self.show_frame)
        categories_button = Radiobutton(self.password_management_window, text="Folders", variable=self.radio_var, value=2,command=self.show_frame)
        
        add_password_button.place(relx=0.3, rely=0.2)
        search_password_button.place(relx=0.5, rely=0.2)
        categories_button.place(relx=0.7, rely=0.2)
        
        self.show_frame()

    def create_addpassword_frame(self):
        self.option=list(self.db.fetch_folders(self.userid))
        self.options=[]
        for i in self.option:
            self.options.append(i[0])
        
        self.addpassword_frame = LabelFrame(self.password_management_window,text="ADD account",  width=self.window_width, height=self.window_height)
        self.addpassword_frame.place(relx=0.3, rely=0.3)
        
        category = Label(self.addpassword_frame, text= " Select Category:")
        category.grid(row=1, column=0, padx=(30,10), pady=10)
        
        self.clicked = StringVar()
        self.category_menu=OptionMenu(self.addpassword_frame,self.clicked,"Social Media","Apps")
        self.category_menu.grid(row=1, column=1, pady=10, sticky=W)
        
        folder = Label(self.addpassword_frame, text= " Folder Name:")
        folder.grid(row=2, column=0, padx=(30,10), pady=10)
        
        self.folder_box=Combobox(self.addpassword_frame, values=self.options, width=30 )
        self.folder_box.bind("<<ComboboxSelected>>",)
        self.folder_box.grid(row=2,column=1,pady=10,sticky=W)
        
        website = Label(self.addpassword_frame, text= " Website or App name:")
        website.grid(row=3, column=0, padx=(30,10), pady=10)
        
        self.website_entry=Entry(self.addpassword_frame,width=30)
        self.website_entry.grid(row=3,column=1,padx=(10,50),pady=10)
        
        username = Label(self.addpassword_frame, text= " Username:")
        username.grid(row=4, column=0, padx=(30,10), pady=15)
        
        self.username_entry=Entry(self.addpassword_frame,width=30)
        self.username_entry.grid(row=4,column=1,padx=(10,50),pady=10)
        
        password = Label(self.addpassword_frame, text= " Password:")
        password.grid(row=5, column=0, padx=(30,10), pady=10)
        
        self.password_entry=Entry(self.addpassword_frame,width=30)
        self.password_entry.grid(row=5,column=1,padx=(10,50),pady=10)
        
        # Password strength suggestions
        password_strength = Label(self.addpassword_frame, text="Password Strength Suggestions:")
        password_strength.grid(row=6, column=1,sticky=W, pady=(5,0))
        
        suggestions = Label(self.addpassword_frame, text="- Length should be more than 8 characters.")
        suggestions.grid(row=7, column=1, sticky=W)
        
        suggestions = Label(self.addpassword_frame, text="- Should contain at least one uppercase letter.")
        suggestions.grid(row=8, column=1, sticky=W)
        
        suggestions = Label(self.addpassword_frame, text="- Should contain at least one lowercase letter.")
        suggestions.grid(row=9, column=1, sticky=W)
        
        suggestions = Label(self.addpassword_frame, text="- Should contain at least one special character.")
        suggestions.grid(row=10, column=1, sticky=W)
        
        suggestions = Label(self.addpassword_frame, text="- Should contain at least one digit (0-9).")
        suggestions.grid(row=11, column=1, sticky=W)
    
        add_button=Button(self.addpassword_frame,text="Save", width=10, command=self.save_account)
        add_button.grid(row=1,column=3,padx=20,pady=10)
        
       
        generatepassword=Button(self.addpassword_frame,text="Generate Password", width=20, command=self.generate_password)
        generatepassword.grid(row=5,column=3,padx=20,pady=10)
    
    
    def generate_password(self):
        password=strongpassword.generate_strong_password()
        messagebox.showinfo("Generated Password","Your generated password is :   "+password+" \n\n Already pasted on password block")
        self.password_entry.delete(0,END)
        self.password_entry.insert(0,password)
      
    def save_account(self):
        category=self.clicked.get().strip()
        folder=self.folder_box.get().strip()
        website=self.website_entry.get().strip()
        username=self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if website and username and password and category and folder :
            if self.db.web_and_username_exist(self.userid,username,website):
                messagebox.showerror("Error","Username already exists for this website or App!")
            else:
                if self.check_password_strength(password):
                        hashed_password = self.aes_cipher.encrypt_password(password)
                        self.db.insert_data( self.userid,website,username, hashed_password,category,folder)
                        messagebox.showinfo("Success", "saved successfully!")
                        self.website_entry.delete(0, END)
                        self.username_entry.delete(0, END)
                        self.password_entry.delete(0, END)
                        self.clicked.set("")
                        self.folder_box.delete(0,END)
                        if folder not in self.options:
                            self.folder_box['values']+=(folder,)
                            self.folder.append(folder)
        else:
            messagebox.showerror("Error", "Please enter all fields.")
         
                
    def check_password_strength(self,password):
        self.strength_messages = []

        if len(password) < 8:
            self.strength_messages.append("Length should be more than 8 characters")
        
        if not any(char.isupper() for char in password):
            self.strength_messages.append("Should contain at least one uppercase letter")
        
        if not any(char.islower() for char in password):
            self.strength_messages.append("Should contain at least one lowercase letter")
        
        if not any(char.isdigit() for char in password):
            self.strength_messages.append("Should contain at least one digit (0-9)")
        
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
        if not any(char in special_chars for char in password):
            self.strength_messages.append("Should contain at least one special character")

        if self.strength_messages:
            error_message = "\n".join(self.strength_messages)
            messagebox.showerror(title='Weak  Password',message=error_message)
            return 0
        else:
            messagebox.showinfo("Success","Password strength check passed")
            return 1
         
        
        
    def create_search_frame(self):
        
        self.search_frame = LabelFrame(self.password_management_window,text="SEARCH PASSWORD",  width=self.window_width, height=self.window_height)
        self.search_frame.place(relx=0.2, rely=0.3)
        
        search_website = Label(self.search_frame, text= " Website or App name:")
        search_website.grid(row=1, column=0, padx=(30,10), pady=5)
        
        self.search_website_entry=Entry(self.search_frame,width=30 ,bg= "white" )
        self.search_website_entry.grid(row=1,column=1,padx=(0,50),pady=5)
        
        search_username = Label(self.search_frame, text= " Username:")
        search_username.grid(row=2, column=0, padx=(30,10), pady=5)
        
        self.search_username_entry=Entry(self.search_frame,width=30,bg="white")
        self.search_username_entry.grid(row=2,column=1,padx=(0,50),pady=5)
        
        search_id = Label(self.search_frame, text= " ID:")
        search_id.grid(row=4, column=0, padx=(30,10), pady=(10,10))
        
        self.searchbyid_entry=Entry(self.search_frame,width=30,bg= "#f2f2f2")
        self.searchbyid_entry.grid(row=4,column=1,padx=(0,50),pady=(10,10))
        
        search_button=Button(self.search_frame,text="Search", width=40 , command=self.search_by_web_user)
        search_button.grid(row=3,column=0,columnspan=2,padx=50,pady=(10,10))
        
        showall_button=Button(self.search_frame,text="Show all Records", width=40 , command=self.show_records)
        showall_button.grid(row=3,column=2,padx=50,pady=10)
        
        searchbyid_button=Button(self.search_frame,text="Search by ID", width=20 , command=self.search_by_id)
        searchbyid_button.grid(row=5,column=0,columnspan=2,padx=50,pady=10)
        
        update_button=Button(self.search_frame,text="update by ID", width=20 , command=self.update_records)
        update_button.grid(row=4,column=2,pady=(10,10))
        
        delete_button=Button(self.search_frame,text="Delete by ID", width=20 , command=self.delete_records)
        delete_button.grid(row=5,column=2)
        
        Label(self.search_frame,text="Your password will display here").grid(row=1,column=2)
        self.show_password_entry=Entry(self.search_frame,width=20,bg="white")
        self.show_password_entry.grid(row=2,column=2)
        self.create_records_tree()
    
    
    
    
    def delete_records(self):
        id=self.searchbyid_entry.get().strip()
        if id!="" and self.userid==self.db.fetch_userid_id(int(id)):
              id=int(id)
              res = messagebox.askquestion('DELETE RECORD',  'Do you really want to delete the data of the id:{0}'.format(id)) 
              if res == 'yes' :
                  self.db.deleteby_id(id)
                  self.searchbyid_entry.delete(0,END)
                  self.search_username_entry.delete(0,END)
                  self.search_website_entry.delete(0,END)
                  messagebox.showinfo('Confirmation',"DATA deleted Successfully")
                  self.show_records()
          
              else : 
                  messagebox.showinfo('Return', 'Returning to main application') 
        else:
            messagebox.showerror("error","Enter the ID correctly")
    
    def search_by_web_user(self):
        website= self.search_website_entry.get().strip()
        username = self.search_username_entry.get().strip()
        hashed_password=self.db.fetch_password(self.userid,website,username)
        password = self.aes_cipher.decrypt_password(hashed_password)
        
        self.show_password_entry.delete(0,END)
        self.show_password_entry.insert(0,password)
        self.search_website_entry.delete(0,END)
        self.search_username_entry.delete(0,END)
         
    def search_by_id(self):
        id=self.searchbyid_entry.get().strip()
        if self.userid!=self.db.fetch_userid_id(int(id)):
            messagebox.showerror("Error","You are not authorized to view this data")
            self.searchbyid_entry.delete(0,END)
            return
        hashed_password=self.db.fetch_passwordby_id(id)
        if hashed_password==None:
            messagebox.showerror("error","Enter the ID correctly")
            return
        password = self.aes_cipher.decrypt_password(hashed_password)
        
        self.show_password_entry.delete(0,END)
        self.show_password_entry.insert(0,password)
        self.searchbyid_entry.delete(0,END)
    
    
    def update_records(self):
        id=self.searchbyid_entry.get().strip()
        if id!="" and self.userid==self.db.fetch_userid_id(int(id)):
            id=int(id)
            top=Toplevel()
            top.title("UPDATE DETAILS")
            top.geometry("400x260+700+300")
            
            web=Label(top,text="Website:")
            web.grid(row=0,column=0,sticky=E)
            
            web_entry=Entry(top,width=20)
            web_entry.grid(row=0,column=1)
            record = self.db.fetchdata_byid(id)
            username=Label(top,text="username:")
            username.grid(row=2,column=0,sticky=E)
        
        
            user_entry=Entry(top,width=20)
            user_entry.grid(row=2,column=1)
        
            passw=Label(top,text="password:")
            passw.grid(row=3,column=0,sticky=E)
        
        
            passw_entry=Entry(top,width=20)
            passw_entry.grid(row=3,column=1)
            
            category = Label(top, text= " Select Category:")
            category.grid(row=4, column=0, padx=(30,10), pady=10)
            
            self.clicked1 = StringVar()
            self.category_menu1=OptionMenu(top,self.clicked1,"Social Media","Apps")
            self.category_menu1.grid(row=4, column=1, pady=10, sticky=W)
            
            folder = Label(top, text= " Folder Name:")
            folder.grid(row=5, column=0, padx=(30,10), pady=10)
        
            self.folder_box2=Combobox(top, values=self.options, width=20 )
            self.folder_box2.bind("<<ComboboxSelected>>",)
            self.folder_box2.grid(row=5,column=1,pady=10,sticky=W)
        
            web_entry.insert(0,record[4])
            user_entry.insert(0,record[5])
            passw_entry.insert(0,self.aes_cipher.decrypt_password(record[6]))
            self.folder_box2.insert(0,record[8])
            self.clicked1.set(record[7])
        
            update=Button(top,text="Update",command=lambda:update_data(id))
            update.grid(row=6,column=0,columnspan=2,pady=5)
        
            def update_data(id):
                website=web_entry.get().strip()
                uname=user_entry.get().strip()
                passw = passw_entry.get().strip()
                categ=self.clicked1.get().strip()
                folder=self.folder_box2.get().strip()
                if website==None and uname==None and folder==None:
                    messagebox.showerror("Error","Please enter all details")
                    return
                if(self.check_password_strength(passw)):
                    passw=self.aes_cipher.encrypt_password(passw)
                    self.db.update_details(id,website,uname,passw,categ,folder)
                    messagebox.showinfo("Success", "updated successfully!")
                    self.searchbyid_entry.delete(0,END)
                    self.folder.append(folder)
                    self.show_records()
                    top.destroy()
            
        else:
            messagebox.showerror("error","Enter the ID")
        
        
        
    def create_records_tree(self):
        columns = ('ID', 'Website or App Name', 'Username', 'Category', 'Folder Name')
        self.records_tree = Treeview(self.search_frame, columns=columns, show='headings')
        self.records_tree.heading('ID', text="ID")
        self.records_tree.heading('Website or App Name', text="Website or App Name")
        self.records_tree.heading('Username', text="Username")
        self.records_tree.heading('Category', text="Category")
        self.records_tree.heading('Folder Name', text="Folder Name")
        
        self.records_tree['displaycolumns'] = ('ID', 'Website or App Name', 'Username',  'Category','Folder Name')  # which columns to display by default

        self.records_tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item['values']
                self.searchbyid_entry.delete(0,END)
                self.search_website_entry.delete(0,END)
                self.search_website_entry.insert(0,record[1])
                
                self.search_username_entry.delete(0,END)
                self.search_username_entry.insert(0,record[2])
         

        self.records_tree.bind('<<TreeviewSelect>>', item_selected)
    
    def show_records(self):
        self.searchbyid_entry.delete(0,END)
        records_list = self.db.show_records(self.userid)
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        for record in records_list:
            self.records_tree.insert('', END, values=(record[0], record[4], record[5], record[7], record[8]))
        
    
    
    
    def create_categories_frame(self):
        
        self.folder_frame = LabelFrame(self.password_management_window,text="Your Folders",  width=self.window_width, height=self.window_height)
        self.folder_frame.place(relx=0.2, rely=0.3)
        
        self.option1=list(self.db.fetch_folders(self.userid))
        self.options1=[]
        for i in self.option1:
            self.options1.append(i[0])
       
        Label(self.folder_frame,text="Your password will be displayed here").grid(row=1, column=3, padx=(10,10), pady=10)
        
        folder = Label(self.folder_frame, text= "Select Folder:")
        folder.grid(row=2, column=0, padx=(10,10), pady=10)
        
        self.folder_box1=Combobox(self.folder_frame, values=self.options, width=30 )
        self.folder_box1.bind("<<ComboboxSelected>>",)
        self.folder_box1.grid(row=2,column=1,pady=10,sticky=W)
        
        for i in self.folder:
            if i not in self.option1:
                self.folder_box1['values']+=(i,)
        
        showall_button=Button(self.folder_frame,text="Show Records", width=30 , command=self.show_folder_records)
        showall_button.grid(row=2,column=2,padx=10,pady=10)
        
        self.passw=Entry(self.folder_frame,width=30)
        self.passw.grid(row=2,column=3,padx=10,pady=10)
        
        self.create_records_tree1()

    def create_records_tree1(self):
        columns = ('ID', 'Website or App Name', 'Username', 'Category', 'Folder Name')
        self.records_tree1 = Treeview(self.folder_frame, columns=columns, show='headings')
        self.records_tree1.heading('ID', text="ID")
        self.records_tree1.heading('Website or App Name', text="Website or App Name")
        self.records_tree1.heading('Username', text="Username")
        self.records_tree1.heading('Category', text="Category")
        self.records_tree1.heading('Folder Name', text="Folder Name")
        
        self.records_tree1['displaycolumns'] = ('ID', 'Website or App Name', 'Username',  'Category','Folder Name')  # which columns to display by default

        self.records_tree1.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        def item_selected(event):
            for selected_item in self.records_tree1.selection():
                item = self.records_tree1.item(selected_item)
                record = item['values']
                hashed_password=self.db.fetch_passwordby_id(record[0])
                password=self.aes_cipher.decrypt_password(hashed_password)
                self.passw.delete(0,END)
                self.passw.insert(0,password)
         

        self.records_tree1.bind('<<TreeviewSelect>>', item_selected)   
        
        
    def show_folder_records(self):
        foldername=self.folder_box1.get()
        records_list = self.db.show_folderrecords(self.userid,foldername)
        for item in self.records_tree1.get_children():
            self.records_tree1.delete(item)
        for record in records_list:
            self.records_tree1.insert('', END, values=(record[0], record[4], record[5], record[7], record[8]))
    
    
    def show_frame(self):
        selected=self.radio_var.get()
        if  selected == 0:
            self.destroy_search_frame()
            self.destroy_categories_frame()
            self.create_addpassword_frame()
        elif selected ==1:
            self.destroy_addpassword_frame()
            self.destroy_categories_frame()
            self.create_search_frame()
        else:
            self.destroy_addpassword_frame()
            self.destroy_search_frame()
            self.create_categories_frame()
            
    def destroy_addpassword_frame(self):
        if hasattr(self, 'addpassword_frame'): 
            self.addpassword_frame.destroy()
    
    def destroy_search_frame(self):
        if hasattr(self, 'search_frame'): 
            self.search_frame.destroy()
            
    def destroy_categories_frame(self):
        if hasattr(self, 'folder_frame'): 
            self.folder_frame.destroy()
         
        

    def run(self):
        self.password_management_window.mainloop()

