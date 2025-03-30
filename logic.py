import random
import math
from typing import List 
counter = 0
class Node:
    """
    Represents a state in the game tree.
    Each Node stores:
      - number (the current integer in our the ),
      - score (the 'common score'),
      - bank  (the 'bank' value),
      - divisor (the last divisor used to reach this node),
      - evaluation_value (used by minimax / alpha-beta search),
      - is_first_player_move (boolean indicating whose turn it is),
      - children (list of Node objects we can move to from here).
    """
    def __init__(self, number: int, score: int, bank: int, divisor: int, is_first_player_move: bool):
        global counter
        counter+= 1
        self.counter = counter
        self.number = number
        self.score = score
        self.bank = bank
        self.divisor = divisor

        # evaluation_value: used during minimax or alpha-beta. If it's first player's turn, we initialize to +∞,
        # because the MAX player tries to get the highest value.
        # If it's second player's turn, we initialize to -∞, because the MIN player tries to get the lowest value.
        self.evaluation_value = math.inf if is_first_player_move else -math.inf

        # is_first_player_move: True if it's the first player's turn (the "maximizing" player),
        # False if it's the second player's turn (the "minimizing" player).
        self.is_first_player_move = is_first_player_move
        
        # children: holds the next possible states (Node objects) after making valid moves.
        self.children = []

    def make_move(self) -> None:
        """
        Applies a move to the current node by dividing the 'number' by 'divisor' (3, 4, or 5).
        Then it updates the bank if the resulting 'number' ends with 0 or 5.
        Also updates the score: +1 if the new number is even, -1 if it's odd.
        Finally, toggles is_first_player_move to switch turns.
        """
        self.number //= self.divisor

        # Check the last digit. If it's '0' or '5', increment the bank by 1.
        last_digit = str(self.number)[-1]
        if last_digit in ('0', '5'):
            self.bank += 1
        
        # If our new number is even, increment score; if odd, decrement score.
        if self.number % 2 == 0:
            self.score += 1
        else:
            self.score -= 1

        # Toggle which player's turn it is.
        self.is_first_player_move = not self.is_first_player_move

    def compute_final_score(self) -> int:
        """
        Computes the final score at the end of the game, based on the rules:
          - If 'score' is even, subtract the bank from it.
          - If 'score' is odd, add the bank to it.
        This is called when no more moves are possible (leaf node).
        """
        if self.score % 2 == 0:
            return self.score - self.bank
        else:
            return self.score + self.bank
    
    def get_possible_moves(self) -> List[int]:
        """
        Returns a list of valid divisors (3,4,5) that can divide self.number with no remainder.
        """
        return [number for number in [3, 4, 5] if self.number % number == 0]


def create_child(parent: Node, divisor: int) -> Node:
    """
    Creates a NEW child Node from 'parent', applying the given 'divisor'.
    - We copy the relevant fields from the parent (number, score, bank, is_first_player_move).
    - Then we call child.make_move(divisor) to apply that move.
    """
    child = Node(
        number=parent.number,
        score=parent.score,
        bank=parent.bank,
        divisor=divisor,
        is_first_player_move=parent.is_first_player_move
    )
    child.make_move()
    return child


def generate_tree(root: Node) -> None:
    """
    Builds the game tree (all possible future states) starting from 'root'.
    We use a queue for breadth-first expansion. For each node:
      - We try dividing the current number by 3, 4, 5 (if valid),
      - Create a child node for each valid move,
      - Make sure we don't generate duplicates (by storing states in a dict),
      - Then add the child to our queue as well.
    """
    queue = [root]
    generated_states = {}

    while queue:
        current_node = queue.pop(0)
        for i in [3, 4, 5]:
            if current_node.number % i == 0:
                child = create_child(current_node, i)
                # We define a key so we don't create duplicate children
                key = (child.number, child.score, child.bank, child.is_first_player_move, child.divisor)
                if key not in generated_states:
                    generated_states[key] = child
                    current_node.children.append(child)
                    queue.append(child)
                else:
                    existing_node = generated_states[key]
                    current_node.children.append(existing_node)



def minimax(node: Node, is_first_player_move: bool) -> None:
    """
    A basic Minimax algorithm (no alpha-beta pruning).
    - If a node has no children => it's a leaf, so we compute its final score.
      If it's even => we consider that +1, else -1, as an example.
    - Otherwise, we recursively call minimax on each child, 
      and then pick the max or min among them, depending on which player's turn it is.
    """
    # Base case: if no children, it's a leaf => compute the final score
    if not node.children:
        final_score = node.compute_final_score()
        # Even final => +1, Odd => -1
        if final_score % 2 == 0:
            node.evaluation_value = 1
        else:
            node.evaluation_value = -1
        
    # Otherwise, explore children
    for child in node.children:
        # Switch turn: if it's currently first player's move, next is second player's move
        minimax(child, not is_first_player_move)

    # After computing child's values, pick max or min:
    if node.children:
        if is_first_player_move:
            # The 'maximizing' player => choose the best (max) among children
            node.evaluation_value = max(child.evaluation_value for child in node.children)
        else:
            # The 'minimizing' player => choose the worst (min) among children
            node.evaluation_value = min(child.evaluation_value for child in node.children)


def generate_random_numbers() -> List[int]:
    """
    Generates 5 random numbers in the range [40020..49980] (stepping by 60)
    because 60 is the LCM of (3,4,5). Then chooses any 5 distinct ones.
    This ensures each generated number is divisible by 3,4,5.
    """
    possible_numbers = []
    for i in range(40_020, 49_980 + 1, 60):
        possible_numbers.append(i)
    return random.sample(possible_numbers, 5)

def alpha_beta(node: Node, alpha: int, beta: int, is_maximizing: bool) -> int:
    """
    Implementation of the Alpha-Beta search (an optimization over plain Minimax).
    node:        the current Node in the game tree.
    alpha:       the highest (best) value so far for the maximizing player (initially very small).
    beta:        the lowest (best) value so far for the minimizing player (initially very large).
    is_maximizing: True if it's the maximizing player's turn, False if it's the minimizing player's turn.
    
    The function returns the 'evaluation_value' for 'node'.
    
    Pruning logic:
    - If alpha >= beta at a MAX node, we stop exploring (beta cutoff).
    - If beta <= alpha at a MIN node, we stop exploring (alpha cutoff).
    """

    # 1) If node is a leaf (no children), compute final score:
    if not node.children:
        final_score = node.compute_final_score()
        if final_score % 2 == 0:
            node.evaluation_value = +1
        else:
            node.evaluation_value = -1
        return node.evaluation_value

    # 2) If it's the MAX player's turn:
    if is_maximizing:
        value = -math.inf
        for child in node.children:
            # Recurse with is_maximizing=False, because we alternate turns
            child_val = alpha_beta(child, alpha, beta, False)
            # Keep track of the best value so far
            if child_val > value:
                value = child_val
            # Update alpha if we found a bigger value
            if value > alpha:
                alpha = value
            # If alpha >= beta, we can stop searching further children (beta cut)
            if alpha >= beta:
                break
        node.evaluation_value = value
        return value

    # 3) Otherwise, it's the MIN player's turn:
    else:
        value = math.inf
        for child in node.children:
            # Recurse with is_maximizing=True
            child_val = alpha_beta(child, alpha, beta, True)
            # Keep track of the smallest value so far
            if child_val < value:
                value = child_val
            # Update beta if we found a smaller value
            if value < beta:
                beta = value
            # If beta <= alpha, we can stop searching further (alpha cut)
            if beta <= alpha:
                break
        node.evaluation_value = value
        return value
