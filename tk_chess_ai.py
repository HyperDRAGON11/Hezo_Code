import tkinter as tk
from tkinter import messagebox
import threading
import time
import chess

SQUARE_SIZE = 80
BORDER = 20
LIGHT_COLOR = "#f0d9b5"
DARK_COLOR  = "#b58863"
HIGHLIGHT_MOVE = "#80c0ff"
HIGHLIGHT_FROM = "#66dd66"
HIGHLIGHT_CHECK = "#ff8c8c"
PIECE_FONT = ("Segoe UI Symbol", 42)
HUMAN_PLAYS_WHITE = True
DEFAULT_DEPTH = 3

UNICODE_PIECES = {
    chess.PAWN:   ("♙","♟"),
    chess.KNIGHT: ("♘","♞"),
    chess.BISHOP: ("♗","♝"),
    chess.ROOK:   ("♖","♜"),
    chess.QUEEN:  ("♕","♛"),
    chess.KING:   ("♔","♚"),
}

PST = {
    chess.PAWN: [
        0,5,5,0,5,10,50,0,0,10,-5,0,5,10,50,0,0,10,-10,20,25,30,10,0,5,5,10,27,27,10,5,5,5,5,10,25,25,10,5,5,0,10,10,0,10,15,10,0,0,0,0,-10,5,0,0,0,0,0,0,0,0,0,0,0
    ],
    chess.KNIGHT: [
       -50,-30,-10,-10,-10,-10,-30,-50,-30,-5,0,0,0,0,-5,-30,-10,0,10,15,15,10,0,-10,-10,5,15,20,20,15,5,-10,-10,0,15,20,20,15,0,-10,-10,5,10,15,15,10,5,-10,-30,-10,0,5,5,0,-10,-30,-50,-30,-20,-10,-10,-20,-30,-50
    ],
    chess.BISHOP: [
       -20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10,-10,5,5,10,10,5,5,-10,-10,0,5,10,10,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
         0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,0,0,5,10,10,5,0,0,5,10,10,15,15,10,10,5,0,0,0,5,5,0,0,0
    ],
    chess.QUEEN: [
       -20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20
    ],
    chess.KING: [
       -30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20
    ],
}

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING:  0,
}

def evaluate(board: chess.Board) -> int:
    if board.is_checkmate():
        return -100000 if board.turn else 100000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for piece_type in PIECE_VALUES:
        for sq in board.pieces(piece_type, chess.WHITE):
            score += PIECE_VALUES[piece_type]
            score += PST[piece_type][sq]
        for sq in board.pieces(piece_type, chess.BLACK):
            score -= PIECE_VALUES[piece_type]
            mirrored = chess.square_mirror(sq)
            score -= PST[piece_type][mirrored]
    score += 2 * board.legal_moves.count() if board.turn == chess.WHITE else -2 * board.legal_moves.count()
    return score

def negamax(board: chess.Board, depth: int, alpha: int, beta: int) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    max_eval = -10**9
    moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
    for move in moves:
        board.push(move)
        val = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        if val > max_eval:
            max_eval = val
        if max_eval > alpha:
            alpha = max_eval
        if alpha >= beta:
            break
    return max_eval

def best_move(board: chess.Board, depth: int) -> chess.Move:
    best = None
    alpha = -10**9
    beta = 10**9
    moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
    for move in moves:
        board.push(move)
        val = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        if val > alpha or best is None:
            alpha = val
            best = move
    return best

