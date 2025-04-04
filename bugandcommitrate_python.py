import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import subprocess
import requests
import csv
from datetime import datetime, timedelta
from git import Repo

# Read repository information from JSON file
def read_repositories(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

# Clone the repository (if not already cloned)
def clone_repo(repo_url):
    repo_name = repo_url.split('/')[-1]
    if not os.path.exists(repo_name):
        print(f"Cloning {repo_name}...")
        clone_url = f"https://github.com/{repo_url.split('github.com/')[1]}.git"
        subprocess.run(['git', 'clone', clone_url])
    else:
        print(f"Repository {repo_name} already exists.")

# Calculate commit rate per month (last 6 months by default)
def calculate_commit_rate_per_month(repo_path, months=6):
    repo = Repo(repo_path)

    # Get all commits from the last 'months' months
    since_date = (datetime.now() - timedelta(days=30*months)).strftime('%Y-%m-%d')
    commits = list(repo.iter_commits(since=since_date))

    # Group commits by month
    monthly_commits = {}
    for commit in commits:
        commit_month = commit.committed_datetime.strftime('%Y-%m')
        monthly_commits[commit_month] = monthly_commits.get(commit_month, 0) + 1

    return monthly_commits

# Fetch issues from GitHub and calculate percentage of "bug" label issues
def fetch_issues_and_bug_percentage(repo_url):
    owner_repo = repo_url.split('github.com/')[1]
    issues_url = f'https://api.github.com/repos/{owner_repo}/issues'

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(issues_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch issues for {repo_url}: {response.text}")
        return None

    issues = response.json()

    total_issues = 0
    bug_issues = 0

    for issue in issues:
        total_issues += 1
        labels = [label['name'] for label in issue.get('labels', [])]
        if 'bug' in labels:
            bug_issues += 1

    bug_percentage = (bug_issues / total_issues) * 100 if total_issues > 0 else 0
    return bug_percentage, total_issues

# Main function to calculate commit rate per month and bug issue percentage for all repositories
def main():
    repositories = read_repositories('apache_python_projects.json')
    
    # Prepare CSV file to store results
    with open('bug_commitrate_python.csv', 'w', newline='') as csvfile:
        fieldnames = ['repository', 'commit_rate', 'bug_percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for repo in repositories:
            repo_url = repo['repository_url']
            project_name = repo['project_name']
            print(f"Print {repo_url} and {project_name}")
            # Clone the repository if not already done
            clone_repo(repo_url)

            # Calculate the commit rate per month (last 6 months by default)
            commit_rate_per_month = calculate_commit_rate_per_month(project_name, months=6)

            # Calculate average commit rate over the last 6 months
            if commit_rate_per_month:
                average_commit_rate = sum(commit_rate_per_month.values()) / len(commit_rate_per_month)
            else:
                average_commit_rate = 0

            # Fetch issue data and calculate bug label percentage
            bug_percentage, total_issues = fetch_issues_and_bug_percentage(repo_url)

            # Write the results to CSV
            writer.writerow({
                'repository': project_name,
                'commit_rate': round(average_commit_rate, 2),
                'bug_percentage': round(bug_percentage, 2)
            })
            print(f"Processed {project_name} ({repo_url})")

    print("Results written to bug_commitrate_python.csv")
    # Load the CSV files
    tdd_metrics_df = pd.read_csv('tdd_metrics_python.csv')
    bug_commitrate_df = pd.read_csv('bug_commitrate_python.csv')

    # Merge the dataframes on 'repository' to combine the data
    merged_df = pd.merge(tdd_metrics_df, bug_commitrate_df, on='repository')

    x = merged_df['tdd_rate']
    y = merged_df['commit_rate']
    # Bar Graph 1: TDD Rate vs Commit Rate
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.5, c='blue', edgecolors='w', s=50)
    plt.title('Scatter Plot of TDD Rate vs Commit Rate')
    plt.xlabel('TDD Rate (%)')
    plt.ylabel('Commit Rate')
    plt.grid(True)

    # Save the first bar graph as a PNG file
    plt.savefig('tdd_rate_vs_commit_rate.png')
    plt.close()  # Close the plot to prevent it from being displayed

    # Bar Graph 2: TDD Rate vs Bug Percentage
    x = merged_df['tdd_rate']
    y = merged_df['bug_percentage']
    # Bar Graph 2: TDD Rate vs Bug Percentage
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.5, c='blue', edgecolors='w', s=50)
    plt.title('Scatter Plot of TDD Rate vs Bug Percentage')
    plt.xlabel('TDD Rate (%)')
    plt.ylabel('Bug Percentage')
    plt.grid(True)

    # Save the second bar graph as a PNG file
    plt.savefig('tdd_rate_vs_bug_percentage.png')
    plt.close()  # Close the plot to prevent it from being displayed
    print("Scatter Plots created for commit_rate and bug_percentage")


if __name__ == "__main__":
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if GITHUB_TOKEN:
        # If the GitHub token is found, call the main() function
        main()
    else:
        # If the GitHub token is not found, exit.
        print("GitHub Token is not set. Exiting")
