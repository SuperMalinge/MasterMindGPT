from typing import Optional, Dict, Union, List
import autogen
from autogen.agentchat.contrib.teachable_agent import TeachableAgent
import spacy
from spacy.matcher import Matcher
import json

# from listmain import chatoutput


llm_config = {
    "model_name": "gpt3",
    "max_history": 2,
    "max_length": 1000,
    "min_length": 1,
    "temperature": 0.7,
    "repetition_penalty": 1.0,
    "num_beams": 5,
    "do_sample": True,
    "clean_up_tokenization_spaces": True,
    "early_stopping": True,
    "no_repeat_ngram_size": 3,
    "num_return_sequences": 1,
}


class agent_tools:
    def __init__(self, name: str):
        self.tools = agent_tools.tools_list()
        self.name = name


def tools_list() -> List[Dict[str, str]]:
    """Returns a list of tools commonly used for game development in Python along with information about each tool."""
    toolslist = [
        {
            "name": "Pygame",
            "description": "Pygame is a set of Python modules designed for writing 2D video games. It includes computer graphics and sound libraries that can be used with Python.",
        },
        {
            "name": "PyKyra",
            "description": "PyKyra is a fast game development framework for Python. It supports features like direct image reading, sound support (MP3, Ogg Vorbis, Wav), and more.",
        },
        {
            "name": "PyOpenGL",
            "description": "PyOpenGL is a Python binding to OpenGL and related APIs. It can be used for creating 2D and 3D graphics in your game and is interoperable with various GUI libraries.",
        },
        {
            "name": "Panda3D",
            "description": "Panda3D is a powerful 3D game engine for Python. It provides a high-level interface for creating 3D games and simulations, with support for physics, networking, and advanced graphics effects.",
        },
        {
            "name": "Arcade",
            "description": "Arcade is an easy-to-learn Python library for creating 2D video games. It is ideal for people learning to program or developers who want to code 2D games without complex frameworks.",
        },
        {
            "name": "Cocos2d",
            "description": "Cocos2d is a framework for building 2D games, demos, and other graphical/interactive applications. It is based on pyglet and is written in pure Python, making it cross-platform.",
        },
        {
            "name": "Pygame Zero",
            "description": "Pygame Zero is for creating games without boilerplate. It is built on top of Pygame and other Python modules, designed to make it easier for beginners to create games with little or no programming experience.",
        },
        {
            "name": "Pyglet",
            "description": "Pyglet is a cross-platform windowing and multimedia library for Python. It provides an object-oriented interface for creating games and other graphical applications.",
        },
        {
            "name": "PyOgre",
            "description": "PyOgre is a Python binding for the OGRE 3D engine. It allows you to create 3D games and applications using Python and is cross-platform.",
        },
        {
            "name": "PySDL2",
            "description": "PySDL2 is a Python wrapper for the SDL2 library, allowing you to create 2D games and other graphical applications using Python. It is cross-platform.",
        },
        {
            "name": "PySFML",
            "description": "PySFML is a Python binding for the SFML library, enabling the creation of 2D games and other graphical applications using Python. It is cross-platform.",
        },
        {
            "name": "PyXel",
            "description": "PyXel is a Python library for creating 2D games, built on top of Pygame and other Python modules. It is designed to make it easier for beginners to create games with little or no programming experience.",
        },
        {
            "name": "PyDwarf",
            "description": "PyDwarf is a Python library for creating 2D games, built on top of Pygame and other Python modules. It is designed to make it easier for beginners to create games with little or no programming experience.",
        },
    ]
    return toolslist


class PreviousProjectsSuccessRate:
    def __init__(self, success_rates_file):
        # File path to store success rates of previous projects
        self.success_rates_file = success_rates_file

    def load_previous_project_data(self, game_info: Dict) -> float:
        # Load previous project data from a file
        with open(self.success_rates_file, "r") as file:
            success_rates = json.load(file)

        # Check the last successful project based on the given game type and genre
        last_successful_project = None
        for project in reversed(success_rates):
            if (
                project["type"] == game_info["type"]
                and project["genre"] == game_info["genre"]
            ):
                last_successful_project = project
                break

        if last_successful_project:
            return last_successful_project["success_rate"]
        else:
            return 0.0  # If no match is found, return a default value


# Example Usage:
# success_rates_file_path = 'd:\success_rates.json'  # Provide the path to your file
# success_rate_provider = PreviousProjectsSuccessRate(success_rates_file_path)
# game_info = {'type': 'YourGameType', 'genre': 'YourGameGenre'}
# last_success_rate = success_rate_provider.load_previous_project_data(game_info)
# print(f"Last successful project's success rate: {last_success_rate}")


def List() -> List[str]:
    return [
        "2.5D",
        "2.5D Artist",
        "2.5D Animator",
        "2.5D Designer",
        "2.5D Game",
        "2.5D Game Artist",
        "2.5D Game Developer",
        "2.5D Game Designer",
        "2.5D Game Programmer",
        "2.5D Game Scripter",
        "2.5D Graphics",
        "2.5D Graphics Artist",
        "2.5D Graphics Designer",
        "2.5D Graphics Programmer",
        "3D",
        "3D Artist",
        "3D Animator",
        "3D Designer",
        "3D Game",
        "3D Game Artist",
        "3D Game Developer",
        "3D Game Designer",
        "3D Game Programmer",
        "3D Game Scripter",
        "3D Graphics",
        "3D Graphics Artist",
        "3D Graphics Designer",
        "3D Graphics Programmer",
        "4X",
        "AAA Game",
        "Action",
        "Action Game",
        "Action-Adventure",
        "Adventure",
        "Adventure Game",
        "Agile",
        "AI Behavior Trees",
        "Art Style",
        "Artificial Intelligence",
        "Audio",
        "Backward Compatibility",
        "Battle Royale",
        "Blender",
        "Bug Tracking",
        "Casual",
        "Characters",
        "Cinematics",
        "Client-Side",
        "Code Optimization",
        "Combat",
        "Community Management",
        "Console Gaming",
        "Construct 3",
        "Cross-platform",
        "Cutscenes",
        "DLC (Downloadable Content)",
        "Distribution",
        "Early Access",
        "Educational",
        "Esports",
        "Expansion Pack",
        "Fighting",
        "First-person Shooter",
        "Full Release",
        "Gamification",
        "Game Art",
        "Game Audio",
        "Game Design",
        "Game Design Document",
        "Game Development",
        "Game Development Kit",
        "Game Economy",
        "Game Engines",
        "Game Genres",
        "Game Jam",
        "Game Mechanics",
        "Gameplay",
        "Gameplay Balancing",
        "Gameplay Engineer",
        "Gameplay Programmer",
        "Gameplay Scripting",
        "Gameplay Systems Designer",
        "Gameplay Systems Programmer",
        "Gameplay Tester",
        "Game Project Management",
        "Game Prototyping",
        "Game Theory",
        "Game Trailers",
        "Gameplay Systems Designer",
        "Gameplay Systems Programmer",
        "Gaming Forums",
        "Godot",
        "Grand Strategy",
        "Graphics",
        "GUI",
        "Hardware Compatibility",
        "Horror",
        "Idle",
        "In-App Purchases",
        "Indie Game",
        "IP (Intellectual Property)",
        "Level Design",
        "Level Editor",
        "Localization",
        "Marketing",
        "Metroidvania",
        "Microtransactions",
        "MMO",
        "Modding",
        "Multiplayer",
        "Narrative Design",
        "Network Programming",
        "Open World",
        "PC Gaming",
        "Patch",
        "Party",
        "Physics Engine",
        "Platformer",
        "Player Engagement",
        "Procedural Generation",
        "Progression Systems",
        "Publishing",
        "Puzzle",
        "Puzzle Game",
        "Puzzles",
        "Real-time Strategy",
        "Racing",
        "RPG",
        "RPG Maker",
        "Rhythm",
        "Roguelike",
        "Save System",
        "Scrum",
        "Scripting Languages",
        "Server-Side",
        "Simulation",
        "Single-player",
        "Sound Design",
        "Splash Screen",
        "Sports",
        "Stealth",
        "Story",
        "Strategy",
        "Strategy Game",
        "Survival",
        "Tactical",
        "Text-based",
        "Third-person Shooter",
        "Tower Defense",
        "Turn-based Strategy",
        "UI (User Interface)",
        "Unreal Engine",
        "User Experience (UX)",
        "Video Game Music",
        "Voice Acting",
        "Waterfall",
        "WebGL",
        "Worldbuilding",
    ]


