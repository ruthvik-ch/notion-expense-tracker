# Notion Expense Tracker

A lightweight Flask app that lets you add expenses to a Notion database using natural language.
It uses OpenAI to extract structured expense data and stores it via the Notion API.

## Setup

```bash
git clone https://github.com/ruthvik-ch/notion-expense-tracker.git
cd .\notion-expense-tracker\
python -m venv .expvenv1 
.expvenv1\Scripts\Activate.ps1
(.expvenv1) pip install -r requirements.txt
(.expvenv1) flask --app app.main run
// for debugging use :- flask --app app.main --debug run

