import tkinter as tk
import random
from PIL import Image, ImageTk

# Main game class
class Game:
    def __init__(self, parent, initial_ammo, on_game_end):
        # Initialize the game window and parameters
        self.root = tk.Toplevel(parent)  # Create a new top-level window
        self.Totalammo = initial_ammo  # Initialize total ammo count
        self.on_game_end = on_game_end  # Callback function to handle game end actions
        self.root.title("Ocean Survivor Game")  # Set window title
        
        self.root.attributes("-fullscreen", True)  # Make the game fullscreen

        # Set screen dimensions
        self.WIDTH, self.HEIGHT = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        # Create a canvas to draw the game elements
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, bg="lightblue")
        self.canvas.pack(fill="both", expand=True)

        # Load and display the background image
        self.background_image_path = "C:\\Users\\DELL\\project\\PG\\ocean1.png"
        self.background_image = Image.open(self.background_image_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        
        # Initialize player (diver) properties
        self.player_x, self.player_y = 50, self.HEIGHT // 2  # Player's starting position
        self.player_speed = 20  # Speed of movement
        # Load player image
        self.player_image = self.load_image("C:\\insert\\diver\\file\\path\\here.png", (70, 70))
        self.player = self.canvas.create_image(self.player_x, self.player_y, anchor=tk.CENTER, image=self.player_image)
        
        # Load submarine image (shown at the end of the game)
        self.submarine_image = self.load_image("C:\\insert\\submarine\\file\\path\\here.png", (300, 200))
        self.submarine = None  # Placeholder for submarine image

        # Initialize bullet and obstacle settings
        self.bullet_size = 7
        self.bullet_speed = 13
        self.bullets = []  # List to track bullets
        self.obstacle_speed = 10
        self.obstacles = []  # List to track obstacles
        self.obstacle_interval = 1000  # Time interval for spawning obstacles (in ms)
        # Load obstacle images (monsters)
        self.obstacle_images = [self.load_image(f"C:\\insert\\obstacle\\file\\path\\here{i}.png") for i in range(1, 13)]

        # Display score on screen
        self.score = 0
        self.score_text = self.canvas.create_text(70, 20, text=f"Score: {self.score}", font=("Pixel Emulator", 16), fill='white')
        
        # Display total ammo count
        self.Totalammo_text = self.canvas.create_text(250, 20, text=f"Total ammo: {self.Totalammo}", font=("Pixel Emulator", 16), fill='white')

        # Initialize game timer (1-minute countdown)
        self.time_left = 60
        self.timer_text = self.canvas.create_text(self.WIDTH - 700, 20, text=f"Time: {self.time_left}", font=("Pixel Emulator", 16), fill='#3F93AF')

        # Game state flag
        self.game_active = True
        
        # Bind keyboard inputs to control player and game actions
        self.canvas.bind_all("<Up>", self.move_up)  # Move up
        self.canvas.bind_all("<Down>", self.move_down)  # Move down
        self.canvas.bind_all("<space>", self.fire_bullet)  # Fire bullet
        self.canvas.bind_all("<Escape>", self.exit_fullscreen)  # Exit fullscreen mode

        # Add a "Back" button to exit the game
        self.back_button = tk.Button(self.root, text="Back", fg="white", bg="#3F93AF", font=('Pixel Emulator', 18, 'bold'), command=self.close_game)
        self.canvas.create_window(1300, 50, anchor="ne", window=self.back_button)

        # Start game elements
        self.create_obstacle()  # Start spawning obstacles
        self.move_obstacles()  # Start moving obstacles
        self.start_timer()  # Start the game timer

    # Load an image and resize it to the specified dimensions
    def load_image(self, path, size=(70, 80)):
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    # Handle end-of-game scenario (player reaches submarine)
    def reach_submarine(self):
        self.game_active = False  # Stop the game
        self.display_submarine()  # Show submarine
        # Move player to submarine's position
        self.canvas.move(self.player, self.WIDTH // 2 - self.player_x, (self.HEIGHT // 2) - self.player_y)

    # Display the submarine and victory message
    def display_submarine(self):
        if self.submarine is None:
            self.submarine = self.canvas.create_image(self.WIDTH // 2, self.HEIGHT // 2 + 40, anchor=tk.CENTER, image=self.submarine_image)
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 - 40, text="You've reached the submarine!", font=("Arial", 24), fill="green")
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2, text=f"Score: {self.score}", font=("Arial", 18,'bold'), fill="white")

    # Move player upward
    def move_up(self, event):
        if self.canvas.coords(self.player)[1] > 150 and self.game_active:
            self.canvas.move(self.player, 0, -self.player_speed)

    # Move player downward
    def move_down(self, event):
        if self.canvas.coords(self.player)[1] < self.HEIGHT - 37 and self.game_active:
            self.canvas.move(self.player, 0, self.player_speed)

    # Spawn a new obstacle at a random vertical position
    def create_obstacle(self):
        if self.game_active:
            y_position = random.randint(150, self.HEIGHT - 30)
            obstacle_image = random.choice(self.obstacle_images)
            obstacle = self.canvas.create_image(self.WIDTH, y_position, anchor=tk.CENTER, image=obstacle_image)
            self.obstacles.append(obstacle)
            self.root.after(random.randint(500, 1500), self.create_obstacle)

    # Move all obstacles on the screen and check for collisions or off-screen obstacles
    def move_obstacles(self):
        if not self.game_active:
            return
        for obstacle in self.obstacles[:]:
            self.canvas.move(obstacle, -self.obstacle_speed, 0)
            if self.canvas.coords(obstacle)[0] < 0:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1  # Increment score for avoiding obstacles
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            elif self.check_collision(self.player, obstacle):  # Check for collision
                self.game_over()
                return
        self.root.after(50, self.move_obstacles)

    # Check if two objects overlap (collision detection)
    def check_collision(self, player, obstacle):
        player_coords = self.canvas.bbox(player)
        obstacle_coords = self.canvas.bbox(obstacle)
        if player_coords and obstacle_coords:
            overlap = not (player_coords[2] < obstacle_coords[0] or player_coords[0] > obstacle_coords[2] or
                           player_coords[3] < obstacle_coords[1] or player_coords[1] > obstacle_coords[3])
            return overlap
        return False

    # Fire a bullet and move it across the screen
    def fire_bullet(self, event):
        if self.game_active and self.Totalammo > 0:
            self.Totalammo -= 1
            self.canvas.itemconfig(self.Totalammo_text, text=f"Total ammo: {self.Totalammo}")
            bullet_y = self.canvas.coords(self.player)[1]
            bullet = self.canvas.create_rectangle(self.player_x + 20, bullet_y - 2,
                                                  self.player_x + 30, bullet_y + 2, fill="yellow")
            self.bullets.append(bullet)
            self.move_bullets()

    # Move bullets and check for collisions with obstacles
    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, self.bullet_speed, 0)
            if self.canvas.coords(bullet)[0] > self.WIDTH:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            for obstacle in self.obstacles[:]:
                if self.check_collision(bullet, obstacle):  # Check collision with obstacle
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    self.canvas.delete(obstacle)
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break
        
        if self.game_active:
            self.root.after(50, self.move_bullets)

    # Start the game timer
    def start_timer(self):
        if self.game_active and self.time_left > 0:
            self.time_left -= 1
            self.canvas.itemconfig(self.timer_text, text=f"Time: {self.time_left}")
            # Gradually increase obstacle speed every 10 seconds
            if self.time_left % 10 == 0:  # Every 10 seconds
               self.obstacle_speed += 1
            self.root.after(1000, self.start_timer)
        elif self.time_left == 0:  # Timer reaches 0
            self.stop_obstacles()  # Stop obstacles
            self.reach_submarine()  # End the game

    # Stop creating and moving obstacles
    def stop_obstacles(self):
        self.game_active = False
        for obstacle in self.obstacles:
            self.canvas.delete(obstacle)
        self.obstacles.clear()

    # Handle game over (player collides with obstacle)
    def game_over(self):
        self.game_active = False
        self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 - 40, text="Game Over", font=("Arial", 24), fill="red")
        self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2, text=f"Score: {self.score}", font=("Arial", 18), fill="white")
        self.canvas.unbind("<Up>")
        self.canvas.unbind("<Down>")
        self.canvas.unbind("<space>")

    # Exit the game and return to the previous screen
    def close_game(self):
        self.on_game_end(self.Totalammo)  # Return updated ammo count
        self.root.destroy()

    # Exit fullscreen mode
    def exit_fullscreen(self, event):
        self.root.attributes("-fullscreen", False)

# Main code to start the game
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window if it's not needed
    Game(root, initial_ammo=10, on_game_end=lambda ammo: print(f"Game ended. Total ammo: {ammo}"))
    root.mainloop()
