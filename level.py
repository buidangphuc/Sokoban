import pygame
import constants as SOKOBAN
import copy

class Level:
    def __init__(self, level_to_load):
        """
        Initializes a new Level object.

        Args:
            level_to_load (int): The level number to load.

        Returns:
            None
        """
        self.last_structure_state = None
        self.last_player_pos = None
        self.load(level_to_load)

    def load(self, level):
        """
        Loads the specified level.

        Args:
            level (int): The level number to load.

        Returns:
            None
        """
        self.structure = []
        max_width = 0
        with open("assets/sokobanLevels/test" + str(level) + ".txt") as level_file:
            rows = level_file.read().split('\n')
            for y in range(len(rows)):
                level_row = []
                if len(rows[y]) > max_width:
                    max_width = len(rows[y])
                for x in range(len(rows[y])):
                    if rows[y][x] == ' ':
                        level_row.append(SOKOBAN.AIR)
                    elif rows[y][x] == '#':
                        level_row.append(SOKOBAN.WALL)
                    elif rows[y][x] == 'B':
                        level_row.append(SOKOBAN.BOX)
                    elif rows[y][x] == '.':
                        level_row.append(SOKOBAN.TARGET)
                    elif rows[y][x] == 'X':
                        level_row.append(SOKOBAN.TARGET_FILLED)
                    elif rows[y][x] == '&':
                        level_row.append(SOKOBAN.AIR)
                        self.position_player = [x,y]
                self.structure.append(level_row)

        self.width = max_width * SOKOBAN.SPRITESIZE
        self.height = (len(rows) - 1) * SOKOBAN.SPRITESIZE

    def cancel_last_move(self, player, interface):
        """
        Cancels the last move made by the player.

        Args:
            player (Player): The player object.
            interface (Interface): The interface object.

        Returns:
            None
        """
        if self.last_structure_state:
            self.structure = copy.deepcopy(self.last_structure_state)
            player.pos = self.last_player_pos
            interface.colorTxtCancel = SOKOBAN.GREY
            self.last_structure_state = None
            self.last_player_pos = None
        else:
            print("No previous state")

    def render(self, window, textures):
        """
        Renders the level on the window.

        Args:
            window (pygame.Surface): The window to render the level on.
            textures (dict): A dictionary mapping level elements to their corresponding textures.

        Returns:
            None
        """
        for y in range(len(self.structure)):
            for x in range(len(self.structure[y])):
                if self.structure[y][x] in textures:
                    window.blit(textures[self.structure[y][x]], (x * SOKOBAN.SPRITESIZE, y * SOKOBAN.SPRITESIZE))
                else:
                    if self.structure[y][x] == SOKOBAN.TARGET_FILLED:
                        pygame.draw.rect(window, (0,255,0), (x * SOKOBAN.SPRITESIZE, y * SOKOBAN.SPRITESIZE, SOKOBAN.SPRITESIZE, SOKOBAN.SPRITESIZE))
                    else:
                        pygame.draw.rect(window, SOKOBAN.WHITE, (x * SOKOBAN.SPRITESIZE, y * SOKOBAN.SPRITESIZE, SOKOBAN.SPRITESIZE, SOKOBAN.SPRITESIZE))
