# love_calculator.py
# Standalone CLI love calculator (no Flask)
import hashlib
import json
import os
import time

HISTORY_FILE = "love_history.json"

def compute_love_percentage(name1: str, name2: str) -> int:
    """Deterministic percentage based on SHA256 of the two names."""
    combined = (name1.strip().lower() + "|" + name2.strip().lower()).encode("utf-8")
    digest = hashlib.sha256(combined).hexdigest()
    return int(digest[:8], 16) % 101

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(entry):
    data = load_history()
    data.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def print_history():
    data = load_history()
    if not data:
        print("\nNo history yet.\n")
        return
    print("\n--- Love History ---")
    for i, e in enumerate(data, 1):
        t = e.get("time", "")
        n1 = e.get("name1", "")
        n2 = e.get("name2", "")
        p = e.get("percentage", "")
        print(f"{i}. [{t}] {n1} ❤️ {n2} => {p}%")
    print("---------------------\n")

def ask_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a non-empty name.")

def main_menu():
    print("❤ Love Calculator (standalone) ❤")
    while True:
        print("Choose an option:")
        print("  1) Calculate love percentage")
        print("  2) View history")
        print("  3) Exit")
        choice = input("> ").strip()
        if choice == "1":
            name1 = ask_nonempty("Your name: ")
            name2 = ask_nonempty("Partner's name: ")
            percent = compute_love_percentage(name1, name2)
            print(f"\n{name1} ❤️ {name2} -> Love Percentage: {percent}%\n")
            save_history({
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "name1": name1,
                "name2": name2,
                "percentage": percent
            })
        elif choice == "2":
            print_history()
        elif choice == "3" or choice.lower() in ("q", "quit", "exit"):
            print("Goodbye 💕")
            break
        else:
            print("Invalid option. Choose 1, 2 or 3.\n")

if __name__ == "__main__":
    main_menu()
