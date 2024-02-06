import os
import tkinter as tk
from data.job import Job
from data.job_management_system import JobManagementSystem
from models.ceo import CEO
from models.agent_actions import Agent_actions
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import tkinter.messagebox as messagebox

#Job_Management_System = JobManagementSystem(root, task_board_gui.Job_listbox, task_board_gui,task_board_gui.chat_output, task_board_gui.task_queue)

class CustomAssistantAgent(RetrieveAssistantAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_task(self, job,Job_Management_System):        
        # Preprocess the job input to structure it correctly        
        processed_input = self.preprocess_chat_input(job['Job'])
        # The job already has the correct structure since it's being passed in
        # with team, job description, status, and subjob details.
        # Add the job to the job management system
        Job_Management_System.add_job(job)

        # Update the job list GUI
        self.task_queue.put(lambda: Job_Management_System.update_job_list())

        # Reset the planner and initiate the workflow
        self.reset()
        self.task_queue.put(lambda: self.logger.log_to_widget(f"Initiated workflow with input: {processed_input}"))
        # Here, instead of specifying 'self.retrieve_assistant_agent_planner',
        # we just use 'self' because 'handle_task' is now an instance method of the agent
        self.initiate_workflow(processed_input, self.task_queue, self.logger)

    def preprocess_chat_input(self, chat_input):
        # Preprocess the chat input so that it's in the correct format
        # the format resembles the job structure in the JobManagementSystem
        # For now, we just return the chat input as is
        return chat_input


class WorkflowManager:    
    # This class is responsible for the workflow management in the workflow_manager.py
    def __init__(self, llm_config, chat_output, job_management_system, ceo_boss, agent_listbox, task_queue):
        self.llm_config = llm_config              
        self.job_management_system = job_management_system
        self.ceo_boss = ceo_boss      
        from gui.task_board_gui import Logger
        self.logger = Logger(chat_output)
        self.task_queue = task_queue  # Queue for inter-thread communication
        self.agent_listbox = agent_listbox  # Keep a reference to agent_listbox if needed
        self.initialize_rag_agents(ceo_boss, agent_listbox)

    def initiate_workflow(self, chat_input):        
        processed_input = self.preprocess_chat_input(chat_input)

        # Create the job
        job = {
            "Team": "1 Planner",
            "Job": processed_input,
            "Status": "unsolved",
            "SubJob": None
        }        
        # Delegate the task and add the job
        self.ceo_boss.delegate_task(job)
        self.task_queue.put(lambda: self.logger.log_to_widget(f"Delegated task: {processed_input}"))
        self.job_management_system.add_job(job)
        
        # Queue GUI update task
        self.task_queue.put(lambda: self.job_management_system.update_job_list())

        # Reset the planner and initiate the chat
        self.retrieve_assistant_agent_planner.reset()
        self.task_queue.put(lambda: self.logger.log_to_widget(f"Initiated workflow with input: {processed_input}"))
        self.retrieve_user_proxy_agent.initiate_chat(self.retrieve_assistant_agent_planner, problem=processed_input)

    def preprocess_chat_input(self, chat_input):
        return chat_input

    def initialize_rag_agents(self, ceo_boss, agent_listbox ):             
        print("Initializing RAG agents with llm_config:", self.llm_config)
        self.logger.log_to_widget("Initializing RAG agents with llm_config:")
        docs_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')        
        try:
            # Create the Planner agent
            self.retrieve_assistant_agent_planner = CustomAssistantAgent(
                name="Planner Agent",
                system_message="You plan the given task.",
                llm_config=self.llm_config,
            )
            print("Planner Agent (RetrieveAssistantAgent) initialized successfully.")
            self.logger.log_to_widget("Planner Agent (RetrieveAssistantAgent) initialized successfully.")
            # Immediately add the agent to the CEO's list
            ceo_boss.add_agent(self.retrieve_assistant_agent_planner, "1 Planner")	

            # Create the Orchestra agent
            self.retrieve_assistant_agent_orchestra = CustomAssistantAgent(
                name="Orchestra Agent",
                system_message="You orchestrate the workflow.",
                llm_config=self.llm_config,
            )
            print("Orchestra Agent (RetrieveAssistantAgent) initialized successfully.")
            self.logger.log_to_widget("Orchestra Agent (RetrieveAssistantAgent) initialized successfully.")
            ceo_boss.add_agent(self.retrieve_assistant_agent_orchestra, "2 Orchestra")     

            # Create the CEO proxy agent                         
            self.retrieve_user_proxy_agent = RetrieveUserProxyAgent(
                name="CEO Proxy Agent",
                system_message="You are the CEO of the company.",
                retrieve_config={
                    "task": "qa",
                    "docs_path": docs_directory,
                },
            )
            print("CEO Proxy Agent (RetrieveUserProxyAgent) initialized successfully.")
            self.logger.log_to_widget("CEO Proxy Agent (RetrieveUserProxyAgent) initialized successfully.")
            # We cant add the CEO proxy agent to the CEO list since he is the one who adds agents to the list
            #therefore we add him to the agent listbox
            #agent_listbox.insert(tk.END, self.retrieve_user_proxy_agent.name)  # Add this line
            # Instead of inserting directly into Tk widgets, use the task queue
            self.task_queue.put(lambda: self.agent_listbox.insert(tk.END, self.retrieve_user_proxy_agent.name))
                                  
        except Exception as e:
            # Add logging or error handling using the task queue
            self.task_queue.put(lambda: self.logger.log_to_widget(f"Error during RAG agents initialization: {e}"))
            raise

    def start_chat_flow(self, chat_input):        
        # Reset the agents at the beginning of a chat flow
        self.retrieve_assistant_agent_planner.reset()        
        self.retrieve_user_proxy_agent.initiate_chat(self.retrieve_assistant_agent_planner, problem=chat_input)
        self.logger.log_to_widget(f"Initiated chat with input: {chat_input}")
        try:
            messages = self.retrieve_user_proxy_agent.chat_messages
            for message in messages:
                self.logger.log_to_widget(message['content'])
        except Exception as e:
           self.logger.log_to_widget(str(e))
