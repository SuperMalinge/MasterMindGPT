import tkinter as tk
import tkinter.messagebox as tkmessagebox
from anytree import Node, RenderTree
from tkinter.ttk import Treeview

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
    def __init__(self, root):
        self.root = root
        self.root.title("MasterMindGPT Task Board")
        self.tasks = []
        self.root.geometry("1100x500")
        self.question_window = None 
        # Create attributes for question-related widgets
        self.question_entry = None
        self.ask_question_entry = None
        self.suggestion_1_entry = None
        self.suggestion_2_entry = None
        self.own_suggestion_entry = None
        self.scratch_question_entry = None


        # Button to add tasks
        self.add_task_button = tk.Button(root, text="Add Task", command=self.open_task_window)
        self.add_task_button.pack()
        self.add_task_button.place(x=450, y=0)

        # Button to delete tasks
        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack()
        self.delete_task_button.place(x=510, y=0)

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

        # Display the chat output
        self.chat_output = tk.Text(root, height=20, width=40)  # Text widget for chat output
        self.chat_output.pack(side=tk.LEFT)    
        self.chat_output.place(x=100, y=0)    

        # Display the task list with a wider width
        self.task_listbox = tk.Listbox(root, width=80)  # Adjust the width here
        self.task_listbox.pack()
        self.task_listbox.place(x=450, y=30)

        # chat input
        self.chat_input = tk.Entry(root, width=80)  # Entry widget for chat input. Prompt goes here
        self.chat_input.pack()
        self.chat_input.place(x=100, y=330, width=325)

    def get_questions(self):
        question_count = sum('questions' in task['Task'].lower() for task in self.tasks)
        self.get_questions_button.config(text=f"Get Questions ({question_count})")
        for task in self.tasks:
            if 'questions' in task['Task'].lower():
                self.chat_output.insert(tk.END, f"Question: {task['Task']}, Ask Question: {task['Ask Question']}, Suggestion 1: {task['Suggestion 1']}, Suggestion 2: {task['Suggestion 2']}, Own Suggestion: {task['Own Suggestion']}, Scratch Question: {task['Scratch Question']}")

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
        #tree structure for the plan. The structure will be gathered from the planner team and then shown in the window
        #a prompt needs to be set first with the start procedure
        #Tree structure will show the files for this project
        #The files will be shown in a tree structure

        # Create a tree structure
        self.tree = Treeview(plan_window, columns=("col1", "col2"), show="headings", height=10)
        self.tree.pack()
        self.tree.insert("", "end", text="L1", values=("1A", "1b"))
        # Create a child node
        self.tree.insert("", "end", text="L2", values=("2A", "2B"))
        # show the tree structure
        self.tree.pack()
                

        self.structure_button = tk.Button(plan_window, text="Get Structure", command=lambda: self.get_structure_output(plan_window))
        #the structure will be gathered from the planner team and then shown in the window
        #a prompt needs to be set first with the start procedure
        

        def build_tree_from_instructions(instructions, parent=None):
            for instruction in instructions:
                node_value, children = instruction[0], instruction[1:]
                current_node = Node(node_value, parent=parent)
            if children:
                build_tree_from_instructions(children, parent=current_node)

            # Example instructions for the agent to build a tree
            instructions = [
                ("A", ("B", ("D", "E"), "C")),
                ("X", ("Y", ("Z",)))
            ]

            # Create the tree based on the instructions
            root = Node("Root")
            build_tree_from_instructions(instructions, parent=root)

            # Visualizing the tree using RenderTree
            # for pre, fill, node in RenderTree(root):
            #     print("%s%s" % (pre, node.name))
              


    def get_plan(self):
        plan_window = tk.Toplevel(self.root)
        self.plan_label = tk.Label(plan_window, text="Plan:")
        self.plan_label.pack()
        self.plan_entry = tk.Entry(plan_window)
        self.plan_entry.pack()
        self.plan_button = tk.Button(plan_window, text="Get Plan", command=lambda: self.get_plan_output(plan_window))
        #the plan will be gathered from the planner team and then shown in the window
        #a prompt needs to be set first with the start procedure

  
    def open_task_window(self):
        task_window = tk.Toplevel(self.root)
        self.team_label = tk.Label(task_window, text="Team:")
        self.team_label.pack()
        # Dropdown menu for selecting level
        teams = ["1 Planner", "2 Orchestra", "2-1 Plan Build", "2-2 Structure Build " , "2-3 Engine Choose or Build", "2-4 Art and Prompt Build","2-5 Quality Assist Orchestra ", "3 Task Maker Logic ", "3-1 GUI Logic ", "3-2 Backend Logic", "3-3 Engine Logic", "3-4 Preview Art","3-5 Quality Assist Logic", "4 Task Manager Code", "4-1 GUI Code", "4-2 Backend Code", "4-3 Engine Code", "4-4 Art Refiner","4-5 Quality Assist Code", "5 Reviewer", "5-1 GUI Review", "5-2 Backend Review", "5-3 Engine Review", "5-4 Art implemention","5-5 Quality Assist Reviewer", "6 Debug and Error", "6-1 GUI Debug", "6-2 Backend Debug", "6-3 Engine Debug", "6-4 Art Debug","6-5 Quality Assist Debug", "7 Finalizer", "7-1 Documentation", "7-2 Manual and Requirements",]
        self.selected_team = tk.StringVar(task_window)
        self.selected_team.set(teams[0])  # Default value
        self.team_entry = tk.OptionMenu(task_window, self.selected_team, *teams)
        self.team_entry.pack()

        self.task_description_label = tk.Label(task_window, text="Task Description:")
        self.task_description_label.pack()
        self.task_description_entry = tk.Entry(task_window)
        self.task_description_entry.pack()

        self.subtask_label = tk.Label(task_window, text="Subtask:")
        self.subtask_label.pack()
        self.subtask_entry = tk.Entry(task_window)
        self.subtask_entry.pack()

        self.status_label = tk.Label(task_window, text="Status:")
        self.status_label.pack()

        # Dropdown menu for selecting status
        status_options = ["solved", "not solved"]
        self.selected_status = tk.StringVar(task_window)
        self.selected_status.set(status_options[0])  # Default value
        self.status_entry = tk.OptionMenu(task_window, self.selected_status, *status_options)
        self.status_entry.pack()

        # Button to add tasks in second window
        self.add_task_button = tk.Button(task_window, text="Add Task", command=lambda: self.add_task(task_window))
        self.add_task_button.pack()

    def add_task(self, task_window):
        team = self.selected_team.get()
        task_description = self.task_description_entry.get()
        status = self.selected_status.get()
        subtask = self.subtask_entry.get()

        if team and task_description and status:
            self.tasks.append({
                "Team": team,
                "Task": task_description,
                "Status": status,
                "Subtask": subtask
            })
            self.update_task_list()
            self.chat_output.insert(tk.END, f"A new task has been added: Team: {team}, Task: {task_description}, Status: {status}, Subtask: {subtask}\n")  # Insert the task into the chat output
            task_window.destroy()
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields")


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
            self.update_task_list()
            question_window.destroy()
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields")



    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if all(key in task for key in ['Team', 'Question', 'Ask Question', 'Suggestion 1', 'Suggestion 2', 'Own Suggestion', 'Scratch Question']):
                team = task.get('Team', '')
                question = task.get('Question', '')
                ask_question = task.get('Ask Question', '')
                suggestion1 = task.get('Suggestion 1', '')
                suggestion2 = task.get('Suggestion 2', '')
                own_suggestion = task.get('Own Suggestion', '')
                scratch_question = task.get('Scratch Question', '')

                self.task_listbox.insert(tk.END, f"Team: {team}, Question: {question}, Ask Question: {ask_question}, Suggestion 1: {suggestion1}, Suggestion 2: {suggestion2}, Own Suggestion: {own_suggestion}, Scratch Question: {scratch_question}")
            else:
                team = task.get('Team', '')
                task_desc = task.get('Task', '')
                status = task.get('Status', '')
                subtask = task.get('Subtask', '')

                self.task_listbox.insert(tk.END, f" Team: {team}, Task: {task_desc}, Status: {status}, Subtask: {subtask}")




    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            self.update_task_list()
        else:
            tk.messagebox.showerror("Error", "Please select a task to delete")

if __name__ == "__main__":
    root = tk.Tk()
    task_board_gui = TaskBoardGUI(root)
    root.mainloop()
