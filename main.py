import tkinter as tk
from tkinter import messagebox
from anytree import Node, RenderTree
from tkinter.ttk import Treeview
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import autogen
import json
from dataclasses import dataclass, field
from typing import Optional


import threading
# "model": "mistral-instruct-7b",

from openai import OpenAI
client = OpenAI(base_url="http://localhost:5001/v1", api_key="not-needed")

llm_config = [
    {
        "model": "mistralai_mistral-7b-instruct-v0.2",
        "api_base": "http://127.0.0.1:5001/v1",
        "api_type": "open_ai",
        "api_key": "sk-111111111111111111111111111111111111111111111111",
    }
]


# Write the configuration to a JSON file
try:
    with open('config.json', 'w') as f:
        json.dump(llm_config, f)
except IOError as e:
    print(f"Error writing config to config.json: {e}")
    exit(1)

# Try loading the configuration with expected filters
try:
    config_list = autogen.config_list_from_json(
        env_or_file='config.json',
        file_location=".",
        filter_dict={
            "model": "mistralai_mistral-7b-instruct-v0.2",
            "api_base": "http://127.0.0.1:5001/v1",
        },
    )
    if not config_list:
        raise ValueError("No matching configurations found.")
except (IOError, ValueError) as e:
    print(f"An error occurred: {e}")
    # Handle no configuration found (Stop the program or allow for retry, etc.)
    exit(1)

print("Models to use: ", [config["model"] for config in config_list])

#use constants for fixed strings
question = "question"
ask_question = "ask question"
suggestion1 = "suggestion 1"
suggestion2 = "suggestion 2"
own_suggestion = "own suggestion"
scratch_question = "scratch question"
task = "task"
status = "status"
subtask = "subtask"
task_description = "task description"
team = "team"
plan = "plan"
structure = "structure"
current_workflow = "current workflow"
question_count = "question count"
Chat_output = "Chat output"

class TaskBoardGUI:
    def __init__(self, root, game, chat_input, company, master, llm_config):
        self.root = root
        self.root.title("MasterMindGPT Job Board")
        self.Job = []
        self.Jobs = []     
        self.chat_output = []           
        self.llm_config = llm_config  # This assumes llm_config is passed in during instantiation               
        self.logger = Logger(self.chat_output)

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
                

        # Button to add Job
        # Display the Job list 
        self.Job_listbox = tk.Listbox(root, width=80)  # Adjust the width here
        self.Job_listbox.pack()
        self.Job_listbox.place(x=450, y=30)

        #initialize the classes
        self.job_management_system = JobManagementSystem(root,self.Job_listbox, self)
        self.workflow_manager = WorkflowManager(llm_config, self.chat_output, self.job_management_system, self.ceo_boss)
        self.agent_actions = Agent_actions(team, task)
        self.GamePlanningGUI = GamePlanningGUI(root)
        self.ceo_boss = CEO()
        
        self.add_Job_button = tk.Button(root, text="Add Job", command=self.job_management_system.open_Job_window)
        self.add_Job_button.pack()
        self.add_Job_button.place(x=450, y=0)

        # Button to delete Job
        self.delete_Job_button = tk.Button(root, text="Delete Job", command=self.job_management_system.delete_Job)
        self.delete_Job_button.pack()
        self.delete_Job_button.place(x=510, y=0)

        # Button to add questions
        self.add_question_button = tk.Button(root, text="Add Question", command=self.add_question_wrapper)       
        
        self.add_question_button.pack()
        self.add_question_button.place(x=580, y=0)

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

        self.get_questions_button = tk.Button(root, text="Get Questions", command=self.job_management_system.open_question_window)
        self.get_questions_button.pack()
        self.get_questions_button.place(x=930, y=0)

        # button to train the agents in the teams
        self.train_button = tk.Button(root, text="Train Agents", command=self.open_train_agents_window)
        self.train_button.pack()
        self.train_button.place(x=1020, y=0)

        # Display the chat output
        self.chat_output = tk.Text(root, height=20, width=40)  # Text widget for chat output
        self.chat_output.pack(side=tk.LEFT)    
        self.chat_output.place(x=100, y=0)    

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
        self.agent_listbox_label.place(x=450, y=215)
        
        self.agent_listbox = tk.Listbox(root, width=40, height=10)
        self.agent_listbox.pack()
        self.agent_listbox.place(x=450, y=200)

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
            if 'questions' in task['Job'].lower():
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
        self.tree = Treeview(parent)
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
            current_node = Node(node_value, parent=parent)
            if children:
                self.build_tree_from_instructions(children, parent=current_node)

    def visualize_tree(self):
        # Visualizing the tree using RenderTree
        for pre, fill, node in RenderTree(self.root):
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
            workflow_manager = WorkflowManager(llm_config, self.chat_output, self.job_management_system, self.ceo_boss)           
            threading.Thread(target=workflow_manager.initiate_workflow, args=(chat_input,)).start()
        else:
            tk.messagebox.showerror("Error", "Please enter a Job to initiate the workflow")

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
                

