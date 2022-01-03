# CLI for markdown-based knowledge bases
This is my command-line tool for markdown-based knowledge bases called `obsi`.
I use with my markdown-based [Obsidian](https://obsidian.md) notes.

## Features
- index generation for tags: create pages that list all usages of a specific tag
- tag recommendations (based on other tags) with machine learning
- generation of calendar-related notes: daily, weekly, and monthly notes with respective links

## Usage
1. Fork and clone this repo
2. Adapt the [templates](templates) to your needs
3. Adapt the location of your notes in [docker-compose.yml](docker-compose.yml).
4. Spin it up with `make`. This will spin up a docker container.
5. Run with `make run`, this will generate everything in the `out/` directory.

## Feature Ideas
- Search Index
- scheduling of tasks/hooks
- automated git commits
- generation of full calendar (days, months, years)
- suggest tags (content-based, link-based)
- find missing tags (e.g. by folder structure)
- spaced repetition
- list tags
- define rules to enforce
- formatting?
