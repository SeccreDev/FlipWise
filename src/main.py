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
        self.root.geometry("500x600")
        self.center_window(self.root)
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Themes
        self.dark_mode = False

        self.light_theme = {
            "bg": "white",
            "fg": "black",
            "button_bg": "#f0f0f0",
            "button_fg": "black"
            }

        self.dark_theme = {
            "bg": "#2e2e2e",
            "fg": "white",
            "button_bg": "#444444",
            "button_fg": "white"
            }

        # Useful bindings
        self.root.bind("<space>", lambda e: self.flip_card())
        self.root.bind("<Right>", lambda e: self.next_card())
        self.root.bind("<Left>", lambda e: self.previous_card())
        self.root.bind("<e>", lambda e: self.edit_card())
        self.root.bind("<s>", lambda e: self.toggle_shuffle_mode())
        self.root.bind("<c>", lambda e: self.clear_cards())
        self.root.bind("<Delete>", lambda e: self.delete_card())

        # Store flashcards as a list of dicts: [{"question": str, "answer": str}]
        self.flashcards = []
        self.filtered_cards = []
        self.current_index = 0
        self.showing_front = True
        self.is_shuffle_mode = False
        self.current_category = "All"
        categories = sorted({card["category"] for card in self.flashcards})

        # Label to display question/answer
        self.card_label = tk.Label(root, text = "No cards yet. Add one!", font = ("Arial", 10), width = 30, height = 10, relief="groove", wraplength = 600)
        self.card_label.pack(expand = True, fill = "both", padx = 10, pady = 10)

        
        # Buttons for flashcard actions
        navegation_frame = tk.Frame(root)
        navegation_frame.pack(pady = 5, padx = 5)
        self.previous_btn = tk.Button(navegation_frame, text="BACK!", command = self.previous_card)
        self.previous_btn.pack(side = tk.LEFT)

        self.flip_btn = tk.Button(navegation_frame,  text = "FLIP!", command = self.flip_card)
        self.flip_btn.pack(side = tk.LEFT)

        self.next_btn = tk.Button(navegation_frame, text = "NEXT!", command = self.next_card)
        self.next_btn.pack(side = tk.LEFT)

        # Buttons for adding/deleting flashcards
        button_frame = tk.Frame(root)
        button_frame.pack(pady = 5, padx = 5)

        self.add_btn = tk.Button(button_frame, text = "+ Add Card", command = self.add_card)
        self.add_btn.pack(side = tk.LEFT)

        self.edit_btn = tk.Button(button_frame, text = "Edit", command = self.edit_card)
        self.edit_btn.pack(side = tk.LEFT)

        self.delete_btn = tk.Button(button_frame, text = "- Delete Card", command = self.delete_card)
        self.delete_btn.pack(side = tk.LEFT)

        # Misc Buttons
        button_frame2 = tk.Frame(root)
        button_frame2.pack(pady = 5, padx = 5)

        self.shuffle_btn = tk.Button(button_frame2, text = "Shuffle Mode", command = self.toggle_shuffle_mode)
        self.shuffle_btn.pack(side = tk.LEFT)

        self.clear_btn = tk.Button(button_frame2, text = "Clear", command = self.clear_cards)
        self.clear_btn.pack(side = tk.LEFT)

        dark_button = tk.Button(button_frame2, text="Dark Mode", command = self.toggle_dark_mode)
        dark_button.pack(side = tk.LEFT)

        # JSON save and load
        button_frame3 = tk.Frame(root)
        button_frame3.pack(pady = 5, padx = 5)
        self.save_btn = tk.Button(button_frame3, text = "Save Flashcards", command = self.save_flashcards)
        self.save_btn.pack(side = tk.LEFT)

        self.load_btn = tk.Button(button_frame3, text = "Load Flashcards", command = self.load_flashcards)
        self.load_btn.pack(side = tk.LEFT)
        
        # Category Selector
        button_frame4 = tk.Frame(root)
        button_frame4.pack(pady = 5, padx = 5)
        self.category_var = tk.StringVar(self.root)
        self.category_var.set("All")
        self.category_menu = tk.OptionMenu(button_frame4, self.category_var, "All", *categories, command = self.switch_category)
        self.category_menu.pack(side = tk.BOTTOM)


        self.update_card_display()
    
    def previous_card(self):
        """
        Move to the previous flashcard (wraps around if at beginning).
        """
        if not self.filtered_cards:
            return
        self.current_index = (self.current_index - 1) % len(self.filtered_cards)
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
        self.current_index = (self.current_index + 1) % len(self.filtered_cards)
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
        self.center_window(add_window)
        self.apply_theme(add_window)

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
                self.refresh_categories()
                self.switch_category(self.current_category)
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
            self.refresh_categories()
            self.switch_category(self.current_category)
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
            self.refresh_categories()
            self.switch_category(self.current_category)
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
        self.center_window(edit_window)
        self.apply_theme(edit_window)

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
                self.refresh_categories()
                self.switch_category(self.current_category)
                messagebox.showinfo("Edit Flashcard", "Flashcard updated successfully!")
            elif not front and not back:
                messagebox.showinfo("Edit Flashcard", "Failed! Missing front and back of flashcard!")
            elif not front:
                messagebox.showinfo("Edit Flashcard", "Failed! Missing front of flashcard!")
            else:
                messagebox.showinfo("Edit Flashcard", "Failed! Missing back of flashcard")
            edit_window.destroy()
        tk.Button(edit_window, text = "Save", command = save_edited_card).pack(pady = 10)

    def toggle_shuffle_mode(self):
        """
        Shuffles the cards.
        """
        if not self.filtered_cards:
            return

        self.is_shuffle_mode = not self.is_shuffle_mode

        if self.is_shuffle_mode:
            self.filtered_cards = list(self.filtered_cards)
            random.shuffle(self.filtered_cards)
            self.current_index = 0
            self.showing_front = True
            self.update_card_display()
            messagebox.showinfo("Shuffle Cards", "Cards shuffled!")
        else:
            if getattr(self, "current_category", "All") ==  "All":
                self.filtered_cards = list(self.flashcards)
            else:
                category = self.current_category
                self.filtered_cards = [card for card in self.flashcards if card.get("category", "General") == category]
            
            self.current_index = 0
            self.showing_front = True
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

    def switch_category(self, selected_category):
        """
        Switches the active category and filters the flashcards shown.
        """
        if selected_category == "All":
            self.filtered_cards = self.flashcards
        else:
            self.filtered_cards = [card for card in self.flashcards if card["category"] == selected_category]

        self.current_index = 0
        self.showing_front = True
        self.update_card_display()

    def refresh_categories(self):
        """
        Refreshes the category dropdown menu based on available flashcards.
        """
        # Gather all categories
        categories = sorted({card.get("category", "General") for card in self.flashcards})
        categories = ["All"] + categories

        # Clear existing menu
        self.category_menu["menu"].delete(0, "end")

        # Rebuild menu with new categories
        for cat in categories:
            self.category_menu["menu"].add_command(label = cat, command = lambda value = cat: (self.category_var.set(value), self.switch_category(value)))

        # Ensure current selection is valid
        if self.category_var.get() not in categories:
            self.category_var.set("All")
            self.switch_category("All")

    def update_card_display(self):
        """
        Update the flashcard label with new text.
        """
        if not self.filtered_cards:
            self.card_label.config(text = "No cards yet. Add one!")
        else:
            card = self.filtered_cards[self.current_index]
            if (self.showing_front):
                text = card["front"]
            else:
                text = card["back"]
            
            category = card["category"]
            self.card_label.config(text = f"{text}\n\n{category}")

    def toggle_dark_mode(self):
        """
        Toggles between light and dark mode.
        """
        self.dark_mode = not self.dark_mode
        self.apply_theme(self.root)
        if self.dark_mode:
            theme = self.dark_theme
        else: 
            theme = self.light_theme

        # Update root background
        self.root.configure(bg = theme["bg"])

        # Update card label
        self.card_label.config(bg = theme["bg"], fg = theme["fg"])

        # Update category dropdown
        self.category_menu.config(bg = theme["button_bg"], fg = theme["button_fg"])

        # Update all buttons
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg = theme["button_bg"], fg = theme["button_fg"], activebackground = theme["bg"], activeforeground = theme["fg"])
        
        # Update all open Toplevel windows
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                self.apply_theme(window)

    def apply_theme(self, window):
        """
        Applies the current theme to a given Toplevel window and its widgets.
        """
        if self.dark_mode:
            theme = self.dark_theme
        else:
            theme = self.light_theme
        window.configure(bg = theme["bg"])

        for widget in window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg = theme["bg"], fg = theme["fg"])
            elif isinstance(widget, tk.Entry):
                widget.config(bg = theme["bg"], fg = theme["fg"], insertbackground = theme["fg"])
            elif isinstance(widget, tk.Button):
                widget.config(bg = theme["button_bg"], fg = theme["button_fg"], activebackground = theme["bg"], activeforeground = theme["fg"])
            elif isinstance(widget, (tk.Frame, tk.Toplevel)):
                self.apply_theme(widget)

    def center_window(self, window):
        """
        Centers the main window on the screen.
        """
        # Get window size
        width = window.winfo_width()
        height = window.winfo_height()

        # If the window width and height is 1, falls back to a default
        if width <= 1 or height <= 1:
            width, height = 400, 300

        # Get screen widht and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate position and sets it with geometry
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlipWiseApp(root)
    root.mainloop()
