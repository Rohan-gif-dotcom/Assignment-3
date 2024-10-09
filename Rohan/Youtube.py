import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
from functools import wraps

# Base class for UI components using encapsulation
# Encapsulation: All components (Header, Sidebar, VideoGrid, etc.) inherit from this class, encapsulating shared functionality.
class UIComponent:
    def __init__(self, master):
        self.master = master
    
    # This method will be overridden by child classes (method overriding).
    def create_widget(self):
        pass

# Decorator for logging actions
# Decorator: A function (log_action) that adds functionality to another function (e.g., search, update_grid).
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Action logged: {func.__name__} called")  # Logs the action
        return func(*args, **kwargs)
    return wrapper

# Header class using method overriding and encapsulation
class Header(UIComponent):
    # Method overriding: Overriding the create_widget method from the parent UIComponent class.
    def create_widget(self):
        # Encapsulation: Creating and managing the header component within this class.
        header = tk.Frame(self.master, bg="red", height=50)
        header.pack(fill=tk.X)
        logo = tk.Label(header, text="YouTube", fg="white", bg="red", font=("Arial", 16, "bold"))
        logo.pack(side=tk.LEFT, padx=10)

        search_frame = tk.Frame(header, bg="red")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, ipady=5)
        search_button = tk.Button(search_frame, text="Search", command=self.search)
        search_button.pack(side=tk.LEFT, padx=5)

    # Polymorphism: The search method could be overridden in another class with a different behavior.
    @log_action  # Decorator: Adding logging functionality to the search method.
    def search(self):
        query = self.search_entry.get()
        print(f"Searching for: {query}")

# Sidebar class showcasing single inheritance
class Sidebar(UIComponent):
    def create_widget(self):
        sidebar = tk.Frame(self.master, bg="gray", width=150)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        buttons = ["Home", "Trending", "Subscriptions", "Library"]
        for button in buttons:
            tk.Button(sidebar, text=button, width=15).pack(pady=5)

# Multiple inheritance example
# Multiple Inheritance: VideoGrid inherits from two classes, UIComponent and SearchableComponent, combining functionalities from both.
class SearchableComponent:
    def search_videos(self, query):
        print(f"Searching videos for query: {query}")

class VideoGrid(UIComponent, SearchableComponent):
    def create_widget(self):
        self.grid = tk.Frame(self.master)
        self.grid.pack(expand=True, fill=tk.BOTH)
        self.update_grid()

    # Method overriding: Overriding the method from the parent class to provide custom functionality for updating the video grid.
    @log_action  # Decorator: Adds logging whenever the grid updates.
    def update_grid(self):
        # Clearing previous widgets in the grid
        for widget in self.grid.winfo_children():
            widget.destroy()

        # Creating video frames
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.grid, width=200, height=150, bg="lightgray", bd=1, relief=tk.RAISED)
                frame.grid(row=i, column=j, padx=10, pady=10)
                frame.pack_propagate(False)

                thumbnail = tk.Label(frame, bg="gray", width=180, height=100)
                thumbnail.pack(pady=(5, 0))

                title = tk.Label(frame, text=f"Video {i*3+j+1}", wraplength=180)
                title.pack(pady=(5, 0))

                views = tk.Label(frame, text=f"{random.randint(100, 1000000)} views", fg="gray")
                views.pack()

# VideoPlayer class with method overriding and encapsulation
class VideoPlayer(UIComponent):
    def create_widget(self):
        player = tk.Frame(self.master, bg="black", height=400)
        player.pack(fill=tk.X, pady=10)

        # Placeholder for video
        video = tk.Label(player, bg="gray", text="Video Player", fg="white", font=("Arial", 24))
        video.pack(expand=True, fill=tk.BOTH)

        controls = tk.Frame(player, bg="lightgray", height=30)
        controls.pack(fill=tk.X)
        play_button = tk.Button(controls, text="Play")
        play_button.pack(side=tk.LEFT, padx=5)
        pause_button = tk.Button(controls, text="Pause")
        pause_button.pack(side=tk.LEFT, padx=5)

# Comments class demonstrating encapsulation and decorator usage
class Comments(UIComponent):
    def create_widget(self):
        comments = tk.Frame(self.master)
        comments.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(comments, text="Comments", font=("Arial", 16, "bold")).pack(anchor=tk.W)

        self.comment_entry = tk.Text(comments, height=3)
        self.comment_entry.pack(fill=tk.X, pady=5)

        submit_button = tk.Button(comments, text="Submit Comment", command=self.submit_comment)
        submit_button.pack(anchor=tk.W)

        self.comments_list = tk.Frame(comments)
        self.comments_list.pack(fill=tk.BOTH, expand=True, pady=10)

        # Adding some sample comments
        self.add_comment("User1", "Great video!")
        self.add_comment("User2", "Very informative, thanks for sharing!")

    @log_action  # Decorator: Adds logging when a comment is submitted.
    def submit_comment(self):
        comment = self.comment_entry.get("1.0", tk.END).strip()
        if comment:
            self.add_comment("You", comment)
            self.comment_entry.delete("1.0", tk.END)

    # Encapsulation: The add_comment method manages how comments are displayed and added.
    def add_comment(self, user, text):
        comment_frame = tk.Frame(self.comments_list, bg="lightgray", bd=1, relief=tk.SUNKEN)
        comment_frame.pack(fill=tk.X, pady=5)

        tk.Label(comment_frame, text=user, font=("Arial", 10, "bold"), bg="lightgray").pack(anchor=tk.W, padx=5, pady=(5, 0))
        tk.Label(comment_frame, text=text, wraplength=400, justify=tk.LEFT, bg="lightgray").pack(anchor=tk.W, padx=5, pady=(0, 5))

# Main App Class
# Encapsulation: The YouTubeApp class encapsulates the entire application structure and behavior.
class YouTubeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube-like Interface with OOP")
        self.geometry("800x600")

        # Instantiating components
        self.header = Header(self)
        self.sidebar = Sidebar(self)
        self.video_grid = VideoGrid(self)
        self.video_player = VideoPlayer(self)
        self.comments = Comments(self)

        self.create_ui()

    # This method organizes all the components into the UI.
    def create_ui(self):
        self.header.create_widget()
        self.sidebar.create_widget()
        self.video_grid.create_widget()
        self.video_player.create_widget()
        self.comments.create_widget()

if __name__ == "__main__":
    app = YouTubeApp()
    app.mainloop()
