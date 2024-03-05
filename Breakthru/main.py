import tkinter as tk

class BreakthruGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Breakthru")
        
        screen_width = 800
        screen_height = 800
        self.numPieces = 12
        self.numPieces2 = 8
        
        self.cell_size = min(screen_width, screen_height) // 7
        
        self.canvas = tk.Canvas(self.master, width=7 * self.cell_size, height=7 * self.cell_size, bg="white")
        self.canvas.pack()
        
        self.board_size = 7
        self.pieces = {(2, 0), (3, 0), (4, 0), (6, 2), (6, 3), (6, 4), (0, 2), (0, 3), (0, 4), (2, 6), (3, 6), (4, 6)} # Exemplo de peças
        self.flag = {(3,3)}
        self.pieces2 = {(2, 2), (2, 3), (2, 4), (4, 2), (4, 3), (4, 4), (3, 2), (3, 4)}
        self.selected_piece = None
        self.selected_piece2 = None
        self.selected_flag = None
        
        self.draw_board()
        self.draw_pieces()
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                
    def update_pieces_positions(self, board):
        self.pieces.clear()
        self.pieces2.clear()
        self.flag.clear()

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 1:
                    self.pieces.add((col, row))
                elif board[row][col] == 2:
                    self.pieces2.add((col, row))
                elif board[row][col] == 3:
                    self.flag.add((col, row))
                
    def draw_pieces(self):
        for piece in self.pieces:
            fill = "gray"
            if piece == self.selected_piece:
                fill = "lightgray"
            self.draw_piece(piece, fill)
        for piece in self.pieces2:
            fill = "yellow"
            if piece == self.selected_piece:
                fill = "lightyellow"
            self.draw_piece(piece, fill)
        for piece in self.flag:
            fill = "red"
            if piece == self.selected_piece:
                fill = "pink"
            self.draw_piece(piece, fill)
            
    def evaluate_board(self, board, player):
        # Definir pesos para os diferentes fatores de avaliação
        weight_pieces = 1.0  # Peso das peças
        weight_flag_distance = 2.0  # Peso da distância da bandeira à linha de chegada
        weight_blocking_pieces = 1.5  # Peso das peças bloqueando a bandeira

        # Inicializar contadores para peças de cada jogador, distância da bandeira e peças bloqueando a bandeira
        player1_pieces = self.numPieces
        player2_pieces = self.numPieces2
        flag_distance = 0
        blocking_pieces = 0

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 3:
                    flag_distance = len(board) - 1 - row
                    # Contar o número de peças do jogador 1 ao redor da bandeira
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if 0 <= row+dr < len(board) and 0 <= col+dc < len(board[0]) and board[row+dr][col+dc] == 1:
                                blocking_pieces += 1

        # Calcular a pontuação com base nos pesos e nos contadores
        player1_score = weight_pieces * player1_pieces + weight_blocking_pieces * blocking_pieces
        player2_score = weight_pieces * player2_pieces + weight_flag_distance * flag_distance

        if player == 1:

            return player1_score - player2_score
        else:

            return player2_score - player1_score

           
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or self.game_over():
            return self.evaluate_board(board, maximizing_player), None
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.generate_moves(board, 2):  # Movimentos do jogador 2 (IA)
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.generate_moves(board, 1):  # Movimentos do jogador 1 (oponente)
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

           
    def game_over(self):
        if self.verificar_bandeira_nos_cantos() or self.check_Death(1) or self.check_Death(2):
            return True
        
        return False
    
    def make_move(self, board, move):
        new_board = [row[:] for row in board]  # Cria uma cópia do tabuleiro atual
        
        # Extrai as informações do movimento
        origin_row, origin_col, (dest_row, dest_col) = move
        
        # Move a peça para o destino e remove da origem
        new_board[dest_row][dest_col] = new_board[origin_row][origin_col]
        new_board[origin_row][origin_col] = 0  # Define a posição original como vazia
        
        return new_board
        
    def create_board_matrix(self):
        board_matrix = [[0] * self.board_size for _ in range(self.board_size)]  # Inicializa uma matriz vazia para representar o tabuleiro
        for piece in self.pieces:
            row, col = piece
            board_matrix[col][row] = 1  # Define o valor da célula como 1 para representar a presença de uma peça azul
        for piece in self.pieces2:
            row, col = piece
            board_matrix[col][row] = 2  # Define o valor da célula como 2 para representar a presença de uma peça verde
        for flag in self.flag:
            row, col = flag
            board_matrix[col][row] = 3  # Define o valor da célula como 3 para representar a presença da bandeira
        return board_matrix
        
    def imprimir_matriz(self, matriz):
        for linha in matriz:
            for elemento in linha:
                print(elemento, end=" ")
            print()
        print("-----------------")
        
    
    def draw_piece(self, piece, fill):
        x, y = piece
        x_center = x * self.cell_size + self.cell_size // 2
        y_center = y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        self.canvas.create_oval(x_center - radius, y_center - radius,
                                 x_center + radius, y_center + radius,
                                 fill=fill, outline="black")
        
    def verificar_bandeira_nos_cantos(self):
        corners = [(0, 0), (0, 6), (6, 0), (6, 6), (6,5), (6,4), (6,3), (6,2), (6,1), (1,6), (2,6), (3,6), (4,6), (5,6)]  # Coordenadas dos cantos do tabuleiro
        flag_position = next(iter(self.flag), None)  # Obter a posição da bandeira, se existir

        if flag_position in corners:
            print("A bandeira está em um dos cantos do tabuleiro!")
            print("Jogo acabou")
            exit(0)
     
    def check_Death(self, piece_type):
        if piece_type == "pieces":
            pieces = self.pieces
        elif piece_type == "pieces2":
            pieces = self.pieces2
        elif piece_type == "flag":
            pieces = self.flag
        else:
            return False

        return len(pieces) == 0
    
    def is_valid_move(self, origin, dest):
        # Verifique se o movimento é lateral (para cima, baixo, esquerda ou direita)
        if (dest[0] == origin[0] and dest[1] != origin[1]) or \
        (dest[1] == origin[1] and dest[0] != origin[0]):
            # Verifique se a posição de destino está vazia ou ocupada por uma peça do jogador oposto
            if (dest not in self.pieces) and (dest not in self.pieces2) and (dest not in self.flag):
                return True
        # Verifique se é possível capturar uma peça adversária
        elif dest in self.pieces2 and abs(dest[0] - origin[0]) == 1 and abs(dest[1] - origin[1]) == 1:
            return True
        elif dest in self.pieces and abs(dest[0] - origin[0]) == 1 and abs(dest[1] - origin[1]) == 1:
            return True
        return False


    
    def is_valid_move_All(self, board, col, row):
        valid_moves = []
        piece = board[row][col]
        player = 1 if piece == 1 else 2
        if piece == 3:
            player = 3

        if player == 1 or player == 2 or player == 3:
            # Verifique os movimentos para cima
            if row > 0:
                move = (row - 1, col)
                if self.is_valid_move((row, col), move):
                    valid_moves.append(move)

            # Verifique os movimentos para baixo
            if row < len(board) - 1:
                move = (row + 1, col)
                if self.is_valid_move((row, col), move):
                    valid_moves.append(move)

            # Verifique os movimentos para a esquerda
            if col > 0:
                move = (row, col - 1)
                if self.is_valid_move((row, col), move):
                    valid_moves.append(move)
            # Verifique os movimentos para a direita
            if col < len(board[row]) - 1:
                move = (row, col + 1)
                if self.is_valid_move((row, col), move):
                    valid_moves.append(move)
        
        return valid_moves

    
    def generate_moves(self, board, player):
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == player: # 1 = player 1
                    # Verificar movimentos válidos para a peça atual
                    valid_moves = self.is_valid_move_All(board, row, col) #Criar a funcao
                    for move in valid_moves:
                        moves.append((row, col, move))
        return moves


    def on_canvas_click(self, event):
        # Get the clicked cell coordinates
        x, y = event.x // self.cell_size, event.y // self.cell_size
        #print(f"Clicked cell: ({x}, {y})")
        moves = []
        matriz = self.create_board_matrix()
        player = matriz[y][x]

        
        # Check if there is no piece already selected
        if not self.selected_piece:
            if (x, y) in self.pieces:
                print("Piece clicked!")
                self.selected_piece = (x, y)
                self.draw_pieces()
                player = matriz[y][x]
                print(player)
                moves = self.generate_moves(matriz, player)
                #print(moves)
                    
            elif (x, y) in self.pieces2:
                print("Piece clicked!")
                self.selected_piece = (x, y)
                self.draw_pieces()
                player = matriz[y][x]
                print(player)
                moves = self.generate_moves(matriz, player)
                #print(moves)

                
            elif (x, y) in self.flag:
                print("Piece clicked!")
                self.selected_piece = (x, y)
                self.draw_pieces() 
                player = matriz[y][x]
                moves = self.generate_moves(matriz, player)
                #print(moves)    
                        
        
        else: 
            
            value, move = self.minimax(matriz, 3, True)
            #print(value)
            #print(move)
            matriz = self.make_move(matriz, move)
            self.update_pieces_positions(matriz)
            self.canvas.delete("all")  # Clear the canvas
            self.draw_board()
            self.draw_pieces()
        
            if (x, y) in self.pieces2 and (abs(x - self.selected_piece[0]), abs(y - self.selected_piece[1])) == (1, 1):
                    self.pieces.remove(self.selected_piece)
                    self.pieces.add((x, y))
                    self.pieces2.remove((x, y))
                    self.canvas.delete("all")  # Clear the canvas
                    self.draw_board()
                    self.draw_pieces()
                    self.selected_piece = None
                    self.numPieces2 -= 1
                    print(self.numPieces2)
                    self.verificar_bandeira_nos_cantos()
                    if self.numPieces2 == 0:
                        print("Game ended")
                        exit(0)
            elif (x, y) in self.pieces and (abs(x - self.selected_piece[0]), abs(y - self.selected_piece[1])) == (1, 1):
                    self.pieces2.remove(self.selected_piece)
                    self.pieces2.add((x, y))
                    self.pieces.remove((x, y))
                    self.canvas.delete("all")  # Clear the canvas
                    self.draw_board()
                    self.draw_pieces()
                    self.selected_piece2 = None
                    self.selected_piece = None
                    self.numPieces -= 1
                    print(self.numPieces)
                    self.verificar_bandeira_nos_cantos()
                    if self.numPieces == 0:
                        print("Game ended")
                        exit(0)
                    
            
            elif (abs(x - self.selected_piece[0]) + abs(y - self.selected_piece[1])) <= 1:
                # Check if the destination cell is empty
                if (x, y) not in self.pieces and (x, y) not in self.pieces2 and (x, y) not in self.flag:
                    # Move the selected piece to the new cell
                    if self.selected_piece in self.pieces:
                        self.pieces.remove(self.selected_piece)
                        self.pieces.add((x, y))
                    elif self.selected_piece in self.pieces2:
                        self.pieces2.remove(self.selected_piece)
                        self.pieces2.add((x, y))
                    elif self.selected_piece in self.flag:
                        self.flag.remove(self.selected_piece)
                        self.flag.add((x, y))
                
                    self.selected_piece = None
                    self.verificar_bandeira_nos_cantos()

                    self.canvas.delete("all")  # Clear the canvas
                    self.draw_board()
                    self.draw_pieces()  # Aqui é necessário chamar a função para redesenhar todas as peças e indicar a seleção
            else:
                print("Invalid move. You can only move one cell at a time.")
                self.selected_piece = None
                self.selected_piece2 = None
                self.selected_flag = None
                self.draw_pieces()
    
    

            

def main():
    root = tk.Tk()
    app = BreakthruGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
