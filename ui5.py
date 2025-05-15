import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.title("🧠 Kernel Memory Tracker")
        self.geometry("720x580")
        self.dark_mode = True

        # Fonts
        self.base_font = ("Segoe UI Variable", 14)
        self.title_font = ("Segoe UI Variable", 26, "semibold")
        self.label_font = ("Segoe UI Variable", 15)
        self.button_font = ("Segoe UI Variable", 13, "bold")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.configure_styles()

        # Header
        self.header = ttk.Label(self, text="🧠 Kernel Memory Tracker", style="Title.TLabel")
        self.header.pack(pady=(30, 15))

        # Info label
        self.label_var = tk.StringVar()
        self.info_label = ttk.Label(self, textvariable=self.label_var, style="TLabel")
        self.info_label.pack(pady=(0, 20))

        # Progress bar frame (for rounded effect)
        pb_frame = tk.Frame(self, bg=self._get_axis_bg())
        pb_frame.pack(pady=(0, 30), padx=30, fill='x')
        self.progress = ttk.Progressbar(pb_frame, orient="horizontal",
                                        mode="determinate",
                                        length=650,
                                        style="TProgressbar")
        self.progress.pack(fill='x')

        # Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(7, 3), dpi=100)
        self.fig.patch.set_facecolor(self._get_bg_color())
        self.ax.set_facecolor(self._get_axis_bg())
        self.ax.tick_params(axis='x', colors=self._get_fg_color())
        self.ax.tick_params(axis='y', colors=self._get_fg_color())
        self.ax.spines['bottom'].set_color(self._get_fg_color())
        self.ax.spines['left'].set_color(self._get_fg_color())
        self.ax.grid(color='#444444', linestyle='--', linewidth=0.5)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Memory Usage (Last 30 seconds)", color=self._get_teal_color(), fontsize=17, pad=15)

        self.line, = self.ax.plot([], [], color=self._get_coral_color(), linewidth=3, alpha=0.9)

        # Canvas widget
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=(0, 30))

        # Now configure plot colors (after canvas exists)
        self._configure_plot_colors()

        # Buttons frame
        btn_frame = tk.Frame(self, bg=self._get_bg_color())
        btn_frame.pack(pady=(0, 20))

        # Pause/Resume button
        self.is_paused = False
        self.pause_button = ttk.Button(btn_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=0, column=0, padx=10)

        # Save graph button
        self.save_button = ttk.Button(btn_frame, text="Save Graph", command=self.save_graph)
        self.save_button.grid(row=0, column=1, padx=10)

        # Toggle theme button
        self.theme_button = ttk.Button(btn_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, padx=10)

        # Data storage
        self.memory_log = []

        # Threshold for alert (e.g. 80%)
        self.threshold = 45
        self.alert_shown = False

        self.update_ui()

    # Color getters based on theme
    def _get_bg_color(self):
        return "#121212" if self.dark_mode else "#f0f0f0"

    def _get_axis_bg(self):
        return "#1E1E1E" if self.dark_mode else "#ffffff"

    def _get_fg_color(self):
        return "#E0E0E0" if self.dark_mode else "#121212"

    def _get_teal_color(self):
        return "#00BFA6"

    def _get_coral_color(self):
        return "#FF6F61"

    def configure_styles(self):
        bg = self._get_bg_color()
        fg = self._get_fg_color()
        teal = self._get_teal_color()
        coral = self._get_coral_color()
        axis_bg = self._get_axis_bg()

        self.configure(bg=bg)

        self.style.configure("TLabel",
                             background=bg,
                             foreground=fg,
                             font=self.base_font)
        self.style.configure("Title.TLabel",
                             background=bg,
                             foreground=teal,
                             font=self.title_font)
        self.style.configure("TProgressbar",
                             troughcolor=axis_bg,
                             bordercolor=axis_bg,
                             background=coral,
                             thickness=28)
        self.style.configure("TButton",
                             font=self.button_font,
                             padding=10)
        self.style.map("TButton",
                       background=[('active', coral), ('!active', teal)],
                       foreground=[('active', bg), ('!active', "#F0F0F0")])

        # Update widget backgrounds for frame containers
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=bg)

    def _configure_plot_colors(self):
        coral = self._get_coral_color()
        teal = self._get_teal_color()
        bg = self._get_bg_color()
        axis_bg = self._get_axis_bg()
        fg = self._get_fg_color()

        self.fig.patch.set_facecolor(bg)
        self.ax.set_facecolor(axis_bg)
        self.ax.tick_params(axis='x', colors=fg)
        self.ax.tick_params(axis='y', colors=fg)
        self.ax.spines['bottom'].set_color(fg)
        self.ax.spines['left'].set_color(fg)
        self.ax.grid(color='#444444', linestyle='--', linewidth=0.5)
        self.ax.set_title("Memory Usage (Last 30 seconds)", color=teal, fontsize=17, pad=15)
        self.line.set_color(coral)

        self.canvas.draw_idle()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.configure_styles()
        self._configure_plot_colors()
        # Also update label colors and progressbar style (already done in configure_styles)

    def save_graph(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png"),
                                                               ("All files", "*.*")])
            if filename:
                self.fig.savefig(filename)
                messagebox.showinfo("Saved", f"Graph saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph:\n{e}")

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

            # Show threshold alert once per breach
            if percent >= self.threshold and not self.alert_shown:
                self.alert_shown = True
                messagebox.showwarning("Threshold Alert",
                                       f"Memory usage crossed {self.threshold}%!\nCurrent: {percent:.2f}%")
            elif percent < self.threshold:
                self.alert_shown = False

        self.after(1000, self.update_ui)


if __name__ == "__main__":
    app = MemoryTrackerApp()
    app.mainloop()

