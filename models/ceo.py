import tkinter as tk

class Agent:
    #this class is responsible for the agent in the ceo.py file
    def __init__(self, name):
        self.name = name
        self.team = None  # Default to None, will be set when the agent is added by the CEO

class CEO:
    # This class is responsible for the CEO in the ceo.py file
    # The CEO is responsible for managing the agents and delegating tasks to them
    # The CEO is the proxy agent in the listbox of agents in the GUI
    # He is the boss of all the agents
    # The CEO is the only agent that can add new agents to the list of agents
    # He is initializing the workflow and processing the queue
    def __init__(self, agent_listbox, chat_output, task_queue, job_management_system):
        self.agents = {}
        self.jobs = []
        self.agent_listbox = agent_listbox  # Tkinter Listbox widget for agents
        from gui.task_board_gui import Logger
        self.logger = Logger(chat_output)
        self.task_queue = task_queue  # Queue for inter-thread communication
        self.job_management_system = job_management_system         
                                  
    def initiate_workflow(self, message):
        if message == "start the workflow":
            print("Starting the workflow...")
            self.logger.log_to_widget("Starting the workflow...")
            # Filter only those tasks that belong to the '1 Planner' team
            planner_tasks = [job for job in self.jobs if job.team == '1 Planner']
            for job in planner_tasks:
                self.delegate_task(job)

    def add_agent(self, agent, team):    
        # Check if the agent is already added or if the team is undefined or empty
        if agent.name in self.agents:
            print(f"Agent {agent.name} is already added.")
            self.logger.log_to_widget(f"Agent {agent.name} is already added to the team {team}.")
            return
        
        # The team should be a non-empty string for an agent to be validly associated with it
        if not team:
            print(f"Agent {agent.name} cannot be added without a specified team.")
            self.logger.log_to_widget(f"Agent {agent.name} cannot be added without a specified team.")
            return

        # Associate the agent with a team
        agent.team = team  # Assuming that the 'Agent' class has a 'team' attribute
        agent_display_name = f"{agent.name} ({team})"
        
        # Add the agent to the dictionary and listbox in a thread-safe manner using task_queue
        self.agents[agent.name] = agent
        self.task_queue.put(lambda: self.agent_listbox.insert(tk.END, agent_display_name))
        
        # Log the addition with the proper confirmation
        confirmation_message = f"Added agent {agent.name} with team: {team} to CEO's list of agents."
        print(confirmation_message)
        self.logger.log_to_widget(confirmation_message)
       
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
        # Uses the JobManagementSystem's add_job method to add a job
        self.job_management_system.add_job(job)
        # The logging is taken care of within the JMS's add_job method

        # example of how to add a job to the CEO's jobs list
        #team = "1 Planner"
        #description = "Plan the project execution"
        #status = "not solved"
        #subjob = None

        #new_job = Job(team, description, status, subjob)
        #job_management_system_instance.add_job(new_job)



