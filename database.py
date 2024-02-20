import sqlite3

class DatabaseManager:
    def __init__(self):
        self.db_name = 'RECORDS.db'

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT,
                            favourite_food TEXT
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS vault (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            username VARCHAR(200),
            password VARCHAR(50),
            category TEXT,
            folder TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id) 
        )
                       
                       ''')
       
        conn.commit()
        conn.close()

    def username_exists(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username=?''', (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def register_user(self, username, password,favourite_food):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (username, password,favourite_food) VALUES (?, ?, ?)''', (username, password,favourite_food))
        conn.commit()
        conn.close()

    def get_favorite_food(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT favourite_food FROM users WHERE username=?''', (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None

    def get_password(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT password FROM users WHERE username=?''', (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
        
    def get_userid(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM users WHERE username=?''', (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    
    def insert_data(self,userid,website,username,password,category, folder):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO vault (user_id,website,username,password,category,folder) VALUES (?, ?, ?, ?, ?, ?)''', (userid,website, username, password, category, folder))
        conn.commit()
        conn.close()
    
    def web_and_username_exist(self,userid,username,website):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT * FROM vault WHERE user_id=? AND website=? AND username=?''', ( userid,website,username,))
            res = cursor.fetchone()
            if res:
                print(res)
            else:
                print("No matching records found.")
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
        conn.close()
        return res is  not  None 
    
    def show_records(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM vault WHERE user_id=?''', (user_id,))
        records = cursor.fetchall()
        conn.close()
        return records
    
    def show_folderrecords(self, user_id,folder):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM vault WHERE user_id=? and folder=?''', (user_id,folder))
        records = cursor.fetchall()
        conn.close()
        return records
    
    def fetch_id(self,userid,website,username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM vault WHERE user_id=? AND website=? AND username=?''', ( userid,website,username))
        res = cursor.fetchone()
        conn.close
        if(res==None):
            return None
        return res[0] 
    
    def fetch_password(self,id,website,username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT password FROM vault WHERE user_id=? AND website=? AND username=?''', (id,website,username))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
        
  
    def update_details(self,id,website,username,password,category,folder):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE vault SET website= ?,username=?,password=?,category=?,folder=? WHERE id= ?''', (website,username,password,category,folder,id,))
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
        conn.commit()
        conn.close()
    
    
    
    def fetch_passwordby_id(self,id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT password FROM vault WHERE id=?''', (id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    
    def fetchdata_byid(self,id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM vault WHERE id=?''', (id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result
        else:
            return None
    
    def deleteby_id(self,id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM vault WHERE id=?''', (id,))
        conn.commit()
        conn.close()
        
    def fetch_userid_id(self,id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT user_id FROM vault WHERE id=?''', (id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    
    def fetch_folders(self,id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT  DISTINCT folder FROM vault WHERE user_id=? ORDER BY folder ASC ''',(id,))  #ASC for alphabetical order
        result=cursor.fetchall()
        conn.close()
        if result:
            return result
        else:
            return []