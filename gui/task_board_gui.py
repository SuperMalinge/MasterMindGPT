import tkinter as tk, tkinter.ttk as ttk
import threading
from data.job_management_system import JobManagementSystem
from models.workflow_manager import WorkflowManager
from models.ceo import CEO
from models.agent_actions import Agent_actions
from gui.game_planning_gui import GamePlanningGUI
from queue import Queue, Empty
import tkinter.messagebox as messagebox
from data.job import Job

llm_config = [
    {
        "model": "mistralai_mistral-7b-instruct-v0.2",
        "api_base": "http://127.0.0.1:5001/v1",
        "api_type": "open_ai",
        "api_key": "sk-111111111111111111111111111111111111111111111111",
    }
]

class TaskBoardGUI:
    # This class is the main GUI class for the task board in the task_board_gui.py file
    def __init__(self, root, game, chat_input, company, master, llm_config, team, task):
        self.root = root
        self.root.title("MasterMindGPT Job Board")
        self.Job = Job
        self.Jobs = []                     
        self.llm_config = llm_config  # This assumes llm_config is passed in during instantiation               

        # Create attributes for Job-related widgets
        self.retrieve_assistant_agent = None
        self.retrieve_user_proxy_agent = None
        self.ceo_boss = None
        self.agents = None                 
        self.root.geometry("1100x500")
        self.question_window = None 
        # Create attributes for question-related widgets
        self.question_entry = None
        self.ask_question_entry = None
        self.suggestion_1_entry = None
        self.suggestion_2_entry = None
        self.own_suggestion_entry = None
        self.scratch_question_entry = None   
        company = "MasterMindGPT Game Maker"    
        self.company = company  
        self.team = team
        self.task = task
        #agent_listbox = None
        self.task_queue = Queue()  # Task queue for thread communication

        # Display the chat output
        self.chat_output = tk.Text(root, height=20, width=40)  # Text widget for chat output
        self.chat_output.pack(side=tk.LEFT)    
        self.chat_output.place(x=100, y=0)   
                      
        # Display the Job list 
        self.Job_listbox = tk.Listbox(root, width=80)  # Adjust the width here
        self.Job_listbox.pack()
        self.Job_listbox.place(x=450, y=30)

        self.job_management_system = JobManagementSystem(root,self.Job_listbox, self, self.chat_output,self.task_queue)
            
        self.add_Job_button = tk.Button(root, text="Add Job", command=self.job_management_system.open_Job_window)
        self.add_Job_button.pack()
        self.add_Job_button.place(x=450, y=0)

        # Button to delete Job
        self.delete_Job_button = tk.Button(root, text="Delete Job", command=self.job_management_system.delete_Job)
        self.delete_Job_button.pack()
        self.delete_Job_button.place(x=520, y=0)

        # Button to add questions
        self.add_question_button = tk.Button(root, text="Add Question", command=self.add_question_wrapper)       
        
        self.add_question_button.pack()
        self.add_question_button.place(x=580, y=0)

        # initialize the game planning gui
        self.GamePlanningGUI = GamePlanningGUI(root, self.chat_output)  

        # Button to get Plan
        self.get_plan_button = tk.Button(root, text="Get Plan", command=self.GamePlanningGUI.open_plan_window)
        self.get_plan_button.pack()
        self.get_plan_button.place(x=665, y=0)

        # Button to get Structure
        self.get_structure_button = tk.Button(root, text="Get Structure", command=self.get_structure)
        self.get_structure_button.pack()
        self.get_structure_button.place(x=720, y=0)

        # Button to get current workflow
        self.get_current_workflow_button = tk.Button(root, text="Get Current Workflow", command=self.get_current_workflow)
        self.get_current_workflow_button.pack()
        self.get_current_workflow_button.place(x=800, y=0)

        self.get_questions_button = tk.Button(root, text="Get Questions", command=self.open_question_window)
        self.get_questions_button.pack()
        self.get_questions_button.place(x=930, y=0)

        # button to train the agents in the teams
        self.train_button = tk.Button(root, text="Train Agents", command=self.open_train_agents_window)
        self.train_button.pack()
        self.train_button.place(x=1020, y=0) 

        # Create the Logger instance
        self.logger = Logger(self.chat_output)
        self.logger.log_to_widget("Initializing...")

        #task list label placed below the Job list
        self.task_list_label = tk.Label(root, text="Job List")
        self.task_list_label.pack()
        self.task_list_label.place(x=450, y=195)        
     
        # chat input
        self.chat_input = tk.Entry(root, width=80)  # Entry widget for chat input. Prompt goes here
        self.chat_input.pack()
        self.chat_input.place(x=100, y=330, width=325)

        # Button to send chat input
        self.send_button = tk.Button(root, text="Prompt", command=self.send_chat_input)
        self.send_button.pack()
        self.send_button.place(x=100, y=350)

        # Create the Listbox widget for agents
        self.agent_listbox_label = tk.Label(root, text="Agent List") 
        self.agent_listbox_label.pack()
        self.agent_listbox_label.place(x=450, y=220)
                
        self.agent_listbox = tk.Listbox(root, width=40, height=10) # listbox for agents
        self.agent_listbox.pack()
        self.agent_listbox.place(x=450, y=200)
      
        # Initialize the classes        
        self.ceo_boss = CEO(self.agent_listbox, self.chat_output, self.task_queue,self.job_management_system)
        self.workflow_manager = WorkflowManager(llm_config, self.chat_output, self.job_management_system, self.ceo_boss, self.agent_listbox, self.task_queue)
        self.agent_actions = Agent_actions(self.task, self.team, self.chat_output)   

        # Start checking the queue
        self.check_queue() 

    def handle_add_question(self):
    # Implementation for adding a question goes here
    # For example, you might want to grab the data from the fields,
    # package it into a structure, and then add it to the selected job.
    # At the end, don't forget to close the question window after adding the question.    
    # Get the input data from the entry fields
        question = self.question_entry.get()
        ask_question = self.ask_question_entry.get()
        suggestion_1 = self.suggestion_1_entry.get()
        suggestion_2 = self.suggestion_2_entry.get()
        own_suggestion = self.own_suggestion_entry.get()
        scratch_question = self.scratch_question_entry.get()
    
    # Now package this data into a dictionary 
    # Assuming selected_Job is a job you want to add these questions to:
        if self.selected_Job:  # If a job is selected
        # For example, assume the job object has an 'add_question' method or similar
            self.selected_Job.add_question(question, ask_question, suggestion_1, suggestion_2, own_suggestion, scratch_question)
        # Log the addition
            self.logger.log_to_widget(f"Question and suggestions added to job: {self.selected_Job.description}")
        else:
            messagebox.showerror("Error", "No job selected to add this question to!")        
        self.question_window.destroy()

    def get_current_workflow(self):
        # If tasks is supposed to come from somewhere else in your class, update this method to use that.
        if hasattr(self, 'tasks'):
            self.chat_output.insert(tk.END, f"Current Workflow: {self.tasks}")
        else:
            print("The 'tasks' attribute is not defined.")
            # Handle the situation appropriately, maybe by setting self.tasks = [] or providing an error message.

    def add_question_wrapper(self):
        # You should determine how to properly create or get a reference to a question_window       
        question_window = self.create_or_get_question_window()
        self.job_management_system.add_question(question_window)

    def create_or_get_question_window(self):
        # Create a new Toplevel window or return an existing reference        
        return tk.Toplevel(self.root)
                                     
    def open_train_agents_window(self):
        train_agents_window = tk.Toplevel(self.root)
        self.train_agents_label = tk.Label(train_agents_window, text="Train Agents: ")
        self.train_agents_label.pack()
        self.train_agents_entry = tk.Entry(train_agents_window)
        self.train_agents_entry.pack()
        self.train_agents_button = tk.Button(train_agents_window, text="Train Agents", command=lambda: self.train_agents(train_agents_window))
        self.train_agents_button.pack()

    def train_agents(self, train_agents_window):
        self.chat_output.insert(tk.END, f"Train Agents: {self.train_agents_entry.get()}\n")
        self.train_agents_entry.delete(0, tk.END)
        train_agents_window.destroy()
      
    def get_questions(self):
        question_count = sum('questions' in Job['Job'].lower() for Job in self.Jobs)
        self.get_questions_button.config(text=f"Get Questions ({question_count})")
        for Job in self.Job:
            if 'questions' in self.task['Job'].lower():
                self.chat_output.insert(tk.END, f"Question: {Job['Job']}, Ask Question: {Job['Ask Question']}, Suggestion 1: {Job['Suggestion 1']}, Suggestion 2: {Job['Suggestion 2']}, Own Suggestion: {Job['Own Suggestion']}, Scratch Question: {Job['Scratch Question']}")

    def get_current_workflow(self):
        self.chat_output.insert(tk.END, f"Current Workflow: {self.tasks}")
        #the current workflow will be gathered from all teams and then shown in the window
        pass

    def get_structure(self):
        plan_window = tk.Toplevel(self.root)
        plan_window.title("Structure")
        plan_window.geometry("500x700")
        self.structure_label = tk.Label(plan_window, text="Structure: ")
        self.structure_label.pack()

        # Create the treeview
        self.create_treeview(plan_window)

        # Create the "Get Structure" button
        self.structure_button = tk.Button(plan_window, text="Get Structure", command=lambda: self.get_structure_output(plan_window))
        self.structure_button.pack()

    def create_treeview(self, parent):
        # Create the treeview
        self.tree = ttk.Treeview(parent)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the treeview scrollbar
        self.tree_scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the treeview
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree.heading("#0", text="Directory Structure", anchor="w")

        # Add the files to the treeview
        file_list = ["main.py"]
        for file in file_list:
            self.tree.insert("", tk.END, text=file)

        # Expand and collapse bindings
        self.tree.bind("<Double-1>", lambda event: self.tree.item(self.tree.focus(), open=True))
        self.tree.bind("<Double-3>", lambda event: self.tree.item(self.tree.focus(), open=False))

        # Create the treeview frame
        self.tree_frame = tk.Frame(parent)
        self.tree_frame.pack(pady=10)

    def build_tree_from_instructions(self, instructions, parent=None):
        for instruction in instructions:
            node_value, children = instruction[0], instruction[1:]
            current_node = ttk.Node(node_value, parent=parent)
            if children:
                self.build_tree_from_instructions(children, parent=current_node)

    def visualize_tree(self):
        # Visualizing the tree using RenderTree
        for pre, fill, node in ttk.RenderTree(self.root):
            print("%s%s" % (pre, node.name))

    def refresh_agents_status(self):
        # This method will fetch status from CEO and update the GUI
        task_statuses = self.ceo_boss.report_tasks_status()
        # (Here you'll write code to update some part of your GUI with the statuses)
        # (For example, you can update the Job listbox with the status of each Job)
        # (You can also update the agent listbox with the status of each agent)
        # (You can also update the chat output with the status of each agent)
        # (You can also update the plan output with the status of each agent)
        # (You can also update the structure output with the status of each agent)
        # (You can also update the current workflow output with the status of each agent)
        # (You can also update the question output with the status of each agent)
        # (You can also update the question count output with the status of each agent)
         
    def send_chat_input(self):
        chat_input = self.chat_input.get()
        if chat_input:
            threading.Thread(target=self.workflow_manager.initiate_workflow, args=(chat_input,)).start()
        else:
            messagebox.showerror("Error", "Please enter a job to initiate the workflow")

    def check_queue(self):
        try:
            #count all jobs in the queue
            #job_count = sum('Job' in Job['Job'].lower() for Job in self.Jobs)
            #print("there are currently", job_count, "jobs in the queue")
            job_to_add = self.task_queue.get(block=False)  # Get a job from the queue
        
            # Assuming job_to_add is of Job type or a tuple, replace with appropriate validation
            valid_job = False
            if isinstance(job_to_add, Job):  # If job_to_add is a Job object
                valid_job = True
            elif isinstance(job_to_add, tuple) and len(job_to_add) == 4:
                valid_job = all(isinstance(field, str) for field in job_to_add)  # Validate job as a tuple of strings

            if valid_job:
                # Here, insert job_to_add if it's valid.
                # You may need to format job_to_add appropriately if it's not already formatted for display
                # For a Job object, this might involve calling a method or accessing attributes to get display string
                if isinstance(job_to_add, Job):
                    display_str = f"{job_to_add.team}, {job_to_add.description}, {job_to_add.status}, {job_to_add.subjob}"
                else:  # If job_to_add is a tuple
                    display_str = ", ".join(job_to_add)
            
                self.Job_listbox.insert(tk.END, display_str)

        except Empty:  # Queue is empty, no action taken
            pass
        finally:
            # This call should also likely be in a try-except block
            try:
                self.ceo_boss.process_queue()  # Process queues if the ceo_boss has any queued actions
            except Exception as e:
                # Log this exception or show an error message
                self.logger.log_to_widget("Error processing the boss's queue: " + str(e))

        self.root.after(1000, self.check_queue)  # Schedule to check the queue again

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

class Logger:
    def __init__(self, chat_output):
        self.chat_output = chat_output

    def log_to_widget(self, message):
        if isinstance(self.chat_output, tk.Text):
            self.chat_output.insert(tk.END, message + "\n")  # Appends a newline after each message
        else:
            raise TypeError("chat_output is not a tk.Text widget")