class Logger:
    def __init__(self, chat_output):
        self.chat_output = chat_output

    def log_to_widget(self, message):        
        self.chat_output.insert(tk.END, f"{message}\n")

class WorkflowManager:
    def __init__(self, llm_config, chat_output, job_management_system, ceo_boss):
        self.llm_config = llm_config
        self.chat_output = chat_output        
        self.job_management_system = job_management_system
        self.ceo_boss = ceo_boss                
        self.initialize_rag_agents(ceo_boss)

    def initiate_workflow(self, chat_input):
        # Create an instance of Logger        
        logger = Logger(self.chat_output)
        processed_input = self.preprocess_chat_input(chat_input)
        self.retrieve_assistant_agent_planner.reset()
        logger.log_to_widget(f"Initiated workflow with input: {processed_input}")
        self.retrieve_user_proxy_agent.initiate_chat(self.retrieve_assistant_agent_planner, problem=processed_input)    
        job = {
            "Team": "1 Planner",
            "Job": processed_input,
            "Status": "unsolved",
            "SubJob": None
        }
        self.ceo_boss.delegate_task(job)
        self.job_management_system.Jobs.append(job)
        self.job_management_system.update_Job_list()
        logger.log_to_widget(f"Delegated to Planner: {processed_input}")

    def process_chat_input(self, chat_input):
        processed_input = self.preprocess_chat_input(chat_input)
        job = {
            "Team": "1 Planner",
            "Job": processed_input,
            "Status": "unsolved",
            "SubJob": None
        }
        self.ceo_boss.delegate_task(job)
        self.Jobs.append(job)
        self.update_Job_list()
        Logger.log_to_widget(f"Delegated to Planner: {processed_input}")

    def preprocess_chat_input(self, chat_input):
        return chat_input

    def initialize_rag_agents(self, ceo_boss):
        print("Initializing RAG agents with llm_config:", self.llm_config)
        docs_directory = r"D:\Pythonprojects\Projects\MasterMindGITHUBAUTOGEN\docs"
        self.ceo_boss = CEO()
        try:
            self.retrieve_assistant_agent_planner = RetrieveAssistantAgent(
                name="Planner Agent",
                system_message="You are a helpful assistant.",
                llm_config=self.llm_config,
            )
            print("Planner Agent (RetrieveAssistantAgent) initialized successfully.")
            # Immediately add the agent to the CEO's list
            self.ceo_boss.add_agent(self.retrieve_assistant_agent_planner)
            self.retrieve_assistant_agent_orchestra = RetrieveAssistantAgent(
                name="Orchestra Agent",
                system_message="You orchestrate the workflow.",
                llm_config=self.llm_config,
            )
            print("Orchestra Agent (RetrieveAssistantAgent) initialized successfully.")
            # Immediately add the agent to the CEO's list
            self.ceo_boss.add_agent(self.retrieve_assistant_agent_orchestra)            
            self.retrieve_user_proxy_agent = RetrieveUserProxyAgent(
                name="CEO Proxy Agent",
                retrieve_config={
                    "task": "qa",
                    "docs_path": docs_directory,
                },
            )
            print("CEO Proxy Agent (RetrieveUserProxyAgent) initialized successfully.")
            # Immediately add the agent to the CEO's list            
        except Exception as e:
            print("Error during RAG agents initialization:", e)
            raise

    def start_chat_flow(self, chat_input):
        # Reset the agents at the beginning of a chat flow
        self.retrieve_assistant_agent_planner.reset()        
        self.retrieve_user_proxy_agent.initiate_chat(self.retrieve_assistant_agent_planner, problem=chat_input)
        Logger.log_to_widget(f"Initiated chat with input: {chat_input}")
        try:
            messages = self.retrieve_user_proxy_agent.chat_messages
            for message in messages:
                Logger.log_to_widget(message['content'])
        except Exception as e:
            Logger.log_to_widget(str(e))


