# Update

I'm excited to announce that the code has been updated and the functionality to add jobs to the job board is now working as expected. The next step in our journey is to set up the agents correctly. Stay tuned for more updates!
* Improved CEO Class 01/2024
* refactored and split code 01/2024
* added the agents to a list on the gui 01/2024
* added queue function for different tasks 01/2024
* handling tasks by Agents is currenty WIP

# Important

1. This repo is currently only a draft.
2. The current version is now using AutoGen with Retrieval Agents. You will NEED to install it in a separate environment. 

The next step is that the CEO Agent is going to send the prompt to the Planner Agent, and this has to be done via the Job board. This is not working right now.

# MasterMindGPT

Next level AutoGen with teams, tools and training to reach your goals.
- create applications or Games 2D/3D

# Installation
- create a new environment with python 3.10
- pip install autogen - for the AutoGen library
- install a local LLM - Here LM Studio was used

# How To Use

- Simply write any instruction in english language in free text to get started.

## Developer 
Discord: SuperMalinge

## Todo List

- [ ] **High Priority:**
   - [ ] Agents opening Tasks
   - [ ] CEO takes control over the plan
   - [ ] Agents training and performance

- [ ] **Features:**
   - [ ] Application planning
   - [ ] Game planning
   - [ ] Web search if the Agent has no clue
   - [ ] Examples for the Quality Team
   - [ ] Code running to check if there is no issue
   - [ ] Manually add more Agents to a team
   - [ ] Vector Database to store snippets and a whole project
   - [ ] Observer Agent that tracks and evaluates the whole process
   - [ ] Performance check on different LLM Models

# MasterMindGPT: A Symphony of Tasks

Imagine a symphony, where each instrument plays its part to create a harmonious melody. That's what MasterMindGPT is all about - a harmonious collaboration of tasks and teams working together to create something extraordinary.

<p align="center">
  <img src="https://github.com/SuperMalinge/MasterMindGPT/raw/master/res/logo.png" alt="logo">
  <br />
  <h1 align="center">MasterMindGPT</h1>
  <br />
  <p align="center">
  <p align="center">
    <a href="https://github.com/SuperMalinge/MasterMindGPT/blob/master/LICENSE">
      <img src="https://img.shields.io/github/license/SuperMalinge/MasterMindGPT?style=flat"  alt=""/>
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/built%20with-Python3-red.svg?style=flat"  alt=""/>
    </a>
    <a href="https://github.com/SuperMalinge/MasterMindGPT/pulls">
      <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat"  alt=""/>
    </a>
    <a href="https://github.com/SuperMalinge/MasterMindGPT/issues">
    	<img src="https://img.shields.io/github/issues/SuperMalinge/MasterMindGPT?style=flat"  alt=""/>
    </a>
    <a href="https://github.com/SuperMalinge/MasterMindGPT/pulls">
      <img src="https://img.shields.io/github/issues-pr/SuperMalinge/MasterMindGPT?style=flat"  alt=""/>
    </a>
    <a href="https://github.com/SuperMalinge/MasterMindGPT/stargazers">
	    <img src="https://img.shields.io/github/stars/SuperMalinge/MasterMindGPT?style=flat" alt="">
    </a>
    <a href="https://img.shields.io/github/last-commit/SuperMalinge/MasterMindGPT/master?style=flat">
	    <img src="https://img.shields.io/github/last-commit/SuperMalinge/MasterMindGPT/master?style=flat" alt="">
    </a>
    <a href="https://pypi.org/project/MasterMindGPT/">
      <img src="https://img.shields.io/pypi/dm/MasterMindGPT" alt="">
    </a>
    <a href="https://github.com/SuperMalinge/MasterMindGPT#backers">
	    <img src="https://img.shields.io/opencollective/backers/MasterMindGPT?style=flat" alt="">
    </a>
    <a href="https://discord.gg/hApmsu39">
	    <img src="https://img.shields.io/discord/YourDiscordServerID?style=flat" alt="">
    </a>
</p>

## The Maestro: Adding Tasks
Our journey begins with the addition of tasks like these:

**First Team - Planners**: The role of the planners is to plan, create tasks, and gather information. Their purpose is to collect enough information from the user to create a comprehensive plan for how the app should look. They will gather information from the web and from a database. They will add `[question]` to the board and ask the user for additional information. The information will be used to plan out various aspects such as Frontend, Backend, Art, Engine, Logic, etc. The basic plan will consist of tasks and subtasks built from this information.

