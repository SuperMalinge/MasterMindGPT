from data.job import Job
from data.job_management_system import JobManagementSystem
from models.ceo import CEO
from models.agent_actions import Agent_actions
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import os
import tkinter as tk


class WorkflowManager:    
    def __init__(self, llm_config, chat_output, job_management_system, ceo_boss, agent_listbox):
        self.llm_config = llm_config              
        self.job_management_system = job_management_system
        self.ceo_boss = ceo_boss      
        from gui.task_board_gui import Logger
        self.logger = Logger(chat_output)          
        self.initialize_rag_agents(ceo_boss,agent_listbox)

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
        CEO.delegate_task(job)
        print("Delegated task:", job)
        self.logger.log_to_widget(f"Delegated task: {processed_input}")
        self.job_management_system.add_job(job)    
        print("Added job:", job)  
        self.logger.log_to_widget(f"Added job: {processed_input}")  
        self.job_management_system.update_job_list()
        print("Updated job list")
        self.logger.log_to_widget(f"Delegated to Planner: {processed_input}")

        # Reset the planner and initiate the chat
        self.retrieve_assistant_agent_planner.reset()
        self.logger.log_to_widget(f"Initiated workflow with input: {processed_input}")
        print("Initiated workflow with input:", processed_input)
        self.retrieve_user_proxy_agent.initiate_chat(self.retrieve_assistant_agent_planner, problem=processed_input)    

    def process_chat_input(self, chat_input):
        from gui.task_board_gui import Logger
        processed_input = self.preprocess_chat_input(chat_input)
        job = {
            "Team": "1 Planner",
            "Job": processed_input,
            "Status": "unsolved",
            "SubJob": None
        }
        CEO.delegate_task(job)
        self.Jobs.append(job)
        self.update_Job_list()
        self.logger.log_to_widget(f"Delegated to Planner: {processed_input}")

    def preprocess_chat_input(self, chat_input):
        return chat_input

    def initialize_rag_agents(self, ceo_boss, agent_listbox ):        
            
        print("Initializing RAG agents with llm_config:", self.llm_config)
        self.logger.log_to_widget("Initializing RAG agents with llm_config:")
        docs_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')        
        try:
            self.retrieve_assistant_agent_planner = RetrieveAssistantAgent(
                name="Planner Agent",
                system_message="You plan the given task.",
                llm_config=self.llm_config,
            )
            print("Planner Agent (RetrieveAssistantAgent) initialized successfully.")
            self.logger.log_to_widget("Planner Agent (RetrieveAssistantAgent) initialized successfully.")
            # Immediately add the agent to the CEO's list
            #CEO.add_agent(self.retrieve_assistant_agent_planner)
            self.retrieve_assistant_agent_orchestra = RetrieveAssistantAgent(
                name="Orchestra Agent",
                system_message="You orchestrate the workflow.",
                llm_config=self.llm_config,
            )
            print("Orchestra Agent (RetrieveAssistantAgent) initialized successfully.")
            self.logger.log_to_widget("Orchestra Agent (RetrieveAssistantAgent) initialized successfully.")
            # Immediately add the agent to the CEO's list
            #CEO.add_agent(self.retrieve_assistant_agent_orchestra)            
            self.retrieve_user_proxy_agent = RetrieveUserProxyAgent(
                name="CEO Proxy Agent",
                retrieve_config={
                    "task": "qa",
                    "docs_path": docs_directory,
                },
            )
            print("CEO Proxy Agent (RetrieveUserProxyAgent) initialized successfully.")
            self.logger.log_to_widget("CEO Proxy Agent (RetrieveUserProxyAgent) initialized successfully.")
            # We cant add the CEO proxy agent to the CEO list since he is the one who adds agents to the list
            #therefore we add him to the agent listbox
            agent_listbox.insert(tk.END, self.retrieve_user_proxy_agent.name)  # Add this line
                                  
        except Exception as e:
            print("Error during RAG agents initialization:", e)
            self.logger.log_to_widget(f"Error during RAG agents initialization: {e}")
            raise

    def start_chat_flow(self, chat_input):
        from gui.task_board_gui import Logger
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
