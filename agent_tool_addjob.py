from langchain.tools import tool

class JobManagementTools():

    Jobs = []  # Initialize a class attribute to hold jobs if not using a persistent store

    @tool("Add a job to the job list")
    def add_job_to_list(team, job_description, status, subjob):
        """Tool to add a job to the job list."""
        if team and job_description and status:
            JobManagementTools.Jobs.append({
                "Team": team,
                "Job": job_description,
                "Status": status,
                "SubJob": subjob
            })
            result = f"A new job has been added: Team: {team}, Job: {job_description}, Status: {status}, SubJob: {subjob}"
        else:
            result = "Error: Please provide all necessary details to add a job."
        return result
