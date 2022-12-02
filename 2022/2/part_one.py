from enum import Enum
from pathlib import Path

with Path("input.txt").open() as f:
    input_lines = f.readlines()

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
    "X": Action.rock,
    "Y": Action.paper,
    "Z": Action.scissors,
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
rounds = [[actions[action] for action in  line.split()] for line in input_lines]
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


def fight(opponent_action, your_action):
    outcome = get_outcome(opponent_action, your_action)
    return action_scores[your_action] + outcome_scores[outcome]


for actions in rounds:
    round_score = fight(*actions)
    total_score += round_score

print(total_score)
