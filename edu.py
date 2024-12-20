import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv

# Initialize the SQLite database

def initialize_database():
    conn = sqlite3.connect("edu_ai_museum.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Visitor")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Visitor (
                VisitorID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                NID TEXT NOT NULL,
                ContactNumber TEXT,
                VisitDate DATE NOT NULL,
                Username TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL
            )
        """)

    # Section table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Section (
            SectionID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Description TEXT
        )
        """)

    # Event table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Event (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventName TEXT NOT NULL,
            EventType TEXT NOT NULL,
            EventDate DATE NOT NULL,
            SectionID INTEGER,
            FOREIGN KEY (SectionID) REFERENCES Section(SectionID)
        )
        """)

    # Feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Feedback (
            FeedbackID INTEGER PRIMARY KEY AUTOINCREMENT,
            VisitorID INTEGER,
            EventID INTEGER,
            FeedbackText TEXT,
            FOREIGN KEY (VisitorID) REFERENCES Visitor(VisitorID),
            FOREIGN KEY (EventID) REFERENCES Event(EventID)
        )
        """)

    # Visitor Event table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS VisitorEvent (
            VisitorEventID INTEGER PRIMARY KEY AUTOINCREMENT,
            VisitorID INTEGER,
            EventID INTEGER,
            InteractionType TEXT,
            FOREIGN KEY (VisitorID) REFERENCES Visitor(VisitorID),
            FOREIGN KEY (EventID) REFERENCES Event(EventID)
        )
        """)

    conn.commit()
    conn.close()

# Add a new section

def add_section():
    def save_section():
        name = entry_name.get()
        description = entry_description.get("1.0", END).strip()

        if name:
            conn = sqlite3.connect("edu_ai_museum.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Section (Name, Description) VALUES (?, ?)", (name, description))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Section added successfully.")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "Section name is required.")

    # Creating the top-level window
    add_window = Toplevel(root)
    add_window.title("Add Section")
    add_window.geometry("400x400")

    # Center the add_window on the screen
    window_width = 500
    window_height = 500
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    add_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Styling labels, entries, and buttons with hover effects
    Label(add_window, text="Section Name:", font=("Arial", 12)).pack(pady=10)
    entry_name = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_name.pack(pady=10, padx=20, fill='x')

    Label(add_window, text="Description:", font=("Arial", 12)).pack(pady=10)
    entry_description = Text(add_window, height=5, width=30, font=("Arial", 12), bd=2, relief="solid")
    entry_description.pack(pady=10, padx=20)

    # Button styling with hover effect
    def on_enter(e):
        save_button.config(bg="lightgreen", relief="raised")

    def on_leave(e):
        save_button.config(bg="#4CAF50", relief="raised")

    save_button = Button(
        add_window,
        text="Save",
        command=save_section,
        font=("Arial", 12),
        bg="#4CAF50",  # Initial color (green)
        bd=2,
        relief="sunken",
        activebackground="lightgreen",
        activeforeground="white"
    )
    save_button.pack(pady=20)

    # Bind the hover effects to the button
    save_button.bind("<Enter>", on_enter)
    save_button.bind("<Leave>", on_leave)
# View all sections
# View sections with improved GUI
def view_data():
    # Establishing database connection with context manager
    with sqlite3.connect("edu_ai_museum.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Section")
        sections = cursor.fetchall()

    # Creating a new top-level window for displaying the sections
    view_window = Toplevel(root)
    view_window.title("Sections")
    view_window.geometry("600x400")

    # Center the window
    window_width = 600
    window_height = 400
    screen_width = view_window.winfo_screenwidth()
    screen_height = view_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    view_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Adding a header label
    Label(view_window, text="Sections", font=("Arial", 18, "bold")).pack(pady=20)

    # Creating a Treeview to display sections in a tabular format
    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Description"), show="headings", height=10)
    tree.heading("#1", text="Section ID")
    tree.heading("#2", text="Section Name")
    tree.heading("#3", text="Section Description")

    # Adding a scrollbar for the Treeview
    scrollbar = Scrollbar(view_window, orient=VERTICAL, command=tree.yview)
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Treeview Styling
    tree.column("#1", width=100, anchor="center")
    tree.column("#2", width=200, anchor="center")
    tree.column("#3", width=250, anchor="center")

    # Packing the Treeview
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Inserting sections into the Treeview
    if sections:
        for section in sections:
            tree.insert("", "end", values=section)
    else:
        # If no sections, display a message at the bottom
        Label(view_window, text="No sections available.", font=("Arial", 12)).pack(pady=20)

    # Close button
    close_button = Button(view_window, text="Close", command=view_window.destroy, font=("Arial", 12), bg="lightgrey", bd=2, relief="raised")
    close_button.pack(pady=20)



# Add a new event

def add_event():
    def save_event():
        # Retrieve values from entry fields
        name = entry_name.get()
        event_type = entry_type.get()
        date = entry_date.get()
        section_id = section_var.get()

        # Validate that all fields are filled
        if name and event_type and date and section_id:
            conn = sqlite3.connect("edu_ai_museum.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Event (EventName, EventType, EventDate, SectionID) VALUES (?, ?, ?, ?)",
                           (name, event_type, date, section_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Event added successfully.")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Fetching sections from the database
    conn = sqlite3.connect("edu_ai_museum.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SectionID, Name FROM Section")
    sections = cursor.fetchall()
    conn.close()

    # Create top-level window for adding events
    add_window = Toplevel(root)
    add_window.title("Add Event")
    add_window.geometry("400x400")  # Window size

    # Center the window on the screen
    window_width = 500
    window_height = 500
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    add_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Styling labels and input fields
    Label(add_window, text="Event Name:", font=("Arial", 12)).pack(pady=10)
    entry_name = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_name.pack(pady=10, padx=20, fill='x')  # Fill horizontally

    Label(add_window, text="Event Type:", font=("Arial", 12)).pack(pady=10)
    entry_type = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_type.pack(pady=10, padx=20, fill='x')  # Fill horizontally

    Label(add_window, text="Event Date (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=10)
    entry_date = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_date.pack(pady=10, padx=20, fill='x')  # Fill horizontally

    # Section selection dropdown
    Label(add_window, text="Section:", font=("Arial", 12)).pack(pady=10)
    section_var = StringVar()
    section_dropdown = ttk.Combobox(add_window, textvariable=section_var, font=("Arial", 12))
    section_dropdown["values"] = [f"{s[0]} - {s[1]}" for s in sections]
    section_dropdown.pack(pady=10, padx=20, fill='x')

    # Save button with hover effect
    def on_button_enter(event):
        save_button.config(bg="lightgreen", fg="black")

    def on_button_leave(event):
        save_button.config(bg="green", fg="white")

    save_button = Button(add_window, text="Save", command=save_event, font=("Arial", 12), bg="green", bd=2,
                         relief="raised")
    save_button.pack(pady=20)
    save_button.bind("<Enter>", on_button_enter)
    save_button.bind("<Leave>", on_button_leave)

# View events
# View events with improved GUI
def view_events():
    # Establishing database connection with context manager
    with sqlite3.connect("edu_ai_museum.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT Event.EventID, Event.EventName, Event.EventType, Event.EventDate, Section.Name
                          FROM Event LEFT JOIN Section ON Event.SectionID = Section.SectionID""")
        events = cursor.fetchall()

    # Creating a new top-level window for displaying the events
    event_window = Toplevel(root)
    event_window.title("Available Events")
    event_window.geometry("700x450")

    # Center the window
    window_width = 700
    window_height = 450
    screen_width = event_window.winfo_screenwidth()
    screen_height = event_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    event_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Adding a header label
    Label(event_window, text="Available Events", font=("Arial", 18, "bold")).pack(pady=20)

    # Creating a Treeview to display events in a tabular format
    tree = ttk.Treeview(event_window, columns=("ID", "Name", "Type", "Date", "Section"), show="headings", height=10)
    tree.heading("#1", text="Event ID")
    tree.heading("#2", text="Event Name")
    tree.heading("#3", text="Event Type")
    tree.heading("#4", text="Event Date")
    tree.heading("#5", text="Section")

    # Adding a scrollbar for the Treeview
    scrollbar = Scrollbar(event_window, orient=VERTICAL, command=tree.yview)
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Treeview Styling
    tree.column("#1", width=100, anchor="center")
    tree.column("#2", width=200, anchor="center")
    tree.column("#3", width=150, anchor="center")
    tree.column("#4", width=120, anchor="center")
    tree.column("#5", width=150, anchor="center")

    # Packing the Treeview
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Inserting events into the Treeview
    if events:
        for event in events:
            tree.insert("", "end", values=event)
    else:
        # If no events, display a message at the bottom
        Label(event_window, text="No events available.", font=("Arial", 12)).pack(pady=20)

    # Close button
    close_button = Button(event_window, text="Close", command=event_window.destroy, font=("Arial", 12), bg="lightgrey", bd=2, relief="raised")
    close_button.pack(pady=20)


