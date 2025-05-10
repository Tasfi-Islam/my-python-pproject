import tkinter as tk
import random

DICTIONARY = ['apple', 'brave', 'clock', 'dance', 'early', 'first', 'group', 'hello',
              'input', 'juice', 'shila', 'nisat', 'tasfi', 'maria', 'queen', 'ready',
              'ghost', 'jelly', 'stone', 'magic', 'snipe', 'green', 'irony', 'cheap',
              'shell', 'money', 'arrow', 'glass', 'melon', 'third', 'xenon', 'redon',
              'spicy', 'gamer', 'words', 'title', 'drone', 'phone', 'candy', 'fluid',
              'ships', 'score', 'eagle', 'grain', 'field', 'plane', 'stars', 'earth',
              'alien', 'smart', 'phony', 'young', 'zebra', 'xerox', 'women', 'valid',
              'value', 'queen', 'dandy', 'knife', 'board', 'lemon', 'lover', 'novel']

class GhostGame:
    def __init__(self, root):
        self.root = root
        self.root.title("2-Player Ghost Game")
        self.root.geometry("400x550")
        self.root.configure(bg="black")

        self.scores = {1: 0, 2: 0}
        self.prefix = ""
        self.current_player = 1
        self.game_over = False

        self.score_label = tk.Label(root, text="Player 1: 0 | Player 2: 0",
                                    font=("Courier", 14, "bold"), bg="black", fg="#39FF14")
        self.score_label.pack(pady=10)

        self.word_display = tk.Label(root, text="_ _ _ _ _",
                                     font=("Courier", 32, "bold"), bg="black", fg="#00FFFF")
        self.word_display.pack(pady=20)

        self.status_label = tk.Label(root, text="Player 1's turn",
                                     font=("Courier", 12), bg="black", fg="#FF00FF")
        self.status_label.pack(pady=5)

        self.letter_frame = tk.Frame(root, bg="black")
        self.letter_frame.pack()

        self.result_label = tk.Label(root, text="", font=("Courier", 12, "bold"),
                                     bg="black", fg="#FFD700")
        self.result_label.pack(pady=12)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game,
                                      font=("Courier", 14, "bold"), bg="#8B00FF", fg="white",
                                      activebackground="#DA70D6", relief="flat", width=12, height=2)
        self.reset_button.pack(pady=20)

        self.update_display()

    def reset_game(self):
        self.prefix = ""
        self.game_over = False
        self.result_label.config(text="")
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_display()

    def update_display(self):
        self.score_label.config(text=f"Player 1: {self.scores[1]} | Player 2: {self.scores[2]}")
        if not self.game_over:
            self.status_label.config(text=f"Player {self.current_player}'s turn")

        display = [self.prefix[i].upper() if i < len(self.prefix) else '_' for i in range(5)]
        self.word_display.config(text=" ".join(display))

        for widget in self.letter_frame.winfo_children():
            widget.destroy()

        possible_letters = list(set(self.get_next_letters()))
        all_letters = list('abcdefghijklmnopqrstuvwxyz')

        distractors = [l for l in all_letters if l not in possible_letters and l not in self.prefix]
        random.shuffle(possible_letters)
        random.shuffle(distractors)

        display_letters = (possible_letters + distractors)[:10]
        random.shuffle(display_letters)

        for i, letter in enumerate(display_letters):
            btn = tk.Button(self.letter_frame, text=letter.upper(), width=4, height=2,
                            font=("Courier", 12, "bold"), bg="#111111", fg="#00FFEF",
                            activebackground="#FF00FF", relief="ridge",
                            command=lambda l=letter: self.play_turn(l))
            btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)

    def get_next_letters(self):
        return [word[len(self.prefix)] for word in DICTIONARY
                if word.startswith(self.prefix) and len(word) > len(self.prefix)]

    def play_turn(self, letter):
        if self.game_over:
            return

        self.prefix += letter.lower()
        display = [self.prefix[i].upper() if i < len(self.prefix) else '_' for i in range(5)]
        self.word_display.config(text=" ".join(display))

        if self.prefix in DICTIONARY and len(self.prefix) == 5:
            self.end_game(loser=self.current_player, reason="Word completed")
        elif not any(word.startswith(self.prefix) for word in DICTIONARY):
            self.end_game(loser=self.current_player, reason="No possible continuations")
        else:
            self.current_player = 2 if self.current_player == 1 else 1
            self.update_display()

    def end_game(self, loser, reason):
        self.game_over = True
        winner = 2 if loser == 1 else 1
        self.scores[winner] += 1

        self.status_label.config(
            text=f"Player {loser} loses ({reason})!\nPlayer {winner} wins! Final word: {self.prefix.upper()}",
            fg="#FF6347"
        )

        for widget in self.letter_frame.winfo_children():
            widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = GhostGame(root)
    root.mainloop()
