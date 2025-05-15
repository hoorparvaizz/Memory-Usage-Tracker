import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def read_kernel_memory():
    try:
        with open("/proc/mem_tracker") as f:
            lines = f.readlines()
            used = int(lines[0].split(":")[1].strip())
            total = int(lines[1].split(":")[1].strip())
            percent = (used / total) * 100 if total > 0 else 0
            return used, total, percent
    except Exception:
        return 0, 1, 0

class MemoryTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.dark_mode = True
        self.style = ttk.Style(self)

        self.title("🧠 Kernel Memory Tracker")
        self.geometry("720x650")

        # Fonts (define early to avoid errors)
        self.base_font = ("Segoe UI Variable", 14)
        self.title_font = ("Segoe UI Variable", 26, "semibold")
        self.button_font = ("Segoe UI Variable", 13, "bold")

        self.configure_styles()

        self.configure(bg=self.bg_color())

        # Header
        self.header = ttk.Label(self, text="🧠 Kernel Memory Tracker", style="Title.TLabel")
        self.header.pack(pady=(30, 15))

        # Info label
        self.label_var = tk.StringVar()
        self.info_label = ttk.Label(self, textvariable=self.label_var, style="TLabel")
        self.info_label.pack(pady=(0, 20))

        # Progress bar frame for rounded effect
        self.pb_frame = tk.Frame(self, bg=self.pb_trough_color())
        self.pb_frame.pack(pady=(0, 30), padx=30, fill='x')
        self.progress = ttk.Progressbar(self.pb_frame, orient="horizontal",
                                        mode="determinate",
                                        length=650,
                                        style="TProgressbar")
        self.progress.pack(fill='x')

        # Matplotlib figure setup
        self.fig, self.ax = plt.subplots(figsize=(7, 3), dpi=100)
        self.fig.patch.set_facecolor(self.bg_color())
        self.ax.set_facecolor(self.ax_bg_color())
        self.set_ax_style()

        self.ax.set_ylim(0, 100)
        self.ax.set_title("Memory Usage (Last 30 seconds)",
                          color=self.title_color(),
                          fontsize=17, pad=15)

        self.line, = self.ax.plot([], [], color="#FF6F61", linewidth=3, alpha=0.9)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=(0, 15))

        # Buttons frame
        self.btn_frame = tk.Frame(self, bg=self.bg_color())
        self.btn_frame.pack(pady=(0, 20))

        # Pause/Resume button
        self.is_paused = False
        self.pause_button = ttk.Button(self.btn_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=0, column=0, padx=10)

        # Save graph button
        self.save_button = ttk.Button(self.btn_frame, text="Save Graph", command=self.save_graph)
        self.save_button.grid(row=0, column=1, padx=10)

        # Toggle theme button
        self.theme_button = ttk.Button(self.btn_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=10)

        # Threshold alert level
        self.threshold = 45

        # Data list to keep last 30 seconds
        self.memory_log = []

        self.update_ui()

    # Color helpers based on theme
    def bg_color(self):
        return "#121212" if self.dark_mode else "#f0f0f0"

    def fg_color(self):
        return "#E0E0E0" if self.dark_mode else "#121212"

    def pb_trough_color(self):
        return "#2A2A2A" if self.dark_mode else "#d0d0d0"

    def ax_bg_color(self):
        return "#1E1E1E" if self.dark_mode else "#ffffff"

    def title_color(self):
        return "#00BFA6" if self.dark_mode else "#007a63"

    def tick_color(self):
        return "#E0E0E0" if self.dark_mode else "#333333"

    def configure_styles(self):
        self.style.theme_use('clam')

        self.style.configure("TLabel",
                             background=self.bg_color(),
                             foreground=self.fg_color(),
                             font=self.base_font)
        self.style.configure("Title.TLabel",
                             background=self.bg_color(),
                             foreground="#00BFA6",
                             font=self.title_font)
        self.style.configure("TProgressbar",
                             troughcolor=self.pb_trough_color(),
                             bordercolor=self.pb_trough_color(),
                             background="#FF6F61",
                             thickness=28)
        self.style.configure("TButton",
                             font=self.button_font,
                             padding=10)
        self.style.map("TButton",
                       background=[('active', '#FF6F61'), ('!active', '#00BFA6')],
                       foreground=[('active', '#121212'), ('!active', '#F0F0F0')])

    def set_ax_style(self):
        # Update axis colors
        self.ax.tick_params(axis='x', colors=self.tick_color())
        self.ax.tick_params(axis='y', colors=self.tick_color())
        self.ax.spines['bottom'].set_color(self.tick_color())
        self.ax.spines['left'].set_color(self.tick_color())
        self.ax.grid(color='#444444' if self.dark_mode else "#cccccc",
                     linestyle='--', linewidth=0.5)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def save_graph(self):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")],
                                                initialfile=f"memory_usage_{now}.png",
                                                title="Save Graph As")
        if filename:
            self.fig.savefig(filename)
            messagebox.showinfo("Saved", f"Graph saved as:\n{filename}")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        # Update window bg
        self.configure(bg=self.bg_color())
        self.pb_frame.config(bg=self.pb_trough_color())
        self.btn_frame.config(bg=self.bg_color())

        # Re-configure styles
        self.configure_styles()

        # Update all widgets colors/styles
        self.header.configure(style="Title.TLabel")
        self.info_label.configure(style="TLabel")

        # Update progressbar style
        self.progress.configure(style="TProgressbar")

        # Update matplotlib colors
        self.fig.patch.set_facecolor(self.bg_color())
        self.ax.set_facecolor(self.ax_bg_color())
        self.set_ax_style()
        self.ax.set_title("Memory Usage (Last 30 seconds)", color=self.title_color(), fontsize=17, pad=15)
        self.canvas.draw_idle()

    def update_ui(self):
        if not self.is_paused:
            used, total, percent = read_kernel_memory()
            self.label_var.set(f"Used: {used:,} KB / Total: {total:,} KB ({percent:.2f}%)")
            self.progress['value'] = percent

            # Threshold alert
            if percent >= self.threshold:
                messagebox.showwarning("Threshold Alert",
                                       f"Memory usage exceeded threshold of {self.threshold}%!\nCurrent: {percent:.2f}%")

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

