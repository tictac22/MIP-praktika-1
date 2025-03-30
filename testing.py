import random
from logic import generate_random_numbers, Node, generate_tree, minimax, alpha_beta
def console_game(root: Node, first_move: bool) -> None:
    print("Welcome to the game")
    print(f"The game starts with the number {root_number}")

    current_node = root
    is_first_player_move = first_move
    output_message = "Player" if is_first_player_move else "Computer"

    while True:
        dividable_number = 0
        print(f"Current number : {current_node.number} Current score : {current_node.score} Current bank : {current_node.bank}")	
        if is_first_player_move:
            available_moves = [number for number in [3, 4, 5] if current_node.number % number == 0]
            dividable_number = input(f"Enter dividable number {available_moves}: ")

            dividable_number = int(dividable_number)
            print("Player chose", dividable_number)
        else:
            print("Computer thinking")
            best_move = 0
            for child in current_node.children:
                if child.evaluation_value == -1:
                    best_move = child.number
                    break
            if best_move == 0:
                print("There are no best moves for computer")
                best_move = random.choice([number for number in [3, 4, 5] if current_node.number % number == 0])
            best_move = int(current_node.number / best_move)
            print("Computer chose", best_move)

            dividable_number = best_move

           

        if current_node.number % dividable_number != 0:
            print("Invalid move")
            continue

        resulted_number = current_node.number // dividable_number

        for i in current_node.children:
            if i.number == resulted_number:
                current_node = i
                break
        
        is_first_player_move = not is_first_player_move
        if not current_node.children:
            print(f"Game over")
            if current_node.compute_final_score() % 2 == 0:
                print(f"{output_message} wins")
            else:
                print(f"{output_message} loses")
            print(f" Number: {current_node.number} Score: {current_node.score} Bank: {current_node.bank} Final score : {current_node.compute_final_score()} ")
            break

def print_tree(root: Node) -> None:
    queue = [root]
    while queue:
        node = queue.pop(0)
        if not node.children:
            print(f" Number : {node.number} Score : {node.score} Bank : {node.bank}, final_score: {node.compute_final_score()}, evaluation_value: {node.evaluation_value}, divisor: {node.divisor}, counter: {node.counter}")
        else:
            print(
                f"Number : {node.number} " 
                f"Score : {node.score} " 
                f"Bank : {node.bank} "
                f"evaluation_value: {node.evaluation_value} "
                f"children:{ [children.number for children in node.children] } "
                f"children_evaluation_value: { [children.evaluation_value for children in node.children] } "
                f"children_score : {[children.score for children in node.children ]} "
                f"children_bank : {[children.bank for children in node.children ]} "
                f"divisor : {node.divisor} "
                f"counter : {node.counter}"
            )
           
        for child in node.children:
            queue.append(child)

if __name__ == "__main__":
    root_number = 48300
    is_first_player_move = True
    root = Node(root_number, 0, 0, 0, is_first_player_move)
    generate_tree(root)
    minimax(root, is_first_player_move)
    print_tree(root)
    #alpha_beta(root, -math.inf, math.inf, is_first_player_move)
    console_game(root, is_first_player_move)
