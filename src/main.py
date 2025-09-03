import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import os
import random

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

        # Useful bindings
        self.root.bind("<space>", lambda e: self.flip_card())
        self.root.bind("<Right>", lambda e: self.next_card())
        self.root.bind("<Left>", lambda e: self.previous_card())
        self.root.bind("<e>", lambda e: self.edit_card())
        self.root.bind("<s>", lambda e: self.shuffle_mode())
        self.root.bind("<c>", lambda e: self.clear_cards())
        self.root.bind("<Delete>", lambda e: self.delete_card())

        # Store flashcards as a list of dicts: [{"question": str, "answer": str}]
        self.flashcards = []
        self.current_index = 0
        self.showing_front = True
        self.is_shuffle_mode = False
        self.current_category = None

        # Label to display question/answer
        self.card_label = tk.Label(root, text="No cards yet. Add one!", font=("Arial", 10), width = 30, height = 10, relief="groove", wraplength = 400)
        self.card_label.pack(pady = 20)

        button_frame = tk.Frame(root)
        button_frame.pack(pady = 10)

        # Buttons for flashcard actions
        self.previous_btn = tk.Button(button_frame, text="BACK!", command = self.previous_card)
        self.previous_btn.grid(row = 0, column = 0, padx = 5)

        self.flip_btn = tk.Button(button_frame,  text = "FLIP!", command = self.flip_card)
        self.flip_btn.grid(row = 0, column = 1, padx = 5)

        self.next_btn = tk.Button(button_frame, text = "NEXT!", command = self.next_card)
        self.next_btn.grid(row = 0, column = 2, padx = 5)

        self.save_btn = tk.Button(button_frame, text = "Save", command = self.save_flashcards)
        self.save_btn.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.add_btn = tk.Button(button_frame, text = "+ Add Card", command = self.add_card)
        self.add_btn.grid(row = 1, column = 1, padx = 5)

        self.delete_btn = tk.Button(button_frame, text = "- Delete Card", command = self.delete_card)
        self.delete_btn.grid(row = 1, column = 2, padx = 5)

        self.load_btn = tk.Button(button_frame, text = "Load", command = self.load_flashcards)
        self.load_btn.grid(row = 1, column = 3, padx = 5, pady = 5)

        self.edit_btn = tk.Button(button_frame, text = "Edit", command = self.edit_card)
        self.edit_btn.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.shuffle_btn = tk.Button(button_frame, text = "Shuffle Mode", command = self.shuffle_mode)
        self.shuffle_btn.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.clear_btn = tk.Button(button_frame, text = "Clear", command = self.clear_cards)
        self.clear_btn.grid(row = 2, column = 2, padx = 5, pady = 5)

        self.update_card_display()
    
    def previous_card(self):
        """
        Move to the previous flashcard (wraps around if at beginning).
        """
        if not self.flashcards:
            return
        self.current_index = (self.current_index - 1) % len(self.flashcards)
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
    
    def add_card(self):
        """
        Add a new flashcard from the input fields.
        """
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Flashcard")

        tk.Label(add_window, text = "Front:").pack(pady = 5)
        front_field = tk.Entry(add_window, width = 40)
        front_field.pack(pady = 5)

        tk.Label(add_window, text = "Back:").pack(pady = 5)
        back_field = tk.Entry(add_window, width = 40)
        back_field.pack(pady = 5)

        tk.Label(add_window, text = "Category:").pack(pady = 5)
        category_field = tk.Entry(add_window, width = 40)
        category_field.pack(pady = 5)
        
        # Saving Button
        def save_card():
            front = front_field.get().strip()
            back = back_field.get().strip()
            category = category_field.get().strip() or "General"
            if front and back:
                self.flashcards.append({"front": front, "back": back, "category": category})
                self.current_index = len(self.flashcards) - 1
                self.showing_front = True
                self.update_card_display()
            elif not front and not back:
                messagebox.showinfo("Add Flashcard", "Failed! Missing front and back of flashcard!")
            elif not front:
                messagebox.showinfo("Add Flashcard", "Failed! Missing front of flashcard!")
            else:
                messagebox.showinfo("Add Flashcard", "Failed! Missing back of flashcard")
            add_window.destroy()
        tk.Button(add_window, text = "Save", command = save_card).pack(pady = 10)


    def delete_card(self):
        """
        Deletes the currently displayed flashcard.
        """
        if not self.flashcards:
            messagebox.showinfo("Delete Card", "No cards to delete.")
            return
        
        front_text = self.flashcards[self.current_index]["front"]
        confirm = messagebox.askyesno("Delete Card", f"Delete this card?\n\nFront: {front_text}")
        
        if confirm:
            del self.flashcards[self.current_index]

            # Adjusting index
            if self.current_index >= len(self.flashcards):
                self.current_index = max(0, len(self.flashcards) - 1)
            
            self.showing_front = True
            self.update_card_display()

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
    
    def edit_card(self):
        """
        Edit the current flashcard.
        """
        if not self.flashcards:
            messagebox.showinfo("Edit Card", "No cards available to edit.")
            return
        
        card = self.flashcards[self.current_index]
        front = card["front"]
        back = card["back"]
        category = card["category"]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Flashcard")

        tk.Label(edit_window, text = "Front:").pack(pady = 5)
        front_field = tk.Entry(edit_window, width = 40)
        front_field.insert(0, front)
        front_field.pack(pady = 5)

        tk.Label(edit_window, text = "Back:").pack(pady = 5)
        back_field = tk.Entry(edit_window, width = 40)
        back_field.insert(0, back)
        back_field.pack(pady = 5)

        tk.Label(edit_window, text = "Category:").pack(pady = 5)
        category_field = tk.Entry(edit_window, width = 40)
        category_field.insert(0, category)
        category_field.pack(pady = 5)
        
        # Saving Button
        def save_edited_card():
            front = front_field.get().strip()
            back = back_field.get().strip()
            category = category_field.get().strip() or "General"
            if front and back:
                self.flashcards[self.current_index] = {"front": front, "back": back, "category": category}
                self.showing_front = True
                self.update_card_display()
                messagebox.showinfo("Edit Flashcard", "Flashcard updated successfully!")
            elif not front and not back:
                messagebox.showinfo("Edit Flashcard", "Failed! Missing front and back of flashcard!")
            elif not front:
                messagebox.showinfo("Edit Flashcard", "Failed! Missing front of flashcard!")
            else:
                messagebox.showinfo("Edit Flashcard", "Failed! Missing back of flashcard")
            edit_window.destroy()
        tk.Button(edit_window, text = "Save", command = save_edited_card).pack(pady = 10)

    def shuffle_mode(self):
        """
        Shuffles the cards.
        """
        if not self.flashcards:
            return

        self.is_shuffle_mode = not self.is_shuffle_mode

        if self.shuffle_mode:
            random.shuffle(self.flashcards)
            self.current_index = 0
            self.showing_front = True
            self.update_card_display()
            messagebox.showinfo("Shuffle Cards", "Cards shuffled!")
        else:
            # Will reset the normal order
            self.flashcards.sort(key = lambda card: card["front"])
            self.current_index = 0
            self.update_card_display()

    def clear_cards(self):
        """
        Clear the currently loaded flashcards.
        """
        if not self.flashcards:
            return
        if messagebox.askyesno("Clear Cards", "Are you sure you want to clear all flashcards?"):
            self.flashcards = []
            self.current_index = 0
            self.showing_front = True
            self.update_card_display()


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
            
            category = card["category"]
            self.card_label.config(text = f"{text}\n\n{category}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlipWiseApp(root)
    root.mainloop()
