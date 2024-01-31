import tkinter as tk, tkinter.ttk as ttk
import threading
from data.job_management_system import JobManagementSystem
from models.workflow_manager import WorkflowManager
from models.ceo import CEO
from models.agent_actions import Agent_actions
from gui.game_planning_gui import GamePlanningGUI
from queue import Queue, Empty
import tkinter.messagebox as messagebox

llm_config = [
    {
        "model": "mistralai_mistral-7b-instruct-v0.2",
        "api_base": "http://127.0.0.1:5001/v1",
        "api_type": "open_ai",
        "api_key": "sk-111111111111111111111111111111111111111111111111",
    }
]

class TaskBoardGUI:
    def __init__(self, root, game, chat_input, company, master, llm_config, team, task):
        self.root = root
        self.root.title("MasterMindGPT Job Board")
        self.Job = []
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
        self.ceo_boss = CEO(self.agent_listbox, self.chat_output, self.task_queue)
        self.workflow_manager = WorkflowManager(llm_config, self.chat_output, self.job_management_system, self.ceo_boss, self.agent_listbox, self.task_queue)
        self.agent_actions = Agent_actions(self.task, self.team, self.chat_output)   

        # Start checking the queue
        self.check_queue()                         

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
            tk.messagebox.showerror("Error", "Please enter a job to initiate the workflow")

    def check_queue(self):
        try:
            job_result = self.task_queue.get(block=False)
            # Here, handle your retrieved job result. For example:
            self.Job_listbox.insert(tk.END, job_result)
        except Empty:            
            pass
        finally:
            self.ceo_boss.process_queue()  # Added call to process the queue
            self.root.after(100, self.check_queue)  # Schedule to check again

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

