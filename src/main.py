import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import os


class FlipWiseApp:
    """
    A simple flashcard application with a Tkinter GUI.
    
    Features:
        - Add new flashcards
        - Flip between question and answer
        - Navigate to next flashcard
        - Save and load flashcards from JSON files
    """

    def __init__(self, root):
        """
        Initialize the FlipWiseApp.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("FlipWise - Flashcard App")

        # Store flashcards as a list of dicts: [{"question": str, "answer": str}]
        self.flashcards = []
        self.current_index = 0
        self.showing_front = True

        # Label to display question/answer
        self.card_label = tk.Label(root, text="No cards yet. Add one!", font=("Arial", 10), width = 30, height = 10, relief="groove", wraplength = 400)
        self.card_label.pack(pady = 20)

        button_frame = tk.Frame(root)
        button_frame.pack(pady = 10)

        # Buttons for flashcard actions
        self.add_btn = tk.Button(button_frame, text = "+ Add Card", command = self.add_card)
        self.add_btn.grid(row = 0, column = 0, padx = 5)

        self.flip_btn = tk.Button(button_frame,  text = "FLIP!", command = self.flip_card)
        self.flip_btn.grid(row = 0, column = 1, padx = 5)

        self.next_btn = tk.Button(button_frame, text = "NEXT!", command = self.next_card)
        self.next_btn.grid(row = 0, column = 2, padx = 5)

        self.save_btn = tk.Button(button_frame, text = "Save", command = self.save_flashcards)
        self.save_btn.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.load_btn = tk.Button(button_frame, text = "Load", command = self.load_flashcards)
        self.load_btn.grid(row = 1, column = 2, padx = 5, pady = 5)

        self.update_card_display()
    
    def add_card(self):
        """
        Add a new flashcard from the input fields.
        """
        front = simpledialog.askstring("New Flashcard", "Enter the question/front:")
        if not front:
            return
        back = simpledialog.askstring("New Flashcard", "Enter the answer/back:")
        if not back:
            return
        
        self.flashcards.append({"front": front, "back": back})
        self.current_index = len(self.flashcards) - 1
        self.showing_front = True
        self.update_card_display()
    
    def flip_card(self):
        """
        Flip the flashcard between question and answer.
        """
        if not self.flashcards:
            return
        self.showing_front = not self.showing_front
        self.update_card_display()
    
    def next_card(self):
        """
        Move to the next flashcard (wraps around if at end).
        """
        if not self.flashcards:
            return
        self.current_index = (self.current_index + 1) % len(self.flashcards)
        self.showing_front = True
        self.update_card_display()

    def save_flashcards(self):
        """
        Save flashcards to a JSON file.
        """
        if not self.flashcards:
            messagebox.showinfo("Save", "No flashcards to save.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.flashcards, f, indent = 2)
            messagebox.showinfo("Save", f"Saved {len(self.flashcards)} cards!")
    
    def load_flashcards(self):
        """
        Load flashcards from a JSON file.
        """
        file_path = filedialog.askopenfilename(filetypes = [("JSON files", "*.json")])

        if file_path and os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.flashcards = json.load(f)
            self.current_index = 0
            self.showing_front = True
            self.update_card_display()
            messagebox.showinfo("Load", f"Loaded {len(self.flashcards)} cards!")

    def update_card_display(self):
        """
        Update the flashcard label with new text.
        """
        if not self.flashcards:
            self.card_label.config(text = "No cards yet. Add one!")
        else:
            card = self.flashcards[self.current_index]
            if (self.showing_front):
                text = card["front"]
            else:
                text = card["back"]

            self.card_label.config(text = text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlipWiseApp(root)
    root.mainloop()
