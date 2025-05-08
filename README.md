# ⏲️ Daily Counter Tracker

A modern, dark-themed desktop application to track your daily activities (e.g. gym, water intake, job applications) using an elegant calendar-style interface — similar to GitHub contribution graphs.

---

🧠 Functionality

Daily Counter Tracker allows you to log and monitor your progress on multiple custom activities (such as water intake, gym sessions, or applications sent) day by day. Each counter records a numeric value for the current day, and displays your entire monthly history in a color-coded calendar grid. You can easily add, remove, or switch between counters. The calendar visually reflects your effort over time, helping you build and maintain habits.

---

## ✨ Features

* **Calendar View**: Track activity per day, per counter
* **Increment/Decrement with a Click**
* **Multiple Counters**: Add or remove categories (like Gym, Water, etc.)
* **Dark/Light Theme Toggle**
* **Data Stored in JSON**: No database setup needed
* **Resizable Window with Clean UI**
* **Proper Taskbar Integration** (single pinned icon behavior)

---

## 📸 Preview

| **Dark Mode**                      | **Light Mode**                    |
| ------------------------------- | --------------------------------- |
| ![image](https://github.com/user-attachments/assets/2fb55345-a7ae-4c0b-b06b-728fec6f04f5) | ![image](https://github.com/user-attachments/assets/ea889c51-f9ed-45c5-b531-848e352ab2e2) |

---

## ⚙️ How to Run

### 🔧 Requirements

* Python 3.8+
* [PySide6](https://pypi.org/project/PySide6/)
* (Optional) pywin32 for taskbar integration

### 📦 Install dependencies:

```bash
pip install PySide6 pywin32
```

### ▶️ Run the app

```bash
python "Daily Tracker.py"
```

---

## 📁 Packaging to EXE

If you want to convert this to a standalone `.exe`:

```bash
pyinstaller --onefile --windowed --icon=Tracker_icon.ico --add-data "Tracker_icon.ico;." "Daily Tracker.py"
```

> To avoid duplicate taskbar icons, the app uses `AppUserModelID`.

---

## 📂 Project Structure

```bash
📁 Project Root
│
├── Daily Tracker.py         # Main Python app
├── data.json                # Auto-generated counter data
├── Tracker_icon.ico         # App icon
├── Dialy Tracker.exe        # Executable File for Windows
└── README.md                # You're here!
```

---

## Special Thanks

This project was built with the help of **ChatGPT** by [OpenAI](https://openai.com), which helped with:

* PySide6 GUI design
* Responsive layout and styling
* EXE conversion and taskbar behavior
* Bug fixing, refactoring, and polish ✨

---

👤 Author

**Aryan Deshmukh**

🔗 [LinkedIn](https://www.linkedin.com/in/aryan-deshmukh-0531321b6) | 💻 [GitHub](https://github.com/ColonialCreature)
