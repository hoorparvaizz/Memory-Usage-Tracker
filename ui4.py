import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

memory_log = []

def read_kernel_memory():
    try:
        with open("/proc/mem_tracker") as f:
            lines = f.readlines()
            used = int(lines[0].split(":")[1].strip())
            total = int(lines[1].split(":")[1].strip())
            percent = (used / total) * 100 if total > 0 else 0
            return used, total, percent
    except Exception as e:
        # Optional: print error to console or log
        # print(f"Error reading mem_tracker: {e}")
        return 0, 1, 0

class MemoryTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("🧠 Kernel Memory Tracker")
        self.geometry("720x580")
        self.configure(bg="#121212")  # Dark background

        # Fonts
        base_font = ("Segoe UI Variable", 14)
        title_font = ("Segoe UI Variable", 26, "semibold")
        label_font = ("Segoe UI Variable", 15)
        button_font = ("Segoe UI Variable", 13, "bold")

        # Style config
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.style.configure("TLabel",
                             background="#121212",
                             foreground="#E0E0E0",
                             font=base_font)
        self.style.configure("Title.TLabel",
                             background="#121212",
                             foreground="#00BFA6",  # teal accent
                             font=title_font)
        self.style.configure("TProgressbar",
                             troughcolor="#2A2A2A",
                             bordercolor="#2A2A2A",
                             background="#FF6F61",  # coral accent
                             thickness=28)
        self.style.configure("TButton",
                             font=button_font,
                             padding=10)
        self.style.map("TButton",
                       background=[('active', '#FF6F61'), ('!active', '#00BFA6')],
                       foreground=[('active', '#121212'), ('!active', '#F0F0F0')])

        # Header
        header = ttk.Label(self, text="🧠 Kernel Memory Tracker", style="Title.TLabel")
        header.pack(pady=(30, 15))

        # Info label
        self.label_var = tk.StringVar()
        label = ttk.Label(self, textvariable=self.label_var, style="TLabel")
        label.pack(pady=(0, 20))

        # Progress bar with frame for rounded feel
        pb_frame = tk.Frame(self, bg="#2A2A2A")
        pb_frame.pack(pady=(0, 30), padx=30, fill='x')
        self.progress = ttk.Progressbar(pb_frame, orient="horizontal",
                                        mode="determinate",
                                        length=650,
                                        style="TProgressbar")
        self.progress.pack(fill='x')

        # Graph setup
        self.fig, self.ax = plt.subplots(figsize=(7, 3), dpi=100)
        self.fig.patch.set_facecolor("#121212")
        self.ax.set_facecolor("#1E1E1E")
        self.ax.tick_params(axis='x', colors="#E0E0E0")
        self.ax.tick_params(axis='y', colors="#E0E0E0")
        self.ax.spines['bottom'].set_color('#E0E0E0')
        self.ax.spines['left'].set_color('#E0E0E0')
        self.ax.grid(color='#444444', linestyle='--', linewidth=0.5)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Memory Usage (Last 30 seconds)", color="#00BFA6", fontsize=17, pad=15)
        self.line, = self.ax.plot([], [], color="#FF6F61", linewidth=3, alpha=0.9)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=(0, 30))

        # Pause button
        self.is_paused = False
        self.pause_button = ttk.Button(self, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=(0, 20))

        # Data storage
        self.memory_log = []

        self.update_ui()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def update_ui(self):
        if not self.is_paused:
            used, total, percent = read_kernel_memory()
            self.label_var.set(f"Used: {used:,} KB / Total: {total:,} KB ({percent:.2f}%)")
            self.progress['value'] = percent

            self.memory_log.append(percent)
            if len(self.memory_log) > 30:
                self.memory_log.pop(0)

            self.line.set_data(range(len(self.memory_log)), self.memory_log)
            self.ax.set_xlim(0, 30)
            self.canvas.draw_idle()

        self.after(1000, self.update_ui)

if __name__ == "__main__":
    app = MemoryTrackerApp()
    app.mainloop()

