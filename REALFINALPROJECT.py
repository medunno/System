import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import mysql.connector

# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="desiree",
    password="desiree<3",
    database="System"
)

# Create cursor
mycursor = mydb.cursor()

# Ensure the table exists
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        Users VARCHAR(250) PRIMARY KEY,
        Passwords VARCHAR(250) NOT NULL,
        Name VARCHAR(250) NOT NULL,
        Course VARCHAR(250) NOT NULL,
        Age INT NOT NULL,
        Sex VARCHAR(250) NOT NULL
    )
""")

# Function to handle label click event
def clickable_label(event):
    login_frame.pack_forget()
    global signup_frame
    def insert():
        username = signup_user_entry.get()
        password = signup_password_entry.get()
        name = signup_name_entry.get()
        course = signup_course_entry.get()
        age = signup_age_entry.get()
        sex = signup_sex_entry.get()
        if username == "" or password == "" or name == "" or age == "" or course == "" or sex == "":
            tkinter.messagebox.showerror('Error', 'Empty Fields Are Not Allowed')
            return
        try:
           age = int(age)
        except ValueError:
           tkinter.messagebox.showerror('Error', 'Age must be an integer')
           return
        mycursor.execute("SELECT Users FROM admin WHERE Users = %s", (username,))
        if mycursor.fetchone():
            tkinter.messagebox.showerror('Error', 'Username Already Exist')
            return False
        sql = 'INSERT INTO admin (Users, Passwords, Name, Age, Course , Sex) VALUES (%s, %s, %s, %s, %s, %s)'
        val = (username, password, name, age, course, sex)
        mycursor.execute(sql, val)
        mydb.commit()
        signup_frame.pack_forget()
        login_frame.pack()
    signup_frame = customtkinter.CTkFrame(window, width=1000, height=800)
    signup_frame.pack()

    signup_user_entry = customtkinter.CTkEntry(signup_frame, width=250, height=50, 
                                               border_width=1, border_color='#018f0b',placeholder_text='Username')
    signup_user_entry.bind("<FocusIn>", 
                           lambda event: signup_user_entry.delete(0, END) if signup_user_entry.get() == 'Username' else None)
    signup_user_entry.place(x=100, y=170)
    
    return_button = customtkinter.CTkButton(signup_frame, text='Return to Login',
                                             height=45, command=lambda: (signup_frame.pack_forget(), login_frame.pack()), 
                                             fg_color='#018f0b', hover_color='#02bf0f', width=120)
    return_button.place(x=228, y=590)

    signup_button = customtkinter.CTkButton(signup_frame, text='Sign Up', fg_color='#018f0b', 
                                            height=45, hover_color='#02bf0f', width=120, command=insert)
    signup_button.place(x=101, y=590)

    signup_password_entry = customtkinter.CTkEntry(signup_frame, width=250, height=50, border_width=1,
                                                    border_color='#018f0b',placeholder_text='Password')
    signup_password_entry.bind("<FocusIn>",
                                lambda event: signup_password_entry.delete(0, END) if signup_password_entry.get() == 'Password' else None)
    signup_password_entry.place(x=100, y=240)
    
    signup_name_entry = customtkinter.CTkEntry(signup_frame, width=250, height=50, border_width=1, 
                                               border_color='#018f0b',placeholder_text='Name')
    signup_name_entry.bind("<FocusIn>", lambda event: signup_name_entry.delete(0, END) if signup_name_entry.get() == 'Name' else None)
    signup_name_entry.place(x=100, y=310)

    signup_course_entry = customtkinter.CTkEntry(signup_frame, width=250, height=50, border_width=1, border_color='#018f0b',placeholder_text='Course')
    signup_course_entry.bind("<FocusIn>", lambda event: signup_course_entry.delete(0, END) if signup_course_entry.get() == 'Course' else None)
    signup_course_entry.place(x=100, y=380)

    signup_age_entry = customtkinter.CTkEntry(signup_frame, width=250, height=50, border_width=1, border_color='#018f0b',placeholder_text='Age')
    signup_age_entry.bind("<FocusIn>", lambda event: signup_age_entry.delete(0, END) if signup_age_entry.get() == 'Age' else None)
    signup_age_entry.place(x=100, y=450)   

    signup_sex_entry = customtkinter.CTkEntry(signup_frame, width=250, height=50, border_width=1, border_color='#018f0b',placeholder_text='Sex')
    signup_sex_entry.bind("<FocusIn>", lambda event: signup_sex_entry.delete(0, END) if signup_sex_entry.get() == 'Sex' else None)
    signup_sex_entry.place(x=100, y=520)

# Function to handle login button click event
def handle_login():
    username = user_entry.get()
    password = password_entry.get()
    
    # Verify login credentials
    mycursor.execute("SELECT * FROM admin WHERE Users = %s AND Passwords = %s", (username, password))
    result = mycursor.fetchone()
    
    if result:
        login_frame.pack_forget()
        if username == 'admin':  # Check if the user is the admin
            admin_frame.pack(fill='both', expand=True)
            load_review_data()
        else:
            user_frame.pack(fill='both', expand=True)
            load_user_data(username)
    else:
        tkinter.messagebox.showerror('Error', 'Invalid Username or Password')

# Function to load review data for admin
def load_review_data():
    mycursor.execute("SELECT * FROM admin")
    rows = mycursor.fetchall()
    
    for row in admin_table.get_children():
        admin_table.delete(row)
    
    for row in rows:
        admin_table.insert("", "end", values=row)

# Function to load user data for a regular user
def load_user_data(username):
    mycursor.execute("SELECT * FROM admin WHERE Users = %s", (username,))
    result = mycursor.fetchone()
    
    for row in user_table.get_children():
        user_table.delete(row)
    
    user_table.insert("", "end", values=result)

# Function to edit selected data
def edit_action():
    selected_item = admin_table.selection()
    if selected_item:
        item_values = admin_table.item(selected_item)['values']
        edit_user_entry.delete(0, END)
        edit_password_entry.delete(0, END)
        edit_name_entry.delete(0, END)
        edit_course_entry.delete(0, END)
        edit_age_entry.delete(0, END)
        edit_sex_entry.delete(0, END)
        edit_user_entry.insert(0, item_values[0])
        edit_password_entry.insert(0, item_values[1])
        edit_name_entry.insert(0, item_values[2])
        edit_course_entry.insert(0, item_values[3])
        edit_age_entry.insert(0, item_values[4])
        edit_sex_entry.insert(0, item_values[5])
    else:
        tkinter.messagebox.showwarning('Warning', 'No item selected')

def save_edit_action():
    selected_item = admin_table.selection()
    if selected_item:
        username = edit_user_entry.get()
        password = edit_password_entry.get()
        name = edit_name_entry.get()
        course = edit_course_entry.get()
        age = edit_age_entry.get()
        sex = edit_sex_entry.get()
        mycursor.execute("UPDATE admin SET Passwords = %s, Name = %s, Course = %s, Age = %s, Sex = %s WHERE Users = %s", 
                         (password, name, course, age, sex, username))
        mydb.commit()
        load_review_data()
        tkinter.messagebox.showinfo('Info', 'Record updated successfully')
    else:
        tkinter.messagebox.showwarning('Warning', 'No item selected')

# Function to delete selected data
def delete_action():
    selected_item = admin_table.selection()
    if selected_item:
        item_values = admin_table.item(selected_item)['values']
        mycursor.execute("DELETE FROM admin WHERE Users = %s", (item_values[0],))
        mydb.commit()
        load_review_data()
        tkinter.messagebox.showinfo('Info', f'Deleted {item_values[0]}')
    else:
        tkinter.messagebox.showwarning('Warning', 'No item selected')

# Function to change password
def change_password():
    selected_item = user_table.selection()
    if selected_item:
        new_password = new_password_entry.get()
        if new_password:
            item_values = user_table.item(selected_item)['values']
            mycursor.execute("UPDATE admin SET Passwords = %s WHERE Users = %s", (new_password, item_values[0]))
            mydb.commit()
            tkinter.messagebox.showinfo('Info', 'Password changed successfully')
        else:
            tkinter.messagebox.showwarning('Warning', 'Password cannot be empty')
    else:
        tkinter.messagebox.showwarning('Warning', 'No item selected')

# Function to sign out
def sign_out():
    admin_frame.pack_forget()
    user_frame.pack_forget()
    login_frame.pack()

# Create the main window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
window = customtkinter.CTk()
window.title('Enrollment System')
window.config(bg='grey')

# Create login frame
login_frame = customtkinter.CTkFrame(window, width=1000, height=800)
login_frame.pack()

# Create login widgets
user_entry = customtkinter.CTkEntry(login_frame, width=250, height=50, 
                                    border_width=1, border_color='#018f0b', placeholder_text='Enter Username')
user_entry.bind("<FocusIn>", lambda event: user_entry.delete(0, END))
user_entry.place(x=380, y=250)

password_entry = customtkinter.CTkEntry(login_frame, width=250, height=50, border_width=1, 
                                        border_color='#018f0b', placeholder_text='Enter Password', show="*")
password_entry.bind("<FocusIn>", lambda event: password_entry.delete(0, END))
password_entry.place(x=380, y=310)

login_button = customtkinter.CTkButton(login_frame, text='Log In', font=("Arial", 20, "bold"), corner_radius=10, 
                                       width=250, height=25, fg_color='#018f0b', hover_color='#02bf0f', command=handle_login)
login_button.place(x=380, y=375)

create_acc_label = customtkinter.CTkLabel(login_frame, text='Create an account?', font=("Arial", 15), text_color='#018f0b')
create_acc_label.bind("<Button-1>", clickable_label)
create_acc_label.place(x=443.5, y=420)

# Create admin frame
admin_frame = customtkinter.CTkFrame(window, width=1000, height=800)

admin_table = ttk.Treeview(admin_frame, columns=('Username', 'Password', 'Name', 'Course', 'Age', 'Sex'), show='headings')
admin_table.heading('Username', text='Username')
admin_table.heading('Password', text='Password')
admin_table.heading('Name', text='Name')
admin_table.heading('Course', text='Course')
admin_table.heading('Age', text='Age')
admin_table.heading('Sex', text='Sex')
admin_table.pack(fill='both', expand=True, padx=20, pady=20)

# Create action buttons for admin
button_frame = customtkinter.CTkFrame(admin_frame)
button_frame.pack(fill='x', pady=10)

edit_button = customtkinter.CTkButton(button_frame, text='Edit', command=edit_action)
edit_button.pack(side='left', padx=10, pady=10)

delete_button = customtkinter.CTkButton(button_frame, text='Delete', command=delete_action)
delete_button.pack(side='left', padx=10, pady=10)

sign_out_button = customtkinter.CTkButton(button_frame, text='Sign Out', command=sign_out)
sign_out_button.pack(side='left', padx=10, pady=10)

# Create entry fields for editing user data in admin frame
edit_frame = customtkinter.CTkFrame(admin_frame)
edit_frame.pack(fill='x', pady=10)

edit_user_entry = customtkinter.CTkEntry(edit_frame, width=200, height=30, placeholder_text='Username')
edit_user_entry.pack(side='left', padx=5)

edit_password_entry = customtkinter.CTkEntry(edit_frame, width=200, height=30, placeholder_text='Password')
edit_password_entry.pack(side='left', padx=5)

edit_name_entry = customtkinter.CTkEntry(edit_frame, width=200, height=30, placeholder_text='Name')
edit_name_entry.pack(side='left', padx=5)

edit_course_entry = customtkinter.CTkEntry(edit_frame, width=200, height=30, placeholder_text='Course')
edit_course_entry.pack(side='left', padx=5)

edit_age_entry = customtkinter.CTkEntry(edit_frame, width=200, height=30, placeholder_text='Age')
edit_age_entry.pack(side='left', padx=5)

edit_sex_entry = customtkinter.CTkEntry(edit_frame, width=200, height=30, placeholder_text='Sex')
edit_sex_entry.pack(side='left', padx=5)

save_edit_button = customtkinter.CTkButton(edit_frame, text='Save', command=save_edit_action)
save_edit_button.pack(side='left', padx=10)

# Create user frame
user_frame = customtkinter.CTkFrame(window, width=1000, height=800)

user_table = ttk.Treeview(user_frame, columns=('Username', 'Password', 'Name', 'Course', 'Age', 'Sex'), show='headings')
user_table.heading('Username', text='Username')
user_table.heading('Password', text='Password')
user_table.heading('Name', text='Name')
user_table.heading('Course', text='Course')
user_table.heading('Age', text='Age')
user_table.heading('Sex', text='Sex')
user_table.pack(fill='both', expand=True, padx=20, pady=20)

# Create change password section for user
password_frame = customtkinter.CTkFrame(user_frame)
password_frame.pack(fill='x', pady=10)

new_password_entry = customtkinter.CTkEntry(password_frame, width=250, height=50, border_width=1, border_color='#018f0b', placeholder_text='New Password')
new_password_entry.pack(side='left', padx=10, pady=10)

change_password_button = customtkinter.CTkButton(password_frame, text='Change Password', command=change_password)
change_password_button.pack(side='left', padx=10, pady=10)

sign_out_button_user = customtkinter.CTkButton(password_frame, text='Sign Out', command=sign_out)
sign_out_button_user.pack(side='left', padx=10, pady=10)

window.mainloop()
