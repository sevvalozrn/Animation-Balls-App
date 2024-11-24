import tkinter as tk
import random


class BallAnimation:
    def __init__(self, root):
        # App startup and window settings
        self.root = root
        self.root.title("Ball Animation")
        self.root.geometry("500x700+400+10")

        # Creating the canvas
        self.canvas = tk.Canvas(self.root, width=490, height=500, bg="dark gray")
        self.canvas.pack()

        # Creating a frame for the buttons
        self.button_frame = tk.Frame(self.root, width=500, height=100)
        self.button_frame.pack()

        # Initial state variables
        self.balls = []
        self.is_running = False
        self.speed = 1
        self.selected_color = None
        self.selected_size = None

        # Size selection interface
        self.create_size_selector()

        # Color selection buttons
        self.create_color_buttons()

        # Control buttons
        self.create_control_buttons()

    # Color selection buttons
    def create_color_buttons(self):
        button_red = tk.Button(self.button_frame, width=4, height=2, bg="red",
                               command=lambda: self.select_color("red"))
        button_red.grid(row=1, column=0, padx=5, pady=5)

        button_yellow = tk.Button(self.button_frame, width=4, height=2, bg="yellow",
                                  command=lambda: self.select_color("yellow"))
        button_yellow.grid(row=1, column=1, padx=5, pady=5)

        button_blue = tk.Button(self.button_frame, width=4, height=2, bg="blue",
                                command=lambda: self.select_color("blue"))
        button_blue.grid(row=1, column=2, padx=5, pady=5)

    # Ball size selection
    def create_size_selector(self):
        size_canvas = tk.Canvas(self.button_frame, width=200, height=70)
        size_canvas.grid(row=0, column=0, columnspan=3, pady=10)

        sizes = [10, 20, 30]
        positions = [(30, 40), (95, 40), (170, 40)]

        for size, (x, y) in zip(sizes, positions):
            oval = size_canvas.create_oval(x - size, y - size, x + size, y + size, fill="gray")
            size_canvas.tag_bind(oval, "<Button-1>", lambda event, s=size: self.select_size(s))

    # Creating control buttons
    def create_control_buttons(self):
        # "Start" button
        start_button = tk.Button(self.button_frame, text="START", command=self.start_animation)
        start_button.grid(row=2, column=0, padx=5, pady=10)

        # "Stop" button
        stop_button = tk.Button(self.button_frame, text="STOP", command=self.stop_animation)
        stop_button.grid(row=2, column=1, padx=5, pady=10)

        # "Reset" button
        reset_button = tk.Button(self.button_frame, text="RESET", command=self.reset_canvas)
        reset_button.grid(row=2, column=2, padx=5, pady=10)

        # "Speed Up" button
        speed_up_button = tk.Button(self.button_frame, text="Speed Up", command=self.speed_up)
        speed_up_button.grid(row=2, column=3, padx=5, pady=10)

    # Setting the selected color
    def select_color(self, color):
        self.selected_color = color

    # Setting the selected size and adding a ball
    def select_size(self, size):
        self.selected_size = size
        if self.selected_color and self.selected_size:
            self.add_ball(size, self.selected_color)

    # Adding a new ball
    def add_ball(self, size, color):
        # Loop until you find a non-overlapping position
        while True:
            x = random.randint(size, 490 - size)
            y = random.randint(size, 500 - size)
            overlap = False

            # Conflict control with existing balls
            for ball in self.balls:
                x1, y1, x2, y2 = self.canvas.coords(ball["id"])
                ball_center_x = (x1 + x2) / 2
                ball_center_y = (y1 + y2) / 2
                distance = ((x - ball_center_x) ** 2 + (y - ball_center_y) ** 2) ** 0.5
                if distance < size + ball["size"]:
                    overlap = True
                    break

            # Confirm the position if there is no conflict
            if not overlap:
                break

        # Add the ball to the non-conflicting position
        dx, dy = random.choice([-1, 1]), random.choice([-1, 1])
        ball = {"id": self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color),
                "dx": dx, "dy": dy, "size": size}
        self.balls.append(ball)

    # Starting the animation
    def start_animation(self):
        if not self.is_running:
            self.is_running = True
            self.animate()

    # Stopping the animation
    def stop_animation(self):
        self.is_running = False

    # Stopping the animation and deleting the balls
    def reset_canvas(self):
        self.stop_animation()
        for ball in self.balls:
            self.canvas.delete(ball["id"])
        self.balls.clear()
        self.speed = 1

    # Increasing the speed of the balls
    def speed_up(self):
        self.speed += 2

    # Continuing the movement of the balls
    def animate(self):
        if not self.is_running:
            return

        for ball in self.balls:
            x1, y1, x2, y2 = self.canvas.coords(ball["id"])
            dx, dy = ball["dx"] * self.speed, ball["dy"] * self.speed

            if x1 + dx < 0 or x2 + dx > 490:
                ball["dx"] = -ball["dx"]
            if y1 + dy < 0 or y2 + dy > 500:
                ball["dy"] = -ball["dy"]

            self.canvas.move(ball["id"], ball["dx"] * self.speed, ball["dy"] * self.speed)

        self.root.after(10, self.animate)


# Running the main app
if __name__ == "__main__":
    root = tk.Tk()
    app = BallAnimation(root)
    root.mainloop()
