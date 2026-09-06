# Smart Study Planner

A console-based Python programme for logging, reviewing, searching and analysing study sessions across a semester.

## Requirements

- Python 3.8 or newer
- No external libraries are required.

## Run the programme

Open a terminal in this folder and run:

```bash
python main.py
```

The programme provides:

1. Add a study session
2. View all sessions
3. Search sessions by subject
4. View statistics
5. Save and exit

Sessions are automatically loaded from `study_log.txt` when the programme starts and saved to the same file when option 5 is selected.

## Session classification

- Short: under 30 minutes
- Medium: 30 to 90 minutes
- Long: over 90 minutes

## Files

- `main.py` - complete programme
- `study_log.txt` - persistent study-session data file
- `README.md` - setup and usage instructions
