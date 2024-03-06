class rawGame:
    def __init__(self, player_choice, ai_player):
        self.numPieces = 12
        self.numPieces2 = 8

        self.board_size = 7
        self.board_matrix = [[0] * self.board_size for _ in range(self.board_size)]  # Matriz do tabuleiro
        for piece in {(2, 0), (3, 0), (4, 0), (6, 2), (6, 3), (6, 4), (0, 2), (0, 3), (0, 4), (2, 6), (3, 6), (4, 6)}:
            row, col = piece
            self.board_matrix[col][row] = 1
        for piece in {(2, 2), (2, 3), (2, 4), (4, 2), (4, 3), (4, 4), (3, 2), (3, 4)}:
            row, col = piece
            self.board_matrix[col][row] = 2
        for flag in {(3, 3)}:
            row, col = flag
            self.board_matrix[col][row] = 3  # Define a célula como 3 para representar a bandeira

        self.selected_piece = None
        self.selected_piece2 = None
        self.selected_flag = None
        self.player = player_choice

        self.ai_player = ai_player
        
    def evaluate_board(self, player):
        weight_pieces = 1.0

        player1_pieces = self.numPieces
        player2_pieces = self.numPieces2

        player1_score = weight_pieces * player1_pieces
        player2_score = weight_pieces * player2_pieces

        if player == 1:
            return player1_score - player2_score
        else:
            return player2_score - player1_pieces
    
    def verificar_bandeira_nos_cantos(self):
        corners = [(0, 0), (0, 6), (6, 0), (6, 6), (6,5), (6,4), (6,3), (6,2), (6,1), (1,6), (2,6), (3,6), (4,6), (5,6)] 
        flag_position = next(((i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board_matrix[i][j] == 3), None)

        if flag_position in corners:
            print("A bandeira está em um dos cantos do tabuleiro!")
            print("Jogo acabou")
            exit(0)
            
    def is_valid_move(self, origin, dest):
        if (dest[0] == origin[0] and abs(dest[1] - origin[1]) == 1) or \
        (dest[1] == origin[1] and abs(dest[0] - origin[0]) == 1):
            if self.board_matrix[dest[1]][dest[0]] == 0:
                return True
        elif (self.board_matrix[dest[1]][dest[0]] in {1, 2, 3}) and abs(dest[0] - origin[0]) == 1 and abs(dest[1] - origin[1]) == 1:
            return True
        return False
    
    def generate_moves(self, player):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if player == 1 and self.board_matrix[col][row] == 1:
                    for d_row in range(-1, 2):
                        for d_col in range(-1, 2):
                            if (d_row != 0 or d_col != 0) and 0 <= row + d_row < self.board_size and 0 <= col + d_col < self.board_size:
                                dest = (row + d_row, col + d_col)
                                if self.is_valid_move((row, col), dest):
                                    moves.append((row, col, dest))
                elif player == 2 and self.board_matrix[col][row] == 2:
                    for d_row in range(-1, 2):
                        for d_col in range(-1, 2):
                            if (d_row != 0 or d_col != 0) and 0 <= row + d_row < self.board_size and 0 <= col + d_col < self.board_size:
                                dest = (row + d_row, col + d_col)
                                if self.is_valid_move((row, col), dest):
                                    moves.append((row, col, dest))
        return moves    


    def game(self):
        current_player = self.player# Define o jogador atual com base na variável self.player
        while True:
            print("Tabuleiro atual:")
            for row in self.board_matrix:
                print(row)
            
            if current_player == 1 and self.board_matrix[3][3] == 1:
                print("Parabéns! Jogador 1 venceu!")
                break
            elif current_player == 2 and self.board_matrix[3][3] == 2:
                print("Parabéns! Jogador 2 venceu!")
                break
            
            if not self.generate_moves(current_player):
                print(f"Jogador {current_player} não tem movimentos válidos. O outro jogador vence!")
                break
            
            if current_player == self.player:  # Se o jogador atual for o mesmo que self.player, é a vez do jogador humano
                print(f"Jogador {current_player}, é sua vez.")
                while True:
                    try:
                        x, y = map(int, input("Digite as coordenadas x e y da peça que deseja mover (separadas por espaço): ").split())
                        if self.board_matrix[y][x] == current_player:
                            break
                        else:
                            print("Coordenadas inválidas. Por favor, escolha uma peça sua.")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite duas coordenadas separadas por espaço.")
                
                while True:
                    try:
                        x_dest, y_dest = map(int, input("Digite as coordenadas x e y para onde deseja mover a peça (separadas por espaço): ").split())
                        if self.is_valid_move((x, y), (x_dest, y_dest)):
                            break
                        else:
                            print("Movimento inválido. Por favor, escolha uma posição válida.")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite duas coordenadas separadas por espaço.")
                
                self.board_matrix[y][x] = 0
                self.board_matrix[y_dest][x_dest] = current_player
            else:  # Caso contrário, é a vez da IA
                _, best_move = self.minimax(3, float('-inf'), float('inf'), False)
                if best_move:
                    x, y, dest = best_move
                    x_dest, y_dest = dest
                    self.board_matrix[y][x] = 0
                    self.board_matrix[y_dest][x_dest] = self.ai_player
                
            self.verificar_bandeira_nos_cantos()
            current_player = 2 if current_player == 1 else 1  # Alterna para o próximo jogador


    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or not self.generate_moves(1) or not self.generate_moves(2):
            return self.evaluate_board(maximizing_player), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.generate_moves(1):
                x, y, dest = move
                if self.board_matrix[y][x] == 1:
                    temp_origin = self.board_matrix[y][x]
                    temp_dest = self.board_matrix[dest[1]][dest[0]]
                    self.board_matrix[y][x] = 0
                    self.board_matrix[dest[1]][dest[0]] = 1
                    eval, _ = self.minimax(depth - 1, alpha, beta, True)
                    self.board_matrix[dest[1]][dest[0]] = temp_dest
                    self.board_matrix[y][x] = temp_origin
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.generate_moves(2):
                x, y, dest = move
                if self.board_matrix[y][x] == 2:
                    temp_origin = self.board_matrix[y][x]
                    temp_dest = self.board_matrix[dest[1]][dest[0]]
                    self.board_matrix[y][x] = 0
                    self.board_matrix[dest[1]][dest[0]] = 2
                    eval, _ = self.minimax(depth - 1, alpha, beta, False)
                    self.board_matrix[dest[1]][dest[0]] = temp_dest
                    self.board_matrix[y][x] = temp_origin
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move


def main():
    print("Escolha o time que deseja jogar:")
    print("1. Silver (peças 1)")
    print("2. Gold (peças 2)")

    player_choice = int(input("Digite o número correspondente à sua escolha: "))

    if player_choice not in [1, 2]:
        print("Escolha inválida. Por favor, selecione 1 para Azul ou 2 para Verde.")
        return

    ai_player = 3 - player_choice  # Escolhe o time oposto ao do jogador

    game_instance = rawGame(player_choice, ai_player)
    game_instance.game()

if __name__ == "__main__":
    main()

