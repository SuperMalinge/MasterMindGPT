from crewai import Task, tools
from textwrap import dedent
from agent_tool_addjob import JobManagementTools
import json
from pydantic import BaseModel

import inspect

# Function to inspect a tool or a function's signature
def inspect_tool_signature(tool):
    signature = inspect.signature(tool)
    print(f'Signature for tool {tool}: {signature}')

class AddAJobToListSchemaSchema(BaseModel):
    team: str
    job_description: str
    status: str
    subjob: str

class PlanningTasks:
    def planning(self, agent, game_type, game_genre):
        """
        Plan the development of a new game.

        Args:
            agent (Agent): The planning agent responsible for creating the game plan.
            game_type (str): The type or category of the game (e.g., simulation, strategy, etc.).
            game_genre (str): The genre of the game (e.g., fantasy, sci-fi, etc.).

        Returns:
            Task: A task representing the plan for the game development, including the game type,
                  game genre, and an overall structure for the game.

        The agent is tasked with creating a comprehensive plan for developing a new game. The plan
        should include details such as the chosen game type, game genre, and a high-level structure
        for the game development process. The final output should be a well-documented plan that
        outlines the key elements of the game.

        Tips:
            - Consider market trends and audience preferences when selecting the game type and genre.
            - Provide a clear and organized structure for the game development process.
            - Include any additional information that is crucial for the successful planning of the game.

        Example Usage:
            
        """
        return Task(description=dedent(f"""
            Plan the development of a new game.

            Game Type: {game_type}
            Game Genre: {game_genre}

            Your task is to create a detailed plan for the development of the game, taking into
            account the selected game type and genre. Include an overall structure that outlines
            the key steps and milestones in the game development process.

            The final output should be a comprehensive plan that serves as a guide for the
            development team.
            
        """),
        agent=agent
        )

    def requirements_analysis(self, game_type, game_genre):
        """
        Analyze the requirements for a new game based on game type and game genre.

        Args:
            game_type (str): The type or category of the game (e.g., simulation, strategy, etc.).
            game_genre (str): The genre of the game (e.g., fantasy, sci-fi, etc.).

        Returns:
            analyzed_requirements (list): A list containing tuples with categories
                                          and details of game features.

        The analysis includes identifying key features that fit the game type and genre, 
        and use the given game type and genre and prompt from the CEO to analyze the requirements.

        Example Usage:
            
        """
        # Placeholder for analysis logic which you'll need to implement
        # Here we assume that such a function `analyze_genre_and_type` exists and returns a list of key features
        # analyzed_requirements = analyze_genre_and_type(game_type, game_genre)

        # For the purpose of this example, let's assume analyzed_requirements are predefined:
        analyzed_requirements = [
            ('multiplayer', 'game_mechanics'),
            ('platformer', 'game_mechanics'),
            # Additional features based on game_type and game_genre
        ]
        
        # Normally, you'd return here but for compatibility with your example, let's create a Task object
        return Task(description=dedent(f"""
            Analyze the requirements for a new game.

            Game Type: {game_type}
            Game Genre: {game_genre}

            Analyzed features that align with the game type and genre include:
            - Multiplayer support
            - Platformer mechanics
            
            Further analysis may yield additional features such as cloud saving, level design preferences, etc.
            
            """),
            analyzed_requirements=analyzed_requirements
        )
    
    def design(self, analyzed_requirements):
        """
        Create a game design document based on the analyzed requirements.

        Args:
            analyzed_requirements (list): A list containing tuples with categories 
                                          and details of game features.

        Returns:
            Task: A task representing the design of the game including design specifications.

        The agent is tasked with creating a comprehensive design specification for a game. 
        This design should take into account the analyzed requirements.

        Tips:
            - Detailed and accurate mapping of requirements to game features is essential.
            - Ensure the design is consistent with the genre and type of game.
            - Reference market trends to align the game's design with audience expectations.

        Example Usage:
            
        """
        if not analyzed_requirements:
            raise ValueError("No analyzed requirements provided.")

        design_specification_sections = {
            'game_mechanics': [],
            'level_design': [],
            'user_interface_design': [],
            'art_style': [],
            'sound_and_music': []
        }

        # Dictionary mapping general requirements to more specific features
        REQUIREMENTS_MAPPING = {
            'multiplayer': ('Multiplayer support with matchmaking', 'game_mechanics'),
            'platformer': ('Platformer game mechanics with double-jump', 'game_mechanics'),
            # ... (other mappings) ...
            'cloud saving': ('Cloud-based save game storage', 'user_interface_design')
            # Ensure all features from analyzed_requirements are mapped appropriately
        }

        # Populate design specification sections
        for requirement_detail in analyzed_requirements:
            feature, category = requirement_detail
            if feature in REQUIREMENTS_MAPPING:
                detailed_feature, section = REQUIREMENTS_MAPPING[feature]
                design_specification_sections[section].append(detailed_feature)

        # Compile the design spec details
        design_specifications = "\n".join(
            f"{section.replace('_', ' ').title()}: {', '.join(features)}"
            for section, features in design_specification_sections.items()
            if features)

        description = f"""
            Game Design Specification:

            {design_specifications}
        """

        return Task(description=description)  # Assuming a Task is a pre-defined data structure
    
    def project_management(self, agent, game_type, game_genre):
        """
        Manage the development of the game.

        Args:
            agent (Agent): The project management agent responsible for managing the game development.
            game_type (str): The type or category of the game (e.g., simulation, strategy, etc.).
            game_genre (str): The genre of the game (e.g., fantasy, sci-fi, etc.).

        Returns:
            Task: A task representing the management of the game development.

        The agent is tasked with managing the development of the game. The management should include
        details such as the game type, genre, and key features. The final output should be a
        well-documented project status report that outlines the key elements of the game.

        Tips:
            - Consider market trends and audience preferences when selecting the game type and genre.
            - Include any additional information that is crucial for the successful planning of the game.

        Example Usage:
            project_management_agent = PlanningTasks()
            project_management_task = project_management_agent.project_management(agent, 'Simulation', 'Sci-Fi')
        """
        return Task(description=dedent(f"""
            Manage the development of the game.

            Game Type: {game_type}
            Game Genre: {game_genre}

            Your task is to manage the development of the game, taking into account the selected
            game type and genre. Include details such as the key features and target audience.

            The final output should be a comprehensive project status report that outlines the key
            elements of the game.
            
        """),
        agent=agent
        )   

    def delegate_team(self, agent, company, prompt):
        """
        Your task is to delegate the game planning process to your agents.

        Args:
            agent (Agent): The CEO agent responsible for delegating the game planning process.
            company (str): The name of the company.
            prompt (str): The prompt for the game planning process.
            add_job_tool (Tool): The tool to add a job to the job list.
        
        Returns:
            Task: A task representing the delegation of the game planning process.
        
        The agent is tasked with delegating the game planning process to the team of agents.
        The delegation should include details such as the company name, prompt, and job description.
        The final output should be a well-documented delegation that outlines the key elements of the game.

        Tips:            
            - Include any additional information that is crucial for the successful planning of the game.

        Example Usage:
            delegate_team_agent = PlanningTasks()
            delegate_team_task = delegate_team_agent.delegate_team(agent, 'Game Planning Company', 'Create a game plan for a new game.', JobManagementTools.add_job_tool)
        """
        return Task(description=dedent(f"""
            Delegate the game planning process to your agents.
        
            Company: {company}
            Prompt: {prompt}
            Job Description: Plan a game from a prompt given by the CEO: {prompt}
        
            Your task is to delegate the game planning process to your agents.
            Ensure the game plan outlines the key elements of the game.
        """),
        
        agent=agent
        )
