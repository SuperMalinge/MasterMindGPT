import tkinter as tk

class Agent:
    def __init__(self, name):
        self.name = name
        self.team = None  # Default to None, will be set when the agent is added by the CEO

class CEO:
    def __init__(self, agent_listbox, chat_output, task_queue):
        self.agents = {}
        self.jobs = []
        self.agent_listbox = agent_listbox  # Tkinter Listbox widget for agents
        from gui.task_board_gui import Logger
        self.logger = Logger(chat_output)
        self.task_queue = task_queue  # Queue for inter-thread communication
        #add team attribue to the agent class    
          
                        
    def initiate_workflow(self, message):
        if message == "start the workflow":
            print("Starting the workflow...")
            self.logger.log_to_widget("Starting the workflow...")
            # Filter only those tasks that belong to the '1 Planner' team
            planner_tasks = [job for job in self.jobs if job.team == '1 Planner']
            for job in planner_tasks:
                self.delegate_task(job)

    def add_agent(self, agent, team):    
        # Check if agent is already added
        if agent.name in self.agents:
            print(f"Agent {agent.name} is already added.")
            self.logger.log_to_widget(f"Agent {agent.name} is already added to the team {team}.")
            return   

        # Associate the agent with a team
        agent.team = team  # Assuming that the 'Agent' class has a 'team' attribute
        self.agents[agent.name] = agent
        print(f"Added agent {agent.name} with team: {team} to CEO's list of agents.")
        self.logger.log_to_widget(f"Added agent {agent.name} with team: {team} to CEO's list of agents.")

        # Insert the agent's name and team to the agent_listbox using the task queue
        agent_display_name = f"{agent.name} ({team})"
        self.task_queue.put(lambda: self.agent_listbox.insert(tk.END, agent_display_name))              
        self.agents[agent.name] = agent
        print(f"Added agent {agent.name} to CEO's list of agents.")
        self.logger.log_to_widget(f"Added agent {agent.name} to CEO's list of agents.")
        #self.agent_listbox.insert(tk.END, agent.name)  # Add this line
        # Invoke the queue to asynchronously add agent's name to the agent_listbox
        self.task_queue.put(lambda: self.agent_listbox.insert(tk.END, agent.name))
        
    def delegate_task(self, job):           
        print(f"Delegating task: {job}")  # Print a message
        self.logger.log_to_widget(f"Delegating task: {job}")  # Print a message
        if not self.agents:
            print("No agents available")
            self.logger.log_to_widget("No agents available")
            #try to add agents to the list
            print("Trying to add agents to the list")
            self.logger.log_to_widget("Trying to add agents to the list")
            #retrieve the agents from the task board gui agent listbox
            print("Retrieving agents from the task board gui agent listbox")
            self.logger.log_to_widget("Retrieving agents from the task board gui agent listbox")
                    
            return

        # Delegate task to the appropriate agent based on job team
        agent = self.agents.get(job['Team'])
        #agent = self.agents.get(job.team)
        if agent:
            agent.handle_task(job)
            self.report_task_delegation(job)
        else:
            print(f"No matching agent found for team {job['Team']}.")
            self.logger.log_to_widget(f"No matching agent found for team {job['Team']}.")
            print("Available agents:", self.agents.keys())
            self.logger.log_to_widget(f"Available agents: {self.agents.keys()}")

    # Add a new method that the main thread can poll, which checks and handles the queue
    def process_queue(self):
        while not self.task_queue.empty():
            try:
                action = self.task_queue.get(block=False)
                action()  # Execute the action in the main thread
            except self.task_queue.empty():
                pass

    def report_task_delegation(self, job):       
        print(f"Delegated task '{job.description}' to {job['Team']}.")
        self.logger.log_to_widget(f"Delegated task '{job.description}' to {job['Team']}.")
        
    def report_tasks_status(self):
        status_report = {agent_name: agent.report_status() for agent_name, agent in self.agents.items()}
        return status_report

    def add_job(self, job):       
        self.jobs.append(job)
        print(f"Added job {job.description} to CEO's list of jobs.")
        self.logger.log_to_widget(f"Added job {job.description} to CEO's list of jobs.")         
        self.task_queue.put(lambda: self.logger.log_to_widget(f"Added job {job.description} to CEO's list of jobs."))


