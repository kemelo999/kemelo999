import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from PIL import Image, ImageTk, ImageSequence, ImageFont, ImageDraw
from tkinter import font
import winsound

# Function to update the button image to the next frame
def update_frame(button, frames, index):
    frame = frames[index]
    index = (index + 1) % len(frames)
    button.config(image=frame)
    root.after(100, update_frame, button, frames, index)  # Adjust the interval as needed

# Load animated GIF and create a list of frames
def load_animated_gif(path):
    image = Image.open(path)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(image)]
    return frames

# Database connection function
def connect_to_database(server, database, username, password):
    try:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
        return None

# Function to fetch data from the database
def fetch_data():
    conn = connect_to_database(server, database, username, password)
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM SuperHeroeVsVillain")
            rows = cursor.fetchall()
            for row in rows:
                formatted_row = [str(item).strip("(),'") for item in row]
                tree.insert("", tk.END, values=formatted_row)
                tree.pack(pady=20)  # Show the Treeview widget
        except Exception as e:
            messagebox.showerror("Fetch Error", f"Failed to fetch data: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to search the database
def search_data():
    conn = connect_to_database(server, database, username, password)
    if conn:
        cursor = conn.cursor()
        try:
            search_value = search_entry.get()
            search_query = "SELECT * FROM SuperHeroeVsVillain WHERE Superhero LIKE ? OR Villain LIKE ?"
            cursor.execute(search_query, ('%' + search_value + '%', '%' + search_value + '%'))
            rows = cursor.fetchall()
            for i in tree.get_children():
                tree.delete(i)
            
            for row in rows:
                formatted_row = [str(item).strip("(),'") for item in row]
                tree.insert("", tk.END, values=formatted_row)
                tree.pack(pady=20)  # Show the Treeview widget
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search data: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to clear the search entry and refresh the treeview
def clear_search():
    search_entry.delete(0, tk.END)
    for i in tree.get_children():
        tree.delete(i)

# Function to show superhero details in a new window
def show_superhero_details(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        superhero_name = item['values'][1]  # Assuming the second column contains the superhero name
        display_superhero_details(superhero_name)      

# Function to fetch and display superhero details
def display_superhero_details(superhero_name):
    conn = connect_to_database(server, database, username, password)
    if conn:
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM SuperHeroeVsVillain WHERE Superhero = ?"
            cursor.execute(query, (superhero_name,))
            row = cursor.fetchone()
            if row:
                detail_window = tk.Toplevel(root)
                detail_window.title(f"Details of {superhero_name}")
                detail_window.geometry("400x300")
                
                for i, col in enumerate(cursor.description):
                    label = tk.Label(detail_window, text=f"{col[0]}: {row[i]}", font=comic_crazy_font)
                    label.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Details Error", f"Failed to fetch details: {e}")
        finally:
            cursor.close()
            conn.close()

def open_about_us():
    about_window = tk.Toplevel(root)
    about_window.title("About Us")
    about_window.geometry("400x300")
    about_window.configure(bg="black")

    # About Us content
    about_text = (
        "Welcome to the Superhero Database!\n\n"
        "This application allows you to explore various superheroes and their "
        "villains, along with detailed information about each character. "
        "Whether you're a kid, a comic lover, or just someone who enjoys "
        "superhero stories, this app is for you!\n\n"
        "Enjoy discovering the amazing world of superheroes!"
    )

    # Display the content in the new window
    label = tk.Label(about_window, text=about_text, font=("Comic Sans MS", 14), bg="black", fg="white", wraplength=350, justify=tk.LEFT)
    label.pack(padx=20, pady=20)

# Database credentials
server = 'LAPTOP-I9DO8U7Q\SQLEXPRESS'
database = 'ProjectTkinter'
username = 'sa'
password = '1234'

# Tkinter Mini Project GUI
root = tk.Tk()
root.title("Project Tkinter")
root.geometry("1040x800")

# Load the background image using PIL
image_path = r'C:\Users\Kemelo-fmtali\Desktop\1366-x-768-marvel-vs-dc-vk10rl9i62v86vpv.jpg'
image = Image.open(image_path)
background_image = ImageTk.PhotoImage(image)

# Create a Canvas widget to display the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Create a custom font
comic_crazy_font = font.Font(family="Comic Sans MS", size=10)

# Frame for search input
search_frame = tk.Frame(canvas, bg='black')
search_frame.pack(pady=20, anchor='nw')

# Input field for searching data
search_label = tk.Label(search_frame, text="Search:", font=comic_crazy_font, bg='black', fg='white')
search_label.grid(row=0, column=0, padx=5, pady=5)


search_entry = tk.Entry(search_frame, font=comic_crazy_font, bg='black', fg='white')
search_entry.grid(row=0, column=1, padx=5, pady=5)


# Button Frame for horizontal alignment of buttons
button_frame = tk.Frame(canvas, bg='black')
button_frame.pack(pady=10)


# Search data
search_button = tk.Button(canvas, text="Search Data", command=search_data, font=comic_crazy_font, bg='black', fg='white')
search_button.pack(pady=10)

# Clear search
clear_button = tk.Button(canvas, text="Clear Search", command=clear_search, font=comic_crazy_font, bg='black', fg='white')
clear_button.pack(pady=10)

# Create and place the "About Us" button
about_button = tk.Button(button_frame, text="About Us", font=("Comic Sans MS", 14), command=open_about_us)
about_button.pack(side=tk.LEFT, padx=10, pady=10)


# Treeview for displaying data
style = ttk.Style()
style.configure("Treeview.Heading", font=comic_crazy_font, background="black", foreground="black")
style.configure("Treeview", font=comic_crazy_font, background="black", foreground="white", fieldbackground="black")

tree = ttk.Treeview(canvas, columns=("Column1", "Column2", "Column3", "Column4"), show='headings')
tree.heading("Column1", text="Rank")
tree.heading("Column2", text="Superhero")
tree.heading("Column3", text="Villain")
tree.heading("Column4", text="City")
tree.pack(pady=20)
tree.pack_forget()  # Hide the Treeview widget initially

# Bind the Treeview item click to show details
tree.bind("<Double-1>", show_superhero_details)


# Character button to fetch data
character_button = tk.Button(canvas, text="Character", command=fetch_data, font=comic_crazy_font, bg='black', fg='white')
character_button.pack(pady=10)


# Exit button
def exit_application():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

exit_button = tk.Button(canvas, text="Exit", command=exit_application, font=comic_crazy_font, bg='black', fg='white')
exit_button.pack(pady=10)


# Pack the buttons in a horizontal layout
search_button.pack(side='left', padx=10)
clear_button.pack(side='left', padx=10)
character_button.pack(side='left', padx=10)
exit_button.pack(side='left', padx=10)

# Run the application
root.mainloop()