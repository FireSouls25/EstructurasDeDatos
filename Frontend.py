import tkinter as tk
import math
from Reloj import Clock
from ControladorReloj import ClockController

class AnalogClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reloj Analógico")
        self.canvas_size = 400
        self.center = self.canvas_size // 2
        self.clock_radius = 180

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()

        self.clock = Clock()
        self.controller = ClockController(self.clock)

        self.dragging_hand = None

        self.draw_clock_face()
        self.create_controls()
        self.update_clock()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw_clock_face(self):
        self.canvas.create_oval(self.center - self.clock_radius, self.center - self.clock_radius,
                                self.center + self.clock_radius, self.center + self.clock_radius,
                                outline="#888", width=4)

        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x = self.center + (self.clock_radius - 30) * math.cos(angle)
            y = self.center + (self.clock_radius - 30) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i if i != 0 else 12), fill="white", font=("Arial", 12, "bold"))

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            x1 = self.center + (self.clock_radius - 10) * math.cos(angle)
            y1 = self.center + (self.clock_radius - 10) * math.sin(angle)
            x2 = self.center + (self.clock_radius - (20 if i % 5 == 0 else 14)) * math.cos(angle)
            y2 = self.center + (self.clock_radius - (20 if i % 5 == 0 else 14)) * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)

    def draw_hand(self, angle_deg, length, width, color):
        angle_rad = math.radians(angle_deg - 90)
        x = self.center + length * math.cos(angle_rad)
        y = self.center + length * math.sin(angle_rad)
        return self.canvas.create_line(self.center, self.center, x, y, fill=color, width=width, capstyle=tk.ROUND, tags="hands")

    def update_clock(self):
        self.canvas.delete("hands")

        if not self.dragging_hand:
            self.clock.tick()

        angles = {
            'second': self.clock.second_hand.value() * 6,
            'minute': self.clock.minute_hand.value() * 6,
            'hour': self.clock.hour_hand.value() * 30
        }

        self.draw_hand(angles['hour'], 60, 6, "#ffffff")
        self.draw_hand(angles['minute'], 90, 4, "#3399ff")
        self.draw_hand(angles['second'], 100, 2, "#ff5555")

        self.canvas.create_oval(self.center - 6, self.center - 6, self.center + 6, self.center + 6, fill="white", outline="")

        self.root.after(1000, self.update_clock)

    def get_angle_from_mouse(self, event):
        dx = event.x - self.center
        dy = event.y - self.center
        angle = math.degrees(math.atan2(dy, dx)) + 90
        return angle % 360

    def on_click(self, event):
        angle = self.get_angle_from_mouse(event)
        hand_angles = {
            'hour': self.clock.hour_hand.value() * 30,
            'minute': self.clock.minute_hand.value() * 6,
            'second': self.clock.second_hand.value() * 6,
        }
        for hand, ha in hand_angles.items():
            if abs((angle - ha + 360) % 360) < 10:
                self.dragging_hand = hand
                break

    def on_drag(self, event):
        if self.dragging_hand:
            angle = self.get_angle_from_mouse(event)
            self.controller.set_by_angle(self.dragging_hand, angle)

    def on_release(self, event):
        self.dragging_hand = None

    def create_controls(self):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=10)

        self.hour_entry = tk.Entry(frame, width=4)
        self.hour_entry.insert(0, "0")
        self.hour_entry.pack(side=tk.LEFT)
        tk.Label(frame, text=":", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)

        self.minute_entry = tk.Entry(frame, width=4)
        self.minute_entry.insert(0, "0")
        self.minute_entry.pack(side=tk.LEFT)
        tk.Label(frame, text=":", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)

        self.second_entry = tk.Entry(frame, width=4)
        self.second_entry.insert(0, "0")
        self.second_entry.pack(side=tk.LEFT)

        set_button = tk.Button(frame, text="Establecer hora", command=self.set_time_from_entries)
        set_button.pack(side=tk.LEFT, padx=10)

    def set_time_from_entries(self):
        try:
            h = int(self.hour_entry.get())
            m = int(self.minute_entry.get())
            s = int(self.second_entry.get())
            if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60):
                raise ValueError
            self.controller.set_time(h, m, s)
        except ValueError:
            print("❌ Hora inválida. Usa formato 0-23 : 0-59 : 0-59")

if __name__ == '__main__':
    root = tk.Tk()
    app = AnalogClockGUI(root)
    root.mainloop()
