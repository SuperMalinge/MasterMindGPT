from models.logger import Logger

class CEO:
    def __init__(self):
        self.agents = {}
        self.jobs = []

    def initiate_workflow(self, message):
        if message == "start the workflow":
            # Filter only those tasks that belong to the '1 Planner' team
            planner_tasks = [job for job in self.jobs if job.team == '1 Planner']
            for job in planner_tasks:
                self.delegate_task(job)

    def add_agent(self, agent):
        self.agents[agent.name] = agent

    def delegate_task(self, job):
        # Check if there are any agents available
        if not self.agents:
            print("No agents available")
            Logger.log_to_widget("No agents available")
            return

        # Delegate task to the appropriate agent based on job team
        agent = self.agents.get(job.team)
        if agent:
            agent.handle_task(job)
            self.report_task_delegation(job)
        else:
            print(f"No matching agent found for team {job.team}.")
            Logger.log_to_widget(f"No matching agent found for team {job.team}.")

    def report_task_delegation(self, job):
        print(f"Delegated task '{job.description}' to {job.team}")
        Logger.log_to_widget(f"Delegated task '{job.description}' to {job.team}")
        # In a GUI application, reporting could be updating a text field, or popping up a message

    def report_tasks_status(self):
        status_report = {agent_name: agent.report_status() for agent_name, agent in self.agents.items()}
        return status_report

    def add_job(self, job):
        self.jobs.append(job)