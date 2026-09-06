"""Smart Study Planner - console-based semester study tracker."""

from collections import defaultdict

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """Return the study-session classification based on duration."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    return "Long"


def add_session(sessions):
    """Prompt for session details, validate duration, and add a dictionary."""
    subject = input("Enter subject: ").strip()
    while not subject:
        print("Subject cannot be empty.")
        subject = input("Enter subject: ").strip()

    topic = input("Enter topic covered: ").strip()
    while not topic:
        print("Topic cannot be empty.")
        topic = input("Enter topic covered: ").strip()

    date_label = input("Enter date/day label: ").strip()
    while not date_label:
        print("Date/day label cannot be empty.")
        date_label = input("Enter date/day label: ").strip()

    while True:
        try:
            duration = float(input("Enter duration in minutes: ").strip())
            if duration <= 0:
                print("Duration must be a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    sessions.append({
        "subject": subject,
        "topic": topic,
        "date": date_label,
        "duration": duration
    })
    print("Study session added successfully.")


def view_sessions(sessions):
    """Display all logged sessions in a formatted table."""
    if not sessions:
        print("No study sessions have been logged.")
        return

    print("\nAll Study Sessions")
    print("-" * 95)
    print(f"{'No.':<5}{'Subject':<20}{'Topic':<28}{'Date/Day':<15}{'Minutes':>10}  {'Class':<10}")
    print("-" * 95)

    for index, session in enumerate(sessions, start=1):
        duration = session["duration"]
        print(
            f"{index:<5}{session['subject'][:19]:<20}"
            f"{session['topic'][:27]:<28}{session['date'][:14]:<15}"
            f"{duration:>10.1f}  {classify_session(duration):<10}"
        )
    print("-" * 95)


def search_by_subject(sessions, subject=None):
    """Find sessions by subject without case-sensitive matching."""
    if subject is None:
        subject = input("Enter subject to search for: ").strip()

    matches = [
        session for session in sessions
        if session["subject"].casefold() == subject.casefold()
    ]

    if not matches:
        print(f"No sessions found for subject '{subject}'.")
        return

    total = sum(session["duration"] for session in matches)

    print(f"\nSessions for: {subject}")
    print("-" * 90)
    print(f"{'No.':<5}{'Topic':<30}{'Date/Day':<18}{'Minutes':>10}  {'Class':<10}")
    print("-" * 90)

    for index, session in enumerate(matches, start=1):
        duration = session["duration"]
        print(
            f"{index:<5}{session['topic'][:29]:<30}"
            f"{session['date'][:17]:<18}{duration:>10.1f}  "
            f"{classify_session(duration):<10}"
        )

    print("-" * 90)
    print(f"Total time spent on {subject}: {total:.1f} minutes ({total / 60:.2f} hours)")


def study_statistics(sessions):
    """Compute and display overall and per-subject study statistics."""
    if not sessions:
        print("No study sessions available for statistics.")
        return

    total_minutes = sum(session["duration"] for session in sessions)
    subject_totals = defaultdict(float)

    for session in sessions:
        subject_totals[session["subject"]] += session["duration"]

    weakest_subject = min(subject_totals, key=subject_totals.get)
    longest_session = max(sessions, key=lambda session: session["duration"])

    print("\nStudy Statistics")
    print("-" * 55)
    print(f"Total hours studied overall: {total_minutes / 60:.2f}")
    print("\nTotal hours studied per subject:")

    for subject, minutes in sorted(subject_totals.items(), key=lambda item: item[0].casefold()):
        print(f"  {subject}: {minutes / 60:.2f} hours")

    print(f"\nWeakest area (least study time): {weakest_subject}")
    print(f"Time spent on weakest area: {subject_totals[weakest_subject] / 60:.2f} hours")

    print("\nLongest single session:")
    print(f"  Subject: {longest_session['subject']}")
    print(f"  Topic: {longest_session['topic']}")
    print(f"  Date/Day: {longest_session['date']}")
    print(f"  Duration: {longest_session['duration']:.1f} minutes")
    print(f"  Classification: {classify_session(longest_session['duration'])}")


def save_sessions(sessions, filename=FILE_NAME):
    """Save all sessions as pipe-separated records."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for session in sessions:
                fields = [
                    session["subject"].replace("|", "/"),
                    session["topic"].replace("|", "/"),
                    session["date"].replace("|", "/"),
                    str(session["duration"])
                ]
                file.write("|".join(fields) + "\n")
        print(f"Sessions saved to {filename}.")
    except OSError as error:
        print(f"Could not save sessions: {error}")


def load_sessions(filename=FILE_NAME):
    """Load saved sessions, safely handling a missing or malformed file."""
    sessions = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                parts = line.rstrip("\n").split("|")
                if len(parts) != 4:
                    print(f"Skipping invalid record on line {line_number}.")
                    continue

                subject, topic, date_label, duration_text = parts

                try:
                    duration = float(duration_text)
                    if duration <= 0:
                        raise ValueError
                except ValueError:
                    print(f"Skipping invalid duration on line {line_number}.")
                    continue

                sessions.append({
                    "subject": subject,
                    "topic": topic,
                    "date": date_label,
                    "duration": duration
                })

    except FileNotFoundError:
        pass
    except OSError as error:
        print(f"Could not load saved sessions: {error}")

    return sessions


def main():
    # Main menu loop keeps the program running until the user chooses to exit.
    sessions = load_sessions()
    print("Welcome to the Smart Study Planner!")

    while True:
        print("\n" + "=" * 45)
        print("SMART STUDY PLANNER")
        print("=" * 45)
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
