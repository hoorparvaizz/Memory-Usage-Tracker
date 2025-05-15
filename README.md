
# 🧠 Kernel Memory Tracker

A real-time Linux kernel memory usage visualizer built with Python and Tkinter. It uses live data from the /proc/mem\_tracker interface and displays usage through a sleek graphical UI with dynamic progress bars and charts.

## 🚀 Features

* 📊 Real-time memory usage tracking (used, total, and percentage).
* 📈 Live matplotlib graph showing memory trend over the last 30 seconds.
* 🎨 Modern GUI with polished fonts, colors, and layout.
* ✅ Clean progress bar indicating current usage.
* 🔄 Auto-refreshes every second for up-to-date stats.
* 🧩 Uses real system data from a custom kernel module (/proc/mem\_tracker).

## 🖥️ Preview

(Include a screenshot here if you have one, or you can generate one by running the app.)

## 📂 Directory Structure

```
.
├── kernel_memory_tracker.py    # Main application file
├── README.md                   # Project documentation
└── /proc/mem_tracker           # Custom kernel file (see below)
```

## ⚙️ Requirements

* Python 3.x
* Tkinter (usually comes with Python)
* Matplotlib
* A Linux system with a working /proc/mem\_tracker interface

Install the required Python modules:

```bash
pip install matplotlib
```

## 🧪 Example /proc/mem\_tracker Output

Ensure your kernel module writes something like this:

```
Used: 463280
Total: 1000000
```

This format is parsed by the tracker to compute the memory usage percentage.

## ▶️ Running the App

```bash
python3 kernel_memory_tracker.py
```

Make sure /proc/mem\_tracker exists and is being updated by your kernel module.

## 💡 Ideas for Enhancement

* Set usage alert thresholds and flash UI when exceeded.
* Display top memory-hogging processes using ps or /proc.
* Export memory logs to CSV or generate usage reports.
* Add CPU and Disk usage tracking for a full system monitor.