class Agent_actions:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.tasks = []

    def handle_task(self, task):
        self.tasks.append(task)
        Logger.log_to_widget(f"{self.name}: received task -> {task}")
        print(f"{self.name}: received task -> {task}")

    def report_status(self):
        # This could return a summary of tasks, their status or any other relevant information
        return {
            "total_tasks": len(self.tasks),
            "current_tasks": [task['Job'] for task in self.tasks]
        }

class CEO:
    def __init__(self):
        self.agents = {}

    def initiate_workflow(self, message):
        # Assuming the message is the cue to start working on tasks
        # CEO checks the tasks assigned to the Planner agent
        if message == "start the workflow":
            planner_tasks = [task for task in self.Jobs if task['Team'] == '1 Planner']
            # Pass the relevant tasks to the Planner agent
            for task in planner_tasks:
                self.delegate_task(task)

    def add_agent(self, agent):
        self.agents[agent.name] = agent

    def delegate_task(self, task):        
        #first lets check if there are any agents available
        if len(self.agents) == 0:
            print("No agents available")
            return
        
        #second lets check if there are any tasks in the queue
        if len(self.Jobs) == 0:
            print("No tasks in the queue")
            return
    
        # Find the right agent to delegate the task
        # Here we'd use a method to process the task if needed.
        # As an example, we're assuming the task goes directly to the Planner
        agent = self.agents.get("1 Planner")
        if agent:
            agent.handle_task(task)
            self.report_task_delegation(task)  # Log the job delegation
        else:
            print(f"No matching agent found for team {task['Team']}.")

    def report_task_delegation(self, task):
        # Report task delegation to the GUI.
        # This needs proper handling to show on GUI
        print(f"Delegated task '{task['Job']}' to {task['Team']}")

    def report_tasks_status(self):
        status_report = {}
        for agent_name, agent in self.agents.items():
            status_report[agent_name] = agent.report_status()
        return status_report


@dataclass
class Job:
    team: str
    description: str
    status: str = 'not solved'
    subjob: Optional[str] = None
    question: Optional[str] = None
    ask_question: Optional[str] = None
    suggestion1: Optional[str] = None
    suggestion2: Optional[str] = None
    own_suggestion: Optional[str] = None
    scratch_question: Optional[str] = None

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

    def update_job_list(self):
        self.Job_listbox.delete(0, tk.END)
        for job in self.Jobs:
            job_details = f"Team: {job.team}, Job: {job.description}, Status: {job.status}"
            if job.subjob:
                job_details += f", SubJob: {job.subjob}"
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
            self.task_board_gui.chat_output.insert(tk.END, "A new Job has been added: " + str(new_job) + "\n")
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

if __name__ == "__main__":
    root = tk.Tk()
    game = []
    chat_input = []
    company = "MasterMindGPT Game Maker"
    master = []

    # Instantiate TaskBoardGUI first
    task_board_gui = TaskBoardGUI(root, game, chat_input, company, master, llm_config)

    # Then, pass the properly initialized Job_listbox from task_board_gui to JobManagementSystem
    job_management_system = JobManagementSystem(root, task_board_gui.Job_listbox, task_board_gui)

    # Finally, pass the properly initialized job_management_system to TaskBoardGUI
    task_board_gui.job_management_system = job_management_system

    # Instantiate GamePlanningGUI
    game_planning_gui = GamePlanningGUI(root)
    
    # Mock configuration, replace with actual configuration
    mock_llm_config = {
        "model": "mistralai_mistral-7b-instruct-v0.2",
        "api_base": "http://127.0.0.1:5001/v1",
        "api_type": "open_ai",
        "api_key": "sk-111111111111111111111111111111111111111111111111",
    }

    print("Loaded model configurations:", llm_config)
    for config in llm_config:
        if config.get("model") == "gpt-4":
            print("Error: 'gpt-4' found instead of 'mistralai_mistral-7b-instruct-v0.2'.")

    
    root.mainloop()
