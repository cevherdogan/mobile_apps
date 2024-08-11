import subprocess
import os
from datetime import datetime
import argparse

def get_git_tags(repo_path):
    result = subprocess.run(['git', '-C', repo_path, 'tag', '--sort=-creatordate'], stdout=subprocess.PIPE, check=True)
    tags = result.stdout.decode('utf-8').strip().split('\n')
    return [tag for tag in tags if tag]  # Filter out any empty strings

def get_tag_titles(repo_path, tags):
    tag_titles = {}
    for tag in tags:
        if tag:  # Ensure tag is not empty
            result = subprocess.run(['git', '-C', repo_path, 'show', tag, '--no-patch', '--format=%s'], stdout=subprocess.PIPE, check=True)
            title = result.stdout.decode('utf-8').strip()
            tag_titles[tag] = title
    return tag_titles

def get_commit_messages_since_last_tag(repo_path, last_tag):
    if last_tag:
        result = subprocess.run(['git', '-C', repo_path, 'log', f'{last_tag}..HEAD', '--oneline'], stdout=subprocess.PIPE, check=True)
    else:
        result = subprocess.run(['git', '-C', repo_path, 'log', '--oneline'], stdout=subprocess.PIPE, check=True)

    commits = result.stdout.decode('utf-8').strip().split('\n')
    return commits if commits != [''] else []

def format_commits_for_summary(commits):
    summary = []
    for commit in commits:
        commit_hash, message = commit.split(' ', 1)
        summary.append(f"- {message} ({commit_hash})")
    return "\n".join(summary)

def update_release_md(repo_path, output_file, new_tag, commit_summary):
    today = datetime.today().strftime('%Y-%m-%d')

    if commit_summary:
        new_table_entry = f"| {new_tag} | {today} | {commit_summary[0].split(' ', 1)[1]} |\n"
        new_summary_entry = f"### {new_tag}\n\n{format_commits_for_summary(commit_summary)}\n\n"
    else:
        new_table_entry = f"| {new_tag} | {today} | No new changes since the last tag. |\n"
        new_summary_entry = f"### {new_tag}\n\nNo new changes since the last tag.\n\n"

    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            content = file.readlines()
    else:
        content = ["# Release Notes\n\n",
                   "This file tracks the tags and the associated changes in the project.\n\n",
                   "| Version | Date       | Summary                                                                 |\n",
                   "|---------|------------|-------------------------------------------------------------------------|\n"]

    table_start = next((i for i, line in enumerate(content) if line.startswith("| Version")), 3)
    table_end = next((i for i, line in enumerate(content) if line.startswith("## Summary of Changes")), len(content))

    content.insert(table_start + 2, new_table_entry)

    summary_section_start = next((i for i, line in enumerate(content) if "## Summary of Changes" in line), None)
    if summary_section_start is not None:
        content.insert(summary_section_start + 1, new_summary_entry)
    else:
        content.append("\n## Summary of Changes\n\n")
        content.append(new_summary_entry)

    with open(output_file, 'w') as file:
        file.writelines(content)

#def determine_next_tag(tags, versioning):
#    if not tags:
#        return "v1.0.0"
#
#    last_tag = tags[0]
#    version_parts = list(map(int, last_tag.lstrip('v').split('.')))
#
#    if versioning == 'major':
#        version_parts[0] += 1
#        version_parts[1] = 0
#        version_parts[2] = 0
#    elif versioning == 'minor':
#        version_parts[1] += 1
#        version_parts[2] = 0
#    elif versioning == 'patch':
#        version_parts[2] += 1
#
#    return f"v{version_parts[0]}.{version_parts[1]}.{version_parts[2]}"

#def determine_next_tag(tags, versioning):
#    latest_tag = tags[0].name  # Assuming tags are sorted and the latest tag is the first
#    version_parts = latest_tag.lstrip('v').split('.')
#
#    # Ensure the version_parts list has three elements
#    while len(version_parts) < 3:
#        version_parts.append('0')  # Add missing parts as '0'
#
#    if versioning == 'major':
#        version_parts[0] = str(int(version_parts[0]) + 1)
#        version_parts[1] = '0'
#        version_parts[2] = '0'
#    elif versioning == 'minor':
#        version_parts[1] = str(int(version_parts[1]) + 1)
#        version_parts[2] = '0'
#    elif versioning == 'patch':
#        version_parts[2] = str(int(version_parts[2]) + 1)
#
#    return 'v' + '.'.join(version_parts)

def determine_next_tag(tags, versioning):
    # Assuming tags is a list of tag names as strings
    latest_tag = tags[0]  # Get the latest tag name (already sorted)
    version_parts = latest_tag.lstrip('v').split('.')

    # Ensure the version_parts list has three elements
    while len(version_parts) < 3:
        version_parts.append('0')  # Add missing parts as '0'

    if versioning == 'major':
        version_parts[0] = str(int(version_parts[0]) + 1)
        version_parts[1] = '0'
        version_parts[2] = '0'
    elif versioning == 'minor':
        version_parts[1] = str(int(version_parts[1]) + 1)
        version_parts[2] = '0'
    elif versioning == 'patch':
        version_parts[2] = str(int(version_parts[2]) + 1)

    return 'v' + '.'.join(version_parts)


def commit_release_md(repo_path, output_file, new_tag):
    subprocess.run(['git', '-C', repo_path, 'add', output_file], check=True)
    subprocess.run(['git', '-C', repo_path, 'commit', '-m', f'Update {output_file} for {new_tag}'], check=True)

def main():
    parser = argparse.ArgumentParser(description='Update RELEASE.md for a GitHub repository.')
    parser.add_argument('--repo', type=str, default='.', help='Path to the Git repository')
    parser.add_argument('--output', type=str, default='RELEASE.md', help='Output file for release notes')
    parser.add_argument('--versioning', type=str, choices=['major', 'minor', 'patch'], default='minor', help='Versioning scheme for the next tag')
    args = parser.parse_args()

    repo_path = args.repo
    output_file = args.output
    versioning = args.versioning

    tags = get_git_tags(repo_path)

    if tags:
        tag_titles = get_tag_titles(repo_path, tags)
        print("\nExisting Tags:\n")
        for tag, title in tag_titles.items():
            print(f"{tag}: {title}")
        last_tag = tags[0]
    else:
        print("No existing tags found.")
        last_tag = None

    default_tag = determine_next_tag(tags, versioning)
    print(f"\nNext tag version will be {default_tag} by default.")

    new_tag = input(f"Enter the new tag version (default: {default_tag}): ").strip()
    if not new_tag:
        new_tag = default_tag

    commit_messages = get_commit_messages_since_last_tag(repo_path, last_tag)

    update_release_md(repo_path, output_file, new_tag, commit_messages)

    commit_release_md(repo_path, output_file, new_tag)

    if commit_messages:
        subprocess.run(['git', '-C', repo_path, 'tag', '-a', new_tag, '-m', f'{new_tag}: {", ".join(commit_messages)}'], check=True)
    else:
        subprocess.run(['git', '-C', repo_path, 'tag', '-a', new_tag, '-m', f'{new_tag}: No new changes since the last tag.'], check=True)

    subprocess.run(['git', '-C', repo_path, 'push', '--tags'], check=True)

if __name__ == "__main__":
    main()

