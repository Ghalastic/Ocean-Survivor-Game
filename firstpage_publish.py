# firstpage.py
from tkinter import *  # Import all necessary components from tkinter for GUI
from PIL import Image, ImageTk  # Import Image and ImageTk for handling images
from rules import Rules  # Import the Rules class from rules.py (for the rules window)
from game_publish import Game  # Import the Game class from game2.py (for the main game)
from card_game_publish import CollectingAmmo  # Import CollectingAmmo class from card_game.py (for the ammo collection subgame)

class Firstpage:
    def __init__(self):
        # Initialize the main window for the first page
        self.a = Tk()  
        
        # Define the path for the background image and load it
        image_path = "C:\\Users\\DELL\\OneDrive - King Abdullaziz University\\Documents\\newb.png"
      
        original_img = Image.open(image_path)  # Open the image from the file
        resized_img = original_img.resize((1500, 800))  # Resize the image to fit the window size
        self.img = ImageTk.PhotoImage(resized_img)  # Convert to PhotoImage format for tkinter

        # Define the path for the logo image and load it
        logo = "C:\\Users\\DELL\\project\\PG\\logo3.png"
        logo_image = Image.open(logo)  # Open the logo image
        self.img2 = ImageTk.PhotoImage(logo_image)  # Convert logo to PhotoImage format

        # Create a canvas widget for displaying the images
        canvas = Canvas(self.a, width=1500, height=700)  
        canvas.pack()  # Pack the canvas into the window

        # Display the background image and logo on the canvas
        canvas.create_image(0, 0, anchor="nw", image=self.img)
        canvas.create_image(350, 200, anchor="nw", image=self.img2)

        # Initialize Totalammo variable to track the player's ammo across games
        self.Totalammo = 0
        self.cardgame_active = False  # Flag to check if card game is active

        # Set the window title for the first page
        self.a.title('Ocean Survivor')

        # Create a "The rules" button to open the Rules window when clicked
        rules_button = Button(self.a, text='The rules', fg='white', bg='#3F93AF', font=('Pixel Emulator', 20, 'bold'), command=self.openRules)
        rules_button.place(x=840, y=400)  # Position the rules button at specific coordinates
        
        # Create a "Play" button to start the main game when clicked
        play_button = Button(self.a, text='Play', fg='white', bg='#3F93AF', font=('Pixel Emulator', 20, 'bold'), command=self.startGame)
        play_button.place(x=660, y=400)  # Position the play button at specific coordinates
        
        # Create a "Collect ammo" button to start the ammo collection game when clicked
        collect_ammo_button = Button(self.a, text='Collect ammo', fg='white', bg='#3F93AF', font=('Pixel Emulator', 20, 'bold'), command=self.collect_ammo)
        collect_ammo_button.place(x=310, y=400)  # Position the collect ammo button at specific coordinates

        # Start the tkinter main event loop
        self.a.mainloop()

    def openRules(self):
        # This method is called when the "The rules" button is clicked
        # It opens the Rules window by creating an instance of the Rules class
        Rules(self.a)

    def collect_ammo(self):
        # This method is called when the "Collect ammo" button is clicked
        # It starts the CollectingAmmo subgame and sets cardgame_active to True
        self.collecting_ammo_game = CollectingAmmo(self.a)
        self.cardgame_active = True  # Mark the card game as active

    def startGame(self):
        # This method is called when the "Play" button is clicked
        if self.cardgame_active:
            # If a card game was played, update the Totalammo with the ammo collected from the game
            self.Totalammo += self.collecting_ammo_game.get_total_ammo()  # Add collected ammo
            self.cardgame_active = False  # Reset the flag after using ammo score

        # Start the main game by creating an instance of the Game class
        Game(self.a, self.Totalammo, self.update_total_ammo)

    def update_total_ammo(self, new_ammo):
        # This method is called at the end of each game session to update the total ammo
        self.Totalammo = new_ammo  # Set the new ammo value

# Run the Firstpage when the script is executed
if __name__ == "__main__":
    Firstpage()  # Create and start the Firstpage window


