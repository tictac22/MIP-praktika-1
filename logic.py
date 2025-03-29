import time
import random
import math
from typing import List 
counterId = 0
class Node:
    def __init__(self, number: int, score: int, bank: int, divisor: int, is_first_player_move: bool):
        global counterId
        counterId += 1
        self.id = counterId

        self.number = number
        self.score = score
        self.bank = bank
        self.divisor = divisor
        self.min_max_value = math.inf if is_first_player_move else -math.inf
        self.is_first_player_move = is_first_player_move
        
        self.children = []

    def make_move(self, divisor: int) -> None:
        self.number //= divisor

        last_digit = str(self.number)[-1]
        if last_digit in ('0', '5'):
            self.bank += 1
        
        if self.number % 2 == 0:
            self.score += 1
        else:
            self.score -= 1

        self.is_first_player_move = not self.is_first_player_move

    def compute_final_score(self) -> int:
        if self.score % 2 == 0:
            return self.score - self.bank
        else:
            return self.score + self.bank
    
    def get_possible_moves(self) -> List[int]:
        return [number for number in [3, 4, 5] if self.number % number == 0]



def create_child(parent: Node, divisor: int) -> Node:
    child = Node(
        number=parent.number,
        score=parent.score,
        bank=parent.bank,
        divisor=divisor,
        is_first_player_move=parent.is_first_player_move
    )
    child.make_move(divisor)
    return child


def generate_tree(root: Node) -> None:

    queue = [root]
    generated_states = {}

    while queue:
        node = queue.pop(0)

        for i in [3, 4, 5]:
            if node.number % i == 0:
                child = create_child(node, i)
                key = (child.number, child.score, child.bank, child.is_first_player_move, child.divisor)
                if key not in generated_states:
                    generated_states[key] = True
                    node.children.append(child)
                    queue.append(child)


def minimax(node: Node, is_first_player_move: bool) -> None:
    if not node.children:
        final_score = node.compute_final_score()
        if final_score % 2 == 0:
            node.min_max_value = 1
        else:
            node.min_max_value = -1
        
    for child in node.children:
        minimax(child, not is_first_player_move)
        if is_first_player_move:
            node.min_max_value = max(child.min_max_value for child in node.children)
        else:
            node.min_max_value = min(child.min_max_value for child in node.children)

def print_tree(root: Node) -> None:
    queue = [root]
    while queue:
        node = queue.pop(0)
        if not node.children:
            print(f" Number : {node.number} Score : {node.score} Bank : {node.bank}, counter : {node.id}, final_score: {node.compute_final_score()}, min_max_value: {node.min_max_value}")
        else:
            print(
                f"Number : {node.number} " 
                f"Score : {node.score} " 
                f"Bank : {node.bank} "
                f"counter : {node.id} "
                f"min_max_value: {node.min_max_value} "
                f"children:{ [children.number for children in node.children] } "
                f"children_min_max_value: { [children.min_max_value for children in node.children] } "
                f"children_score : {[children.score for children in node.children ]} "
                f"children_bank : {[children.bank for children in node.children ]} "

            )
           
        for child in node.children:
            queue.append(child)
    


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
                if child.min_max_value == -1:
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


def generate_random_numbers() -> List[int]:
    possible_numbers = []
    for i in range(40_020, 49_980 + 1, 60):
        possible_numbers.append(i)
    return random.sample(possible_numbers, 5)
random_numbers = generate_random_numbers()


def alpha_beta(node, alpha, beta, is_maximizing):
    """
    node: the current game state (Node).
    alpha: the highest (best) value we can guarantee so far for the MAX player.
    beta: the lowest (best) value we can guarantee so far for the MIN player.
    is_maximizing: True if we're at a MAX level; False if at a MIN level.
    """

    # 1) If node is a leaf, we directly compute a final or heuristic score:
    if not node.children:
        # Suppose we map final_score to +1 or -1, or any heuristic you prefer:
        final_score = node.compute_final_score()
        if final_score % 2 == 0:
            node.min_max_value = +1    # Example: even final => +1
        else:
            node.min_max_value = -1    # Example: odd final => -1
        return node.min_max_value

    # 2) If it’s the MAX player's turn (alfa node):


    #       48300
    #    /     \     \
    #  16100   12075  96600 
    #  /   \
    # 4025  3220  
    # /      /  X
    # 805   805 644
    # /       /   \ 
    # 161    161   161
    #
    #
    #
    if is_maximizing:
        value = -math.inf  # Start lower than all possible values
        for child in node.children:
            child_val = alpha_beta(child, alpha, beta, False)  # Recur as MIN
            if child_val > value:
                value = child_val
            # Now we update alpha:
            if value > alpha:
                alpha = value
            # *** Alfa-nogriešana (beta ≤ alpha) check ***
            # Because we’re in a MAX node, we watch if alpha >= beta.
            # If so, we can prune (break) => no need to explore more children.
            if alpha >= beta:
                break
        node.min_max_value = value
        return value

    # 3) If it’s the MIN player's turn (beta node):
    else:
        value = math.inf  # Start higher than all possible values
        for child in node.children:
            child_val = alpha_beta(child, alpha, beta, True)  # Recur as MAX
            if child_val < value:
                value = child_val
            # Now we update beta:
            if value < beta:
                beta = value
            # *** Beta-nogriešana (beta ≤ alpha) check ***
            # Because we’re in a MIN node, we watch if beta <= alpha.
            # If so, we can prune (break).
            if beta <= alpha:
                break
        node.min_max_value = value
        return value



if __name__ == "__main__":
    #root_number = random.choice(random_numbers)
    root_number = 48_300
    print(f"Root number is {root_number}")

    is_first_player_move = True
    root = Node(root_number, 0, 0, 0, is_first_player_move)
    generate_tree(root)
    # minimax(root, is_first_player_move)
    alpha_beta(root, -math.inf, math.inf, is_first_player_move)
    print_tree(root)
    console_game(root, is_first_player_move)
