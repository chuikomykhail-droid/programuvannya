import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame


class CheckersGUI:
    def __init__(self, root, game_logic):
        self.root = root
        self.game = game_logic
        self.root.title("Шашки")

        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.PANEL_WIDTH = 350
        board_space_w = screen_w - self.PANEL_WIDTH
        max_dim = min(board_space_w, screen_h) * 0.95
        self.SQUARE_SIZE = int(max_dim // 8)

        self.p_pad = int(self.SQUARE_SIZE * 0.15)
        self.d_pad = int(self.SQUARE_SIZE * 0.40)
        self.c_off = self.SQUARE_SIZE // 2
        self.line_w = max(3, int(self.SQUARE_SIZE * 0.06))

        self.root.bind("<Escape>", lambda e: self.root.quit())
        self.root.bind("r", lambda e: self.restart_game())
        self.root.bind("R", lambda e: self.restart_game())
        self.root.bind("к", lambda e: self.restart_game())
        self.root.bind("К", lambda e: self.restart_game())

        self.main_frame = tk.Frame(root, bg="dimgray")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.board_frame = tk.Frame(self.main_frame, bg="dimgray")
        self.board_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.ui_frame = tk.Frame(self.main_frame, bg="darkgray", width=self.PANEL_WIDTH)
        self.ui_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.ui_frame.pack_propagate(False)

        self.turn_lbl = tk.Label(self.ui_frame, text="Хід білих", font=("Helvetica", 24, "bold"), bg="darkgray",
                                 fg="white")
        self.turn_lbl.pack(pady=(80, 40))

        self.restart_btn = tk.Button(self.ui_frame, text="Почати знову (R)", font=("Helvetica", 14, "bold"),
                                     bg="forestgreen", fg="white", activebackground="green", cursor="hand2",
                                     command=self.restart_game, borderwidth=0, pady=15)
        self.restart_btn.pack(fill=tk.X, padx=30, pady=10)

        self.exit_btn = tk.Button(self.ui_frame, text="Вийти (Esc)", font=("Helvetica", 14, "bold"),
                                  bg="firebrick", fg="white", activebackground="red", cursor="hand2",
                                  command=self.root.quit, borderwidth=0, pady=15)
        self.exit_btn.pack(fill=tk.X, padx=30, pady=10)

        self.setup_music_player()

        self.canvas = tk.Canvas(self.board_frame, width=8 * self.SQUARE_SIZE, height=8 * self.SQUARE_SIZE,
                                highlightthickness=0, bg="dimgray")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.selected_piece = None
        self.valid_moves = {}
        self.is_animating = False
        self.animating_piece = None
        self.shrinking_pieces = []

        self.textures = {}
        self.load_textures()

        self.canvas.bind("<Button-1>", self.on_click)
        self.update_turn_state()
        self.draw_board()

    def setup_music_player(self):
        self.music_frame = tk.Frame(self.ui_frame, bg="gray", bd=2, relief="groove")
        self.music_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=30)

        tk.Label(self.music_frame, text="🎵 Фонова музика", font=("Helvetica", 14, "bold"), bg="gray", fg="wheat").pack(
            pady=10)

        pygame.mixer.init()
        self.is_playing = False
        self.playlist = ["1.mp3", "2.mp3", "3.mp3", "4.mp3", "5.mp3"]
        self.current_track_idx = 0

        self.track_lbl = tk.Label(self.music_frame, text="Очікування...", font=("Helvetica", 10), bg="gray", fg="white",
                                  wraplength=280)
        self.track_lbl.pack(pady=(0, 5))

        btn_container = tk.Frame(self.music_frame, bg="gray")
        btn_container.pack(fill=tk.X, padx=20, pady=5)

        self.btn_play_music = tk.Button(btn_container, text="▶ Play", font=("Helvetica", 11, "bold"),
                                        bg="dodgerblue", fg="white", activebackground="blue", cursor="hand2",
                                        borderwidth=0,
                                        command=self.toggle_music, width=8, pady=8)
        self.btn_play_music.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

        self.btn_next_music = tk.Button(btn_container, text="⏭ Next", font=("Helvetica", 11, "bold"),
                                        bg="dimgray", fg="white", activebackground="gray", cursor="hand2",
                                        borderwidth=0,
                                        command=self.next_track, width=8, pady=8)
        self.btn_next_music.pack(side=tk.RIGHT, padx=(5, 0), expand=True, fill=tk.X)

        tk.Label(self.music_frame, text="Гучність", font=("Helvetica", 9), bg="gray", fg="white").pack(pady=(5, 0))
        self.vol_slider = tk.Scale(self.music_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                   bg="gray", fg="limegreen", highlightthickness=0, bd=0,
                                   troughcolor="dimgray", command=self.set_volume)
        self.vol_slider.set(30)
        self.vol_slider.pack(fill=tk.X, padx=20, pady=(0, 10))

        if self.playlist:
            self.load_track(self.current_track_idx, auto_play=False)

    def load_track(self, index, auto_play=True):
        if not self.playlist: return
        track_name = self.playlist[index]
        pygame.mixer.music.load(track_name)
        display_name = track_name.split(".")[0][:30]
        self.track_lbl.config(text=f"🎵 {display_name}")

        if auto_play:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.vol_slider.get() / 100)
            self.btn_play_music.config(text="⏸ Pause")
            self.is_playing = True

    def toggle_music(self):
        if not self.playlist: return
        if self.is_playing:
            pygame.mixer.music.pause()
            self.btn_play_music.config(text="▶ Play")
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.vol_slider.get() / 100)
            self.btn_play_music.config(text="⏸ Pause")
            self.is_playing = True

    def next_track(self):
        if not self.playlist: return
        self.current_track_idx = (self.current_track_idx + 1) % len(self.playlist)
        self.load_track(self.current_track_idx, auto_play=self.is_playing)

    def set_volume(self, val):
        pygame.mixer.music.set_volume(int(val) / 100)

    def restart_game(self):
        if self.is_animating: return
        self.game.reset()
        self.selected_piece = None
        self.valid_moves = {}
        self.is_animating = False
        self.animating_piece = None
        self.shrinking_pieces = []
        self.update_turn_state()
        self.draw_board()

    def load_textures(self):
        sz = (self.SQUARE_SIZE, self.SQUARE_SIZE)
        self.textures['light_sq'] = ImageTk.PhotoImage(Image.open("light_wood.png").resize(sz))
        self.textures['dark_sq'] = ImageTk.PhotoImage(Image.open("dark_wood.png").resize(sz))
        p_sz = (self.SQUARE_SIZE - 2 * self.p_pad, self.SQUARE_SIZE - 2 * self.p_pad)
        self.textures['white_p'] = ImageTk.PhotoImage(Image.open("white_piece.png").resize(p_sz))
        self.textures['black_p'] = ImageTk.PhotoImage(Image.open("black_piece.png").resize(p_sz))
        self.textures['white_k'] = ImageTk.PhotoImage(Image.open("white_king.png").resize(p_sz))
        self.textures['black_k'] = ImageTk.PhotoImage(Image.open("black_king.png").resize(p_sz))

    def update_turn_state(self):
        if self.game.turn == "white":
            self.turn_lbl.config(text="Хід білих", fg="white")
        else:
            self.turn_lbl.config(text="Хід чорних", fg="black")

        self.valid_moves = self.game.get_valid_moves(self.game.turn)
        if not self.valid_moves:
            winner = "Чорні" if self.game.turn == "white" else "Білі"
            messagebox.showinfo("Кінець гри", f"Перемога! {winner} виграли.")
            self.restart_game()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                is_dark = (row + col) % 2 != 0
                img = self.textures['dark_sq'] if is_dark else self.textures['light_sq']
                self.canvas.create_image(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, anchor="nw", image=img)

        if self.selected_piece and not self.is_animating:
            r, c = self.selected_piece.row, self.selected_piece.col
            self.canvas.create_rectangle(
                c * self.SQUARE_SIZE, r * self.SQUARE_SIZE,
                (c + 1) * self.SQUARE_SIZE, (r + 1) * self.SQUARE_SIZE, outline="limegreen", width=self.line_w
            )

        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]
                if piece and piece != self.animating_piece:
                    cx, cy = col * self.SQUARE_SIZE + self.c_off, row * self.SQUARE_SIZE + self.c_off
                    if piece.is_king:
                        img = self.textures['white_k'] if piece.color == "white" else self.textures['black_k']
                    else:
                        img = self.textures['white_p'] if piece.color == "white" else self.textures['black_p']
                    self.canvas.create_image(cx, cy, anchor="center", image=img)

        for sp in self.shrinking_pieces:
            r, c, padding = sp['row'], sp['col'], sp['padding']
            if padding < self.c_off:
                self.canvas.create_oval(
                    c * self.SQUARE_SIZE + padding, r * self.SQUARE_SIZE + padding,
                    (c + 1) * self.SQUARE_SIZE - padding, (r + 1) * self.SQUARE_SIZE - padding, fill=sp['color'],
                    outline="black"
                )

        if self.selected_piece and not self.is_animating:
            for (move_r, move_c), data in self.valid_moves.get(self.selected_piece, {}).items():
                path = data.get('path', [])
                if len(data.get('captures', [])) > 0 and len(path) > 1:
                    for i in range(len(path) - 1):
                        r1, c1, r2, c2 = path[i][0], path[i][1], path[i + 1][0], path[i + 1][1]
                        self.canvas.create_line(
                            c1 * self.SQUARE_SIZE + self.c_off, r1 * self.SQUARE_SIZE + self.c_off,
                            c2 * self.SQUARE_SIZE + self.c_off, r2 * self.SQUARE_SIZE + self.c_off,
                            fill="red", width=self.line_w, arrow=tk.LAST, arrowshape=(16, 20, 6)
                        )
                self.canvas.create_oval(
                    move_c * self.SQUARE_SIZE + self.d_pad, move_r * self.SQUARE_SIZE + self.d_pad,
                    (move_c + 1) * self.SQUARE_SIZE - self.d_pad, (move_r + 1) * self.SQUARE_SIZE - self.d_pad,
                    fill="limegreen", outline=""
                )

    def on_click(self, event):
        if self.is_animating: return
        col, row = event.x // self.SQUARE_SIZE, event.y // self.SQUARE_SIZE
        if col < 0 or col >= 8 or row < 0 or row >= 8: return

        clicked_piece = self.game.board[row][col]

        if clicked_piece in self.valid_moves:
            self.selected_piece = clicked_piece
            self.draw_board()
            return

        if self.selected_piece:
            target_pos = (row, col)
            if target_pos in self.valid_moves.get(self.selected_piece, {}):
                data = self.valid_moves[self.selected_piece][target_pos]
                self.start_animation(self.selected_piece, target_pos, data['path'], data['captures'])
            else:
                self.selected_piece = None
                self.draw_board()

    def start_animation(self, piece, target_pos, path, captures):
        self.is_animating = True
        self.animating_piece = piece
        self.selected_piece = None
        self.draw_board()

        r0, c0 = path[0]
        cx, cy = c0 * self.SQUARE_SIZE + self.c_off, r0 * self.SQUARE_SIZE + self.c_off

        if piece.is_king:
            img = self.textures['white_k'] if piece.color == "white" else self.textures['black_k']
        else:
            img = self.textures['white_p'] if piece.color == "white" else self.textures['black_p']
        clone_id = self.canvas.create_image(cx, cy, anchor="center", image=img)

        self.animate_segment(piece, target_pos, path, captures, 0, 0, 12, clone_id)

    def animate_segment(self, piece, target_pos, path, captures, seg_idx, frame, max_frames, clone_id):
        if seg_idx >= len(path) - 1:
            self.canvas.delete(clone_id)

            for r, c in captures:
                captured_piece = self.game.board[r][c]
                if captured_piece:
                    self.shrinking_pieces.append({
                        'row': r, 'col': c,
                        'color': "white" if captured_piece.color == "white" else "black",
                        'padding': self.p_pad
                    })

            self.game.move_piece(piece, target_pos)
            self.animating_piece = None

            if self.shrinking_pieces:
                self.animate_shrink(0, 10)
            else:
                self.end_move_transition()
            return

        r_start, c_start = path[seg_idx]
        r_end, c_end = path[seg_idx + 1]
        progress = frame / max_frames

        cur_r = r_start + (r_end - r_start) * progress
        cur_c = c_start + (c_end - c_start) * progress

        cx, cy = cur_c * self.SQUARE_SIZE + self.c_off, cur_r * self.SQUARE_SIZE + self.c_off
        self.canvas.coords(clone_id, cx, cy)

        if frame < max_frames:
            self.root.after(15, self.animate_segment, piece, target_pos, path, captures, seg_idx, frame + 1, max_frames,
                            clone_id)
        else:
            self.root.after(15, self.animate_segment, piece, target_pos, path, captures, seg_idx + 1, 0, max_frames,
                            clone_id)

    def animate_shrink(self, frame, max_frames):
        if frame > max_frames:
            self.end_move_transition()
            return
        current_padding = self.p_pad + (self.c_off - self.p_pad) * (frame / max_frames)
        for sp in self.shrinking_pieces:
            sp['padding'] = current_padding
        self.draw_board()
        self.root.after(15, self.animate_shrink, frame + 1, max_frames)

    def end_move_transition(self):
        self.shrinking_pieces = []
        self.is_animating = False
        self.update_turn_state()
        self.draw_board()