class TextAnalyzerAgent(TeachableAgent):
    def __init__(
        self,
        name="analyzer",
        system_message: Optional[str] = None,
        human_input_mode: Optional[str] = "NEVER",
        llm_config: Optional[Dict] = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            human_input_mode=human_input_mode,
            llm_config=llm_config,
            **kwargs,
        )
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self.patterns = [
            {
                "label": "GAME_TYPE",
                "pattern": [{"LOWER": {"IN": List()}}, {"LOWER": "game"}],
            },
            {
                "label": "GAME_GENRE",
                "pattern": [
                    {"LOWER": {"IN": List()}},
                    {"LOWER": "game"},
                    {"LOWER": {"IN": List()}},
                ],
            },
            {
                "label": "GAME_OBJECTIVE",
                "pattern": [
                    {"LOWER": "complete"},
                    {"LOWER": "the"},
                    {"LOWER": "story"},
                ],
            },
            {
                "label": "GAME_OBJECTIVE",
                "pattern": [{"LOWER": "solve"}, {"LOWER": "puzzles"}],
            },
            {
                "label": "GAME_OBJECTIVE",
                "pattern": [{"LOWER": "defeat"}, {"LOWER": "enemies"}],
            },
            {
                "label": "GAME_OBJECTIVE",
                "pattern": [{"LOWER": "collect"}, {"LOWER": "items"}],
            },
            {"label": "GAME_OBJECTIVE", "pattern": [{"LOWER": "survive"}]},
            {"label": "GAME_OBJECTIVE", "pattern": [{"LOWER": "escape"}]},
            {
                "label": "GAME_OBJECTIVE",
                "pattern": [{"LOWER": "build"}, {"LOWER": "and"}, {"LOWER": "manage"}],
            },
            {
                "label": "GAME_OBJECTIVE",
                "pattern": [
                    {"LOWER": "create"},
                    {"LOWER": "and"},
                    {"LOWER": "customize"},
                ],
            },
            {"label": "GAME_PLATFORM", "pattern": [{"LOWER": "mobile"}]},
            {"label": "GAME_PLATFORM", "pattern": [{"LOWER": "console"}]},
            {"label": "GAME_PLATFORM", "pattern": [{"LOWER": "pc"}]},
            {
                "label": "GAME_MECHANICS",
                "pattern": [{"LOWER": "physics"}, {"LOWER": "engine"}],
            },
            {
                "label": "GAME_MECHANICS",
                "pattern": [{"LOWER": "artificial"}, {"LOWER": "intelligence"}],
            },
            {
                "label": "GAME_MECHANICS",
                "pattern": [{"LOWER": "procedural"}, {"LOWER": "generation"}],
            },
            {
                "label": "GAME_MECHANICS",
                "pattern": [{"LOWER": "progression"}, {"LOWER": "systems"}],
            },
            {
                "label": "GAME_MECHANICS",
                "pattern": [{"LOWER": "save"}, {"LOWER": "system"}],
            },
            {"label": "GAME_MECHANICS", "pattern": [{"LOWER": "cinematics"}]},
            {"label": "GAME_MECHANICS", "pattern": [{"LOWER": "cutscenes"}]},
            {
                "label": "GAME_MECHANICS",
                "pattern": [{"LOWER": "scripting"}, {"LOWER": "languages"}],
            },
            {"label": "GAME_MECHANICS", "pattern": [{"LOWER": "middleware"}]},
            {"label": "GAME_MECHANICS", "pattern": [{"LOWER": "webgl"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "level"}, {"LOWER": "design"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "game"}, {"LOWER": "design"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "game"}, {"LOWER": "engine"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "game"}, {"LOWER": "development"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "game"}, {"LOWER": "programming"}],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "game"}, {"LOWER": "art"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "game"}, {"LOWER": "audio"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "game"},
                    {"LOWER": "design"},
                    {"LOWER": "document"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "game"},
                    {"LOWER": "development"},
                    {"LOWER": "kit"},
                ],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "gameplay"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "gameplay"}, {"LOWER": "programmer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "gameplay"}, {"LOWER": "scripting"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "gameplay"},
                    {"LOWER": "systems"},
                    {"LOWER": "designer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "gameplay"},
                    {"LOWER": "systems"},
                    {"LOWER": "programmer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "gameplay"}, {"LOWER": "tester"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "gameplay"}, {"LOWER": "engineer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "gameplay"}, {"LOWER": "programmer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "gameplay"}, {"LOWER": "scripter"}],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "2d"}]},
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "3d"}]},
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "2.5d"}]},
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "2d"}, {"LOWER": "artist"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "animator"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "designer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "graphics"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "artist"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "designer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "programmer"},
                ],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "2d"}, {"LOWER": "game"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "game"}, {"LOWER": "artist"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "game"}, {"LOWER": "designer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "game"}, {"LOWER": "developer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2d"},
                    {"LOWER": "game"},
                    {"LOWER": "programmer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2d"}, {"LOWER": "game"}, {"LOWER": "scripter"}],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "3d"}, {"LOWER": "artist"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "3d"}, {"LOWER": "animator"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "3d"}, {"LOWER": "designer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "3d"}, {"LOWER": "graphics"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "3d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "artist"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "3d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "designer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "3d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "programmer"},
                ],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "3d"}, {"LOWER": "game"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "3d"}, {"LOWER": "game"}, {"LOWER": "artist"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "3d"}, {"LOWER": "game"}, {"LOWER": "designer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "3d"}, {"LOWER": "game"}, {"LOWER": "developer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "3d"},
                    {"LOWER": "game"},
                    {"LOWER": "programmer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2.5d"}, {"LOWER": "artist"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2.5d"}, {"LOWER": "animator"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2.5d"}, {"LOWER": "designer"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2.5d"}, {"LOWER": "graphics"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2.5d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "artist"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2.5d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "designer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2.5d"},
                    {"LOWER": "graphics"},
                    {"LOWER": "programmer"},
                ],
            },
            {"label": "GAME_DESIGN", "pattern": [{"LOWER": "2.5d"}, {"LOWER": "game"}]},
            {
                "label": "GAME_DESIGN",
                "pattern": [{"LOWER": "2.5d"}, {"LOWER": "game"}, {"LOWER": "artist"}],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2.5d"},
                    {"LOWER": "game"},
                    {"LOWER": "designer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2.5d"},
                    {"LOWER": "game"},
                    {"LOWER": "developer"},
                ],
            },
            {
                "label": "GAME_DESIGN",
                "pattern": [
                    {"LOWER": "2.5d"},
                    {"LOWER": "game"},
                    {"LOWER": "programmer"},
                ],
            },
            {
                "label": "GAME_PLATFORM",
                "pattern": [{"LOWER": "mobile"}, {"LOWER": "gaming"}],
            },
            {
                "label": "GAME_PLATFORM",
                "pattern": [{"LOWER": "console"}, {"LOWER": "gaming"}],
            },
            {
                "label": "GAME_PLATFORM",
                "pattern": [{"LOWER": "pc"}, {"LOWER": "gaming"}],
            },
            {"label": "GAME_ECONOMY", "pattern": [{"LOWER": "microtransactions"}]},
            {
                "label": "GAME_ECONOMY",
                "pattern": [
                    {"LOWER": "dlc"},
                    {"LOWER": "downloadable"},
                    {"LOWER": "content"},
                ],
            },
            {"label": "GAME_ECONOMY", "pattern": [{"LOWER": "patch"}]},
            {
                "label": "GAME_ECONOMY",
                "pattern": [{"LOWER": "expansion"}, {"LOWER": "pack"}],
            },
            {
                "label": "GAME_ECONOMY",
                "pattern": [{"LOWER": "in-app"}, {"LOWER": "purchases"}],
            },
            {"label": "GAME_ECONOMY", "pattern": [{"LOWER": "cross-platform"}]},
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "indie"}, {"LOWER": "game"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "aaa"}, {"LOWER": "game"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "early"}, {"LOWER": "access"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "full"}, {"LOWER": "release"}],
            },
            {"label": "GAME_DEVELOPMENT", "pattern": [{"LOWER": "marketing"}]},
            {"label": "GAME_DEVELOPMENT", "pattern": [{"LOWER": "publishing"}]},
            {"label": "GAME_DEVELOPMENT", "pattern": [{"LOWER": "distribution"}]},
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "intellectual"}, {"LOWER": "property"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "game"}, {"LOWER": "theory"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "level"}, {"LOWER": "editor"}],
            },
            {"label": "GAME_DEVELOPMENT", "pattern": [{"LOWER": "modding"}]},
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "community"}, {"LOWER": "management"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "version"}, {"LOWER": "control"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "bug"}, {"LOWER": "tracking"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [
                    {"LOWER": "game"},
                    {"LOWER": "dev"},
                    {"LOWER": "conference"},
                ],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "game"}, {"LOWER": "jam"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "code"}, {"LOWER": "optimization"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "hardware"}, {"LOWER": "compatibility"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "network"}, {"LOWER": "programming"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "art"}, {"LOWER": "style"}],
            },
            {"label": "GAME_DEVELOPMENT", "pattern": [{"LOWER": "worldbuilding"}]},
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "narrative"}, {"LOWER": "design"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "sound"}, {"LOWER": "design"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "game"}, {"LOWER": "economy"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "ai"}, {"LOWER": "behavior"}, {"LOWER": "trees"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "splash"}, {"LOWER": "screen"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "game"}, {"LOWER": "trailers"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "video"}, {"LOWER": "game"}, {"LOWER": "music"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "voice"}, {"LOWER": "acting"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "gaming"}, {"LOWER": "forums"}],
            },
            {
                "label": "GAME_DEVELOPMENT",
                "pattern": [{"LOWER": "backward"}, {"LOWER": "compatibility"}],
            },
            {"label": "GAME_DEVELOPMENT", "pattern": [{"LOWER": "esports"}]},
            {"label": "GAME_ENGINES", "pattern": [{"LOWER": "unity"}]},
            {"label": "GAME_ENGINES", "pattern": [{"LOWER": "blender"}]},
            {
                "label": "GAME_ENGINES",
                "pattern": [{"LOWER": "unreal"}, {"LOWER": "engine"}],
            },
            {
                "label": "GAME_ENGINES",
                "pattern": [
                    {"LOWER": "gamemaker"},
                    {"LOWER": "studio"},
                    {"LOWER": "2"},
                ],
            },
            {"label": "GAME_ENGINES", "pattern": [{"LOWER": "godot"}]},
            {
                "label": "GAME_ENGINES",
                "pattern": [{"LOWER": "construct"}, {"LOWER": "3"}],
            },
            {
                "label": "GAME_ENGINES",
                "pattern": [{"LOWER": "rpg"}, {"LOWER": "maker"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "adventure"}, {"LOWER": "game"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "puzzle"}, {"LOWER": "game"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "strategy"}, {"LOWER": "game"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "action"}, {"LOWER": "game"}],
            },
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "rpg"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "simulation"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "sports"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "racing"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "fighting"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "stealth"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "survival"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "horror"}]},
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "battle"}, {"LOWER": "royale"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "first-person"}, {"LOWER": "shooter"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "third-person"}, {"LOWER": "shooter"}],
            },
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "platformer"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "metroidvania"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "mmo"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "roguelike"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "rhythm"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "party"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "educational"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "idle"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "casual"}]},
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "text-based"}]},
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "visual"}, {"LOWER": "novel"}],
            },
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "sandbox"}]},
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "open"}, {"LOWER": "world"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "real-time"}, {"LOWER": "strategy"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "turn-based"}, {"LOWER": "strategy"}],
            },
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "tower"}, {"LOWER": "defense"}],
            },
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "4x"}]},
            {
                "label": "GAME_GENRES",
                "pattern": [{"LOWER": "grand"}, {"LOWER": "strategy"}],
            },
            {"label": "GAME_GENRES", "pattern": [{"LOWER": "tactical"}]},
        ]
        self.matcher.add("GAME_TYPE", None, self.patterns[0])
        self.matcher.add("GAME_GENRE", None, self.patterns[1])
        self.matcher.add("GAME_OBJECTIVE", None, self.patterns[2])
        self.matcher.add("GAME_DEVELOPMENT", None, self.patterns[3])
        self.matcher.add("GAME_ENGINES", None, self.patterns[4])
        self.matcher.add("GAME_PLATFORM", None, self.patterns[5])
        self.matcher.add("GAME_MECHANICS", None, self.patterns[6])
        self.matcher.add("GAME_DESIGN", None, self.patterns[7])
        self.matcher.add("GAME_ECONOMY", None, self.patterns[8])
        self.matcher.add("GAME_GENRES", None, self.patterns[9])

    def choose_game_tools(self, game_type: str, game_genre: str) -> List[str]:
        design = {"type": game_type, "genre": game_genre}
        tools = GameTools.identify_required_tools(design)
        if tools is None:
            # If no tools are identified, select default tools
            tools = self.choose_default_tools(game_type, game_genre)
        return tools

    # Additional methods like design_game, design_interactive_structure, design_game_objective, and design_game_elements can have their logic similarly implemented.

    def design_game(self, game_type: str, game_genre: str) -> Dict:
        if game_type == "Adventure Game" and game_genre == "Action-Adventure":
            return {
                "type": "Adventure Game",
                "genre": "Action-Adventure",
                "interactive_structure": "Single-player",
                "objective": "Complete the story by solving puzzles and defeating enemies",
                "elements": [
                    "Story",
                    "Puzzles",
                    "Combat",
                    "Enemies",
                    "Boss Fights",
                    "Objectives",
                    "Rewards",
                    "Story",
                    "Puzzles",
                    "Combat",
                    "Enemies",
                    "Boss Fights",
                    "Objectives",
                    "Rewards",
                ],
            }
        elif game_type == "Puzzle Game" and game_genre == "Strategy":
            return {
                "type": "Puzzle Game",
                "genre": "Strategy",
                "interactive_structure": "Single-player",
                "objective": "Solve puzzles to complete the game",
                "elements": [
                    "Puzzles",
                    "difficulties",
                    "levels",
                    "hints",
                    "challenges",
                    "strategies",
                    "rewards",
                    "enemies",
                    "bosses",
                    "objectives",
                    "story",
                    "puzzles",
                    "difficulties",
                    "levels",
                    "hints",
                    "challenges",
                    "strategies",
                ],
            }
        elif game_type == "Role-playing Game" and game_genre == "Fantasy":
            return {
                "type": "Role-playing Game",
                "genre": "Fantasy",
                "interactive_structure": "Multiplayer",
                "objective": "Complete quests and level up your character",
                "elements": [
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Story",
                    "Characters",
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Story",
                    "Characters",
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Story",
                    "Characters",
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Story",
                    "Characters",
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Story",
                    "Characters",
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Story",
                    "Characters",
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Characters",
                ],
            }
        elif game_type == "Simulation Game" and game_genre == "Life Simulation":
            return {
                "type": "Simulation Game",
                "genre": "Life Simulation",
                "interactive_structure": "Single-player",
                "objective": "Manage a virtual life and achieve goals",
                "elements": [
                    "Resource Management",
                    "Goal-setting",
                    "Story",
                    "Characters",
                    "Relationships",
                    "Skills",
                    "Stats",
                    "Jobs",
                    "Hobbies",
                    "Activities",
                    "Events",
                    "Achievements",
                    "Badges",
                    "Quests",
                    "Story",
                    "Characters",
                    "Relationships",
                    "Skills",
                    "Stats",
                    "Jobs",
                    "Hobbies",
                    "Activities",
                    "Events",
                    "Achievements",
                    "Badges",
                    "Quests",
                    "Story",
                    "Characters",
                    "Relationships",
                    "Skills",
                    "Stats",
                    "Jobs",
                    "Hobbies",
                    "Activities",
                    "Events",
                    "Achievements",
                    "Badges",
                    "Quests",
                    "Story",
                    "Characters",
                    "Relationships",
                    "Skills",
                    "Stats",
                    "Jobs",
                    "Hobbies",
                    "Activities",
                    "Events",
                    "Achievements",
                    "Badges",
                    "Quests",
                    "Story",
                    "Characters",
                    "Relationships",
                    "Skills",
                    "Stats",
                    "Jobs",
                    "Hobbies",
                    "Activities",
                    "Events",
                    "Achievements",
                    "Badges",
                ],
            }
        elif game_type == "Sports Game" and game_genre == "Simulation":
            return {
                "type": "Sports Game",
                "genre": "Simulation",
                "interactive_structure": "Multiplayer",
                "objective": "Compete against other players in realistic sports simulations",
                "elements": [
                    "Realistic Physics",
                    "Team Management",
                    "Multiplayer",
                    "Leaderboards",
                    "Story",
                    "Characters",
                    "Teams",
                    "Players",
                    "Stadiums",
                    "Equipment",
                    "Uniforms",
                    "Stats",
                    "Seasons",
                    "Tournaments",
                    "Leagues",
                    "Playoffs",
                    "Championships",
                    "Awards",
                    "Drafts",
                    "Free Agency",
                    "Trades",
                    "Injuries",
                    "Retirements",
                    "Contracts",
                    "Salary Cap",
                    "Roster",
                    "Depth Chart",
                    "Lineup",
                    "Strategy",
                    "Playbooks",
                    "Game Plans",
                    "Scouting",
                    "Training",
                    "Practice",
                    "Coaching",
                    "Playcalling",
                    "Stats",
                    "Scouting",
                    "Training",
                    "Practice",
                    "Coaching",
                    "Playcalling",
                    "Stats",
                    "Scouting",
                    "Training",
                    "Practice",
                    "Coaching",
                    "Playcalling",
                    "Stats",
                ],
            }
        elif game_type == "First-person Shooter" and game_genre == "Action":
            return {
                "type": "First-person Shooter",
                "genre": "Action",
                "interactive_structure": "Multiplayer",
                "objective": "Eliminate other players in fast-paced combat",
                "elements": [
                    "Fast-paced Combat",
                    "Weapon Customization",
                    "Multiplayer",
                    "Leaderboards",
                    "Story",
                    "Characters",
                    "Maps",
                    "Weapons",
                    "Ammo",
                    "Health",
                    "Armor",
                    "Power-ups",
                    "Aiming",
                    "Shooting",
                    "Reloading",
                    "Weapon Recoil",
                    "Weapon Spread",
                    "Weapon Damage",
                    "Weapon Accuracy",
                    "Weapon Range",
                    "Weapon Fire Rate",
                    "Weapon Hitboxes",
                    "Weapon Collision",
                    "Weapon Upgrades",
                    "Weapon Attachments",
                    "Weapon Skins",
                    "Weapon Ammo",
                    "Weapon Ammo Types",
                    "Weapon Ammo Capacity",
                    "Weapon Ammo Pickups",
                    "Weapon Ammo Resupply",
                    "Weapon Ammo Regeneration",
                    "Weapon Ammo Crafting",
                    "Weapon Ammo Upgrades",
                    "Weapon Ammo Management",
                    "Weapon Ammo Conservation",
                    "Weapon Ammo Depletion",
                    "Weapon Ammo Loss",
                    "Weapon Ammo Sharing",
                    "Weapon Ammo Stealing",
                    "Weapon Ammo Trading",
                    "Weapon Ammo Economy",
                    "Weapon Ammo Scarcity",
                    "Weapon Ammo Shortage",
                    "Weapon Ammo Surplus",
                    "Weapon Ammo Stockpiling",
                    "Weapon Ammo Hoarding",
                    "Weapon Ammo Wasting",
                    "Weapon Ammo Overflow",
                    "Weapon Ammo Overflows",
                    "Weapon Ammo Overfill",
                    "Weapon Ammo Overload",
                    "Weapon Ammo Overuse",
                    "Weapon Ammo Overspend",
                ],
            }
        elif game_type == "Strategy Game" and game_genre == "Real-time":
            return {
                "type": "Strategy Game",
                "genre": "Real-time",
                "interactive_structure": "Multiplayer",
                "objective": "Build and manage a base while competing against other players",
                "elements": [
                    "Base-building",
                    "Resource Management",
                    "Multiplayer",
                    "Real-time Combat",
                    "Unit Management",
                    "Unit Customization",
                    "Unit Upgrades",
                    "Unit Abilities",
                    "Unit Classes",
                    "Unit Counters",
                    "Unit Stats",
                    "Unit Movement",
                    "Unit Positioning",
                    "Unit Formations",
                    "Unit AI",
                    "Unit Pathfinding",
                    "Unit Targeting",
                    "Unit Spawning",
                    "Unit Training",
                    "Unit Production",
                    "Unit Deployment",
                    "Unit Control",
                    "Unit Health",
                    "Unit Damage",
                    "Unit Armor",
                    "Unit Speed",
                    "Unit Range",
                    "Unit Line of Sight",
                    "Unit Hitboxes",
                    "Unit Collision",
                    "Unit Death",
                    "Unit Respawning",
                    "Unit Reviving",
                    "Unit Healing",
                    "Unit Repairing",
                    "Unit Upkeep",
                    "Unit Supply",
                    "Unit Energy",
                    "Unit Fuel",
                    "Unit Ammo",
                    "Unit Morale",
                    "Unit Experience",
                    "Unit Leveling",
                    "Unit Abilities",
                    "Unit Upgrades",
                    "Unit Classes",
                    "Unit Counters",
                    "Unit Stats",
                    "Unit Movement",
                    "Unit Positioning",
                    "Unit Formations",
                    "Unit AI",
                    "Unit Pathfinding",
                    "Unit Targeting",
                    "Unit Spawning",
                    "Unit Training",
                    "Unit Production",
                    "Unit Deployment",
                    "Unit Control",
                    "Unit Health",
                    "Unit Damage",
                    "Unit Armor",
                    "Unit Speed",
                    "Unit Range",
                    "Unit Line of Sight",
                    "Unit Hitboxes",
                    "Unit Collision",
                    "Unit Death",
                    "Unit Respawning",
                    "Unit Reviving",
                    "Unit Healing",
                    "Unit Repairing",
                    "Unit Upkeep",
                    "Unit Supply",
                    "Unit Energy",
                    "Unit Fuel",
                    "Unit Ammo",
                    "Unit Morale",
                    "Unit Experience",
                    "Unit Leveling",
                    "Maps",
                    "Terrain",
                    "Resources",
                    "Buildings",
                    "Defenses",
                    "Turrets",
                    "Vehicles",
                    "Characters",
                    "Story",
                ],
            }
        elif game_type == "Educational Game" and game_genre == "Math":
            return {
                "type": "Educational Game",
                "genre": "Math",
                "interactive_structure": "Single-player",
                "objective": "Learn math concepts through interactive gameplay",
                "elements": [
                    "Math Problems",
                    "Interactive Feedback",
                    "Progress Tracking",
                    "Leaderboards",
                    "Achievements",
                    "Badges",
                    "Story",
                ],
            }
        elif game_type == "Horror Game" and game_genre == "Survival":
            return {
                "type": "Horror Game",
                "genre": "Survival",
                "interactive_structure": "Single-player",
                "objective": "Survive in a terrifying environment",
                "elements": [
                    "Jump Scares",
                    "Stealth",
                    "Puzzles",
                    "Combat",
                    "Resource Management",
                    "Environmental Hazards",
                    "Enemies",
                    "Bosses",
                    "Story",
                ],
            }
        elif game_type == "Racing Game" and game_genre == "Arcade":
            return {
                "type": "Racing Game",
                "genre": "Arcade",
                "interactive_structure": "Multiplayer",
                "objective": "Race against other players in high-speed competitions",
                "elements": [
                    "Power-ups",
                    "Drifting",
                    "Boosting",
                    "Multiplayer",
                    "Leaderboards",
                    "Customization",
                    "Story",
                    "Characters",
                    "Vehicles",
                    "Tracks",
                    "Time Trials",
                    "Race Courses",
                    "Laps",
                    "Obstacles",
                    "Hazards",
                    "AI",
                    "Difficulty Levels",
                    "Tuning",
                ],
            }
        elif game_type == "Card Game" and game_genre == "Strategy":
            return {
                "type": "Card Game",
                "genre": "Strategy",
                "interactive_structure": "Multiplayer",
                "objective": "Outsmart your opponents with strategic card play",
                "elements": [
                    "Deck-building",
                    "Card Abilities",
                    "Multiplayer",
                    "Turn-based Combat",
                    "Resource Management",
                    "Card Collection",
                    "Card Trading",
                ],
            }
        elif game_type == "Platformer" and game_genre == "Action":
            return {
                "type": "Platformer",
                "genre": "Action",
                "interactive_structure": "Single-player",
                "objective": "Navigate through levels and defeat enemies",
                "elements": [
                    "Jumping",
                    "Combat",
                    "Level Design",
                    "Power-ups",
                    "Collectibles",
                    "Bosses",
                    "Story",
                    "Characters",
                    "Enemies",
                    "Hazards",
                    "Obstacles",
                    "Puzzles",
                    "Secrets",
                    "Rewards",
                    "Leaderboards",
                    "Achievements",
                    "Badges",
                ],
            }
        elif game_type == "City-building Game" and game_genre == "Simulation":
            return {
                "type": "City-building Game",
                "genre": "Simulation",
                "interactive_structure": "Single-player",
                "objective": "Build and manage a city",
                "elements": [
                    "Resource Management",
                    "City Planning",
                    "Economy",
                    "Population",
                    "Infrastructure",
                    "Zoning",
                    "Taxes",
                    "Budget",
                    "Disasters",
                    "Story",
                    "Quests",
                    "Characters",
                ],
            }
        elif game_type == "Rhythm Game" and game_genre == "Music":
            return {
                "type": "Rhythm Game",
                "genre": "Music",
                "interactive_structure": "Single-player",
                "objective": "Hit the right notes in time with the music",
                "elements": ["Music Tracks", "Beat-matching"],
            }
        elif game_type == "Fighting Game" and game_genre == "Action":
            return {
                "type": "Fighting Game",
                "genre": "Action",
                "interactive_structure": "Multiplayer",
                "objective": "Defeat your opponents in one-on-one combat",
                "elements": [
                    "Combo Moves",
                    "Special Attacks",
                    "Health Bars",
                    "Multiplayer",
                    "Story",
                    "Characters",
                    "Stages",
                    "Power-ups",
                    "Leaderboards",
                    "Achievements",
                    "Badges",
                ],
            }
        elif game_type == "Tower Defense Game" and game_genre == "Strategy":
            return {
                "type": "Tower Defense Game",
                "genre": "Strategy",
                "interactive_structure": "Single-player",
                "objective": "Defend your base against waves of enemies",
                "elements": [
                    "Tower Placement",
                    "Upgrade System",
                    "Waves",
                    "Enemies",
                    "Base",
                    "Story",
                    "Characters",
                ],
            }
        elif game_type == "Stealth Game" and game_genre == "Action-Adventure":
            return {
                "type": "Stealth Game",
                "genre": "Action-Adventure",
                "interactive_structure": "Single-player",
                "objective": "Complete objectives without being detected",
                "elements": [
                    "Sneaking",
                    "Disguises",
                    "Distracting Enemies",
                    "Hiding",
                    "Silent Takedowns",
                    "Stealing",
                    "Pickpocketing",
                    "Lockpicking",
                    "Hacking",
                    "Security Cameras",
                    "Alarms",
                    "Security Guards",
                    "Enemies",
                    "Story",
                ],
            }
        elif game_type == "Survival Game" and game_genre == "Open-world":
            return {
                "type": "Survival Game",
                "genre": "Open-world",
                "interactive_structure": "Single-player",
                "objective": "Survive in a harsh environment with limited resources",
                "elements": [
                    "Resource Gathering",
                    "Crafting",
                    "Base-building",
                    "Hunger",
                    "Thirst",
                    "Temperature",
                    "Health",
                    "Stamina",
                    "Weather",
                    "Day/Night Cycle",
                    "Wildlife",
                    "Hunting",
                    "Fishing",
                    "Leveling",
                    "Environmental Hazards",
                    "Enemies",
                    "Bosses",
                    "Story",
                ],
            }
        elif game_type == "Party Game" and game_genre == "Casual":
            return {
                "type": "Party Game",
                "genre": "Casual",
                "interactive_structure": "Multiplayer",
                "objective": "Compete against your friends in fun mini-games",
                "elements": [
                    "Mini-games",
                    "Multiplayer",
                    "Leaderboards",
                    "Achievements",
                    "Badges",
                ],
            }
        elif game_type == "RPG" and game_genre == "Open-world":
            return {
                "type": "RPG",
                "genre": "Open-world",
                "interactive_structure": "Single-player",
                "objective": "Explore a vast open world and complete quests",
                "elements": [
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Looting",
                    "Crafting",
                    "Resource Gathering",
                    "Skill Trees",
                    "Leveling",
                    "Story",
                    "Puzzles",
                ],
            }
        elif game_type == "MMORPG" and game_genre == "Fantasy":
            return {
                "type": "MMORPG",
                "genre": "Fantasy",
                "interactive_structure": "Multiplayer",
                "objective": "Explore a vast open world, complete quests, and level up your character",
                "elements": [
                    "Quests",
                    "Character Customization",
                    "Combat",
                    "Multiplayer",
                    "Guilds",
                    "Raids",
                    "Dungeons",
                    "Looting",
                    "Crafting",
                    "Resource Gathering",
                    "Skill Trees",
                    "Leveling",
                ],
            }
        elif game_type == "Roguelike" and game_genre == "Dungeon Crawler":
            return {
                "type": "Roguelike",
                "genre": "Dungeon Crawler",
                "interactive_structure": "Single-player",
                "objective": "Explore randomly generated dungeons and defeat monsters",
                "elements": [
                    "Random Generation",
                    "Permadeath",
                    "Combat",
                    "Looting",
                    "Crafting",
                    "Resource Gathering",
                    "Skill Trees",
                    "Leveling",
                    "Story",
                    "Puzzles",
                    "Bosses",
                    "Enemies",
                    "Rewards",
                ],
            }
        elif game_type == "Metroidvania" and game_genre == "Action-Adventure":
            return {
                "type": "Metroidvania",
                "genre": "Action-Adventure",
                "interactive_structure": "Single-player",
                "objective": "Explore a large interconnected world and gain new abilities",
                "elements": [
                    "Exploration",
                    "Power-ups",
                    "Combat",
                    "Looting",
                    "Crafting",
                    "Resource Gathering",
                    "Skill Trees",
                    "Leveling",
                    "Story",
                    "Puzzles",
                    "Bosses",
                    "Enemies",
                    "Rewards",
                ],
            }
        elif game_type == "Visual Novel" and game_genre == "Romance":
            return {
                "type": "Visual Novel",
                "genre": "Romance",
                "interactive_structure": "Single-player",
                "objective": "Experience a romantic story through text and images",
                "elements": [
                    "Story",
                    "Choices",
                    "Multiple Endings",
                    "Emotional Tension",
                    "Emotional Resolution",
                    "Emotional Connection",
                    "Emotional Development",
                    "Emotional Expression",
                    "Emotional Impact",
                    "Emotional Depth",
                    "Emotional Complexity",
                    "Emotional Engagement",
                    "Emotional Immersion",
                    "Emotional Satisfaction",
                    "relationships",
                ],
            }
        elif game_type == "Idle Game" and game_genre == "Simulation":
            return {
                "type": "Idle Game",
                "genre": "Simulation",
                "interactive_structure": "Single-player",
                "objective": "Progress through the game by idling and upgrading",
                "elements": [
                    "Upgrades",
                    "Resource Management",
                    "Progression",
                    "Story",
                    "Characters",
                    "Quests",
                    "Achievements",
                    "Badges",
                    "Leaderboards",
                ],
            }
        elif game_type == "Battle Royale" and game_genre == "Action":
            return {
                "type": "Battle Royale",
                "genre": "Action",
                "interactive_structure": "Multiplayer",
                "objective": "Be the last player standing in a shrinking arena",
                "elements": [
                    "Survival",
                    "Looting",
                    "Combat",
                    "Multiplayer",
                    "Leaderboards",
                    "Story",
                    "Characters",
                    "Weapons",
                    "Armor",
                    "Health",
                    "Ammo",
                    "Power-ups",
                    "Vehicles",
                    "Map",
                    "Shrinking Arena",
                    "Hazards",
                    "Obstacles",
                    "Enemies",
                    "Bosses",
                    "Rewards",
                ],
            }
        elif game_type == "Escape Room Game" and game_genre == "Puzzle":
            return {
                "type": "Escape Room Game",
                "genre": "Puzzle",
                "interactive_structure": "Single-player",
                "objective": "Escape from a series of rooms by solving puzzles",
                "elements": [
                    "Puzzles",
                    "Mystery",
                    "Story",
                    "Characters",
                    "Enemies",
                    "Bosses",
                    "Rewards",
                ],
            }
        else:
            return {
                "type": game_type,
                "genre": game_genre,
                "interactive_structure": "Unknown",
                "objective": "Unknown",
                "elements": [],
            }

    def design_interactive_structure(self, game_type: str, game_genre: str) -> str:
        # Lookup the suggested interactive structures based on the provided type and genre
        type_interaction = game_type_to_interactions.get(game_type)
        genre_interaction = genre_to_interactions.get(game_genre)

        # Define a dictionary mapping game types to common interactive structures
        game_type_to_interactions = {
            "RPG": "dialogue and choice systems",
            "Action": "combat mechanics",
            "Adventure": "action based situations and exploration",
            "Strategy": "resource management and strategic decision making",
            "Simulation": "complex systems modeling real world processes",
            "Survival": "survival systems",
            "Shooter": "combat mechanics",
            "Stealth": "stealth mechanics",
            "Sports": "sports mechanics",
            "Racing": "racing mechanics",
            "Fighting": "fighting mechanics",
            "Platformer": "platforming mechanics",
            "Card": "card mechanics",
            "Party": "party mechanics",
            "Rhythm": "rhythm mechanics",
            "Educational": "educational mechanics",
            "City-building": "city-building mechanics",
            "Tower Defense": "tower defense mechanics",
            "MMO": "multiplayer interaction",
            "Metroidvania": "exploration mechanics",
            "Visual Novel": "dialogue and choice systems",
            "Idle": "idle mechanics",
            "Battle Royale": "combat mechanics",
            "Escape Room": "puzzle solving and exploration",
            "Open World": "player-environment interaction",
            "Multiplayer": "multiplayer interaction",
            "Narrative": "dialogue and choice systems",
            "Progression": "progression and reward systems",
        }

        # Define a dictionary mapping genres to common interactive structures
        genre_to_interactions = {
            "Fantasy": "fantasy mechanics",
            "Sci-fi": "sci-fi mechanics",
            "Horror": "horror mechanics",
            "Mystery": "mystery mechanics",
            "Romance": "romance mechanics",
            "Comedy": "comedy mechanics",
            "Drama": "drama mechanics",
            "Thriller": "thriller mechanics",
            "Action": "action mechanics",
            "Adventure": "adventure mechanics",
            "casual": "casual mechanics",
        }

        # Return a string describing the suggested interactive structure
        return f"Suggested interactions: {type_interaction} and {genre_interaction}"


