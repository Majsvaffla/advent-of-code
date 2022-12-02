from enum import Enum
from pathlib import Path

with Path("input.txt").open() as f:
    input_lines = f.readlines()

# input_lines = [
#     "A Y",
#     "B X",
#     "C Z",
# ]

class Action(str, Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"

class Outcome(str,Enum):
    loss = "loss"
    draw = "draw"
    win = "win"

actions = {
    "A": Action.rock,
    "B": Action.paper,
    "C": Action.scissors,
}
outcomes = {
    "X": Outcome.loss,
    "Y": Outcome.draw,
    "Z": Outcome.win,
}
action_scores = {
    Action.rock: 1,
    Action.paper: 2,
    Action.scissors: 3,
}
outcome_scores = {
    Outcome.loss: 0,
    Outcome.draw: 3,
    Outcome.win: 6,
}
rounds = [
    (
        actions[line.split()[0]],
        outcomes[line.split()[1]],
    )
    for line in input_lines
]
total_score = 0


def get_outcome(opponent_action, your_action):
    if your_action == opponent_action:
        return Outcome.draw
    wins = [
        your_action == Action.rock and opponent_action == Action.scissors,
        your_action == Action.paper and opponent_action == Action.rock,
        your_action == Action.scissors and opponent_action == Action.paper,
    ]
    if any(wins):
        return Outcome.win
    return Outcome.loss


def get_your_action(opponent_action, outcome):
    for your_action in actions.values():
        possible_outcome = get_outcome(opponent_action, your_action)
        if possible_outcome == outcome:
            return your_action


def get_score(opponent_action, outcome):
    your_action = get_your_action(opponent_action, outcome)
    print(opponent_action, your_action, outcome)
    return action_scores[your_action] + outcome_scores[outcome]


for r in rounds:
    round_score = get_score(*r)
    total_score += round_score

print(total_score)
