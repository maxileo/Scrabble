import pygame
import sys
import copy
import random
import json

pygame.init()

WIDTH, HEIGHT = 1200, 750
BOARD_SIZE = int(HEIGHT * 9/10)
LETTER_FONT_SIZE = 32
LETTER_VALUE_FONT_SIZE = 13
INFO_FONT_SIZE = 24
BOARD_INFO_FONT_SIZE = 11
TEXT_INFO_FONT_SIZE = 16


class Media:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.order_imgs = []
        for index in range(3):
            order_img = pygame.image.load(f"MEDIA/order{index+1}.png")
            order_img = pygame.transform.scale(order_img, (self.cell_size*0.8, self.cell_size))
            self.order_imgs.append(order_img)


class Letter:
    @staticmethod
    def draw_letter(surface, rect, letter, letterTextColor, isLetterNow, isLetterSelected):
        
        fill_color = (247, 243, 237)
        if isLetterNow:
            fill_color = (247, 234, 183)
        outline_color = (28, 27, 26)
        shadow_color = (46, 46, 45)
        selected_color = (235, 197, 108)
        outline_thickness = 2
        font = pygame.font.Font(None, LETTER_FONT_SIZE)
        # Draw shadow
        shadow_rect = rect.move(-2, 2)
        pygame.draw.rect(surface, shadow_color, shadow_rect)
        if isLetterSelected:
            fill_color = selected_color
        pygame.draw.rect(surface, fill_color, rect)
        pygame.draw.rect(surface, outline_color, rect, outline_thickness)

        # Draw centered letter
        text_surface = font.render(letter, True, letterTextColor)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

        letter_value = str(Letter.get_letter_value(letter))
        font_value = pygame.font.Font(None, LETTER_VALUE_FONT_SIZE)
        text_surface = font_value.render(letter_value, True, letterTextColor)
        text_rect = text_surface.get_rect(center=rect.center).move(rect.width * 1.5/5, rect.height * 1.5/5)
        surface.blit(text_surface, text_rect)

    @staticmethod
    def get_letter_value(letter):
        letter_values = {
            'A': 1, 'B': 5, 'C': 1, 'D': 3, 'E': 1, 'F': 4, 'G': 6, 'H': 8, 'I': 1, 'J': 10, 'L': 1, 'M': 4, 'N': 1, 'O': 2, 'P': 2, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 10, 'Z': 10
        }
        return letter_values[letter]

