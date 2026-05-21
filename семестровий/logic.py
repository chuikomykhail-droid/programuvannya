class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False

    def _get_capture_moves(self, board, current_r, current_c, captured_so_far, path_so_far):
        moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            if self.is_king:
                step = 1
                enemy_found = None
                while True:
                    r = current_r + dr * step
                    c = current_c + dc * step
                    if not (0 <= r < 8 and 0 <= c < 8): break
                    target = board[r][c]
                    if target is None or (r == self.row and c == self.col):
                        if enemy_found:
                            new_captured = captured_so_far + [enemy_found]
                            new_path = path_so_far + [(r, c)]
                            next_moves = self._get_capture_moves(board, r, c, new_captured, new_path)
                            if next_moves:
                                for pos, data in next_moves.items():
                                    if pos not in moves or len(data['captures']) > len(moves[pos]['captures']):
                                        moves[pos] = data
                            else:
                                moves[(r, c)] = {'captures': new_captured, 'path': new_path}
                        step += 1
                    elif target.color == self.color or (r, c) in captured_so_far: break
                    else:
                        if enemy_found: break
                        enemy_found = (r, c)
                        step += 1
            else:
                enemy_r, enemy_c = current_r + dr, current_c + dc
                jump_r, jump_c = current_r + 2 * dr, current_c + 2 * dc
                if 0 <= jump_r < 8 and 0 <= jump_c < 8:
                    enemy = board[enemy_r][enemy_c]
                    if enemy and enemy.color != self.color and (enemy_r, enemy_c) not in captured_so_far:
                        if board[jump_r][jump_c] is None or (jump_r == self.row and jump_c == self.col):
                            new_captured = captured_so_far + [(enemy_r, enemy_c)]
                            new_path = path_so_far + [(jump_r, jump_c)]
                            next_moves = self._get_capture_moves(board, jump_r, jump_c, new_captured, new_path)
                            if next_moves:
                                for pos, data in next_moves.items():
                                    if pos not in moves or len(data['captures']) > len(moves[pos]['captures']):
                                        moves[pos] = data
                            else:
                                moves[(jump_r, jump_c)] = {'captures': new_captured, 'path': new_path}
        return moves

    def get_moves(self, board):
        capture_moves = self._get_capture_moves(board, self.row, self.col, [], [(self.row, self.col)])
        if capture_moves: return capture_moves

        moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        forward_dir = -1 if self.color == "white" else 1

        for dr, dc in directions:
            if self.is_king:
                step = 1
                while True:
                    r = self.row + dr * step
                    c = self.col + dc * step
                    if 0 <= r < 8 and 0 <= c < 8 and board[r][c] is None:
                        moves[(r, c)] = {'captures': [], 'path': [(self.row, self.col), (r, c)]}
                        step += 1
                    else: break
            else:
                r, c = self.row + dr, self.col + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] is None:
                    if dr == forward_dir:
                        moves[(r, c)] = {'captures': [], 'path': [(self.row, self.col), (r, c)]}
        return moves


class GameLogic:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.turn = "white"
        self._setup_board()

    def _setup_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    if row < 3: self.board[row][col] = Piece(row, col, "black")
                    elif row > 4: self.board[row][col] = Piece(row, col, "white")

    def get_valid_moves(self, player_color):
        all_moves = {}
        must_capture = False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == player_color:
                    moves = piece.get_moves(self.board)
                    if moves:
                        all_moves[piece] = moves
                        for target, data in moves.items():
                            if len(data['captures']) > 0: must_capture = True
        if must_capture:
            filtered_moves = {}
            for piece, moves in all_moves.items():
                captures_only = {target: data for target, data in moves.items() if len(data['captures']) > 0}
                if captures_only: filtered_moves[piece] = captures_only
            return filtered_moves
        return all_moves

    def move_piece(self, piece, target_pos):
        target_r, target_c = target_pos
        valid_moves = piece.get_moves(self.board)
        move_data = valid_moves.get(target_pos, {})
        captured_pieces = move_data.get('captures', [])

        self.board[piece.row][piece.col] = None
        piece.row, piece.col = target_r, target_c
        self.board[target_r][target_c] = piece

        for r, c in captured_pieces:
            self.board[r][c] = None

        if piece.color == "white" and target_r == 0: piece.is_king = True
        elif piece.color == "black" and target_r == 7: piece.is_king = True

        self.turn = "black" if self.turn == "white" else "white"