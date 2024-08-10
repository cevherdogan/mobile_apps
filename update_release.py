import subprocess
import os
from datetime import datetime

def get_git_tags():
    result = subprocess.run(['git', 'tag', '--sort=-creatordate'], stdout=subprocess.PIPE, check=True)
    tags = result.stdout.decode('utf-8').strip().split('\n')
    return [tag for tag in tags if tag]  # Filter out any empty strings

def get_tag_titles(tags):
    tag_titles = {}
    for tag in tags:
        if tag:  # Ensure tag is not empty
            result = subprocess.run(['git', 'show', tag, '--no-patch', '--format=%s'], stdout=subprocess.PIPE, check=True)
            title = result.stdout.decode('utf-8').strip()
            tag_titles[tag] = title
    return tag_titles

def get_commit_messages_since_last_tag(last_tag):
    if last_tag:
        result = subprocess.run(['git', 'log', f'{last_tag}..HEAD', '--oneline'], stdout=subprocess.PIPE, check=True)
    else:
        result = subprocess.run(['git', 'log', '--oneline'], stdout=subprocess.PIPE, check=True)

    commits = result.stdout.decode('utf-8').strip().split('\n')
    return commits if commits != [''] else []

def format_commits_for_summary(commits):
    summary = []
    for commit in commits:
        commit_hash, message = commit.split(' ', 1)
        summary.append(f"- {message} ({commit_hash})")
    return "\n".join(summary)

def update_release_md(new_tag, commit_summary):
    release_file = 'RELEASE.md'
    today = datetime.today().strftime('%Y-%m-%d')

    if commit_summary:
        new_table_entry = f"| {new_tag} | {today} | {commit_summary[0].split(' ', 1)[1]} |\n"
        new_summary_entry = f"### {new_tag}\n\n{format_commits_for_summary(commit_summary)}\n\n"
    else:
        new_table_entry = f"| {new_tag} | {today} | No new changes since the last tag. |\n"
        new_summary_entry = f"### {new_tag}\n\nNo new changes since the last tag.\n\n"

    if os.path.exists(release_file):
        with open(release_file, 'r') as file:
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

    with open(release_file, 'w') as file:
        file.writelines(content)

def determine_next_tag(tags):
    if not tags:
        return "v1.0"

    last_tag = tags[0]
    major, minor = map(int, last_tag.lstrip('v').split('.'))

    if minor < 9:
        minor += 1
    else:
        major += 1
        minor = 0

    return f"v{major}.{minor}"

def commit_release_md(new_tag):
    subprocess.run(['git', 'add', 'RELEASE.md'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Update RELEASE.md for {new_tag}'], check=True)

def main():
    tags = get_git_tags()

    if tags:
        tag_titles = get_tag_titles(tags)
        print("\nExisting Tags:\n")
        for tag, title in tag_titles.items():
            print(f"{tag}: {title}")
        last_tag = tags[0]
    else:
        print("No existing tags found.")
        last_tag = None

    default_tag = determine_next_tag(tags)
    print(f"\nNext tag version will be {default_tag} by default.")

    new_tag = input(f"Enter the new tag version (default: {default_tag}): ").strip()
    if not new_tag:
        new_tag = default_tag

    commit_messages = get_commit_messages_since_last_tag(last_tag)

    update_release_md(new_tag, commit_messages)

    commit_release_md(new_tag)

    if commit_messages:
        subprocess.run(['git', 'tag', '-a', new_tag, '-m', f'{new_tag}: {", ".join(commit_messages)}'], check=True)
    else:
        subprocess.run(['git', 'tag', '-a', new_tag, '-m', f'{new_tag}: No new changes since the last tag.'], check=True)

    subprocess.run(['git', 'push', '--tags'], check=True)

if __name__ == "__main__":
    main()