# Admin dashboard
def open_admin_dashboard():
    admin_window = Toplevel(root)
    admin_window.title("Admin Dashboard")
    admin_window.geometry("400x400")

    # Center the admin window
    window_width = 500
    window_height = 500
    screen_width = admin_window.winfo_screenwidth()
    screen_height = admin_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    admin_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Create a Label for the dashboard title
    Label(admin_window, text="Admin Dashboard", font=("Arial", 18, "bold"), fg="#2c3e50").pack(pady=20)

    # Create the buttons with hover effects
    def on_hover_button(event, widget, color):
        widget.config(bg=color)

    def on_leave_button(event, widget, original_color):
        widget.config(bg=original_color)

    # Button for adding a visitor
    add_visitor_button = Button(admin_window, text="Add Visitor", font=("Arial", 12), width=20, bg="#3498db", fg="white", relief=SOLID, bd=0, command=add_visitor)
    add_visitor_button.pack(pady=10)
    add_visitor_button.bind("<Enter>", lambda e: on_hover_button(e, add_visitor_button, "#2980b9"))
    add_visitor_button.bind("<Leave>", lambda e: on_leave_button(e, add_visitor_button, "#3498db"))

    # Button for viewing visitors
    view_visitors_button = Button(admin_window, text="View Visitors", font=("Arial", 12), width=20, bg="#3498db", fg="white", relief=SOLID, bd=0, command=view_visitors)
    view_visitors_button.pack(pady=10)
    view_visitors_button.bind("<Enter>", lambda e: on_hover_button(e, view_visitors_button, "#2980b9"))
    view_visitors_button.bind("<Leave>", lambda e: on_leave_button(e, view_visitors_button, "#3498db"))

    # Button for updating a visitor
    update_visitor_button = Button(admin_window, text="Update Visitor", font=("Arial", 12), width=20, bg="#3498db", fg="white", relief=SOLID, bd=0, command=update_visitor)
    update_visitor_button.pack(pady=10)
    update_visitor_button.bind("<Enter>", lambda e: on_hover_button(e, update_visitor_button, "#2980b9"))
    update_visitor_button.bind("<Leave>", lambda e: on_leave_button(e, update_visitor_button, "#3498db"))

    # Button for deleting a visitor
    delete_visitor_button = Button(admin_window, text="Delete Visitor", font=("Arial", 12), width=20, bg="#3498db", fg="white", relief=SOLID, bd=0, command=delete_visitor)
    delete_visitor_button.pack(pady=10)
    delete_visitor_button.bind("<Enter>", lambda e: on_hover_button(e, delete_visitor_button, "#2980b9"))
    delete_visitor_button.bind("<Leave>", lambda e: on_leave_button(e, delete_visitor_button, "#3498db"))

    # Button for adding an event
    add_event_button = Button(admin_window, text="Add Event", font=("Arial", 12), width=20, bg="#3498db", fg="white", relief=SOLID, bd=0, command=add_event)
    add_event_button.pack(pady=10)
    add_event_button.bind("<Enter>", lambda e: on_hover_button(e, add_event_button, "#2980b9"))
    add_event_button.bind("<Leave>", lambda e: on_leave_button(e, add_event_button, "#3498db"))

    # Button for adding a section
    add_section_button = Button(admin_window, text="Add Section", font=("Arial", 12), width=20, bg="#3498db", fg="white", relief=SOLID, bd=0, command=add_section)
    add_section_button.pack(pady=10)
    add_section_button.bind("<Enter>", lambda e: on_hover_button(e, add_section_button, "#2980b9"))
    add_section_button.bind("<Leave>", lambda e: on_leave_button(e, add_section_button, "#3498db"))

    # Run the admin window
    admin_window.mainloop()


