from models.logger import Logger

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