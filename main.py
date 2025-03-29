import tkinter as tk
from logic import generate_random_numbers, Node, generate_tree, minimax, alpha_beta, console_game, print_tree
import math
import random
import time
window = tk.Tk()
window.title("MIP praktika 1")
window.geometry("800x800")

class GameUI:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.current_number_label = None
        self.current_score_label = None
        self.current_bank_label = None
        self.start_game_button = None
        self.selected_divider = None

        self.window.title("MIP praktika 1")
        self.window.geometry("800x800")

        # --- Variables for the UI ---
        #self.initial_generated_numbers = generate_random_numbers()
        self.initial_generated_numbers = [48300,48300,48300,48300]
        self.initial_number = tk.IntVar()
        self.initial_number.set(self.initial_generated_numbers[0])
        self.start_number_frame = tk.Frame(window)

        self.first_move = tk.StringVar()
        self.first_move.set("Player") 
        self.first_move_frame = tk.Frame(window)

        self.selected_algorithm = tk.StringVar()
        self.selected_algorithm.set("Minimax")
        self.algorithm_frame = tk.Frame(window)

        self.selected_divider = tk.IntVar()

        self.generate_initial_ui()

        self.is_first_player_move = True if self.first_move.get() == "Player" else False

    def generate_initial_ui(self):
        # --- Radio buttons for selecting the starting number ---
        self.start_number_frame.pack(pady=(0, 20), anchor='w')  # Adds padding below the group
        for i in self.initial_generated_numbers:
            radio = tk.Radiobutton(self.start_number_frame, text=i, variable=self.initial_number, value=i)
            radio.pack(pady=5, anchor='w')


        # --- Frame for first move options ---
        self.first_move_frame.pack(pady=(0, 20), anchor='w')  
        first_moves_options = ["Player", "Computer"]
        for i in first_moves_options:
            radio = tk.Radiobutton(self.first_move_frame, text=i, variable=self.first_move, value=i)
            radio.pack(pady=5, anchor='w')
        
        # --- Frame for algorithm options ---
        self.algorithm_frame.pack(pady=(0, 20), anchor='w')  
        algorithm_options = ["Minimax", "Alpha-beta"]
        for i in algorithm_options:
            radio = tk.Radiobutton(self.algorithm_frame, text=i, variable=self.selected_algorithm, value=i)
            radio.pack(pady=5, anchor='w')
        

        self.start_game_button = tk.Button(window, text ="Start the game", command=self.start_game)
        self.start_game_button.pack(anchor='w', pady=10)

    def clear_ui(self):
        self.current_number_label.destroy()
        self.current_score_label.destroy()
        self.current_bank_label.destroy()
        self.start_game_button.destroy()
        self.dividers_frame.destroy()
        if hasattr(self, 'computer_label'):
            self.computer_label.destroy()

    def draw_ui(self):
        possible_moves = self.state.get_possible_moves()

        if not possible_moves:
            self.final_message = tk.Label(window, text=f"Game over! Final score: {self.state.compute_final_score()}")
            self.final_message.pack(anchor='w', pady=2)

            self.restart_game_button = tk.Button(window, text ="Restart the game", command=self.restart_game)
            self.restart_game_button.pack(anchor='w', pady=10)
            return

        if not self.is_first_player_move:
            self.computer_label = tk.Label(window, text="Computer is thinking...")
            self.computer_label.pack(anchor='w', pady=2)

        self.current_number_label = tk.Label(window, text=f"Current number: {self.state.number}")
        self.current_number_label.pack(anchor='w', pady=2)

        self.current_score_label = tk.Label(window, text=f"Current score: {self.state.score}")
        self.current_score_label.pack(anchor='w', pady=2)

        self.current_bank_label = tk.Label(window, text=f"Current bank: {self.state.bank}")
        self.current_bank_label.pack(anchor='w', pady=2)

        self.dividers_frame = tk.Frame(window)
        self.dividers_frame.pack(pady=(0, 20), anchor='w')  
        for i in possible_moves:
            radio = tk.Radiobutton(self.dividers_frame, text=i, variable=self.selected_divider, value=i, command=self.on_divider_selected)
            radio.pack(pady=5, anchor='w')

    def restart_game(self):
        self.initial_generated_numbers = generate_random_numbers()
        self.initial_number.set(self.initial_generated_numbers[0])
        self.start_number_frame = tk.Frame(self.window)
        self.first_move_frame = tk.Frame(self.window)
        self.algorithm_frame = tk.Frame(self.window)
        self.selected_divider = tk.IntVar()
        self.final_message.destroy()
        self.restart_game_button.destroy()
        self.clear_ui()
        self.generate_initial_ui()


    def start_game(self):
        print("you selected", self.initial_number.get(), self.first_move.get(), self.selected_algorithm.get())
        self.is_first_player_move = True if self.first_move.get() == "Player" else False
        self.state = Node(self.initial_number.get(), 0, 0, 0, self.is_first_player_move)
        generate_tree(self.state)

        if self.selected_algorithm.get() == "Minimax":
            minimax(self.state, self.is_first_player_move)
        else:
            alpha_beta(self.state, -math.inf, math.inf, self.is_first_player_move)

        # When the game starts remove the previous ui and show current state of the game
        self.start_number_frame.destroy()
        self.first_move_frame.destroy()
        self.algorithm_frame.destroy()
        self.start_game_button.destroy()
        
        self.draw_ui()

        if not self.is_first_player_move:
            self.window.after(2000, self.computer_turn)

    
    def on_divider_selected(self):
        selected_divider = self.selected_divider.get()
        for i in self.state.children:
            if i.divisor == selected_divider:
                self.state = i
                break
        
        self.is_first_player_move = not self.is_first_player_move
        self.clear_ui()
        self.draw_ui()
        if not self.is_first_player_move:
            self.window.after(2000, self.computer_turn)


    def computer_turn(self):
        for i in self.state.children:
            if i.min_max_value == -1:
                self.state = i
                break
        self.is_first_player_move = not self.is_first_player_move
        self.clear_ui()
        self.draw_ui()

GameUI(window)
window.mainloop()