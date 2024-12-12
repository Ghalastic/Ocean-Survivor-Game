# Import necessary modules
import tkinter as tk
import random
from PIL import Image, ImageTk

# Class definition for the "CollectingAmmo" game
class CollectingAmmo:
    def __init__(self, parent):
        # Create a new top-level window for the game
        self.r = tk.Toplevel(parent)
        self.r.geometry("1500x700")  # Set the size of the window
        #self.r.attributes("-fullscreen", True)  # Make the window fullscreen
        self.bg_image_path = "C:\\Users\\DELL\\project\\PG\\ocean1.png"  # Path to background image
        self.original_bg = Image.open(self.bg_image_path)  # Open the background image
        # Resize the background image to fit the window size
        self.background_img = ImageTk.PhotoImage(self.original_bg.resize((1500, 700))) 
        self.canvas = tk.Canvas(self.r, width=1500, height=700)  # Create a canvas for drawing
        self.canvas.pack(fill="both", expand=True)  # Add the canvas to the window
        # Place the background image on the canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)  
        self.r.title('Collecting Ammo')  # Set the window title
        
        # Initialize game variables: score, rounds, and max rounds
        self.user_score, self.rounds, self.max_rounds = 0, 0, 3
        # Create card values (random integers between 1 and 10) for 3 cards
        self.card_values = {i: random.randint(1, 10) for i in range(1, 4)}
        # Load images for the cards (resized to 50x50 pixels)
        self.card_images = {i: self.load_image(r"C:\\Users\\DELL\\project\\PG\\star.png") for i in range(1, 4)}

        # Create labels and buttons for the game
        self.create_labels()
        self.create_buttons()
        self.r.bind("<Configure>", self.on_resize)  # Bind resize event to handle window resizing
        # Create a "Back" button to exit the game
        back_button = tk.Button(self.r, text="Back", bg="#3F93AF", fg="white", font=('Pixel Emulator', 18,' bold'), command=self.r.destroy)
        back_button.place(x=685, y=580, anchor="center")

    # Helper method to load and resize images
    def load_image(self, path, size=(50, 50)):
        img = Image.open(path).resize(size, Image.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(img)

    # Event handler for resizing the window
    def on_resize(self, event):
        # Resize the background image to match the new window size
        resized_bg = self.original_bg.resize((self.r.winfo_width(), self.r.winfo_height()), Image.LANCZOS)
        self.background_img = ImageTk.PhotoImage(resized_bg)
        # Update the canvas with the resized background image
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        # Redraw the "Choose a card" text at the top of the window
        self.canvas.create_text(self.r.winfo_width() / 2, 70, text="Choose a card", font=("Pixel Emulator", 19, "bold"), fill="#3F93AF", tags="choose_card_text")

    # Method to create the labels for round information and results
    def create_labels(self):
        # Round and ammo label, displaying round number and total ammo
        self.round_label = tk.Label(self.r, text=f"Round 1 | Your total ammo: 0", font=("Pixel Emulator", 14, "bold"), bg="#3F93AF", fg="white")
        # Result label, displaying the results of the current round
        self.result_label = tk.Label(self.r, text="", font=("Pixel Emulator", 13, "bold"), bg="#3F93AF", fg="white")
        
        # The "Choose a card" label is no longer needed, as it is drawn on the canvas
        # self.canvas.create_text(750, 70, text="Choose a card", font=("Pixel Emulator", 16, "bold"), fill="white")
        
        # Place the round label and result label on the window
        self.round_label.place(relx=0.5, rely=0.2, anchor="center")
        self.result_label.place(relx=0.5, rely=0.6, anchor="center")

    # Method to create the buttons for card selection
    def create_buttons(self):
        # List of relative positions for the three buttons
        button_positions = [(0.5, 0.3), (0.5, 0.4), (0.5, 0.5)]
        # Create the card selection buttons and place them in the window
        for i, (relx, rely) in enumerate(button_positions, 1):
            button = tk.Button(self.r, image=self.card_images[i], command=lambda i=i: self.submit_choice(i), relief="raised", bg="#3F93AF")
            button.place(relx=relx, rely=rely, anchor="center")

    # Method to handle the player's card choice and determine the round result
    def submit_choice(self, card_number):
        if self.rounds >= self.max_rounds: return  # End the game if the max rounds have been reached
        user_card = self.card_values[card_number]  # Get the value of the user's selected card
        computer_card = random.randint(1, 10)  # Generate a random value for the computer's card
        
        # Determine the winner of the round based on the card values
        if user_card > computer_card:
            self.user_score += user_card  # User wins and adds card value to score
            ammo_this_round = user_card
            result_text = "You win this round!"
        elif user_card < computer_card:
            ammo_this_round = 0  # Computer wins, no ammo for the player
            result_text = "Computer wins this round!"
        else:
            ammo_this_round = 1  # It's a tie, give the player 1 point
            self.user_score += ammo_this_round
            result_text = "It's a tie! You get one point."

        # Update the round label with the current round and total ammo
        self.round_label.config(text=f"Round {self.rounds + 1} | Your total ammo: {self.user_score}")
        # Update the result label with the round results
        self.result_label.config(text=f"Your card: {user_card} | Computer's card: {computer_card} \n {result_text}")
        
        self.rounds += 1  # Increment the round count
        if self.rounds == self.max_rounds:
            self.end_game()  # End the game after the max rounds are reached
        
    # Method to disable all buttons at the end of the game
    def end_game(self):
        for widget in self.r.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(tk.DISABLED)  # Disable all buttons to prevent further interaction

    # Method to get the total ammo at the end of the game
    def get_total_ammo(self):
        total_ammo = self.user_score  # Store the current total ammo
        self.user_score = 0  # Reset the user's score after retrieval
        return total_ammo

# Main script to run the game
if __name__ == "__main__":
   r= tk.Tk()  # Create the main root window
   r.withdraw()  # Hide the main window (we are using a new Toplevel window for the game)
   game = CollectingAmmo(r)  # Create the CollectingAmmo game instance
   r.mainloop()   # Start the main event loop for the Tkinter application

    


    



    


    


