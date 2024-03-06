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
        weight_defense = 100.0
        weight_flag = 1000.0
        weight_border = 500.0  # Novo peso para a proximidade da bandeira com a borda

        player1_pieces = self.numPieces
        player2_pieces = self.numPieces2

        player1_score = weight_pieces * player1_pieces
        player2_score = weight_pieces * player2_pieces
        
        x, y = self.find_flag_position()

        # Calcula a distância da bandeira até a borda mais próxima
        distance_to_border = min(x, y, self.board_size - 1 - x, self.board_size - 1 - y)
        border_score = weight_border * (self.board_size - distance_to_border)

        # Verifica se alguma peça do jogador 2 está ameaçada
        pieces_threatened = self.are_pieces_threatened(2)

        # Se alguma peça estiver ameaçada, aumente a pontuação do jogador 2 para priorizar a defesa
        if pieces_threatened:
            return player2_score - player1_score + weight_defense + border_score
        if self.is_flag_threatened(x, y):
            return player2_score - player1_score + weight_flag + border_score
        else:
            return player2_score - player1_score + border_score



    def are_pieces_threatened(self, player):
        # Verifica se alguma peça do jogador está ameaçada
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board_matrix[row][col] == player:
                    for d_row in range(-1, 2):
                        for d_col in range(-1, 2):
                            if (d_row != 0 or d_col != 0) and 0 <= row + d_row < self.board_size and 0 <= col + d_col < self.board_size:
                                if self.board_matrix[row + d_row][col + d_col] == 1:
                                    return True
        return False


    def find_flag_position(self):
        # Encontra a posição da bandeira no tabuleiro
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board_matrix[row][col] == 3:  # Flag
                    return row, col
        # Retorna (-1, -1) se a bandeira não for encontrada (o que não deve acontecer)
        return -1, -1
        
    def is_flag_threatened(self, flag_row, flag_col):
        # Verifica se a bandeira está ameaçada por uma peça do jogador 1 nas diagonais
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_row, d_col in diagonals:
            new_row = flag_row + d_row
            new_col = flag_col + d_col
            if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                if self.board_matrix[new_row][new_col] == 1:
                    print("TA AMEACADA PORRA!!!!")
                    return True
        return False


    def verificar_bandeira_nos_cantos(self):
        corners = [(0, 0), (0, 6), (6, 0), (6, 6), (6,5), (6,4), (6,3), (6,2), (6,1), (1,6), (2,6), (3,6), (4,6), (5,6)] 
        flag_position = next(((i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board_matrix[i][j] == 3), None)

        if flag_position in corners:
            print("A bandeira está em um dos cantos do tabuleiro!")
            print("Jogo acabou")
            exit(0)
            
    def is_valid_move(self, origin, dest, player):
        opponent = 2 if player == 1 else 1
        if (dest[0] == origin[0] and abs(dest[1] - origin[1]) == 1) or \
        (dest[1] == origin[1] and abs(dest[0] - origin[0]) == 1):
            if self.board_matrix[dest[1]][dest[0]] == 0 or self.board_matrix[dest[1]][dest[0]] == 3:  # Adicionado condição para a bandeira
                return True
        elif (self.board_matrix[dest[1]][dest[0]] == opponent) and abs(dest[0] - origin[0]) == 1 and abs(dest[1] - origin[1]) == 1 or self.board_matrix[dest[1]][dest[0]] == opponent + 1:
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
                                    if self.is_valid_move((row, col), dest, player):
                                        moves.append((row, col, dest))
                    elif player == 2 and self.board_matrix[col][row] == 2:
                        for d_row in range(-1, 2):
                            for d_col in range(-1, 2):
                                if (d_row != 0 or d_col != 0) and 0 <= row + d_row < self.board_size and 0 <= col + d_col < self.board_size:
                                    dest = (row + d_row, col + d_col)
                                    if self.is_valid_move((row, col), dest, player):
                                        moves.append((row, col, dest))
                                        
                    elif player == 2 and self.board_matrix[col][row] == 3:
                        for d_row in range(-1, 2):
                            for d_col in range(-1, 2):
                                if (d_row != 0 or d_col != 0) and 0 <= row + d_row < self.board_size and 0 <= col + d_col < self.board_size:
                                    dest = (row + d_row, col + d_col)
                                    if self.is_valid_move((row, col), dest, player):
                                        moves.append((row, col, dest))

            print(moves)
            return moves


    def game(self):
        current_player = self.player
        other_player = self.ai_player
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
                        if self.is_valid_move((x, y), (x_dest, y_dest), current_player):
                            break
                        else:
                            print("Movimento inválido. Por favor, escolha uma posição válida.")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite duas coordenadas separadas por espaço.")

                self.board_matrix[y][x] = 0
                if self.board_matrix[y_dest][x_dest] == other_player:
                    if other_player == 1:
                        self.numPieces -= 1
                    else:
                        self.numPieces2 -= 1
                self.board_matrix[y_dest][x_dest] = current_player

            else:  # Caso contrário, é a vez da IA
                moves = self.generate_moves(current_player)
                _, best_move = self.minimax(1, False)
                #print(best_move)
                if best_move:
                    x, y, dest = best_move
                    x_dest, y_dest = dest
                    self.board_matrix[y][x] = 0
                    if self.board_matrix[y_dest][x_dest] == self.player:
                        if self.player == 1:
                            self.numPieces -= 1
                            print(self.numPieces)
                        else:
                            self.numPieces2 -= 1
                            print(self.numPieces2)
                    self.board_matrix[y_dest][x_dest] = self.ai_player

                    self.last_move = (x, y, dest)

            self.verificar_bandeira_nos_cantos()
            current_player = 2 if current_player == 1 else 1  # Alterna para o próximo jogador
            other_player = 1 if current_player == 2 else 2



    def minimax(self, depth, maximizing_player):
        current_player = self.ai_player
        if depth == 0:
            return self.evaluate_board(not maximizing_player), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.generate_moves(current_player):
                x, y, dest = move
                if self.board_matrix[y][x] == current_player:
                    temp_origin = self.board_matrix[y][x]
                    temp_dest = self.board_matrix[dest[1]][dest[0]]
                    self.board_matrix[y][x] = 0
                    self.board_matrix[dest[1]][dest[0]] = current_player
                    eval, _ = self.minimax(depth - 1, False)
                    self.board_matrix[dest[1]][dest[0]] = temp_dest
                    self.board_matrix[y][x] = temp_origin
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.generate_moves(current_player):
                x, y, dest = move
                if self.board_matrix[y][x] == current_player:
                    temp_origin = self.board_matrix[y][x]
                    temp_dest = self.board_matrix[dest[1]][dest[0]]
                    self.board_matrix[y][x] = 0
                    self.board_matrix[dest[1]][dest[0]] = current_player
                    eval, _ = self.minimax(depth - 1, True)
                    self.board_matrix[dest[1]][dest[0]] = temp_dest
                    self.board_matrix[y][x] = temp_origin
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
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

