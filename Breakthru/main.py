import tkinter as tk

class BreakthruGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Breakthru")
        
        screen_width = 800
        screen_height = 800
        
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
                
    def draw_pieces(self):
        for piece in self.pieces:
            fill = "gray"
            if piece == self.selected_piece:
                fill = "lightgray"
            self.draw_piece(piece, fill)
        for piece in self.pieces2:
            fill = "yellow"
            if piece == self.selected_piece2:
                fill = "lightyellow"
            self.draw_piece(piece, fill)
        for piece in self.flag:
            fill = "red"
            if piece == self.selected_flag:
                fill = "pink"
            self.draw_piece(piece, fill)

    
    def draw_piece(self, piece, fill):
        x, y = piece
        x_center = x * self.cell_size + self.cell_size // 2
        y_center = y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        self.canvas.create_oval(x_center - radius, y_center - radius,
                                 x_center + radius, y_center + radius,
                                 fill=fill, outline="black")
          
            
    def on_canvas_click(self, event):
        # Get the clicked cell coordinates
        x, y = event.x // self.cell_size, event.y // self.cell_size
        #print(f"Clicked cell: ({x}, {y})")
        
        # Check if there is no piece already selected
        if not self.selected_piece:
            if (x, y) in self.pieces:
                print("Piece clicked!")
                self.selected_piece = (x, y)
                self.draw_pieces()
            elif (x, y) in self.pieces2:
                print("Piece clicked!")
                self.selected_piece = (x, y)
                self.draw_pieces()
            elif (x, y) in self.flag:
                print("Piece clicked!")
                self.selected_piece = (x, y)
                self.draw_pieces() 
        
        else:
            # Check if the clicked cell is adjacent to the selected piece
            if abs(x - self.selected_piece[0]) <= 1 and abs(y - self.selected_piece[1]) <= 1:
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
                    self.canvas.delete("all")  # Clear the canvas
                    self.draw_board()
                    self.draw_pieces()  # Aqui é necessário chamar a função para redesenhar todas as peças e indicar a seleção
            else:
                print("Invalid move. You can only move one cell at a time.")
    

            

def main():
    root = tk.Tk()
    app = BreakthruGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
