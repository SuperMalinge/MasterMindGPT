import tkinter as tk
from anytree import Node, RenderTree
from tkinter.ttk import Treeview
from crewai import Crew

import threading

from companyagents import CompanyAgents
from planning_tasks import PlanningTasks

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
    def __init__(self, root, game, chat_input, company, master):
        self.root = root
        self.root.title("MasterMindGPT Job Board")
        self.Job = []
        self.Jobs = []

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
        self.add_Job_button = tk.Button(root, text="Add Job", command=self.open_Job_window)
        self.add_Job_button.pack()
        self.add_Job_button.place(x=450, y=0)

        # Button to delete Job
        self.delete_Job_button = tk.Button(root, text="Delete Job", command=self.delete_Job)
        self.delete_Job_button.pack()
        self.delete_Job_button.place(x=510, y=0)

        # Button to add questions        
        self.add_question_button = tk.Button(root, text="Add Question", command=self.open_question_window)
        self.add_question_button.pack()
        self.add_question_button.place(x=580, y=0)

        # Button to get Plan
        self.get_plan_button = tk.Button(root, text="Get Plan", command=self.get_plan)
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

        # Display the chat output
        self.chat_output = tk.Text(root, height=20, width=40)  # Text widget for chat output
        self.chat_output.pack(side=tk.LEFT)    
        self.chat_output.place(x=100, y=0)    

        # Display the Job list 
        self.Job_listbox = tk.Listbox(root, width=80)  # Adjust the width here
        self.Job_listbox.pack()
        self.Job_listbox.place(x=450, y=30)
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

        # Get the list of agents
        self.agents = CompanyAgents().get_agents()

        # Create the Listbox widget for agents
        self.agent_listbox_label = tk.Label(root, text="Agent List")
        self.agent_listbox_label.pack()
        self.agent_listbox_label.place(x=450, y=215)
        
        self.agent_listbox = tk.Listbox(root, width=40, height=10)
        self.agent_listbox.pack()
        self.agent_listbox.place(x=450, y=200)

        # Populate the agent listbox
    def populate_agent_listbox(self):
        for agent in self.agents:
            self.agent_listbox.insert(tk.END, agent)        

    def log_to_widget(self, message):
        self.chat_output.insert(tk.END, f"{message}\n")       
                                   
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

    def get_plan(self):
        plan_window = tk.Toplevel(self.root)
        plan_label = tk.Label(plan_window, text="Plan:")
        plan_label.pack()
        plan_entry = tk.Entry(plan_window)
        plan_entry.pack()
        plan_button = tk.Button(plan_window, text="Get Plan", command=lambda: self.get_plan_output(plan_window))
        plan_button.pack()
        # The plan will be gathered from the planner team and then shown in the window
        # A prompt needs to be set first with the start procedure

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

        if team and job_description and status:
            self.Jobs.append({
                "Team": team,
                "Job": job_description,
                "Status": status,
                "SubJob": subjob
            })
            self.update_Job_list()
            self.chat_output.insert(tk.END, f"A new Job has been added: Team: {team}, Job: {job_description}, Status: {status}, SubJob: {subjob}\n")  # Insert the Job into the chat output
            job_window.destroy()
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields")
            #Example on how to add a Job: self.Jobs.append({"Team": "1 Planner", "Job": "Plan a game from a prompt given by the CEO", "Status": "not solved", "SubJob": "Plan a game from a prompt given by the CEO"})

    def get_plan_output(self, plan_window):
        # Add logic to get and display the plan output
        pass

    def open_question_window(self):
        question_window = tk.Toplevel(self.root)

        teams = ["1 Planner", "2 Orchestra", "2-1 Plan Build", "2-2 Structure Build " , "2-3 Engine Choose or Build", "2-4 Art and Prompt Build","2-5 Quality Assist Orchestra ", "3 Task Maker Logic ", "3-1 GUI Logic ", "3-2 Backend Logic", "3-3 Engine Logic", "3-4 Preview Art","3-5 Quality Assist Logic", "4 Task Manager Code", "4-1 GUI Code", "4-2 Backend Code", "4-3 Engine Code", "4-4 Art Refiner","4-5 Quality Assist Code", "5 Reviewer", "5-1 GUI Review", "5-2 Backend Review", "5-3 Engine Review", "5-4 Art implemention","5-5 Quality Assist Reviewer", "6 Debug and Error", "6-1 GUI Debug", "6-2 Backend Debug", "6-3 Engine Debug", "6-4 Art Debug","6-5 Quality Assist Debug", "7 Finalizer", "7-1 Documentation", "7-2 Manual and Requirements",]
        self.selected_team = tk.StringVar(question_window)
        self.selected_team.set(teams[0])  # Default value
        self.team_label = tk.Label(question_window, text="Team:")
        self.team_entry = tk.OptionMenu(question_window, self.selected_team, *teams)
        self.team_entry.pack()

        self.question_label = tk.Label(question_window, text="Question:")
        self.question_label.pack()
        self.question_label_entry = tk.Entry(question_window)
        self.question_label_entry.pack()        

        self.ask_question_label = tk.Label(question_window, text="Ask Question:")
        self.ask_question_label.pack()
        self.ask_question_label_entry = tk.Entry(question_window)
        self.ask_question_label_entry.pack()

        self.suggestion_1_label = tk.Label(question_window, text="Suggestion 1:")
        self.suggestion_1_label.pack()
        self.suggestion_1_label_entry = tk.Entry(question_window)
        self.suggestion_1_label_entry.pack()

        self.suggestion_2_label = tk.Label(question_window, text="Suggestion 2:")
        self.suggestion_2_label.pack()
        self.suggestion_2_label_entry = tk.Entry(question_window)
        self.suggestion_2_label_entry.pack()

        self.own_suggestion_label = tk.Label(question_window, text="Own Suggestion:")
        self.own_suggestion_label.pack()
        self.own_suggestion_label_entry = tk.Entry(question_window)
        self.own_suggestion_label_entry.pack()

        self.scratch_question_label = tk.Label(question_window, text="Scratch Question:")
        self.scratch_question_label.pack()
        self.scratch_question_label_entry = tk.Entry(question_window)
        self.scratch_question_label_entry.pack()

        self.add_question_button = tk.Button(question_window, text="Add Question", command=lambda: self.add_question(question_window))
        self.add_question_button.pack()        

    def add_question(self, question_window):
        team = self.selected_team.get()
        question = self.question_label_entry.get()
        ask_question = self.ask_question_label_entry.get()
        suggestion1 = self.suggestion_1_label_entry.get()
        suggestion2 = self.suggestion_2_label_entry.get()
        own_suggestion = self.own_suggestion_label_entry.get()
        scratch_question = self.scratch_question_label_entry.get()
            
        if team and question and ask_question and suggestion1 and suggestion2 and own_suggestion and scratch_question:
            self.tasks.append({
                "Team": team,
                "Question": question,
                "Ask Question": ask_question,
                "Suggestion 1": suggestion1,
                "Suggestion 2": suggestion2,
                "Own Suggestion": own_suggestion,
                "Scratch Question": scratch_question
            })
            self.chat_output.insert(tk.END, f"A new question has been added: Team: {team}, Question: {question}, Ask Question: {ask_question}, Suggestion 1: {suggestion1}, Suggestion 2: {suggestion2}, Own Suggestion: {own_suggestion}, Scratch Question: {scratch_question}\n")
            self.update_Job_list()
            question_window.destroy()
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields")

    def update_Job_list(self):
        self.Job_listbox.delete(0, tk.END)
        for Job in self.Jobs:
            if all(key in Job for key in ['Team', 'Question', 'Ask Question', 'Suggestion 1', 'Suggestion 2', 'Own Suggestion', 'Scratch Question']):
                team = Job.get('Team', '')
                question = Job.get('Question', '')
                ask_question = Job.get('Ask Question', '')
                suggestion1 = Job.get('Suggestion 1', '')
                suggestion2 = Job.get('Suggestion 2', '')
                own_suggestion = Job.get('Own Suggestion', '')
                scratch_question = Job.get('Scratch Question', '')

                self.Job_listbox.insert(tk.END, f"Team: {team}, Question: {question}, Ask Question: {ask_question}, Suggestion 1: {suggestion1}, Suggestion 2: {suggestion2}, Own Suggestion: {own_suggestion}, Scratch Question: {scratch_question}")
            else:
                team = Job.get('Team', '')
                Job_desc = Job.get('Job', '')
                status = Job.get('Status', '')
                subJob = Job.get('SubJob', '')
                self.Job_listbox.insert(tk.END, f" Team: {team}, Job: {Job_desc}, Status: {status}, SubJob: {subJob}")

    def delete_Job(self):
        selected_index = self.Job_listbox.curselection()
        if selected_index:
            self.Jobs.pop(selected_index[0])
            self.update_Job_list()
        else:
            tk.messagebox.showerror("Error", "Please select a Job to delete")

    def send_chat_input(self):
        chat_input = self.chat_input.get()
        if chat_input:
            self.chat_output.insert(tk.END, f"User: {chat_input}\n")
            self.chat_output.see(tk.END)
            self.chat_input.delete(0, tk.END)

            # Run the long-running task in a separate thread
            threading.Thread(target=self.start_chat_flow, args=(chat_input,)).start()

    def start_chat_flow(self, tasks):
        agents = CompanyAgents()
        tasks = PlanningTasks()

        CEO_Agent = agents.CEOAgent()
        Game_planner = agents.GamePlanningAgent()

        prompt = self.chat_input.get()
        task1 = tasks.delegate_team(CEO_Agent, self.company, prompt)
        
        self.crew = Crew(
            log_handler=self.log_to_widget,
            agents=[CEO_Agent, Game_planner],
            tasks=[task1],
            verbose=True
        )
        result = self.crew.kickoff()
        return result  

if __name__ == "__main__":
    root = tk.Tk()
    game = []
    chat_input = []
    company = "MasterMindGPT Game Maker"
    master = []

    task_board_gui = TaskBoardGUI(root, game,chat_input,company, master )
    root.mainloop()