class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tkinter Chess vs AI")
        self.board = chess.Board()
        self.square_size = SQUARE_SIZE
        self.flipped = not HUMAN_PLAYS_WHITE
        self.select_from = None
        self.legal_targets = set()
        self.ai_thinking = False
        self.depth = DEFAULT_DEPTH
        self.canvas = tk.Canvas(self.root, width=BORDER*2 + 8*self.square_size,
                                height=BORDER*2 + 8*self.square_size, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=6)
        self.canvas.bind("<Button-1>", self.on_click)
        self.btn_undo = tk.Button(self.root, text="Undo", command=self.on_undo)
        self.btn_reset = tk.Button(self.root, text="Reset", command=self.on_reset)
        self.btn_flip = tk.Button(self.root, text="Flip Board", command=self.on_flip)
        tk.Label(self.root, text="AI Depth:").grid(row=1, column=3, sticky="e", padx=5)
        self.depth_var = tk.IntVar(value=self.depth)
        self.depth_menu = tk.OptionMenu(self.root, self.depth_var, 2,3,4,5, command=self.on_depth_change)
        self.btn_undo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.btn_reset.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.btn_flip.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.depth_menu.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.status = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status, anchor="w")
        self.status_label.grid(row=2, column=0, columnspan=6, sticky="we", padx=5, pady=5)
        self.draw_board()
        self.update_status()
        if not HUMAN_PLAYS_WHITE:
            self.root.after(300, self.trigger_ai_move)

    def square_to_xy(self, sq: chess.Square):
        file = chess.square_file(sq)
        rank = chess.square_rank(sq)
        if self.flipped:
            file = 7 - file
            rank = 7 - rank
        x = BORDER + file * self.square_size
        y = BORDER + (7 - rank) * self.square_size
        return x, y

    def xy_to_square(self, x: int, y: int):
        file = (x - BORDER) // self.square_size
        rank_from_top = (y - BORDER) // self.square_size
        if file < 0 or file > 7 or rank_from_top < 0 or rank_from_top > 7:
            return None
        rank = 7 - rank_from_top
        if self.flipped:
            file = 7 - file
            rank = 7 - rank
        return chess.square(file, rank)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for f in range(8):
                rr = 7 - r if not self.flipped else r
                ff = f if not self.flipped else 7 - f
                x = BORDER + f * self.square_size
                y = BORDER + r * self.square_size
                color = LIGHT_COLOR if (ff + rr) % 2 == 0 else DARK_COLOR
                self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, fill=color, outline=color)
        if self.board.is_check():
            king_sq = self.board.king(self.board.turn)
            if king_sq is not None:
                x, y = self.square_to_xy(king_sq)
                self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size,
                                             outline=HIGHLIGHT_CHECK, width=4)
        if self.select_from is not None:
            x, y = self.square_to_xy(self.select_from)
            self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size,
                                         outline=HIGHLIGHT_FROM, width=4)
            for t in self.legal_targets:
                tx, ty = self.square_to_xy(t)
                self.canvas.create_oval(tx + 0.35*self.square_size, ty + 0.35*self.square_size,
                                        tx + 0.65*self.square_size, ty + 0.65*self.square_size,
                                        fill=HIGHLIGHT_MOVE, outline="")
        for sq, piece in self.board.piece_map().items():
            x, y = self.square_to_xy(sq)
            sym = UNICODE_PIECES[piece.piece_type][0 if piece.color == chess.WHITE else 1]
            self.canvas.create_text(x + self.square_size/2, y + self.square_size/2,
                                    text=sym, font=PIECE_FONT)
        for i in range(8):
            file_char = "abcdefgh"[i]
            fi = i if not self.flipped else 7 - i
            x = BORDER + i * self.square_size + self.square_size - 14
            y = BORDER + 8 * self.square_size + 4
            self.canvas.create_text(x, y, text=file_char if not self.flipped else "abcdefgh"[fi])
            rank_char = str(i+1)
            ri = i if self.flipped else 7 - i
            x = 4
            y = BORDER + i * self.square_size + 14
            self.canvas.create_text(x, y, text=rank_char if not self.flipped else str(ri+1))

    def update_status(self):
        if self.board.is_game_over():
            outcome = self.board.outcome()
            if outcome is None:
                self.status.set("Game over")
            elif outcome.winner is None:
                self.status.set("Draw")
            elif outcome.winner:
                self.status.set("White wins")
            else:
                self.status.set("Black wins")
        else:
            self.status.set(("White" if self.board.turn else "Black") + " to move")

    def on_click(self, event):
        if self.ai_thinking or self.board.is_game_over():
            return
        is_human_turn = (self.board.turn == chess.WHITE and HUMAN_PLAYS_WHITE) or (self.board.turn == chess.BLACK and not HUMAN_PLAYS_WHITE)
        if not is_human_turn:
            return
        sq = self.xy_to_square(event.x, event.y)
        if sq is None:
            return
        if self.select_from is None:
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.board.turn:
                self.select_from = sq
                self.legal_targets = {m.to_square for m in self.board.legal_moves if m.from_square == sq}
                self.draw_board()
        else:
            move = chess.Move(self.select_from, sq)
            if move not in self.board.legal_moves:
                move = chess.Move(self.select_from, sq, promotion=chess.QUEEN)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.select_from = None
                self.legal_targets = set()
                self.draw_board()
                self.update_status()
                if not self.board.is_game_over():
                    self.trigger_ai_move()
            else:
                piece = self.board.piece_at(sq)
                if piece and piece.color == self.board.turn:
                    self.select_from = sq
                    self.legal_targets = {m.to_square for m in self.board.legal_moves if m.from_square == sq}
                else:
                    self.select_from = None
                    self.legal_targets = set()
                self.draw_board()

    def trigger_ai_move(self):
        self.ai_thinking = True
        self.status.set("AI thinking...")
        threading.Thread(target=self._ai_worker, daemon=True).start()

    def _ai_worker(self):
        start = time.time()
        try:
            mv = best_move(self.board, self.depth)
        except Exception:
            mv = None
        elapsed = time.time() - start
        self.root.after(0, self._apply_ai_move, mv, elapsed)

    def _apply_ai_move(self, mv, elapsed):
        if mv is None:
            self.ai_thinking = False
            messagebox.showerror("AI Error", "AI could not find a move.")
            return
        self.board.push(mv)
        self.ai_thinking = False
        self.draw_board()
        self.update_status()
        if self.board.is_game_over():
            outcome = self.board.outcome()
            if outcome is not None:
                if outcome.winner is None:
                    messagebox.showinfo("Game Over", "Draw!")
                elif outcome.winner:
                    messagebox.showinfo("Game Over", "White wins!")
                else:
                    messagebox.showinfo("Game Over", "Black wins!")

    def on_undo(self):
        if self.ai_thinking:
            return
        if len(self.board.move_stack) >= 1:
            self.board.pop()
        if len(self.board.move_stack) >= 1:
            human_turn_color = chess.WHITE if HUMAN_PLAYS_WHITE else chess.BLACK
            if self.board.turn != human_turn_color:
                self.board.pop()
        self.select_from = None
        self.legal_targets = set()
        self.draw_board()
        self.update_status()

    def on_reset(self):
        if self.ai_thinking:
            return
        self.board.reset()
        self.select_from = None
        self.legal_targets = set()
        self.draw_board()
        self.update_status()
        if not HUMAN_PLAYS_WHITE:
            self.root.after(300, self.trigger_ai_move)

    def on_flip(self):
        self.flipped = not self.flipped
        self.draw_board()

    def on_depth_change(self, value):
        try:
            self.depth = int(value)
        except:
            self.depth = DEFAULT_DEPTH

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ChessApp().run()