class CreateProjectPlan:
    def create_project_plan(self, design: Dict) -> Dict:
        # Example logic: Create a project plan based on the game design
        # Placeholder logic:
        # Determine the development process, tools, project management strategy, difficulty level, and requirements based on the game design
        development_process = self.define_development_process(design)
        tools = self.identify_required_tools(design)
        project_management_strategy = self.define_project_management_strategy()
        difficulty = TextAnalyzerAgent().difficulty_level(design)
        requirements = TextAnalyzerAgent().requirement_analysis(design)
        return {
            "development_process": development_process,
            "tools": tools,
            "project_management": project_management_strategy,
            "difficulty_level": difficulty,
            "requirements": requirements,
        }


class PlanProject(TextAnalyzerAgent, CreateProjectPlan):
    def plan_project(self, text: str) -> Dict:
        game_info = self.analyze_text(text)
        # Check if all required keys are present in game_info before proceeding
        required_keys = [
            "type",
            "genre",
            "development_process",
            "GUI_template",
            "objective",
            "elements",
            "interactive_structure",
            "story_template",
        ]
        if all(key in game_info for key in required_keys):
            # Additional elements for comprehensive AI-driven planning
            additional_keys = [
                "previous_project_data",
                "competitor_analysis",
                "algorithmic_optimization",
                "tools",
                "feedback_loops",
                "project_constraints",
            ]
            if all(key in game_info for key in additional_keys):
                game_design = self.design_game(
                    game_info["type"],
                    game_info["genre"],
                    game_info["development_process"],
                    game_info["story_template"],
                    game_info["GUI_template"],
                    game_info["interactive_structure"],
                    game_info["objective"],
                    game_info["elements"],
                )
                project_plan = self.create_project_plan(game_design)
                return (
                    project_plan  # Returning the project plan for AI-driven processing
                )
            else:
                # Raise an error if essential AI-driven planning keys are missing
                raise KeyError("Insufficient AI-driven planning information.")
        else:
            # Raise an error if fundamental keys are missing
            raise KeyError("Insufficient basic information for project planning.")

    def choose_gui_template(self, game_info: dict) -> str:
        game_type_to_gui = {
            "RPG": "RPG_GUI_Template",
            "Adventure Game": "Adventure_GUI_Template",
            "Puzzle Game": "Puzzle_GUI_Template",
            "Simulation Game": "Simulation_GUI_Template",
            "Sports Game": "Sports_GUI_Template",
            "First-person Shooter": "FPS_GUI_Template",
            "Strategy Game": "Strategy_GUI_Template",
            "Educational Game": "Educational_GUI_Template",
            "Horror Game": "Horror_GUI_Template",
            "Racing Game": "Racing_GUI_Template",
            "Card Game": "Card_GUI_Template",
            "Platformer": "Platformer_GUI_Template",
            "City-building Game": "City-building_GUI_Template",
            "Rhythm Game": "Rhythm_GUI_Template",
            "Fighting Game": "Fighting_GUI_Template",
            "Tower Defense Game": "Tower_Defense_GUI_Template",
            "Stealth Game": "Stealth_GUI_Template",
            "Survival Game": "Survival_GUI_Template",
            "Party Game": "Party_GUI_Template",
            "Visual Novel": "Visual_Novel_GUI_Template",
            "Idle Game": "Idle_GUI_Template",
            "Battle Royale": "Battle_Royale_GUI_Template",
            "Escape Room Game": "Escape_Room_GUI_Template",
            # Additional game types and their GUI templates
        }

        # Check if the game type exists in the mapping dictionary
        if game_info["type"] in game_type_to_gui:
            return game_type_to_gui[game_info["type"]]
        else:
            return "Default_GUI_Template"  # Return a default template if the type is not found

    def determine_development_process(self, design: Dict) -> str:
        game_type = design.get("type", "")

        game_types_to_processes = {
            "Adventure Game": "Agile",  # Constant narrative/feature iteration
            "Puzzle Game": "Scrum",  # Structured for frequent iterations and testing
            "Action Game": "Kanban",  # Need for a steady workflow and efficiency
            "Simulation Game": "Lean",  # Optimizing resources, reducing waste
            "Sports Game": "Agile",  # Need for adaptability and continuous improvement
            "First-person Shooter": "Scrum",  # Detailed gameplay mechanics and balancing
            "Strategy Game": "Kanban",  # Need for optimization and workflow management
            "Educational Game": "Lean",  # Focused on efficiency and optimized development
            "Horror Game": "Agile",  # Adaptive development for horror elements
            "Racing Game": "Scrum",  # Constant balancing and gameplay iteration
            "Card Game": "Kanban",  # Steady development pace and workflow optimization
            "Platformer": "Lean",  # Focused resource allocation for level design and mechanics
            "City-building Game": "Agile",  # Constant iteration for city dynamics and mechanics
            "Rhythm Game": "Scrum",  # Frequent iterations for music and rhythm mechanics
            "Fighting Game": "Kanban",  # Steady workflow for combat mechanics
            "Tower Defense Game": "Lean",  # Lean for efficient resource usage and mechanics
            "Stealth Game": "Agile",  # Continuous iteration for stealth mechanics and level design
            "Survival Game": "Scrum",  # Balancing gameplay mechanics and player progression
            "Party Game": "Kanban",  # Optimization and workflow for multiplayer mechanics
            "Visual Novel": "Scrum",  # Structured iterations for narrative and story development
            "Idle Game": "Kanban",  # Efficient workflow for game mechanics and progression
            "Battle Royale": "Lean",  # Lean for optimized resource management and mechanics
            "Escape Room Game": "Agile",  # Adaptive development for puzzle mechanics and immersion
            "RPG": "Scrum",  # Structured iterations for complex RPG elements
            "MMORPG": "Kanban",  # Steady workflow and optimization for massive online worlds
            "Roguelike": "Lean",  # Lean for resource efficiency and mechanics
            "Metroidvania": "Agile",  # Iterative development for map design and mechanics
        }

        # Find the process for the given game type or default to 'Waterfall'
        return game_types_to_processes.get(game_type, "Waterfall")


