import tkinter as tk
import random
import math

# --------------------
# CONFIG COLORS & FONT
# --------------------
BG_COLOR = "#050505"
NEON_PINK = "#ff00ff"
NEON_BLUE = "#00ffff"
NEON_YELLOW = "#ffd700"
NEON_RED = "#ff2e63"
NEON_GREEN = "#16c79a"
WHITE = "#ffffff"

FONT_BIG = ("Arial", 22, "bold")
FONT_MED = ("Arial", 14, "bold")

# --------------------
# MAIN APP CLASS
# --------------------
class MiniCasino:
    def __init__(self, root):
        self.root = root
        root.title("✨ Neon Mini Casino ✨")
        root.geometry("800x600")
        root.configure(bg=BG_COLOR)
        self.main_menu()

    # --------------------
    # CLEAR SCREEN
    # --------------------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # --------------------
    # MAIN MENU
    # --------------------
    def main_menu(self):
        self.clear()
        tk.Label(self.root, text="✨ NEON MINI CASINO ✨",
                 font=FONT_BIG, fg=NEON_PINK, bg=BG_COLOR).pack(pady=30)

        self.create_button("🎯 Roulette", self.roulette_screen)
        self.create_button("🎰 Slots", self.slots_screen)
        self.create_button("🃏 Blackjack", self.blackjack_screen)
        self.create_button("Exit", self.root.quit)

    # --------------------
    # BUTTON CREATOR
    # --------------------
    def create_button(self, text, command):
        btn = tk.Button(
            self.root, text=text, width=20, font=FONT_MED,
            bg=NEON_BLUE, fg=WHITE, command=command
        )
        btn.pack(pady=10)

    # --------------------
    # ROULETTE SCREEN
    # --------------------
    def roulette_screen(self):
        self.clear()
        tk.Label(self.root, text="🎯 NEON ROULETTE", font=FONT_BIG,
                 fg=NEON_YELLOW, bg=BG_COLOR).pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=500, height=500, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.C = 250
        self.R = 180

        # Draw wheel
        self.segments = []
        for i in range(36):
            start = i * 10
            color = NEON_RED if i % 2 == 0 else NEON_BLUE
            seg = self.canvas.create_arc(
                self.C - self.R, self.C - self.R,
                self.C + self.R, self.C + self.R,
                start=start, extent=10, fill=color, outline=NEON_YELLOW, width=2
            )
            self.segments.append(seg)

        # Center
        self.canvas.create_oval(self.C - 40, self.C - 40, self.C + 40, self.C + 40, fill=NEON_YELLOW)

        # Ball
        self.ball = self.canvas.create_oval(0, 0, 0, 0, fill=WHITE)
        self.angle = 0
        self.speed = 0
        self.spinning = False

        self.result_text = self.canvas.create_text(self.C, self.C, text="", font=("Arial", 28, "bold"), fill=NEON_PINK)

        # Buttons
        self.create_screen_button("SPIN", self.spin_roulette)
        self.create_screen_button("BACK", self.main_menu)

    def create_screen_button(self, text, command):
        btn = tk.Button(self.root, text=text, width=15, font=FONT_MED, bg=NEON_GREEN, fg=WHITE, command=command)
        btn.pack(pady=5)

    def spin_roulette(self):
        if self.spinning: return
        self.canvas.itemconfig(self.result_text, text="")
        self.angle = random.uniform(0, math.pi*2)
        self.speed = random.uniform(0.35, 0.45)
        self.spinning = True
        self.animate_ball()

    def animate_ball(self):
        if self.speed < 0.01:
            self.spinning = False
            number = int((self.angle % (2*math.pi)) / (2*math.pi) * 36)
            self.canvas.itemconfig(self.result_text, text=str(number))
            return
        x = self.C + math.cos(self.angle)*self.R
        y = self.C + math.sin(self.angle)*self.R
        self.canvas.coords(self.ball, x-8, y-8, x+8, y+8)
        self.angle += self.speed
        self.speed *= 0.985
        self.root.after(20, self.animate_ball)

    # --------------------
    # SLOTS SCREEN
    # --------------------
    def slots_screen(self):
        self.clear()
        tk.Label(self.root, text="🎰 NEON SLOTS", font=FONT_BIG, fg=NEON_YELLOW, bg=BG_COLOR).pack(pady=10)

        self.reels = []
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=20)

        for _ in range(3):
            lbl = tk.Label(frame, text="❓", font=("Arial", 45), width=3, bg=NEON_BLUE, fg=WHITE)
            lbl.pack(side="left", padx=10)
            self.reels.append(lbl)

        self.slots_result = tk.Label(self.root, text="", font=FONT_MED, bg=BG_COLOR, fg=NEON_PINK)
        self.slots_result.pack(pady=10)

        self.create_screen_button("SPIN", self.spin_slots)
        self.create_screen_button("BACK", self.main_menu)

    def spin_slots(self):
        symbols = ["🍒","🍋","🔔","⭐","7️⃣"]
        results = [random.choice(symbols) for _ in range(3)]
        for i in range(3):
            self.reels[i].config(text=results[i])
        if results.count(results[0])==3:
            self.slots_result.config(text="🎉 JACKPOT!")
        else:
            self.slots_result.config(text="Try again!")

    # --------------------
    # BLACKJACK SCREEN
    # --------------------
    def blackjack_screen(self):
        self.clear()
        tk.Label(self.root, text="🃏 NEON BLACKJACK", font=FONT_BIG, fg=NEON_YELLOW, bg=BG_COLOR).pack(pady=10)

        self.player_cards = []
        self.dealer_cards = []

        self.player_lbl = tk.Label(self.root, text="Player: ", font=FONT_MED, bg=BG_COLOR, fg=NEON_PINK)
        self.player_lbl.pack(pady=5)
        self.dealer_lbl = tk.Label(self.root, text="Dealer: ", font=FONT_MED, bg=BG_COLOR, fg=NEON_PINK)
        self.dealer_lbl.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Deal", width=10, bg=NEON_GREEN, fg=WHITE, command=self.deal).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Hit", width=10, bg=NEON_GREEN, fg=WHITE, command=self.hit).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Stand", width=10, bg=NEON_GREEN, fg=WHITE, command=self.stand).pack(side="left", padx=5)

        tk.Button(self.root, text="BACK", width=12, bg=NEON_RED, fg=WHITE, command=self.main_menu).pack(pady=10)

        self.status_lbl = tk.Label(self.root, text="", font=FONT_MED, bg=BG_COLOR, fg=NEON_PINK)
        self.status_lbl.pack(pady=10)

    # --------------------
    # BLACKJACK LOGIC
    # --------------------
    def draw_card(self):
        return random.choice(["2","3","4","5","6","7","8","9","10","J","Q","K","A"])

    def card_value(self, card):
        if card in ["J","Q","K"]: return 10
        if card == "A": return 11
        return int(card)

    def update_blackjack(self):
        self.player_lbl.config(text=f"Player: {' '.join(self.player_cards)}")
        self.dealer_lbl.config(text=f"Dealer: {' '.join(self.dealer_cards)}")

    def deal(self):
        self.player_cards = [self.draw_card(), self.draw_card()]
        self.dealer_cards = [self.draw_card(), self.draw_card()]
        self.status_lbl.config(text="")
        self.update_blackjack()

    def hit(self):
        self.player_cards.append(self.draw_card())
        self.update_blackjack()

    def stand(self):
        player = sum(self.card_value(c) for c in self.player_cards)
        dealer = sum(self.card_value(c) for c in self.dealer_cards)
        if player > 21: result = "Player busts!"
        elif dealer > 21 or player > dealer: result = "Player wins!"
        elif dealer > player: result = "Dealer wins!"
        else: result = "Push (tie)"
        self.status_lbl.config(text=result)

# --------------------
# RUN APP
# --------------------
root = tk.Tk()
app = MiniCasino(root)
root.mainloop()