![task1](https://github.com/SuperMalinge/MasterMindGPT/assets/64928345/df9965b5-6512-4b48-8efd-92d5c89234c8)

adding tasks like these:
```
[Task][Level:1][Basic Plan][Prio:1][not solved][Basic plan on how the app should look like]
...

```

- processing-> add tasks and subtasks for the teams to a Board > priorizing on what needs to be done first
Any ```[Task][Level:1][Plan][Prio:1][not solved]``` remaining? assign tasks! and make them [Task][Level:2]

## The Orchestra: Level 2 Team

Next, our orchestra - the Level 2 Team - checks on all tasks. Do we have the resources to solve the tasks? Does the AI understand what needs to be done? Is anything missing? All teams are assigned to the tasks, and the taskboard is updated accordingly.
Get all ```[Task][Level:2]```
Does the AI understand on what needs to be done?
Is anything missing?
Assign all Teams to the tasks - Orchestra - ``` [Task][Level:2-1][Frontend][Prio:1][not solved][Build choose options for the menue] ```
Taskboard looks like this now:
```
[Task][Level:2-1][Frontend][Prio:1][not solved][Build choose options for the menue] 
[Task][Level:2-2][Backend][Prio:1][not solved][build the choose options for processing data] 
...

```
## The Sections: Teams 3-1 to 3-4

Now, the sections of our orchestra - Teams 3-1 to 3-4 - look at the taskboard and get to work. Each team builds logic, searches for code, applies it, and when done, sends it back marked as a `[solved task]`.

#### 3-1 Team: Frontend
1. Get all tasks with ```[Task][Level:2-1][Frontend][Prio:1][not solved]```
2. Build logic without methods first.
3. Search and Look for code and apply it
4. when its done, send it back with ```[solved task]```

#### 3-2 Team: Backend
1. Get all tasks with ```[Task][Level:2-2][Backend][Prio:1][not solved]```
2. Build logic without methods first.
3. Search and Look for code and apply it
4. when its done, send it back with ```[Task][Level:3][Art][Prio:1][solved]```

#### 3-3 Team: Engine
1. Get all tasks with ```[Task][Level:2-3][Engine][Prio:1][not solved]```
2. Build logic without methods first.
3. Search and Look for code and apply it
4. when its done, send it back with ```[Task][Level:3][Engine][Prio:1][solved]```

#### 3-3 Team: Art
1. Get all tasks with ```[Task][Level:2-3][Art][Prio:1][not solved]```
2. choose a model and create the art.
3. when its done, send it back with ```[Task][Level:3-1][Art][Prio:1][solved]```

Taskboard looks like this now:
```
[Task][Level:3-1][Frontend][Prio:1][solved][Build choose options for the menue][Code] 
[Task][Level:3-2][Backend][Prio:1][solved][build the choose options for processing data][Code]
... 


## The Finale: Quality Check Phase

In the finale, our Quality Team steps in. They check all solved tasks for logic, quality, and completeness. They ask the user if the result is satisfying, and if not, they reprocess it or let the user provide the answer. The whole plan is saved and rated for quality, and all tasks are elevated to Level 4.

1. Get all ```[Task][Level:3-*][solved]``` and check them if they are logical, good quality, not just a few words / code, no place holders
2. can we make it complete? does the chain from the first to the last make sense?
3. ask user if this is statisfying, if not try to reprocess it of let the user give the answer:
 ```[Question][Level3][There is missing info for frontend task]```
4. Save the whole plan and make it a pattern / basic plan for the specific topic. Rate it on the quality
5. Make them all ```[Task][Level:4-*][TEAM][Prio:1][Not solved][Build choose options for the menue]``` 

Taskboard looks like this now:
```
[Task][Level:4-1][Frontend][Prio:1][not solved][Build choose options for the menue][Code] 
[Task][Level:4-2][Backend][Prio:1][not solved][build the choose options for processing data][Code]

```

## The Encore: Teams 4-1 to 4-4

In the encore, Teams 4-1 to 4-4 take the stage. They get all tasks assigned to them, build the complete Frontend, Backend, Art, and Engine, search and look for code, compile it, and when done, send it back marked as a `[solved task]`.

1. Get all tasks with ```[Task][Level:4-1][Frontend][not solved]```
2. Build the complete Frontend.
3. Search and Look for code and compile it
4. when its done, send it back with ```[solved task]```

#### 4-2 Team: Backend
1. Get all tasks with ```[Task][Level:4-2][Backend][not solved]```
2. Build the complete Frontend.
3. Search and Look for code and compile it
4. when its done, send it back with ```[solved task]```

#### 4-3 Team: Art
1. Get all tasks with ```[Task][Level:4-3][Art][not solved]```
2. Anything that needs to be done again?.
3. Create the art
4. when its done, send it back with ```[solved task]```

#### 4-4 Team: Engine
1. Get all tasks with ```[Task][Level:4-4][Engine][not solved]```
2. Build the complete Engine.
3. Search and Look for code and compile it
4. when its done, send it back with ```[solved task]```

Taskboard looks like this now:
```
[Task][Level:4-1][Frontend][Prio:1][solved][Build choose options for the menue][Code] 
[Task][Level:4-2][Backend][Prio:1][solved][build the choose options for processing data][Code]
...

```

### Quality check Phase

#### 5 Team Quality TWO
1. Get all ```[Task][Level:4-*][*TEAM*][Prio:*][solved]``` and check them if they can be compiled. No errors. No placeholders. 
2. Reassign if anything needs to be done again. Maybe even from the start? Maybe break it down to more tasks? anything missing?
3. Build questions if anything is wrong ```[Question][Level5][a part of the code is missing, would you like this? Code]```
4. ask user if this is statisfied, if not try to reprocess it or let the user give the answer
5. Save the whole plan and make it a pattern / basic plan for the specific topic. Rate it on the quality
6. Make them all ```[Task][Level:5-*][TEAM][Prio:1][Not solved][*]``` 

Taskboard looks like this now:
```
[Task][Level:5-1][Frontend][Prio:1][not solved][Build choose options for the menue][Code] 
[Task][Level:5-2][Backend][Prio:1][not solved][build the choose options for processing data][Code]

Review Code
```

#### 5-1 Team: ReviewFrontend
1. Get all tasks with ```[Task][Level:5-1][Frontend][Prio:1][not solved]```
2. Build the complete Frontend.
3. Look for error. Check if anything is missing
4. when its done, send it back with ```[solved task]```

#### 5-2 Team: ReviewBackend
1. Get all tasks with ```[Task][Level:5-2][Backend][Prio:1][not solved]```
2. Build the complete Frontend.
3. Search and Look for code and compile it
4. when its done, send it back with ```[solved task]```

5-3 Team: ReviewArt
1. Get all tasks with ```[Task][Level:5-3]Art[Prio:1][not solved]```
2. Anything that needs to be done again?.
3. Create the art
4. when its done, send it back with ```[solved task]```

5-4 Team: ReviewEngine
1. Get all tasks with ```[Task][Level:5-1][Engine][Prio:1][not solved]```
2. Build the complete Engine.
3. Search and Look for code and compile it
4. when its done, send it back with ```[solved task]```

Taskboard looks like this now:
```
[Task][Level:5-1][Frontend][Prio:1][solved][Build choose options for the menue][Code] 
[Task][Level:5-2][Backend][Prio:1][solved][build the choose options for processing data][Code]
```

### Quality check Phase
#### 5 Team Analyze ONE
1. Get all ```[Task][Level:54-*][*TEAM*][Prio:*][solved]``` and analzye them. No errors. No placeholders. etc.
2. Reassign if anything needs to be done again. Maybe even from the start? Maybe break it down to more tasks? anything missing?
3. Build questions if anything is wrong ```[Question][Level5][a part of the code is missing, would you like this? Code]```
4. ask user if this is statisfied, if not try to reprocess it or let the user give the answer
5. Save the whole plan and make it a pattern / basic plan for the specific topic. Rate it on the quality

6 Debug and Error

    Get all tasks with [Task][Level:6-*][*TEAM*][Prio:*][not solved]
    Debug and fix errors.
    when its done, send it back with [solved task]

6-1 Team: GUI Debug

    Get all tasks with [Task][Level:6-1][GUI][Prio:1][not solved]
    Debug and fix GUI errors.
    when its done, send it back with [solved task]

6-2 Team: Backend Debug

    Get all tasks with [Task][Level:6-2][Backend][Prio:1][not solved]
    Debug and fix Backend errors.
    when its done, send it back with [solved task]

6-3 Team: Engine Debug

    Get all tasks with [Task][Level:6-3][Engine][Prio:1][not solved]
    Debug and fix Engine errors.
    when its done, send it back with [solved task]

6-4 Team: Art Debug

    Get all tasks with [Task][Level:6-4][Art][Prio:1][not solved]
    Debug and fix Art errors.
    when its done, send it back with [solved task]

6-5 Team: Quality Assist Debug

    Get all tasks with [Task][Level:6-5][Quality Assist][Prio:1][not solved]
    Assist in debugging and fixing errors.
    when its done, send it back with [solved task]

7 Finalizer

    Get all tasks with [Task][Level:7-*][*TEAM*][Prio:*][not solved]
    Finalize the project.
    when its done, send it back with [solved task]

7-1 Team: Documentation

    Get all tasks with [Task][Level:7-1][Documentation][Prio:1][not solved]
    Complete the project documentation.
    when its done, send it back with [solved task]

7-2 Team: Manual and Requirements

    Get all tasks with [Task][Level:7-2][Manual and Requirements][Prio:1][not solved]
    Complete the project manual and requirements.
    when its done, send it back with [solved task]

Contributing

Please read CONTRIBUTING.md for details on contributing to this project.
License

This project is licensed under the MIT license - see the LICENSE file for details.
