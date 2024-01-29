import tkinter as tk
from data.job import Job  
from models.logger import Logger

class JobManagementSystem:
    def __init__(self, root, Job_listbox, task_board_gui):
        self.root = root
        self.Job_listbox = Job_listbox
        self.Jobs = []
        self.selected_Job = None
        self.selected_team = None
        self.selected_status = None
        self.selected_subjob = None
        self.selected_question = None
        self.selected_ask_question = None
        self.selected_suggestion_1 = None
        self.selected_suggestion_2 = None
        self.selected_own_suggestion = None
        self.selected_scratch_question = None
        self.selected_task = None
        self.selected_task_description = None
        self.selected_status = None
        self.selected_subtask = None
        self.selected_current_workflow = None
        self.selected_question_count = None
        self.task_board_gui = task_board_gui
        self.logger = Logger(chat_output=None)

    def update_job_list(self):
        self.Job_listbox.delete(0, tk.END)
        for job in self.Jobs:            
            job_details = f"Team: {job['team']}, Job: {job['description']}, Status: {job['status']}"            
            if job.subjob:
                job_details += f", SubJob: {job['subjob']}"
            self.Job_listbox.insert(tk.END, job_details)
        
    def update_Job_count(self):
        Job_count = len(self.Jobs)
        self.add_Job_button.config(text=f"Add Job ({Job_count})")

    def delete_Job(self):
        try:
            index = self.Job_listbox.curselection()[0]
            self.Job_listbox.delete(index)
            del self.Jobs[index]
            self.update_Job_list()
        except IndexError:
            tk.messagebox.showerror("Error", "Please select a Job")

    def add_question(self, question_window):

        question_label = tk.Label(question_window, text="Question:")
        question_label.pack()
        self.question_entry = tk.Entry(question_window)
        self.question_entry.pack()

        ask_question_label = tk.Label(question_window, text="Ask Question:")
        ask_question_label.pack()
        self.ask_question_entry = tk.Entry(question_window)
        self.ask_question_entry.pack()

        suggestion_1_label = tk.Label(question_window, text="Suggestion 1:")
        suggestion_1_label.pack()
        self.suggestion_1_entry = tk.Entry(question_window)
        self.suggestion_1_entry.pack()

        suggestion_2_label = tk.Label(question_window, text="Suggestion 2:")
        suggestion_2_label.pack()
        self.suggestion_2_entry = tk.Entry(question_window)
        self.suggestion_2_entry.pack()

        own_suggestion_label = tk.Label(question_window, text="Own Suggestion:")
        own_suggestion_label.pack()
        self.own_suggestion_entry = tk.Entry(question_window)
        self.own_suggestion_entry.pack()

        scratch_question_label = tk.Label(question_window, text="Scratch Question:")
        scratch_question_label.pack()
        self.scratch_question_entry = tk.Entry(question_window)
        self.scratch_question_entry.pack()

        add_question_button = tk.Button(question_window, text="Add Question", command=lambda: self.add_question(question_window))
        add_question_button.pack()
    
    def open_Job_window(self):
        job_window = tk.Toplevel(self.root)
        team_label = tk.Label(job_window, text="Team:")
        team_label.pack()

        # Dropdown menu for selecting level
        teams = ["1 Planner", "2 Orchestra", "2-1 Plan Build", "2-2 Structure Build", "2-3 Engine Choose or Build",
                 "2-4 Art and Prompt Build", "2-5 Quality Assist Orchestra", "3 Task Maker Logic", "3-1 GUI Logic",
                 "3-2 Backend Logic", "3-3 Engine Logic", "3-4 Preview Art", "3-5 Quality Assist Logic",
                 "4 Task Manager Code", "4-1 GUI Code", "4-2 Backend Code", "4-3 Engine Code", "4-4 Art Refiner",
                 "4-5 Quality Assist Code", "5 Reviewer", "5-1 GUI Review", "5-2 Backend Review", "5-3 Engine Review",
                 "5-4 Art implementation", "5-5 Quality Assist Reviewer", "6 Debug and Error", "6-1 GUI Debug",
                 "6-2 Backend Debug", "6-3 Engine Debug", "6-4 Art Debug", "6-5 Quality Assist Debug", "7 Finalizer",
                 "7-1 Documentation", "7-2 Manual and Requirements"]

        selected_team = tk.StringVar(job_window)
        selected_team.set(teams[0])  # Default value
        self.selected_team = selected_team  
        team_entry = tk.OptionMenu(job_window, selected_team, *teams)
        team_entry.pack()

        job_description_label = tk.Label(job_window, text="Job Description:")
        job_description_label.pack()
        self.job_description_entry = tk.Entry(job_window)
        self.job_description_entry.pack()

        subjob_label = tk.Label(job_window, text="SubJob:")
        subjob_label.pack()
        self.subjob_entry = tk.Entry(job_window)
        self.subjob_entry.pack()        

        status_label = tk.Label(job_window, text="Status:")
        status_label.pack()

        # Dropdown menu for selecting status
        status_options = ["solved", "not solved"]
        self.selected_status = tk.StringVar(job_window)
        self.selected_status.set(status_options[0])  # Default value
        status_entry = tk.OptionMenu(job_window, self.selected_status, *status_options)
        status_entry.pack()

        # Button to add tasks in the second window
        add_task_button = tk.Button(job_window, text="Add Job", command=lambda: self.add_job(job_window))
        add_task_button.pack()

    def add_job(self, job_window):
        team = self.selected_team.get()
        job_description = self.job_description_entry.get()
        status = self.selected_status.get()
        subjob = self.subjob_entry.get()

        if team and job_description:
            new_job = Job(team=team, description=job_description, status=status, subjob=subjob)
            self.Jobs.append(new_job)
            self.update_job_list()            
            self.logger.log_to_widget("A new Job has been added: " + str(new_job) + "\n")
            job_window.destroy()
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields")

    def open_question_window(self):
        question_window = tk.Toplevel(self.root)
        question_window.title("Questions")
        question_window.geometry("500x700")
        question_label = tk.Label(question_window, text="Questions:")
        question_label.pack()
        question_entry = tk.Entry(question_window)
        question_entry.pack()
        question_button = tk.Button(question_window, text="Get Questions", command=lambda: self.get_questions_output(question_window))
        question_button.pack()
