from crewai import Agent
from agent_tool_addjob import JobManagementTools


class CompanyAgents:
  
    def CEOAgent(self):
        # CEO to run the game planning company
        return Agent(
            role='CEO of the Game Planning Company',
            goal="""You are the CEO of a game planning company.""",
            backstory="""You are the CEO of a game planning company. You will delegate all agents to create a game.""",
            verbose=True,
            tools=[
                JobManagementTools.add_job_to_list
            ]   
        )

    def GamePlanningAgent(self):
        """
        Plan a game from a prompt given by the CEO.

        Returns:
            Agent: The game planning agent.
        """
        return Agent(
            role='Game planner',
            goal="""Plan a game from a prompt given by the CEO.""",
            backstory="""You're a game planner in a major game development company. You are in the Team PLANNING working on different tasks. You want to create a plan to make a game from a prompt.""",
            memory=True,
            verbose=True,
            tools=[
                JobManagementTools.add_job_to_list
            ]
        )
    
    def get_agents(self):
        # Return a list with the names or roles of the available agents
        return [
            'CEOAgent',            # Assuming these are the roles or names
            'GamePlanningAgent',   # Replace with actual attributes if different
            
        ]
          
      