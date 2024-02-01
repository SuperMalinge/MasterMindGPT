import tkinter as tk
from data.job import Job  
import tkinter.messagebox as messagebox

class JobManagementSystem:
    #This is the JMS class that handles the job management system in the job_management_system.py file
    #The JMS is responsible for managing the jobs     
    def __init__(self, root, Job_listbox, task_board_gui, chat_output, task_queue):
        self.root = root
        self.Job_listbox = Job_listbox
        self.Jobs = []
        self.selected_Job = None        
        self.selected_subjob = None
        self.selected_question = None
        self.selected_ask_question = None
        self.selected_suggestion_1 = None
        self.selected_suggestion_2 = None
        self.selected_own_suggestion = None
        self.selected_scratch_question = None
        self.selected_task = None
        self.selected_task_description = None        
        self.selected_subtask = None
        self.selected_current_workflow = None
        self.selected_question_count = None
        self.task_board_gui = task_board_gui
        self.selected_team = tk.StringVar()
        self.job_description_entry = tk.Entry()
        self.selected_status = tk.StringVar()
        self.subjob_entry = tk.Entry()
        from gui.task_board_gui import Logger
        self.logger = Logger(chat_output)  
        self.agent_add_job("1 Planner", "test", "not solved", "None")
        self.task_queue = task_queue
          
    def update_Job_count(self):
        # Retrieve the current number of jobs
        Job_count = len(self.Jobs)
        # Update the Job_count attribute of task_board_gui if needed
        # Assuming task_board_gui is the correct place where this attribute is used
        if hasattr(self.task_board_gui, 'Job_count'):
            self.task_board_gui.Job_count = Job_count
        # Update the Job_count_label widget text if it exists
        if hasattr(self.task_board_gui, 'Job_count_label'):
            self.task_board_gui.Job_count_label.config(text=f"Job Count: {Job_count}")
        # Assume add_Job_button is a button widget in the task_board_gui to add a Job
        # The text will now always show the number of jobs including zero (e.g., "Add Job (0)")
        self.task_board_gui.add_Job_button.config(text=f"Add Job ({Job_count})")     

    # deletes a job from the job listbox in task board gui when it is selected
    def delete_Job(self):
        try:
            index = self.Job_listbox.curselection()[0]
            self.Job_listbox.delete(index)
            del self.Jobs[index]
            self.update_job_list()
        except IndexError:
            messagebox.showerror("Error", "Please select a Job")
            
    # adds a question to the question listbox in task board gui when something is not clear        
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

    # adds a new job to the job listbox in task board gui
    def add_job(self, job_window):
        try:
            team = self.selected_team.get()
            if not team:
                messagebox.showerror("Error", "Please enter a value for the team")
                return

            job_description = self.job_description_entry.get()
            status = self.selected_status.get()
            subjob = self.subjob_entry.get()
            new_job = Job(team, job_description, status, subjob)
            self.Jobs.append(new_job)
            self.Job_listbox.delete(0, tk.END)
            self.update_job_list()        
            team = self.selected_team.get()
            job_description = self.job_description_entry.get()
            status = self.selected_status.get()
            subjob = self.subjob_entry.get()        
            self.logger.log_to_widget("A new Job has been added: " + str(new_job) + "\n")
            job_window.destroy()                  
        except Exception as e:
            # Log exception or show an error message
            self.logger.log_to_widget("Error adding job: " + str(e))
            messagebox.showerror("Error", "Failed to add job: " + str(e))   

    # Change the add_job method to accept a Job object directly
    def add_job_simple(self, new_job):        
        if not new_job.team:
            self.logger.log_to_widget("Error: Please provide a team for the job.")
            return

        # Appends the new job to the internal list of Jobs
        self.Jobs.append(new_job)
        # Inserts the new job into the GUI listbox, after clearing it
        self.update_job_list()
        # Log that the new job was added
        self.logger.log_to_widget("A new Job has been added: " + str(new_job) + "\n")
        # Optionally, call any additional methods to handle a new job addition like updating counters, etc.

    def agent_add_job(self, team, job_description, status, subjob):
        # Create the Job object
        new_job = Job(team, job_description, status, subjob)
        # Add Job to the internal list; this operation doesn't interact with GUI, so no queue is needed
        self.Jobs.append(new_job)
        # Queue the GUI operation to add the job to the listbox in the main thread        
        self.add_job_to_listbox(new_job)
        #here is an example of how to add a job to the job management system
        #self.job_management_system.agent_add_job("1 Planner", "Plan the game", "not solved", "None")

    def add_job_to_listbox(self, job):
        if isinstance(job, Job):  # In case job is a Job object            
            job_str = f"Team: {job.team}, Description: {job.description}, Status: {job.status}, Subjob: {job.subjob}"
        else:  # In case job is passed as a string or other format handle here
            job_str = str(job)
        # update the Job_listbox with the new job
        self.Job_listbox.insert(tk.END, job_str)
        # assuming logging to the widget is a thread-safe operation here, adapt if necessary:
        self.logger.log_to_widget("A new Job has been added: " + job_str + "\n")

    # updates the job listbox in task board gui
    def update_job_list(self):
        self.Job_listbox.delete(0, tk.END)
        for job in self.Jobs:   
            job_dict = dict(job)         
            job_details = f"Team: {job_dict['team']}, Job: {job_dict['description']}, Status: {job_dict['status']}"           
            if job.subjob:
                job_details += f", SubJob: {job_dict['subjob']}"
            self.Job_listbox.insert(tk.END, job_details)
            self.update_Job_count()            
            print("Job list updated")
            
class Job:
    def __init__(self, team, description, status, subjob=None):
        self.team = team
        self.description = description
        self.status = status
        self.subjob = subjob

    def __iter__(self):
        # Correctly yield key-value pairs
        yield ('team', self.team)
        yield ('description', self.description)
        yield ('status', self.status)
        if self.subjob is not None:
            yield ('subjob', self.subjob)