# Visitor dashboard
def open_visitor_dashboard():
    # Create a new window for the visitor dashboard
    visitor_window = Toplevel(root)
    visitor_window.title("Visitor Dashboard")
    visitor_window.geometry("400x300")

    # Center the window on the screen
    window_width = 500
    window_height = 500
    screen_width = visitor_window.winfo_screenwidth()
    screen_height = visitor_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    visitor_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Styling for the title label
    title_label = Label(visitor_window, text="Visitor Dashboard", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    # Hover effect for buttons
    def on_button_enter(event, button):
        button.config(bg="lightblue", fg="black")

    def on_button_leave(event, button):
        button.config(bg="skyblue", fg="white")

    # Button to view sections
    view_sections_button = Button(visitor_window, text="View Sections", command=view_data, font=("Arial", 14), bg="skyblue", bd=2, relief="raised")
    view_sections_button.pack(pady=10, padx=20, fill='x')
    view_sections_button.bind("<Enter>", lambda event, button=view_sections_button: on_button_enter(event, button))
    view_sections_button.bind("<Leave>", lambda event, button=view_sections_button: on_button_leave(event, button))

    # Button to view events
    view_events_button = Button(visitor_window, text="View Events", command=view_events, font=("Arial", 14), bg="skyblue", bd=2, relief="raised")
    view_events_button.pack(pady=10, padx=20, fill='x')
    view_events_button.bind("<Enter>", lambda event, button=view_events_button: on_button_enter(event, button))
    view_events_button.bind("<Leave>", lambda event, button=view_events_button: on_button_leave(event, button))


# Login validation
def validate_login(username, password, role):
    if role == "Admin" and username == "1" and password == "1":
        open_admin_dashboard()
    elif role == "Visitor" and username == "1" and password == "1":
        open_visitor_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
# Function to add a visitor
def add_visitor():
    def save_visitor():
        # Retrieve values from entry fields
        name = entry_name.get()
        nid = entry_nid.get()
        contact = entry_contact.get()
        date = entry_date.get()
        username = entry_username.get()
        password = entry_password.get()

        # Validate that all fields are filled
        if name and nid and contact and date and username and password:
            try:
                conn = sqlite3.connect("edu_ai_museum.db")
                cursor = conn.cursor()
                cursor.execute(""" 
                INSERT INTO Visitor (Name, NID, ContactNumber, VisitDate, Username, Password)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (name, nid, contact, date, username, password))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Visitor added successfully.")
                add_window.destroy()
                view_visitors()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username must be unique.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Create a new window for adding a visitor
    add_window = Toplevel(root)
    add_window.title("Add Visitor")
    add_window.geometry("400x800")  # Window size

    # Center the window on the screen
    window_width = 400
    window_height = 600
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    add_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Styling labels and input fields
    Label(add_window, text="Visitor Name:", font=("Arial", 12)).pack(pady=10)
    entry_name = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_name.pack(pady=10, padx=20, fill='x')

    Label(add_window, text="NID:", font=("Arial", 12)).pack(pady=10)
    entry_nid = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_nid.pack(pady=10, padx=20, fill='x')

    Label(add_window, text="Contact Number:", font=("Arial", 12)).pack(pady=10)
    entry_contact = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_contact.pack(pady=10, padx=20, fill='x')

    Label(add_window, text="Visit Date (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=10)
    entry_date = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_date.pack(pady=10, padx=20, fill='x')

    Label(add_window, text="Username:", font=("Arial", 12)).pack(pady=10)
    entry_username = Entry(add_window, font=("Arial", 12), bd=2, relief="solid")
    entry_username.pack(pady=10, padx=20, fill='x')

    Label(add_window, text="Password:", font=("Arial", 12)).pack(pady=10)
    entry_password = Entry(add_window, show="*", font=("Arial", 12), bd=2, relief="solid")
    entry_password.pack(pady=10, padx=20, fill='x')

    # Save button with hover effect
    def on_button_enter(event):
        save_button.config(bg="lightgreen", fg="black")

    def on_button_leave(event):
        save_button.config(bg="green", fg="white")

    save_button = Button(add_window, text="Save", command=save_visitor, font=("Arial", 12), bg="green", bd=2, relief="raised")
    save_button.pack(pady=20)
    save_button.bind("<Enter>", on_button_enter)
    save_button.bind("<Leave>", on_button_leave)

# View all visitors
# View all visitors
def view_visitors():
    # Fetch visitors from the database
    conn = sqlite3.connect("edu_ai_museum.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Visitor")
    visitors = cursor.fetchall()
    conn.close()

    # Create a new window to display visitors
    view_window = Toplevel(root)
    view_window.title("Visitors")
    view_window.geometry("500x400")

    # Center the window
    window_width = 500
    window_height = 400
    screen_width = view_window.winfo_screenwidth()
    screen_height = view_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    view_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Heading
    Label(view_window, text="All Visitors", font=("Arial", 18, "bold")).pack(pady=20)

    # Scrollable frame to display the visitors list
    canvas = Canvas(view_window)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(view_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = Frame(canvas)
    scrollable_frame.pack(fill="both", expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Add visitor details to the scrollable frame
    if visitors:
        for visitor in visitors:
            visitor_details = f"ID: {visitor[0]}, Name: {visitor[1]}, Username: {visitor[5]}"
            Label(scrollable_frame, text=visitor_details, font=("Arial", 12)).pack(pady=5)
    else:
        Label(scrollable_frame, text="No visitors available.", font=("Arial", 12)).pack()

    # Update the scrollable frame's scrollregion to enable scrolling
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Close button
    close_button = Button(view_window, text="Close", command=view_window.destroy, font=("Arial", 12), bg="lightgrey",
                          bd=2, relief="raised")
    close_button.pack(pady=10)


# Update a visitor's information
def update_visitor():
    def save_update():
        visitor_id = visitor_id_var.get()
        username = entry_username.get()
        password = entry_password.get()

        if visitor_id and username and password:
            try:
                conn = sqlite3.connect("edu_ai_museum.db")
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE Visitor
                SET Username = ?, Password = ?
                WHERE VisitorID = ?
                """, (username, password, visitor_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Visitor information updated successfully.")
                update_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "All fields are required.")

    update_window = Toplevel(root)
    update_window.title("Update Visitor")
    update_window.geometry("400x300")

    # Center the window
    window_width = 400
    window_height = 500
    screen_width = update_window.winfo_screenwidth()
    screen_height = update_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    update_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Heading
    Label(update_window, text="Update Visitor Information", font=("Arial", 16, "bold")).pack(pady=20)

    # Visitor ID input
    Label(update_window, text="Enter Visitor ID:", font=("Arial", 12)).pack(pady=5)
    visitor_id_var = Entry(update_window, font=("Arial", 12), bd=2, relief="solid")
    visitor_id_var.pack(pady=5, padx=20, fill="x")

    # New username input
    Label(update_window, text="New Username:", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(update_window, font=("Arial", 12), bd=2, relief="solid")
    entry_username.pack(pady=5, padx=20, fill="x")

    # New password input
    Label(update_window, text="New Password:", font=("Arial", 12)).pack(pady=5)
    entry_password = Entry(update_window, font=("Arial", 12), bd=2, relief="solid", show="*")
    entry_password.pack(pady=5, padx=20, fill="x")

    # Update button with hover effect
    def on_enter(event):
        update_button.config(bg="lightseagreen")

    def on_leave(event):
        update_button.config(bg="seagreen")

    update_button = Button(update_window, text="Update", command=save_update, font=("Arial", 12, "bold"), bg="seagreen", bd=2, relief="raised")
    update_button.pack(pady=20)

    update_button.bind("<Enter>", on_enter)  # Add hover effect
    update_button.bind("<Leave>", on_leave)

    # Cancel button
    cancel_button = Button(update_window, text="Cancel", command=update_window.destroy, font=("Arial", 12), bg="lightgrey", bd=2, relief="raised")
    cancel_button.pack(pady=5)

# Delete a visitor
def delete_visitor():
    def delete_user():
        visitor_id = visitor_id_var.get()

        if visitor_id:
            try:
                conn = sqlite3.connect("edu_ai_museum.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Visitor WHERE VisitorID = ?", (visitor_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Visitor deleted successfully.")
                delete_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Visitor ID is required.")

    delete_window = Toplevel(root)
    delete_window.title("Delete Visitor")
    delete_window.geometry("400x250")

    # Center the window
    window_width = 400
    window_height = 250
    screen_width = delete_window.winfo_screenwidth()
    screen_height = delete_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    delete_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Heading
    Label(delete_window, text="Delete Visitor", font=("Arial", 16, "bold")).pack(pady=20)

    # Visitor ID input
    Label(delete_window, text="Enter Visitor ID:", font=("Arial", 12)).pack(pady=5)
    visitor_id_var = Entry(delete_window, font=("Arial", 12), bd=2, relief="solid")
    visitor_id_var.pack(pady=5, padx=20, fill="x")  # Make it fill horizontally

    # Delete button with hover effect
    def on_enter(event):
        delete_button.config(bg="lightcoral")

    def on_leave(event):
        delete_button.config(bg="tomato")

    delete_button = Button(delete_window, text="Delete", command=delete_user, font=("Arial", 12, "bold"), bg="tomato", bd=2, relief="raised")
    delete_button.pack(pady=20)

    delete_button.bind("<Enter>", on_enter)  # Add hover effect
    delete_button.bind("<Leave>", on_leave)

    # Padding and better visual appeal
    Button(delete_window, text="Cancel", command=delete_window.destroy, font=("Arial", 12), bg="lightgrey", bd=2, relief="raised").pack(pady=5)





def export_events():
    conn = sqlite3.connect("edu_ai_museum.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event")
    events = cursor.fetchall()

    with open('events.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["EventID", "EventName", "EventType", "EventDate", "SectionID"])
        for event in events:
            writer.writerow(event)
    messagebox.showinfo("Success", "Events data exported to events.csv")


def on_hover(event, widget, color):
    widget.config(bg=color)

def on_leave(event, widget, original_color):
    widget.config(bg=original_color)



def main_screen():
    global root
    root = Tk()
    root.title("EDU AI Museum")
    root.geometry("700x700")

    window_width = 800
    window_height = 800

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position to center the window
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Create a Canvas widget for the gradient background
    canvas = Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill=BOTH, expand=True)

    # Create gradient effect (vertical gradient from blue to red)
    gradient_colors = ['#3498db', '#9b59b6', '#e74c3c']
    for i, color in enumerate(gradient_colors):
        canvas.create_rectangle(0, window_height * i / len(gradient_colors), window_width, window_height * (i + 1) / len(gradient_colors), fill=color, outline=color)

    # Create a Label for the welcome message
    welcome_label = Label(root, text="WELCOME TO EDU AI MUSEUM", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#3498db")
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")  # Centered horizontally at the top of the screen

    # Create a Frame to hold the login components
    frame = Frame(root, bg="white", bd=5, relief=SOLID)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Title Label
    Label(frame, text="Login", font=("Arial", 24, "bold"), fg="#2c3e50").grid(row=0, columnspan=2, pady=20)

    # Username Entry
    Label(frame, text="Username:", font=("Arial", 14), fg="#34495e").grid(row=1, column=0, sticky=W, padx=20, pady=10)
    entry_username = Entry(frame, font=("Arial", 14), bd=2, relief=SOLID, fg="#34495e", highlightbackground="#2980b9", highlightcolor="#2980b9")
    entry_username.grid(row=1, column=1, padx=20, pady=10)

    # Bind hover effect for username entry box
    entry_username.bind("<Enter>", lambda e: on_hover(e, entry_username, "#ecf0f1"))  # Light grey on hover
    entry_username.bind("<Leave>", lambda e: on_leave(e, entry_username, "#ffffff"))  # White background on leave

    # Password Entry
    Label(frame, text="Password:", font=("Arial", 14), fg="#34495e").grid(row=2, column=0, sticky=W, padx=20, pady=10)
    entry_password = Entry(frame, font=("Arial", 14), bd=2, relief=SOLID, show="*", fg="#34495e", highlightbackground="#2980b9", highlightcolor="#2980b9")
    entry_password.grid(row=2, column=1, padx=20, pady=10)

    # Bind hover effect for password entry box
    entry_password.bind("<Enter>", lambda e: on_hover(e, entry_password, "#ecf0f1"))
    entry_password.bind("<Leave>", lambda e: on_leave(e, entry_password, "#ffffff"))

    # Role Selection
    Label(frame, text="Role:", font=("Arial", 14), fg="#34495e").grid(row=3, column=0, sticky=W, padx=20, pady=10)
    role_var = StringVar(value="Admin")
    Radiobutton(frame, text="Admin", variable=role_var, value="Admin", font=("Arial", 12), fg="#34495e", bg="white", activebackground="white", activeforeground="#2980b9").grid(row=3, column=1, sticky=W)
    Radiobutton(frame, text="Visitor", variable=role_var, value="Visitor", font=("Arial", 12), fg="#34495e", bg="white", activebackground="white", activeforeground="#2980b9").grid(row=4, column=1, sticky=W)

    # Login Button
    login_button = Button(frame, text="Login", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=20, relief=SOLID, bd=0,
                          command=lambda: validate_login(entry_username.get(), entry_password.get(), role_var.get()))
    login_button.grid(row=5, columnspan=2, pady=20)

    # Bind hover events to the login button
    login_button.bind("<Enter>", lambda e: on_hover(e, login_button, "#45a049"))  # Darker green on hover
    login_button.bind("<Leave>", lambda e: on_leave(e, login_button, "#4CAF50"))  # Original color on leave

    # Add a "Quit" button to close the application
    quit_button = Button(frame, text="Quit", font=("Arial", 14, "bold"), bg="#f44336", fg="white", width=20, relief=SOLID, bd=0, command=root.quit)
    quit_button.grid(row=6, columnspan=2, pady=10)

    # Bind hover events to the quit button
    quit_button.bind("<Enter>", lambda e: on_hover(e, quit_button, "#e53935"))  # Darker red on hover
    quit_button.bind("<Leave>", lambda e: on_leave(e, quit_button, "#f44336"))  # Original color on leave

    # Run the main loop
    root.mainloop()

# Run the main screen
main_screen()
# Run the application
if __name__ == "__main__":
    initialize_database()
    main_screen()
