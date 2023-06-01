import pygame
import sys
from pygame.locals import *
import constants as SOKOBAN
from level import *
from player import *
from player_interface import *
from solver import *
from pyautogui import press, typewrite, hotkey
import os
import _thread
import time
import pygame.mixer


def move(threadName, delay, strategy):
    """
    Simulates the player's moves based on a given strategy.

    Args:
        threadName (str): The name of the thread.
        delay (int): The delay between each move.
        strategy (list): The list of moves to simulate.

    Returns:
        None
    """
    for step in strategy:
        if step in ['R', 'r']:
            press('right')
        if step in ['L', 'l']:
            press('left')
        if step in ['D', 'd']:
            press('down')
        if step in ['U', 'u']:
            press('up')
        time.sleep(0.2)


class Game:
    def __init__(self, window):
        """
        Initializes a new Game object.

        Args:
            window (pygame.Surface): The Pygame window.

        Returns:
            None
        """
        self.window = window
        self.load_textures()
        self.player = None
        self.index_level = 1
        self.load_level()
        self.play = True
        self.player_interface = PlayerInterface(self.player, self.level)
        self.steps = 0
        pygame.mixer.init()
        self.bg_music = pygame.mixer.Sound("assets/sounds.wav")
        self.font_alert = pygame.font.Font('assets/fonts/FreeSansBold.ttf', 26)

    def load_textures(self):
        """
        Loads the textures used in the game.

        Returns:
            None
        """
        self.textures = {
            SOKOBAN.WALL: pygame.image.load('assets/images/wall.png').convert_alpha(),
            SOKOBAN.BOX: pygame.image.load('assets/images/box.png').convert_alpha(),
            SOKOBAN.TARGET: pygame.image.load('assets/images/target.png').convert_alpha(),
            SOKOBAN.TARGET_FILLED: pygame.image.load('assets/images/valid_box.png').convert_alpha(),
            SOKOBAN.PLAYER: pygame.image.load('assets/images/player_sprites.png').convert_alpha()
        }

    def load_level(self):
        """
        Loads the current level.

        Returns:
            None
        """
        self.level = Level(self.index_level)
        self.board = pygame.Surface((self.level.width, self.level.height))
        if self.player:
            self.player.pos = self.level.position_player
            self.player_interface.level = self.level
            self.player.move_count = 0
        else:
            self.player = Player(self.level)
            self.player.move_count = 0

    def start(self):
        """
        Starts the game loop.

        Returns:
            None
        """
        self.bg_music.play(-1)
        while self.play:
            self.process_event(pygame.event.wait())
            self.update_screen()

    def process_event(self, event):
        """
        Processes Pygame events.

        Args:
            event (pygame.event.Event): The Pygame event.

        Returns:
            None
        """
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Quit game
                self.play = False
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d]:
                # Move players
                self.steps += 1
                self.player.move(event.key, self.level, self.player_interface)
                if self.has_win():
                    self.index_level += 1
                    if (self.index_level == 16):
                        self.index_level = 1
                    self.player.move_count = 0
                    self.load_level()
            if event.key == K_r:
                self.load_level()
            if event.key == K_l:
                self.level.cancel_last_move(self.player, self.player_interface)
        if event.type == MOUSEBUTTONUP:
            self.player_interface.click(event.pos, self.level, self)
        if event.type == MOUSEMOTION:
            self.player_interface.mouse_pos = event.pos

    def update_screen(self):
        """
        Updates the game screen.

        Returns:
            None
        """
        pygame.draw.rect(self.board, SOKOBAN.WHITE,
                         (0, 0, self.level.width * SOKOBAN.SPRITESIZE, self.level.height * SOKOBAN.SPRITESIZE))
        pygame.draw.rect(self.window, SOKOBAN.WHITE, (0, 0, SOKOBAN.WINDOW_WIDTH, SOKOBAN.WINDOW_HEIGHT))

        self.level.render(self.board, self.textures)
        self.player.render(self.board, self.textures)

        pox_x_board = (SOKOBAN.WINDOW_WIDTH / 2) - (self.board.get_width() / 2)
        pos_y_board = (SOKOBAN.WINDOW_HEIGHT / 2) - (self.board.get_height() / 2)
        self.window.blit(self.board, (pox_x_board, pos_y_board))

        self.player_interface.render(self.window, self.index_level)
        pygame.draw.rect(self.board, SOKOBAN.WHITE,
                         (0, 0, self.level.width * SOKOBAN.SPRITESIZE, self.level.height * SOKOBAN.SPRITESIZE))
        pygame.draw.rect(self.window, SOKOBAN.WHITE, (0, 0, SOKOBAN.WINDOW_WIDTH, SOKOBAN.WINDOW_HEIGHT))

        self.level.render(self.board, self.textures)
        self.player.render(self.board, self.textures)

        pox_x_board = (SOKOBAN.WINDOW_WIDTH / 2) - (self.board.get_width() / 2)
        pos_y_board = (SOKOBAN.WINDOW_HEIGHT / 2) - (self.board.get_height() / 2)
        self.window.blit(self.board, (pox_x_board, pos_y_board))

        self.player_interface.render(self.window, self.index_level)

        # Render player's move count
        move_count_text = f"Steps: {self.player.move_count}"
        move_count_surface = self.font_alert.render(move_count_text, True, SOKOBAN.BLACK)
        move_count_position = (20, SOKOBAN.WINDOW_HEIGHT - move_count_surface.get_height() - 20)
        self.window.blit(move_count_surface, move_count_position)

        pygame.display.flip()

    def has_win(self):
        """
        Checks if the player has won the current level.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        nb_missing_target = 0
        for y in range(len(self.level.structure)):
            for x in range(len(self.level.structure[y])):
                if self.level.structure[y][x] == SOKOBAN.TARGET:
                    nb_missing_target += 1

        if nb_missing_target == 0:
            if self.index_level == 15:
                # Render message and options
                message = "Congratulations! You have completed all levels!"
                options = "Press Q to quit the game or press E to play the extreme level."
                message_surface = self.font_alert.render(message, True, SOKOBAN.RED)
                options_surface = self.font_alert.render(options, True, SOKOBAN.RED)

                # Calculate positions to center the text on the screen
                message_pos = ((SOKOBAN.WINDOW_WIDTH - message_surface.get_width()) // 2,
                               (SOKOBAN.WINDOW_HEIGHT - message_surface.get_height()) // 2)
                options_pos = ((SOKOBAN.WINDOW_WIDTH - options_surface.get_width()) // 2,
                               message_pos[1] + message_surface.get_height() + 20)

                # Render text on the game window
                self.window.blit(message_surface, message_pos)
                self.window.blit(options_surface, options_pos)
                pygame.display.flip()

                # Wait for player input
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_e:
                            self.index_level = 16
                            self.load_level()
                            break
            else:
                level_scoreboard = self.get_scoreboard()
                if self.index_level in level_scoreboard:
                    if self.player.move_count < level_scoreboard[self.index_level]:
                        level_scoreboard[self.index_level] = self.player.move_count
                else:
                    level_scoreboard[self.index_level] = self.player.move_count

                # Save the scoreboard
                self.save_scoreboard(level_scoreboard)
                self.player.move_count = 0
                self.index_level += 1
                if self.index_level == 17:
                    self.index_level = 1
                self.load_level()
        return False
    def get_scoreboard(self):
        """
        Retrieves the current scoreboard.

        Returns:
            dict: The current scoreboard where level numbers are keys and minimum steps are values.
        """
        scoreboard_file = "assets/scoreboard.txt"
        scoreboard = {}
        if os.path.isfile(scoreboard_file):
            with open(scoreboard_file, 'r') as file:
                for line in file:
                    level, steps = line.strip().split(':')
                    scoreboard[int(level)] = int(steps)
        return scoreboard

    def save_scoreboard(self, scoreboard):
        """
        Saves the updated scoreboard.

        Args:
            scoreboard (dict): The updated scoreboard where level numbers are keys and minimum steps are values.

        Returns:
            None
        """
        scoreboard_file = "assets/scoreboard.txt"
        with open(scoreboard_file, 'w') as file:
            for level, steps in scoreboard.items():
                file.write(f"{level}:{steps}\n")

    def auto_move(self):
        """
        Automatically moves the player based on a pre-calculated strategy.

        Returns:
            None
        """
        answer_dir = "assets/answer"
        if not os.path.exists(answer_dir):
            os.makedirs(answer_dir)
        file_name = f"{answer_dir}/level_{self.index_level}.txt"
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                strategy = file.read().strip().split(", ")
        else:
            strategy = get_move(self.level.structure, self.level.position_player, 'ucs')
            with open(file_name, 'w') as file:
                file.write(', '.join(str(i) for i in strategy))

        if strategy is not None:
            try:
                move_thread = _thread.start_new_thread(move, ("Thread-1", 5, strategy))
            except:
                print("Error: unable to start thread")
