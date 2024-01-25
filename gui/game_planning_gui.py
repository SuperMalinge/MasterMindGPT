
class GamePlanningGUI:
    def __init__(self, root):
        self.root = root
        #self.create_widgets(self.root)

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
        Logger.log_to_widget(f"Plan: {self.game_name_entry.get()}")        
        self.game_name_entry.delete(0, tk.END)
        plan_window.destroy()

    def save_and_close(self):
        self.save_plan()
        self.root.destroy()

    def save_plan(self):
        # Retrieve the values from the entry fields
        game_name = self.game_name_entry.get()
        game_genre = self.game_genre_entry.get()
        game_type = self.game_type_entry.get()
        game_story = self.game_story_text.get("1.0", tk.END)

        # This could be writing to a file, updating a database, etc.
        # For now, let's just print the values
        print("Game Name:", game_name)
        print("Game Genre:", game_genre)
        print("Game Type:", game_type)
        print("Game Story:", game_story)
                        
