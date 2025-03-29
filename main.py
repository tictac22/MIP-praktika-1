import tkinter as tk
from logic import generate_random_numbers, Node, generate_tree, alpha_beta, console_game, print_tree
import math

window = tk.Tk()
window.title("MIP praktika 1")
window.geometry("800x800")



# --- Variables for the UI ---
initial_generated_numbers = generate_random_numbers()
initial_number = tk.IntVar()
initial_number.set(initial_generated_numbers[0])

first_move = tk.StringVar()
first_move.set("Player") 

selected_algorithm = tk.StringVar()
selected_algorithm.set("Minimax")
    
def on_start_game():
    print("you selected", initial_number.get(), first_move.get(), selected_algorithm.get())
    pass
def generate_ui():
    # --- Radio buttons for selecting the starting number ---
    start_number_frame = tk.Frame(window)
    start_number_frame.pack(pady=(0, 20), anchor='w')  # Adds padding below the group
    for i in initial_generated_numbers:
        radio = tk.Radiobutton(start_number_frame, text=i, variable=initial_number, value=i)
        radio.pack(pady=5, anchor='w')


    # --- Frame for first move options ---
    first_move_frame = tk.Frame(window)
    first_move_frame.pack(pady=(0, 20), anchor='w')  
    first_moves_options = ["Player", "Computer"]
    for i in first_moves_options:
        radio = tk.Radiobutton(first_move_frame, text=i, variable=first_move, value=i)
        radio.pack(pady=5, anchor='w')
    
    # --- Frame for algorithm options ---
    algorithm_frame = tk.Frame(window)
    algorithm_frame.pack(pady=(0, 20), anchor='w')  
    algorithm_options = ["Minimax", "Alpha-beta"]
    for i in algorithm_options:
        radio = tk.Radiobutton(algorithm_frame, text=i, variable=selected_algorithm, value=i)
        radio.pack(pady=5, anchor='w')
    


    B = tk.Button(window, text ="Start the game", command=on_start_game)
    B.pack(anchor='w', pady=10)




# btn_generate = tk.Button(window, text="Generate 5 Random Numbers", command=on_generate)
# btn_generate.pack(pady=5)

# btn_start = tk.Button(window, text="Start Game", command=on_start_game)
# btn_start.pack(pady=5)

generate_ui()
window.mainloop()