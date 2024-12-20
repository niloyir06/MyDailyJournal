# Modern Journaling & To-Do App

A simple Python/PyQt5 desktop application to journal your thoughts and manage your to-do tasks with a simple UI. I created this simple minimalistic app to avoid the distractions of feature-rich and cluttered productivity applications. It was also nice to learn PyQT5. 

## Features

- **Journaling:** Write and save rich-text journal entries. Supports formatting like bold, italic, underline, strikethrough, bullet/numbered lists, and highlight.
- **To-Do List:** Quickly add tasks and remove them once done. Tasks are displayed in a neat list, each with a remove icon.
- **Date Selection:** Choose a date from a built-in calendar to view or edit journal entries and tasks from different days.
- **Auto-Save:** Journal entries are auto-saved after a short period of inactivity, ensuring your work is never lost.
- **Customizable UI:**
  Light gray background for the UI, white text boxes for a clean look. Icons and colors for formatting and highlight actions are easily adjustable in the code.

## Requirements

- Python 3.6+
- PyQt5

Install PyQt5 with:

```bash
pip install pyqt5
```

## How to Run

```bash
python main.py
```

## Packaging into an Executable

Use PyInstaller (or another tool) to create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile main.pypip install pyqt5
```
