# Author: Aziz Mohmand
# Date: 2024-07-05
# Description: A program to score a game of bowling for two players.

class Player:
    def __init__(self, name):
        # Initialize a player with their name, an empty list of frames, and set the current frame to 0.
        self.name = name
        self.frames = [[] for _ in range(10)]
        self.current_frame = 0

    def record_roll(self, pins):
        # Record the number of pins knocked down in the current frame.
        if self.current_frame < 10:
            self.frames[self.current_frame].append(pins)
            # If a frame is completed (either by 2 rolls or a strike), move to the next frame.
            if len(self.frames[self.current_frame]) == 2 or pins == 10:
                self.current_frame += 1

    def calculate_score(self):
        # Calculate the total score for the player.
        score = 0
        for i in range(10):
            frame = self.frames[i]
            if len(frame) == 2 and sum(frame) == 10:  # Spare
                next_roll = self.frames[i + 1][0] if i + 1 < 10 else 0
                score += 10 + next_roll
            elif len(frame) == 1 and frame[0] == 10:  # Strike
                next_rolls = self._get_next_two_rolls(i)
                score += 10 + sum(next_rolls)
            else:  # Open frame
                score += sum(frame)
        return score

    def _get_next_two_rolls(self, frame_index):
        # Helper function to get the next two rolls after a strike.
        rolls = []
        for i in range(frame_index + 1, 10):
            rolls.extend(self.frames[i])
            if len(rolls) >= 2:
                return rolls[:2]
        return rolls[:2]

def get_roll(player_name):
    # Prompt the user for the number of pins knocked down by the player.
    while True:
        try:
            pins = int(input(f"Enter the number of pins knocked down by {player_name}: "))
            if 0 <= pins <= 10:
                return pins
            else:
                print("Invalid input. Please enter a number between 0 and 10.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_turn_scores(player):
    # Handle a player's turn by recording one or two rolls, depending on whether the first roll is a strike.
    roll1 = get_roll(player.name)
    player.record_roll(roll1)
    if roll1 < 10:
        roll2 = get_roll(player.name)
        player.record_roll(roll2)

def get_game_scores(players):
    # Manage the entire game, allowing each player to take turns for 10 frames.
    for frame in range(10):
        for player in players:
            print(f"Frame {frame + 1}, {player.name}'s turn:")
            get_turn_scores(player)

    # Calculate and display the final scores for each player.
    scores = [player.calculate_score() for player in players]
    for player, score in zip(players, scores):
        print(f"{player.name}'s total score: {score}")
    return scores

def main():
    # Set up the game by getting player names and initializing Player objects.
    player_names = [input("Enter the name of Player 1: "), input("Enter the name of Player 2: ")]
    players = [Player(name) for name in player_names]

    while True:
        # Play a game and determine the winner.
        get_game_scores(players)
        winner = max(players, key=lambda player: player.calculate_score())
        print(f"The winner is {winner.name} with a score of {winner.calculate_score()}!")

        # Ask if the users want to play another game.
        another_game = input("Do you want to play another game? (yes/no): ").strip().lower()
        if another_game != 'yes':
            break
        # Reset players for a new game.
        players = [Player(name) for name in player_names]

if __name__ == "__main__":
    main()