class GameTools:
    @staticmethod
    def identify_required_tools(design: Dict) -> List[str]:
        # choose the tools based on the game design and return a list of tools
        game_type = design.get("type", "")
        game_genre = design.get("genre", "")

        tools_list = [
            {"Adventure Game": {"Action-Adventure": ["Pygame", "PyKyra", "PyOpenGL"]}},
            {"RPG": {"Fantasy": ["Panda3D", "Cocos2d"]}},
            {"Puzzle Game": {"Strategy": ["Pygame", "Pyglet", "PySFML"]}},
            {"Strategy Game": {"Tactical": ["Pygame", "Pyglet", "PySFML"]}},
            {"Educational Game": {"Interactive": ["Pygame", "Pyglet", "PySFML"]}},
            {"Simulation Game": {"Life Simulation": ["Pygame", "Pyglet", "PySFML"]}},
            {"Sports Game": {"Simulation": ["Pygame", "Pyglet", "PySFML"]}},
            {"First-person Shooter": {"Action": ["Pygame", "Pyglet", "PySFML"]}},
            {"Horror Game": {"Survival": ["Pygame", "Pyglet", "PySFML"]}},
            {"Racing Game": {"Arcade": ["Pygame", "Pyglet", "PySFML"]}},
            {"Card Game": {"Strategy": ["Pygame", "Pyglet", "PySFML"]}},
            {"Platformer": {"Action": ["Pygame", "Pyglet", "PySFML"]}},
            {"City-building Game": {"Simulation": ["Pygame", "Pyglet", "PySFML"]}},
            {"Rhythm Game": {"Music": ["Pygame", "Pyglet", "PySFML"]}},
            {"Fighting Game": {"Action": ["Pygame", "Pyglet", "PySFML"]}},
            {"Tower Defense Game": {"Strategy": ["Pygame", "Pyglet", "PySFML"]}},
            {"Stealth Game": {"Action-Adventure": ["Pygame", "Pyglet", "PySFML"]}},
            {"Survival Game": {"Open-world": ["Pygame", "Pyglet", "PySFML"]}},
            {"Party Game": {"Casual": ["Pygame", "Pyglet", "PySFML"]}},
            {"Visual Novel": {"Romance": ["Pygame", "Pyglet", "PySFML"]}},
            {"Idle Game": {"Simulation": ["Pygame", "Pyglet", "PySFML"]}},
            {"Battle Royale": {"Action": ["Pygame", "Pyglet", "PySFML"]}},
            {"Escape Room Game": {"Puzzle": ["Pygame", "Pyglet", "PySFML"]}},
            {"MMORPG": {"Fantasy": ["Pygame", "Pyglet", "PySFML"]}},
            {"Roguelike": {"Dungeon Crawler": ["Pygame", "Pyglet", "PySFML"]}},
            {"Metroidvania": {"Action-Adventure": ["Pygame", "Pyglet", "PySFML"]}},
        ]

        for tools in tools_list:
            if game_type in tools:
                genres = tools[game_type]
                for genre in genres:
                    if game_genre == genre:
                        return genres[game_genre]

        return []

    def choose_game_tools(self, game_type: str, game_genre: str) -> List[str]:
        # Use the GameTools class to identify the required tools based on the game design
        required_tools = GameTools.identify_required_tools(
            {"type": game_type, "genre": game_genre}
        )
        return required_tools

    def list_elements(self, elements: List) -> str:
        # Example logic: List the elements
        return ", ".join(elements)


class PlanProject(TextAnalyzerAgent, CreateProjectPlan):
    def plan_project(self, text: str) -> Dict:
        # Analyze the text, design the game, and create a project plan
        game_info = self.analyze_text(text)
        game_design = self.design_game(game_info["type"], game_info["genre"])
        project_plan = self.create_project_plan(game_design)
        return project_plan
