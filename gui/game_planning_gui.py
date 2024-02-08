import tkinter as tk

class GamePlanningGUI:
    # This class is responsible for the Game Planning GUI in game_planning_gui.py
    # The agent will use this GUI to plan the game they are going to create
    # The agent will enter the game name, genre, type, and story
    def __init__(self, root, chat_output):
        self.root = root   
        from gui.task_board_gui import Logger
        self.logger = Logger(chat_output)       
        
    def create_widgets(self, window):
        # Game Name
        game_name_label = tk.Label(window, text="Game Name:")
        game_name_label.pack()
        self.game_name_entry = tk.Entry(window)
        self.game_name_entry.pack()

        # Game Genre
        game_genre_label = tk.Label(window, text="Game Genre:")
        game_genre_label.pack()
        self.game_genre_entry = tk.Entry(window)
        self.game_genre_entry.pack()

        # Game Type
        game_type_label = tk.Label(window, text="Game Type:")
        game_type_label.pack()
        self.game_type_entry = tk.Entry(window)
        self.game_type_entry.pack()

        # Game Story
        game_story_label = tk.Label(window, text="Game Story:")
        game_story_label.pack()
        self.game_story_text = tk.Text(window, height=10, width=30)
        self.game_story_text.pack()

        # Save and Close button
        save_close_button = tk.Button(window, text="Save and Close", command=self.save_and_close)
        save_close_button.pack()

    def open_plan_window(self):
        plan_window = tk.Toplevel(self.root)        
        plan_window.title("Plan")          
        plan_window.geometry("500x700")  
        self.create_widgets(plan_window)

    def get_plan_output(self, plan_window):               
        self.logger.log_to_widget(f"Plan: {self.game_name_entry.get()}")        
        self.game_name_entry.delete(0, tk.END)
        plan_window.destroy()

    def save_and_close(self):
        # Save the plan
        self.save_plan()

        # Close the window
        self.root.destroy()

    def save_plan(self):
        # Retrieve the values from the entry fields
        game_name = self.game_name_entry.get()
        game_genre = self.game_genre_entry.get()
        game_type = self.game_type_entry.get()
        game_story = self.game_story_text.get("1.0", tk.END)

        # Save the values
        # This could be writing to a file, updating a database, etc.
        # For now, let's just print the values
        print("Game Name:", game_name)
        print("Game Genre:", game_genre)
        print("Game Type:", game_type)
        print("Game Story:", game_story)
                        
