# obsi, supercharge your knowledge base
This is `obsi`, a command-line tool to supercharge markdown-based knowledge bases.
Originally used for markdown-based [Obsidian](https://obsidian.md) notes,
it works with every markdown-based tool for note-taking or digital gardening.

## Features
- create Anki Decks from your Obsidian Vault to memorize notes
- create indexes for tags, i.e. pages that link to all pages with a specific tag
- generate tag recommendations (based on other tags) with machine learning to make sure all pages are properly tagged
- generate calendar-related notes: daily, weekly, and monthly notes with respective links for the next years to come so you don't have to manually create notes for daily pages ever again

while doing this, obsi is:
- customizable with Jinja-based [templates](templates), so you can adapt everything to your needs
- easily extendable with Python, if you need more functionality
- fully containerized within Docker, no dependencies needed
- super careful with your vault and will never overwrite anything
- tool-independent to make sure, your notes stay truly text-based

## Usage
Get obsi running with these five steps:

1. Fork and then clone this repo to your local machine
2. Adapt the [templates](templates) to your needs
3. Adapt the location of your notes in [docker-compose.yml](docker-compose.yml).
4. Spin it up with `make`. This will spin up a docker container and read your vault/notes.
5. Find the generated files in [out/](out/) and copy them into your vault if desired.

## Feature Ideas
These are a few ideas I'm planning to integrate. Watch this repo to get notified.
- Search Index
- scheduling of tasks/hooks
- automated git commits
- generation of full calendar (days, months, years)
- suggest tags (content-based, link-based)
- find missing tags (e.g. by folder structure)
- spaced repetition by extracting sentences from notes
- list tags
- define rules to enforce
- formatting?