class Board:
    def __init__(self, size, rows, cols, width, height):
        self.size = size
        self.rows = rows
        self.cols = cols
        self.cell_size = self.size // self.cols
        self.board = [
            [ ['', 'TRIPLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_WORD', 0] ],
            [ ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0] ],
            [ ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0] ],
            [ ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0] ],
            [ ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0] ],
            [ ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0] ],
            [ ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0] ],
            [ ['', 'TRIPLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'MIDDLE', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_WORD', 0] ],
            [ ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0] ],
            [ ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0] ],
            [ ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0] ],
            [ ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0] ],
            [ ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0] ],
            [ ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_WORD', 0], ['', 'NORMAL', 0] ],
            [ ['', 'TRIPLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_WORD', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'DOUBLE_LETTER', 0], ['', 'NORMAL', 0], ['', 'NORMAL', 0], ['', 'TRIPLE_WORD', 0] ]
            
        ]
        self.cell_colors = {
            "NORMAL": (0, 163, 134),
            "TRIPLE_WORD": (196, 0, 1),
            "DOUBLE_LETTER": (155, 183, 205),
            "TRIPLE_LETTER": (2, 51, 127),
            "DOUBLE_WORD": (207, 107, 80),
            "MIDDLE": (243, 188, 81)
        }
        #self.startX = (width - self.size) // 2
        #self.startY = int(height * 1/16)
        self.startY = (height - self.size) // 2
        self.startX = self.startY

        self.letter_size = int(self.cell_size * 8/10)
 
    def draw_board(self, screen, turnPositions, nrRemainingLetters, chosenLetter):
        global INFO_FONT_SIZE, LETTER_FONT_SIZE, LETTER_VALUE_FONT_SIZE, BOARD_INFO_FONT_SIZE

        font = pygame.font.Font(None, INFO_FONT_SIZE)
        text_surface = font.render(f"Litere ramase: {nrRemainingLetters}", True, WHITE)
        text_rect = text_surface.get_rect(center=pygame.Rect(self.startX, self.startY - self.cell_size, self.cell_size*3, self.cell_size).center)
        screen.blit(text_surface, text_rect)


        for row in range(self.rows):
            for col in range(self.cols):
                cell_color = self.cell_colors[self.board[row][col][1]]
                cell_rect = pygame.Rect(self.startX + col * self.cell_size, self.startY + row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, cell_color, cell_rect)
                
                outline_col = WHITE
                outline_weight = 1

                if (chosenLetter != '' and self.board[col][row][0] == '') or (row, col) in turnPositions:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if cell_rect.collidepoint((mouse_x, mouse_y)):
                        outline_col = (42, 61, 48)
                        outline_weight = 2

                pygame.draw.rect(screen, outline_col, cell_rect, outline_weight)

                if self.board[row][col][1] != "NORMAL" and self.board[row][col][1] != "MIDDLE":
                    words_to_write = self.board[row][col][1].split("_")
                    if words_to_write[0] == "DOUBLE":
                        words_to_write[0] = "DUBLEAZA"
                    if words_to_write[0] == "TRIPLE":
                        words_to_write[0] = "TRIPLEAZA"
                    if words_to_write[1] == "LETTER":
                        words_to_write[1] = "LITERA"
                    if words_to_write[1] == "WORD":
                        words_to_write[1] = "CUVANTUL"
                
                    font = pygame.font.Font(None, BOARD_INFO_FONT_SIZE)
                    
                    text_surface = font.render(words_to_write[0], True, WHITE)
                    text_rect = text_surface.get_rect(center=cell_rect.center).move(0, -5)
                    screen.blit(text_surface, text_rect)

                    text_surface = font.render(words_to_write[1], True, WHITE)
                    text_rect = text_surface.get_rect(center=cell_rect.center).move(0, 5)
                    screen.blit(text_surface, text_rect)
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col][0] != '':
                    letter_now = False
                    if (col, row) in turnPositions:
                        letter_now = True
                    self.draw_letter_board(screen, self.board[row][col][0], row, col, letter_now)

    def draw_letter_board(self, surface, letter, i, j, is_letter_now):
        diff = (self.cell_size - self.letter_size) / 2
        rect = pygame.Rect(self.startX + diff + i * self.cell_size, self.startY + diff + j * self.cell_size, self.letter_size, self.letter_size)
        Letter.draw_letter(surface, rect, letter, (20, 20, 20), is_letter_now, False)

    def get_words(self):
        words = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0] != '':
                    if (j-1 >= 0 and self.board[i][j-1][0] == '') or j == 0:
                        k = j
                        while k < self.cols and self.board[i][k][0] != '':
                            k = k + 1
                        if k - j >= 2:
                            word = ""
                            moves = []
                            for k_aux in range(j, k):
                                word = word + self.board[i][k_aux][0]
                                moves.append((k_aux, i))
                            words.append((word, moves))
                    if (i-1 >= 0 and self.board[i-1][j][0] == '') or i == 0:
                        k = i
                        while k < self.rows and self.board[k][j][0] != '':
                            k = k + 1
                        if k - i >= 2:
                            word = ""
                            moves = []
                            for k_aux in range(i, k):
                                word = word + self.board[k_aux][j][0]
                                moves.append((j, k_aux))
                            words.append((word, moves))
        return words
    
    def fill_cluster(self, visited, i, j, k):
        if i-1 >= 0 and self.board[i-1][j][0] != '' and visited[i-1][j][0] == False:
            visited[i-1][j][0] = True
            visited[i-1][j][1] = k
            self.fill_cluster(visited, i-1, j, k)
        if i+1 < self.cols and self.board[i+1][j][0] != '' and visited[i+1][j][0] == False:
            visited[i+1][j][0] = True
            visited[i+1][j][1] = k
            self.fill_cluster(visited, i+1, j, k)
        if j-1 >= 0 and self.board[i][j-1][0] != '' and visited[i][j-1][0] == False:
            visited[i][j-1][0] = True
            visited[i][j-1][1] = k
            self.fill_cluster(visited, i, j-1, k)
        if j+1 < self.rows and self.board[i][j+1][0] != '' and visited[i][j+1][0] == False:
            visited[i][j+1][0] = True
            visited[i][j+1][1] = k
            self.fill_cluster(visited, i, j+1, k)




    def get_nr_clusters(self):
        visited = [[[False, 0] for _ in range(self.cols)] for _ in range(self.rows)]
        nrClusters = 1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0] != '' and visited[i][j][0] == False:
                    self.fill_cluster(visited, i, j, nrClusters)
                    nrClusters += 1
        
        return nrClusters - 1

    
    def is_board_ok(self, turnPositions):
        words = self.get_words()

        for (word, moves) in words:

            wordOk = False
            for move in moves:
                if move == (self.rows // 2, self.cols // 2) or move not in turnPositions:
                    wordOk = True
                else:
                    for (wordOther, movesOther) in words:
                        if moves != movesOther:
                            if move in movesOther:
                                wordOk = True
            if wordOk == False:
                return False
            
        nrClusters = self.get_nr_clusters()
        print("NR CLUSTERS ", nrClusters)
        if nrClusters > 1:
            return False

        return True

class Player:
    def __init__(self, letters, turn, width, height, board_size, letter_size):
        self.letters = copy.deepcopy(letters)
        self.selectedLetters = [False]*len(self.letters)
        self.score = 0
        self.turn = turn

        self.isTurnNow = False

        self.letter_size = letter_size

        self.holder_width = self.letter_size * 10
        #self.holder_width = (width - board_size) * 6/10
        self.holder_height = self.holder_width * 1/4

        self.startY = (height - board_size) // 2
        self.startX = self.startY + board_size + self.holder_width * 1/10
        self.startY = self.startY + self.holder_height * self.turn * 2

        self.startLettersX = self.startX + self.letter_size
        self.startLettersY = self.startY + self.letter_size

        self.HOLDER_IMAGE = pygame.image.load("MEDIA/holder.png")
        self.HOLDER_IMAGE = pygame.transform.scale(self.HOLDER_IMAGE, (self.holder_width, self.holder_height))

    def draw_score(self, surface, order):
        global mediaManager
        global INFO_FONT_SIZE, LETTER_FONT_SIZE, LETTER_VALUE_FONT_SIZE, BOARD_INFO_FONT_SIZE

        rect = pygame.Rect(self.startX, self.startY - self.letter_size, self.holder_width * 1 / 5, self.letter_size)
        font = pygame.font.Font(None, INFO_FONT_SIZE)

        text_surface = font.render(f"Player{self.turn+1} SCOR: {self.score}", True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

        if order < 3:
            surface.blit(mediaManager.order_imgs[order], (self.startX + self.holder_width * 1.7 / 5, self.startY - self.letter_size))

    def draw_score_end_game(self, surface, order):
        global mediaManager
        global INFO_FONT_SIZE, LETTER_FONT_SIZE, LETTER_VALUE_FONT_SIZE, BOARD_INFO_FONT_SIZE

        rect = pygame.Rect(self.startX, 100 + order * self.letter_size * 2, self.holder_width * 1 / 5, self.letter_size)
        font = pygame.font.Font(None, INFO_FONT_SIZE)

        text_surface = font.render(f"Player{self.turn+1} SCOR: {self.score}", True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

        if order < 3:
            surface.blit(mediaManager.order_imgs[order], (self.startX + self.holder_width * 1.7 / 5, 100 + order * self.letter_size * 2))

    def draw_holder(self, surface):
        rect = pygame.Rect(self.startX, self.startY, self.holder_width, self.holder_height)
        
        screen.blit(self.HOLDER_IMAGE, (self.startX, self.startY))

        for i in range(len(self.letters)):
            rect = pygame.Rect(self.startLettersX + i * self.letter_size * 1.2, self.startLettersY, self.letter_size, self.letter_size)
            if self.isTurnNow == True:
                letterColor = (20, 20, 20)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rect.collidepoint((mouse_x, mouse_y)):
                    letterColor = (35, 122, 75)
            else:
                letterColor = (100, 100, 100)
            Letter.draw_letter(surface, rect, self.letters[i], letterColor, False, self.selectedLetters[i])

        #pygame.draw.rect(surface, (255, 255, 255), rect)
        #pygame.draw.rect(surface, (20, 20, 20), rect, 4)

    def check_click_holder(self, mouseX, mouseY):
        for i in range(len(self.letters)):
            rect = pygame.Rect(self.startLettersX + i * self.letter_size * 1.2, self.startLettersY, self.letter_size, self.letter_size)
            if rect.collidepoint((mouseX, mouseY)):
                return i
        return -1
    

class Button:
    def __init__(self, rect, fill_color, hover_color, outline_color, text, font_size, should_draw = True):
        self.rect = rect
        self.fill_color = fill_color
        self.hover_color = hover_color
        self.outline_color = outline_color
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.outline_weight = 2

        self.should_draw = should_draw

    def draw(self, surface):
        fill_color = self.fill_color
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.clicked(mouse_x, mouse_y):
            fill_color = self.hover_color
        pygame.draw.rect(surface, fill_color, self.rect)
        pygame.draw.rect(surface, self.outline_color, self.rect, self.outline_weight)
        text_surface = self.font.render(self.text, True, (30, 50, 30))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, mouse_x, mouse_y):
        if self.rect.collidepoint((mouse_x, mouse_y)):
            return True
        return False
    
class InfoText:
    def __init__(self, text, type, fill_color, outline_color, text_color, rect):
        self.text = text
        self.type = type
        self.fill_color = fill_color
        self.text_color = text_color
        self.outline_color = outline_color
        self.rect = rect
        self.font = pygame.font.Font(None, TEXT_INFO_FONT_SIZE)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.fill_color, self.rect)
        pygame.draw.rect(surface, self.outline_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.x + self.rect.height // 4, self.rect.y + (self.rect.height - text_rect.height) // 2)
        surface.blit(text_surface, text_rect)

    

class InfoBoard:
    def __init__(self, rect, cell_size):
        self.rect = rect
        self.fill_color = (67, 68, 74)
        self.outline_color = (215, 215, 217)
        self.cell_size = cell_size

        self.texts = []
        self.height_text = self.cell_size * 2 / 3 + self.cell_size * 1 / 10
        self.max_length_texts = rect.height // (self.height_text)

        self.colors = {
            "POINTS": {
                "FILL": (232, 171, 72),
                "OUTLINE": (20, 20, 19),
                "TEXT": (237, 234, 232)
            },
            "WRONG": {
                "FILL": (219, 102, 59),
                "OUTLINE": (20, 20, 19),
                "TEXT": (237, 234, 232)
            },
            "TURN": {
                "FILL": (75, 115, 201),
                "OUTLINE": (20, 20, 19),
                "TEXT": (237, 234, 232)
            },
            "BONUS": {
                "FILL": (70, 128, 73),
                "OUTLINE": (20, 20, 19),
                "TEXT": (237, 234, 232)
            }
        }

    def draw(self, surface):
        pygame.draw.rect(surface, self.fill_color, self.rect)
        pygame.draw.rect(surface, self.outline_color, self.rect, 2)

        for text in self.texts:
            text.draw(surface)

    def add_new_text(self, text, type):
        if len(self.texts) == 0:
            new_text_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.cell_size * 2 / 3)
            new_text = InfoText(text, type, self.colors[type]["FILL"], self.colors[type]["OUTLINE"], self.colors[type]["TEXT"], new_text_rect)
            self.texts.append(new_text)
        else:
            if len(self.texts) == self.max_length_texts:
                for i in range(len(self.texts)-1, 0, -1):
                    self.texts[i].rect = copy.deepcopy(self.texts[i-1].rect)
                self.texts.pop(0)
            
            new_text_rect = self.texts[-1].rect.move(0, self.height_text)
            new_text = InfoText(text, type, self.colors[type]["FILL"], self.colors[type]["OUTLINE"], self.colors[type]["TEXT"], new_text_rect)
            self.texts.append(new_text)

    
class Game:
    def __init__(self, board, nr_players):
        self.board = board
        self.nr_players = nr_players
        self.turnPositions = []
        self.turn = 0
        self.entered_final_game = False
        self.stopGame = False
        self.running = True
        self.consecutivePasses = 0
        self.smallestNrRemoved = 100
        self.finalMoves = [[0, 0, 0]]*10
        self.lettersRules = {
          'A': 10, 'B': 2, 'C': 5, 'D': 4, 'E': 9, 'F': 2, 'G': 2, 'H': 1, 'I': 11, 'J': 1, 'L': 5, 'M': 3, 'N': 6, 'O': 5, 'P': 4, 'R': 6, 'S': 6, 'T': 7, 'U': 5, 'V': 2, 'X': 1, 'Z': 1
        }
        # self.lettersRules = {
        #    'A': 5, 'B': 1, 'C': 1, 'D': 1, 'E': 5, 'F': 1, 'G': 1, 'H': 1, 'I': 5, 'J': 1, 'L': 1, 'M': 1, 'N': 1, 'O': 5, 'P': 1, 'R': 2, 'S': 2, 'T': 2, 'U': 5, 'V': 2, 'X': 0, 'Z': 0
        # }
        self.allLetters = []
        for key, value in self.lettersRules.items():
            for i in range(value):
                self.allLetters.append(key)
        random.shuffle(self.allLetters)
        print(len(self.allLetters))

        self.players = []
        for index in range(nr_players):
            player = Player(self.generatePlayerLetters(7), index, WIDTH, HEIGHT, BOARD_SIZE, board.letter_size)
            self.players.append(player)
        
        with open("words.json", 'r') as file:
            self.scrabble_words = json.load(file)

    def isCorrectWord(self, word):
        return word in self.scrabble_words

    def generatePlayerLetters(self, howMany):
        letters = []
        for i in range(howMany):
            if len(self.allLetters) > 0:
                random_index = random.randint(0, len(self.allLetters) - 1)
                letters.append(self.allLetters[random_index])
                self.allLetters.pop(random_index)
        return letters
    
    def check(self):
        isBoardOk = self.board.is_board_ok(self.turnPositions)
        if isBoardOk == False:
            return False
        words = self.board.get_words()
        for (word, moves) in words:
            if not self.isCorrectWord(word):
                return False
        return True
    
    def removeRecursive(self, newMoves, k):
        if k == len(newMoves):
            for move in newMoves:
                if move[2]:
                    self.board.board[move[0][1]][move[0][0]][0] = move[1]
                else:
                    self.board.board[move[0][1]][move[0][0]][0] = ''
            if self.check():
                print(newMoves)
                nrRemoved = 0
                for move in newMoves:
                    if move[2] == False:
                        nrRemoved += 1
                if nrRemoved < self.smallestNrRemoved:
                    self.smallestNrRemoved = nrRemoved
                    for i in range(len(newMoves)):
                        self.finalMoves[i] = copy.deepcopy(newMoves[i])
        else:
            newMoves[k][2] = True
            self.removeRecursive(newMoves, k+1)
            newMoves[k][2] = False
            self.removeRecursive(newMoves, k+1)

    
    def removeWrongLetters(self):
        words = self.board.get_words()
        newMoves = []
        for (word, moves) in words:
            for i in range(len(moves)):
                if moves[i] in self.turnPositions and [moves[i], self.board.board[moves[i][1]][moves[i][0]][0], False] not in newMoves:
                    newMoves.append([moves[i], self.board.board[moves[i][1]][moves[i][0]][0], False])
                    self.finalMoves[len(newMoves)-1] = [moves[i], self.board.board[moves[i][1]][moves[i][0]][0], False]
        print("NEW MOVES", newMoves)
        self.smallestNrRemoved = 100
        self.removeRecursive(newMoves, 0)
        print("SMALLEST", self.smallestNrRemoved)
        for i in range(len(newMoves)):
            if self.finalMoves[i][2]:
                self.board.board[self.finalMoves[i][0][1]][self.finalMoves[i][0][0]][0] = self.finalMoves[i][1]
            else:
                letter = self.finalMoves[i][1]
                self.board.board[self.finalMoves[i][0][1]][self.finalMoves[i][0][0]][0] = ''
                print("LITERA GRESITA " + letter)
                self.players[self.turn].letters.append(letter)
                self.players[self.turn].selectedLetters.append(False)

    def endTurn(self):
        global infoBoardManager

        isBoardOk = self.board.is_board_ok(self.turnPositions)
        if isBoardOk == False:
            print("BOARD IS NOT OK")
            infoBoardManager.add_new_text("Literele sunt puse gresit :(", "WRONG")
            return (False, None)
        else:
            points = 0
            words = self.board.get_words()
            for (word, moves) in words:
                newWord = False
                for turnPos in self.turnPositions:
                    if turnPos in moves:
                        newWord = True
                        break
                
                if newWord:
                    if self.isCorrectWord(word):
                        for move in moves:
                            if self.board.board[move[1]][move[0]][0] == '':
                                infoBoardManager.add_new_text(f"{word} ELIMINAT", "WRONG")
                    else:
                        infoBoardManager.add_new_text(f"{word} E GRESIT", "WRONG")

            self.removeWrongLetters()

            words = self.board.get_words()            
                    
            for (word, moves) in words:
                newWord = False
                for turnPos in self.turnPositions:
                    if turnPos in moves:
                        newWord = True
                        break
                
                if newWord:
                    if self.isCorrectWord(word):
                        word_points_text = f"{word}: "
                        word_values_text = ""
                        print("WORD " + word + " IS CORRECT")
                        word_base_score = 0
                        multiplier = 1
                        for move in moves:
                            if self.board.board[move[1]][move[0]][0] != '':
                                letter_value = Letter.get_letter_value(self.board.board[move[1]][move[0]][0])
                                if move in self.turnPositions:
                                    what_kind = self.board.board[move[1]][move[0]][1]
                                    if "_" in what_kind:
                                        what_kind = what_kind.split("_")
                                        if what_kind[1] == "LETTER":
                                            if what_kind[0] == "DOUBLE":
                                                word_base_score = word_base_score + 2 * letter_value
                                                word_values_text = word_values_text + f"+2x{letter_value}"
                                            if what_kind[0] == "TRIPLE":
                                                word_base_score = word_base_score + 3 * letter_value
                                                word_values_text = word_values_text + f"+3x{letter_value}"
                                        if what_kind[1] == "WORD":
                                            if what_kind[0] == "DOUBLE":
                                                multiplier = multiplier * 2
                                            if what_kind[0] == "TRIPLE":
                                                multiplier = multiplier * 3
                                            word_base_score = word_base_score + letter_value
                                            word_values_text = word_values_text + f"+{letter_value}"
                                    else:
                                        word_base_score = word_base_score + letter_value
                                        word_values_text = word_values_text + f"+{letter_value}"
                                else:
                                    word_base_score = word_base_score + letter_value
                                    word_values_text = word_values_text + f"+{letter_value}"
                            else:
                                multiplier = 0
                                break
                        
                        if multiplier != 0:
                            if multiplier == 1:
                                word_points_text = word_points_text + word_values_text[1:]
                            else:
                                word_points_text = word_points_text + '(' + word_values_text[1:] + ')' + f"x{multiplier}"
                            
                            word_points_text = word_points_text + f' = {word_base_score * multiplier}'
                            infoBoardManager.add_new_text(word_points_text, "POINTS")
                        word_base_score = word_base_score * multiplier
                        print(word_base_score)
                        points = points + word_base_score


            return (True, points)
        
    def nextTurn(self):
        global chosenLetter, infoBoardManager
        self.players[self.turn].isTurnNow = False
        self.turn += 1
        if self.turn >= self.nr_players:
            self.turn = 0
        self.players[self.turn].isTurnNow = True
        chosenLetter = ''
        self.turnPositions = []

        infoBoardManager.add_new_text(f"Randul lui Player {self.turn + 1} !", "TURN")

        self.reloadTurnButtons()
        
    def reloadTurnButtons(self):
        rect_endTurn = pygame.Rect(self.players[self.turn].startLettersX + self.players[self.turn].holder_width - self.players[self.turn].letter_size * 5, 
                                self.players[self.turn].startLettersY + self.players[self.turn].letter_size * 2, 
                                self.players[self.turn].letter_size * 4, self.players[self.turn].letter_size)
        global endTurn_button
        endTurn_button = Button(rect_endTurn, (59, 125, 64), (74, 161, 83), (19, 20, 19), "End turn", INFO_FONT_SIZE, should_draw=True)
        rect_discard = pygame.Rect(self.players[self.turn].startLettersX - self.players[self.turn].letter_size,
                                self.players[self.turn].startLettersY + self.players[self.turn].letter_size * 2,
                                self.players[self.turn].letter_size * 4, self.players[self.turn].letter_size)
        global discard_button
        discard_button = Button(rect_discard, (59, 125, 64), (74, 161, 83), (19, 20, 19), "Discard", INFO_FONT_SIZE, should_draw=True)
        
    def handleResize(self, newWidth, newHeight):
        global WIDTH, HEIGHT, BOARD_SIZE
        global INFO_FONT_SIZE, LETTER_FONT_SIZE, LETTER_VALUE_FONT_SIZE, BOARD_INFO_FONT_SIZE
        ogWidth, ogHeight = WIDTH, HEIGHT
        WIDTH, HEIGHT = newWidth, newHeight
        BOARD_SIZE = int(HEIGHT * 9/10)

        self.board.size = BOARD_SIZE
        self.board.cell_size = self.board.size // self.board.cols
        self.board.startY = (HEIGHT - self.board.size) // 2
        self.board.startX = self.board.startY

        self.board.letter_size = int(self.board.cell_size * 8/10)

        for player in self.players:
            player.letter_size = self.board.letter_size
            player.holder_width = player.letter_size * 10
            player.holder_height = player.holder_width * 1/4
            player.startY = (HEIGHT - BOARD_SIZE) // 2
            player.startX = player.startY + BOARD_SIZE + player.holder_width * 1/10
            player.startY = player.startY + player.holder_height * player.turn * 2
            player.startLettersX = player.startX + player.letter_size
            player.startLettersY = player.startY + player.letter_size
            player.HOLDER_IMAGE = pygame.image.load("MEDIA/holder.png")
            player.HOLDER_IMAGE = pygame.transform.scale(player.HOLDER_IMAGE, (player.holder_width, player.holder_height))


        rect_restart = pygame.Rect(gameManager.players[self.turn].startLettersX + gameManager.players[self.turn].holder_width / 2 - gameManager.players[self.turn].letter_size * 3,
                           HEIGHT // 2,
                           gameManager.players[self.turn].letter_size * 4, gameManager.players[self.turn].letter_size)
        global restart_button
        restart_button = Button(rect_restart, (59, 125, 64), (74, 161, 83), (19, 20, 19), "Restart", INFO_FONT_SIZE, should_draw=True)

        self.reloadTurnButtons()


        
        LETTER_FONT_SIZE = int(32 * (newHeight / ogHeight))
        LETTER_VALUE_FONT_SIZE = int(13 * (newHeight / ogHeight))
        INFO_FONT_SIZE = int(24 * (newHeight / ogHeight))
        BOARD_INFO_FONT_SIZE = int(11 * (newHeight / ogHeight))

        global mediaManager
        for index in range(len(mediaManager.order_imgs)):
            order_img = pygame.image.load(f"MEDIA/order{index+1}.png")
            mediaManager.order_imgs[index] = pygame.transform.scale(order_img, (self.board.cell_size*0.8, self.board.cell_size))

        rect_infoBoard = pygame.Rect(gameManager.players[0].startLettersX + gameManager.players[0].holder_width + gameManager.players[0].letter_size,
                             gameManager.players[0].startLettersY,
                             WIDTH - (gameManager.board.size + gameManager.players[0].holder_width) - 5 * gameManager.players[0].letter_size,
                             HEIGHT - 2 * gameManager.players[0].startLettersY
                             )
        global infoBoardManager
        try:
            info_texts = infoBoardManager.texts
            infoBoardManager = InfoBoard(rect_infoBoard, gameManager.board.cell_size)
            for info_text in info_texts:
                infoBoardManager.add_new_text(info_text.text, info_text.type)
        except Exception as e:
            infoBoardManager = InfoBoard(rect_infoBoard, gameManager.board.cell_size)
            pass

    


WHITE = (255, 255, 255)
BACKGROUND_COLOR = (29, 30, 33)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Scrabble")

cursor_image = pygame.image.load("MEDIA/mouse.png")
cursor_image = pygame.transform.scale(cursor_image, (32, 32))
#pygame.mouse.set_visible(False)
cursor_img_rect = cursor_image.get_rect()

board = Board(BOARD_SIZE, 15, 15, WIDTH, HEIGHT)
gameManager = Game(board, nr_players=2)

mediaManager = Media(gameManager.board.cell_size)

infoBoardManager = None
endTurn_button = None
restart_button = None
discard_button = None

gameManager.handleResize(WIDTH, HEIGHT)

chosenLetter = ''
gameManager.players[gameManager.turn].isTurnNow = True

gameManager.stopGame = True

while gameManager.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameManager.running = False
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            newWidth, newHeight = event.size
            gameManager.handleResize(newWidth, newHeight)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row = (mouseY - board.startY) // board.cell_size
            clicked_col = (mouseX - board.startX) // board.cell_size

            # event de a pune
            if chosenLetter != '':
                if clicked_row >= 0 and clicked_row < board.rows and clicked_col >= 0 and clicked_col < board.cols:
                    if board.board[clicked_col][clicked_row][0] == '':
                        board.board[clicked_col][clicked_row][0] = chosenLetter
                        chosenLetter = ''
                        gameManager.turnPositions.append((clicked_row, clicked_col))
                else:
                    gameManager.players[gameManager.turn].letters.append(chosenLetter)
                    gameManager.players[gameManager.turn].selectedLetters.append(False)
                    chosenLetter = ''
            else:
                if clicked_row >= 0 and clicked_row < board.rows and clicked_col >= 0 and clicked_col < board.cols:
                    if (clicked_row, clicked_col) in gameManager.turnPositions:
                        chosenLetter = board.board[clicked_col][clicked_row][0]
                        board.board[clicked_col][clicked_row][0] = ''
                        gameManager.turnPositions.remove((clicked_row, clicked_col))
                        

            letter_index = gameManager.players[gameManager.turn].check_click_holder(mouseX, mouseY)
            if event.button == 1 and letter_index != -1:
                chosenLetter = gameManager.players[gameManager.turn].letters[letter_index]
                gameManager.players[gameManager.turn].letters.pop(letter_index)
                gameManager.players[gameManager.turn].selectedLetters.pop(letter_index)
            elif event.button == 3 and letter_index != -1:
                print("SELECTED " + gameManager.players[gameManager.turn].letters[letter_index])
                gameManager.players[gameManager.turn].selectedLetters[letter_index] = not gameManager.players[gameManager.turn].selectedLetters[letter_index]

            if discard_button.clicked(mouseX, mouseY):
                # PASS DISCARD
                selectedIndexes = []
                for index in range(len(gameManager.players[gameManager.turn].selectedLetters)):
                    if gameManager.players[gameManager.turn].selectedLetters[index] == True:
                        selectedIndexes.append(index)
                if len(selectedIndexes) == 0:
                    # PASS
                    infoBoardManager.add_new_text(f"Player {gameManager.turn+1} a zis PASS", "TURN")
                    gameManager.nextTurn()
                    gameManager.consecutivePasses = gameManager.consecutivePasses + 1
                    if gameManager.consecutivePasses / gameManager.nr_players >= 2:
                        infoBoardManager.add_new_text("PASS de 2 ori consecutiv", "BONUS")
                        infoBoardManager.add_new_text("ENDING GAME", "BONUS")
                        gameManager.stopGame = True
                else:
                    # DISCARD
                    if len(selectedIndexes) == 1 or len(selectedIndexes) == len(gameManager.players[gameManager.turn].letters):
                        discardedLettersStr = ""
                        discardedLetters = []
                        for index in selectedIndexes:
                            discardedLettersStr = discardedLettersStr + f" {gameManager.players[gameManager.turn].letters[index]}"
                            discardedLetters.append(gameManager.players[gameManager.turn].letters[index])
                            gameManager.players[gameManager.turn].letters.pop(index)
                            gameManager.players[gameManager.turn].selectedLetters.pop(index)
                            for i in range(len(selectedIndexes)):
                                if selectedIndexes[i] > index:
                                    selectedIndexes[i] = selectedIndexes[i] - 1
                        
                        newLetters = gameManager.generatePlayerLetters(len(selectedIndexes))
                        for newLetter in newLetters:
                            gameManager.players[gameManager.turn].letters.append(newLetter)
                            gameManager.players[gameManager.turn].selectedLetters.append(False)
                        infoBoardManager.add_new_text(f"DISCARD {discardedLettersStr}", "BONUS")
                        infoBoardManager.add_new_text("ENDING TURN", "BONUS")

                        for discardedLetter in discardedLetters:
                            gameManager.allLetters.append(discardedLetter)

                        gameManager.nextTurn()
                    else:
                        infoBoardManager.add_new_text("DISCARD UNA sau TOATE literele", "WRONG")

            if endTurn_button.clicked(mouseX, mouseY):
                print("END")
                (result, points) = gameManager.endTurn()
                if result == True:
                    gameManager.players[gameManager.turn].isTurnNow = False
                    if len(gameManager.players[gameManager.turn].letters) == 0:
                        points = points + 50
                        infoBoardManager.add_new_text("BONUS +50", "BONUS")
                    gameManager.players[gameManager.turn].score += points
                    newLetters = gameManager.generatePlayerLetters(7 - len(gameManager.players[gameManager.turn].letters))
                    if len(newLetters) != 7 - len(gameManager.players[gameManager.turn].letters):
                        gameManager.entered_final_game = True

                    # END GAME
                    if gameManager.entered_final_game and len(newLetters) == 0 and len(gameManager.players[gameManager.turn].letters) == 0:
                        additionalPoints = 0
                        gameManager.stopGame = True
                        for player in gameManager.players:
                            if player.turn != gameManager.turn:
                                for letter in player.letters:
                                    letter_value = Letter.get_letter_value(letter)
                                    additionalPoints = additionalPoints + letter_value
                        gameManager.players[gameManager.turn].score += additionalPoints

                    for newLetter in newLetters:
                        gameManager.players[gameManager.turn].letters.append(newLetter)
                        gameManager.players[gameManager.turn].selectedLetters.append(False)

                    # CHANGE TURN
                    gameManager.nextTurn()


    screen.fill(BACKGROUND_COLOR)
    board.draw_board(screen, gameManager.turnPositions, len(gameManager.allLetters), chosenLetter)

    infoBoardManager.draw(screen)

    if gameManager.stopGame == False:
        sorted_players = sorted(gameManager.players, key=lambda player: player.score, reverse=True)
        for index in range(len(sorted_players)):
            sorted_players[index].draw_holder(screen)
            sorted_players[index].draw_score(screen, index)
        
        endTurn_button.draw(screen)
        selectedIndexes = []
        for index in range(len(gameManager.players[gameManager.turn].selectedLetters)):
            if gameManager.players[gameManager.turn].selectedLetters[index] == True:
                selectedIndexes.append(index)
        if len(selectedIndexes) == 0:
            discard_button.text = "Pass"
        else:
            discard_button.text = "Discard"
        discard_button.draw(screen)

        if chosenLetter != '':
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rect = pygame.Rect(mouse_x, mouse_y, board.letter_size, board.letter_size)
            Letter.draw_letter(screen, rect.move(-24, -16), chosenLetter, (20, 20, 20), False, False)
    else:
        sorted_players = sorted(gameManager.players, key=lambda player: player.score, reverse=True)
        for index in range(len(sorted_players)):
            sorted_players[index].draw_score_end_game(screen, index)

        restart_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameManager.running = False
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                gameManager.handleResize(newWidth, newHeight)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if restart_button.clicked(mouseX, mouseY):
                    board = Board(BOARD_SIZE, 15, 15, WIDTH, HEIGHT)
                    gameManager = Game(board, nr_players=2)
                    gameManager.players[gameManager.turn].isTurnNow = True
                    gameManager.stopGame = False
                    infoBoardManager.texts = []

    #cursor_img_rect.center = pygame.mouse.get_pos()
    #screen.blit(cursor_image, cursor_img_rect.move(16, 16))

    pygame.display.flip()

pygame.quit()
