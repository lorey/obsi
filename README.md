![obsi logo](logo.png)

![continuous integration badge](https://img.shields.io/github/workflow/status/lorey/obsi/ci)
![language badge](https://img.shields.io/github/languages/top/lorey/obsi)
![version badge](https://img.shields.io/github/v/tag/lorey/obsi)

# obsi, supercharge your knowledge base
This is `obsi`, a command-line tool to supercharge markdown-based knowledge bases.
Originally used for markdown-based [Obsidian](https://obsidian.md) notes,
it works with every markdown-based tool for note-taking or digital gardening.
Examples of generated files from an exemplary vault can be found in the [example](example) directory.

## Obsi compared to...

- [Obsidian](https://obsidian.md): Obsidian is a program/app that allows you to interactively work with your markdown-files, it can be extended with many plugins that all run within Obsidian. obsi is command line based and works directly with your files for you. It's basically a text-focused extension of what you can do with Obsidian.
- [DataView](https://github.com/blacksmithgu/obsidian-dataview): DataView is an Obsidian addon which allows you to dynamically query your vault like a database. The results are shown in Obsidian. The issue is that they are not persisted and can thus not be used without Obsidian, e.g. when not using the app. To me, this was a huge drawback, as I wanted to have my notes tool-independent. Also, its functionality is limited to fetching data, not file-generation or even machine learning applications.

## Features

Here's what obsi can do.

- Anki decks: create and update Anki Decks from your Obsidian Vault to memorize and re-visit notes.
- Indexing: create indexes for tags, i.e. pages that link to all pages with a specific tag.
- Machine Learning Recommendations: get tag recommendations (based on other tags) to make sure all pages are properly tagged.
- Calendar generation: daily, weekly, monthly, and yearly notes, created from a template you can edit, properly interlinked, for the next years to come. You don't have to manually create notes in your calendar ever again.

while doing this, obsi is:
- customizable with Jinja-based [templates](templates), so you can adapt everything to your needs
- easily extendable with Python, if you need more functionality
- fully containerized within Docker, no dependencies needed
- super careful with your vault and will never overwrite anything
- tool-independent to make sure, your notes stay truly text-based

### Calendar generation

The calendar functionality generates calendar notes for you based on the templates provided.
The calendar generated with the default templates is also part of this repo and can be downloaded directly at [example/output/calendar](example/output/calendar) (copy and paste the notes you like to your vault, that's it).
The following notes are created by default:
- [yearly notes](templates/year.md) (shown in red)
- [monthly notes](templates/month.md) (shown in orange)
- [weekly notes](templates/week.md) (shown in lime)
- [daily notes](templates/day.md) (shows in green)

![calendar](calendar.png)


### Anki decks
Anki decks can get created in two ways.
1. ...from files, so the note becomes a card itself. You don't have to do anything, it happends automatically for every note.
2. ...by creating cards within markdown. You can put cards anywhere inside a markdown file and have as many as you want inside one file. The syntax is described below.

Regular Q&A card:
````
```obsi
Q: Who is the author of obsi?
A: Karl Lorey
```
````
will result in one anki card with 'Who is the author of obsi?' as question and 'Karl Lorey' as the answer.

Regular and reversed card:
````
```obsi
Q: obsi
Q: tool to supercharge your markdown knowledge base
```
````
will result in two cards. One with the first Q as question and the second Q as answer. And one reversed card.

## Usage

Get obsi running with these five steps:

1. Fork and then clone this repo to your local machine
2. Adapt the [templates](templates) to your needs
3. Adapt the location of your notes in [docker-compose.yml](docker-compose.yml).
4. Spin it up with `make`. This will spin up a docker container and read your vault/notes.
5. Find the generated files in your desired "out" directory, e.g. [example/output](example/output), and copy them into your vault if desired.

## Feature Ideas
These are a few ideas I'm planning to integrate. Watch this repo to get notified.

- Search Index
- scheduling of tasks/hooks
- automated git commits
- suggest tags (content-based, link-based)
- find missing tags (e.g. by folder structure)
- spaced repetition by extracting sentences from notes
- list tags
- define rules to enforce
- formatting?
