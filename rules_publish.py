# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 20:01:14 2024

@author: DELL
"""
# Import necessary libraries
from tkinter import *  # Import all classes and functions from tkinter for GUI
from PIL import Image, ImageTk  # Import Image and ImageTk for image handling

class Rules:
    def __init__(self, parent):
        # Create a Toplevel window for displaying the game rules
        self.r = Toplevel(parent)  # Create a new window that is a child of the parent window
        #.r.attributes("-fullscreen", True)  # Set the window to fullscreen mode
        self.r.geometry("1500x700")  # Set window size to match the image size
        
        # Load and resize the background image
        bg = "C:\\Users\\DELL\\project\\PG\\ocean1.png"  # Path to the background image
        original_img = Image.open(bg)  # Open the original image
        resized_img = original_img.resize((1500, 800))  # Resize the image to fit the window
        self.background_img = ImageTk.PhotoImage(resized_img)  # Convert the image for use in Tkinter
        
        # Create a canvas to hold the background image
        canvas = Canvas(self.r, width=1500, height=700)  # Create a canvas with specified dimensions
        canvas.pack(fill="both", expand=True)  # Pack the canvas to fill the window
        canvas.create_image(0, 0, anchor="nw", image=self.background_img)  # Place the background image on the canvas
        
        # Set the title of the window
        self.r.title('Ocean Survivor - Rules')  
        
        # Define the rules text to be displayed
        rules_text = (
            "                        Rules of the Game:\n"
            "1. Pre-Game Card Battle (Ammo Accumulation):\n"
            "- Play a 3-round card game against the computer to win ammo.\n"
            "- Compare card values (1-9); if the player's card is higher,\n  they win ammo equal to the card's value.\n"
            "- Tie: Player gains 1 ammo; Computer win: No ammo for the player.\n\n"
            "2. Diving Phase (Main Game):\n"
            "- After the card game, dive into the ocean aiming to reach\n  the submarine.\n"
            "- Time Limit: Complete the dive within 1 minute.\n\n"
            "3. Combat and Obstacles:\n"
            "- Use ammo to shoot enemies or dodge them to conserve resources.\n"
            "- Score: Points awarded for enemies defeated.\n"
        )
        
        # Add the rules text on top of the background image
        Label(self.r, text=rules_text, bg='#3F93AF', fg='white', font=('Pixel Emulator', 18), justify="left").place(x=105, y=90)
        
        # Add a close button to allow the user to exit the rules window
        close_button = Button(self.r, text="Close", fg='white', bg='#3F93AF', font=('Pixel Emulator', 18, 'bold'), command=self.r.destroy)
        canvas.create_window(700, 600, anchor="center", window=close_button)  # Position the button on the canvas
        
        # Start the Tkinter main loop to keep the window open
        self.r.mainloop()  
