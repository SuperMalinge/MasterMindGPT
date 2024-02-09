# This class will be used to define the actions that an agent can perform. it is in the agent_actions.py file
class Agent_actions:
    def __init__(self, name, team, chat_output):
        self.name = name
        self.team = team
        self.tasks = []        

    # This function announces the task that the agent has received
    def handle_task(self, task):
        from gui.task_board_gui import Logger
        self.tasks.append(task)
        Logger.log_to_widget(f"{self.name}: received task -> {task}")
        print(f"{self.name}: received task -> {task}")

    def report_status(self):
        # This could return a summary of tasks, their status or any other relevant information
        return {
            "total_tasks": len(self.tasks),
            "current_tasks": [task['Job'] for task in self.tasks]
        }

