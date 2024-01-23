import tkinter as tk
from gui.task_board_gui import TaskBoardGUI
from models.workflow_manager import WorkflowManager
from data.job_management_system import JobManagementSystem
from gui.game_planning_gui import GamePlanningGUI
import json

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

if __name__ == "__main__":
    root = tk.Tk()
    game = []
    chat_input = []
    company = "MasterMindGPT Game Maker"
    master = []
    task = []
    team = []

    task_board_gui = TaskBoardGUI(root, game, chat_input, company, master, llm_config,task, team)
    job_management_system = JobManagementSystem(root, task_board_gui.Job_listbox, task_board_gui)
    task_board_gui.job_management_system = job_management_system
    game_planning_gui = GamePlanningGUI(root)


    root.mainloop()
