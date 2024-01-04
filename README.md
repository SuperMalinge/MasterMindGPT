# Important

1.This repo is currently only a draft. Right now im testing the MasterMindGPT with CrewAI for agent support. It seems to fit better than AutoGen

2. The Current verision is using Python 3.10 and also using CrewAI. You will NEED to install both in an extra enviroment. Also i have altered CrewAI to give
the Chat into the Main window. This is not in this repo implemented.

the Next step is that the CEO Agent is going to send the prompt to the Planner Agent and this has to be done via the Job board. < not working right now

# MasterMindGPT

Next level Autogen with teams, tools and training to reach your goals.
- create applications or Games 2D/3D

# Installation

# How To Use

- Simply write any instruction in any language in free text to get started.


## Developer 

## Introduction

First Team - Planners-: Planning, task making and gathering information.
Its purpose is to gather enough information from the user to make a complete plan on how the app should look like.
It will gather information from the web and from a database.
add ```[question]``` to the board and ask the user for additional information
The information will be used to plan out: Frontend,Backend,Art,Engine,Logic etc.
Basic plan: Tasks and subtasks will be build out of this.

![task1](https://github.com/SuperMalinge/MasterMindGPT/assets/64928345/df9965b5-6512-4b48-8efd-92d5c89234c8)



adding tasks like these:
```
[Task][Level:1][Basic Plan][Prio:1][not solved][Basic plan on how the app should look like]
...

```


- processing-> add tasks and subtasks for the teams to a Board > priorizing on what needs to be done first
Any ```[Task][Level:1][Plan][Prio:1][not solved]``` remaining? assign tasks! and make them [Task][Level:2]

Second Team-Level 2 Orchestra -: Checks on all tasks. Do we have the resources to solve the tasks?
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
Teams will look at the taskboard and get the tasks:

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

```

### Quality check Phase
4 Team Quality ONE
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

#### 4-1 Team: Frontend
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
...
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
