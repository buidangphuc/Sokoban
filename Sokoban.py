import pygame
import os
from pygame.locals import *
import constants as SOKOBAN
from game import *

class Menu:
    def __init__(self):
        """
        Initializes a new Menu object.

        Args:
            None

        Returns:
            None
        """
        self.image = pygame.image.load('assets/images/menu.png').convert_alpha()
        self.new_game_txt = "New Game"
        self.load_game_txt = "Extreme Level"
        self.tutorial_txt = "Tutorial"
        self.scoreboard_txt = "Scoreboard"
        self.quit_game_txt = "Quit"
        self.font = pygame.font.Font('assets/fonts/FreeSansBold.ttf', 30)
        self.smaller_font = pygame.font.Font('assets/fonts/FreeSansBold.ttf', 18)
        self.tutorial_active = False
        self.scoreboard_active = False

    def click(self, click_pos, window):
        """
        Handles a click event on the menu.

        Args:
            click_pos (tuple): The position of the click event.
            window (pygame.Surface): The game window surface.

        Returns:
            bool: True if the game should continue running, False if it should quit.
        """
        x = click_pos[0]
        y = click_pos[1]

        if not self.tutorial_active and not self.scoreboard_active:
            if x > self.new_game_txt_position[0] and x < self.new_game_txt_position[0] + self.new_game_txt_surface.get_width() \
            and y > 300 and y < 300 + self.new_game_txt_surface.get_height():
                sokoban = Game(window)
                sokoban.start()
            elif x > self.extreme_game_txt_position[0] and x < self.extreme_game_txt_position[0] + self.load_game_txt_surface.get_width() \
            and y > 370 and y < 370 + self.load_game_txt_surface.get_height():
                sokoban = Game(window)
                sokoban.index_level = 16
                sokoban.load_level()
                sokoban.start()
            elif x > self.tutorial_txt_position[0] and x < self.tutorial_txt_position[0] + self.tutorial_txt_surface.get_width() \
            and y > 440 and y < 440 + self.tutorial_txt_surface.get_height():
                self.tutorial_active = True
            elif x > self.scoreboard_txt_position[0] and x < self.scoreboard_txt_position[0] + self.scoreboard_txt_surface.get_width() \
            and y > 510 and y < 510 + self.scoreboard_txt_surface.get_height():
                self.scoreboard_active = True
            elif x > self.quit_game_txt_position[0] and x < self.quit_game_txt_position[0] + self.quit_game_txt_surface.get_width() \
            and y > 580 and y < 580 + self.quit_game_txt_surface.get_height():
                return False
        else:
            if x > self.back_txt_position[0] and x < self.back_txt_position[0] + self.back_txt_surface.get_width() \
            and y > self.back_txt_position[1] and y < self.back_txt_position[1] + self.back_txt_surface.get_height():
                self.tutorial_active = False
                self.scoreboard_active = False
        return True
    
    

    def render(self, window):
        """
        Renders the menu on the game window.

        Args:
            window (pygame.Surface): The game window surface.

        Returns:
            None
        """
        window.blit(self.image, (0,0))

        self.new_game_txt_surface = self.font.render(self.new_game_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.new_game_txt_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (self.new_game_txt_surface.get_width() / 2), 300)
        window.blit(self.new_game_txt_surface, self.new_game_txt_position)

        self.load_game_txt_surface = self.font.render(self.load_game_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.extreme_game_txt_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (self.load_game_txt_surface.get_width() / 2), 370)
        window.blit(self.load_game_txt_surface, self.extreme_game_txt_position)

        self.tutorial_txt_surface = self.font.render(self.tutorial_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.tutorial_txt_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (self.tutorial_txt_surface.get_width() / 2), 440)
        window.blit(self.tutorial_txt_surface, self.tutorial_txt_position)

        self.scoreboard_txt_surface = self.font.render(self.scoreboard_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.scoreboard_txt_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (self.scoreboard_txt_surface.get_width() / 2), 510)
        window.blit(self.scoreboard_txt_surface, self.scoreboard_txt_position)

        self.quit_game_txt_surface = self.font.render(self.quit_game_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.quit_game_txt_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (self.quit_game_txt_surface.get_width() / 2), 580)
        window.blit(self.quit_game_txt_surface, self.quit_game_txt_position)

    def render_tutorial(self, window):
        """
        Renders the tutorial text on the game window.

        Args:
            window (pygame.Surface): The game window surface.

        Returns:
            None
        """
        window.fill(SOKOBAN.WHITE)

        tutorial_text = [
            "Mục tiêu:",
            "Đặt tất cả các hộp lên các điểm đích trên bản đồ.",
            "Điều khiển:",
            "Mũi tên hoặc WASD để di chuyển nhân vật.",
            "R - Chơi lại.",
            "Esc - Thoát game.",
            "Lưu ý:",
            "- Điểm số sẽ tính dựa trên số bước đi, nhân vật di chuyển qua tường hoặc đẩy 2 thùng vẫn tính 1 lượt",
            "- Không thể đẩy hộp ra khỏi bản đồ hoặc đẩy vào các vật cản không di chuyển được.",
            "- Bạn chỉ có thể đẩy một hộp một lúc.",
            "- Bạn không thể kéo các hộp.",
            "- 'Auto' để vượt qua màn chơi.",
            "- 'Undo the last move' để đưa thùng lại vị trí trước đó"
        ]
        text_y = 100
        for line in tutorial_text:
            text_surface = self.smaller_font.render(line, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
            text_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (text_surface.get_width() / 2), text_y)
            window.blit(text_surface, text_position)
            text_y += 30
        
        self.back_txt_surface = self.smaller_font.render("Back", True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.back_txt_position = (20, 20)
        window.blit(self.back_txt_surface, self.back_txt_position)

        pygame.display.flip()
    def render_scoreboard(self,window):
        """
        Displays the scoreboard.

        Args:
            None

        Returns:
            None
        """
        scoreboard = self.get_scoreboard()
        window.fill(SOKOBAN.WHITE)

        scoreboard_title = self.font.render("Scoreboard", True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        scoreboard_title_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (scoreboard_title.get_width() / 2), 100)
        window.blit(scoreboard_title, scoreboard_title_position)

        y_position = 150
        for level, steps in scoreboard.items():
            level_text = self.smaller_font.render(f"Level {level}:", True, SOKOBAN.BLACK, SOKOBAN.WHITE)
            level_text_position = ((SOKOBAN.WINDOW_WIDTH / 2) - (level_text.get_width() / 2), y_position)
            window.blit(level_text, level_text_position)

            steps_text = self.smaller_font.render(str(steps), True, SOKOBAN.BLACK, SOKOBAN.WHITE)
            steps_text_position = (level_text_position[0] + level_text.get_width() + 10, y_position)
            window.blit(steps_text, steps_text_position)

            y_position += 40

        self.back_txt_surface = self.smaller_font.render("Back", True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.back_txt_position = (20, 20)
        window.blit(self.back_txt_surface, self.back_txt_position)

        pygame.display.flip()

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



def main():
    """
    The main function to run the Sokoban game.

    Args:
        None

    Returns:
        None
    """
    pygame.init()
    pygame.key.set_repeat(100, 100)
    pygame.display.set_caption("Sokoban Game")
    window = pygame.display.set_mode((SOKOBAN.WINDOW_WIDTH, SOKOBAN.WINDOW_HEIGHT))
    menu = Menu()

    run = True
    while run:
        event = pygame.event.wait()
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_j:
                sokoban = Game(window)
                sokoban.start()
            elif event.key == K_c:
                sokoban = Game(window)
            elif event.key == K_ESCAPE:
                run = False
        if event.type == MOUSEBUTTONUP:
            if menu.tutorial_active:
                menu.click(event.pos, window)
            else:
                run = menu.click(event.pos, window)

        pygame.draw.rect(window, SOKOBAN.WHITE, (0,0,SOKOBAN.WINDOW_WIDTH,SOKOBAN.WINDOW_HEIGHT))
        if menu.tutorial_active:
            menu.render_tutorial(window)
        elif menu.scoreboard_active:
            menu.render_scoreboard(window)
        else:
            menu.render(window)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
