import pygame
import random
import json


# --- Your existing CrosswordPuzzle class with modifications ---
class CrosswordPuzzle:
    """
    A class to represent and generate a crossword puzzle.

    Attributes:
        width (int): The width of the crossword grid.
        height (int): The height of the crossword grid.
        grid (list of list of str): The 2D list representing the crossword grid.
                                     Empty cells are represented by an empty string or '#'.
        solution_grid (list of list of str): The grid with the correct answers.
        words (list of dict): A list of word dictionaries containing word and clue.
        placed_words (list of dict): A list of dictionaries, each containing
                                     details about a placed word (word, start_x, start_y, direction).
    """

    def __init__(self, width=15, height=15):
        """
        Initializes the crossword puzzle grid with a given width and height.
        """
        self.width = width
        self.height = height
        # Initialize the grid with empty cells (e.g., '#')
        self.grid = [['#' for _ in range(width)] for _ in range(height)]
        self.solution_grid = [['#' for _ in range(width)] for _ in range(height)]
        self.words = []
        self.placed_words = []

    def add_word(self, word, clue):
        """
        Adds a word and its clue to the list of words to be placed in the puzzle.
        Also performs an initial check to ensure the word can fit on the grid at all.
        """
        word_upper = word.upper()
        # A word must be able to fit either horizontally or vertically
        if len(word_upper) <= self.width or len(word_upper) <= self.height:
            self.words.append({'word': word_upper, 'clue': clue})
        else:
            print(
                f"Word '{word}' is too long to fit in the puzzle grid (max length {max(self.width, self.height)}). Skipping.")

    def _can_place_word(self, word, start_x, start_y, direction):
        """
        Checks if a word can be placed at a given position and direction
        without conflicting with existing letters, going out of bounds,
        or touching existing words improperly (i.e., not intersecting).

        Args:
            word (str): The word to check.
            start_x (int): The starting X-coordinate (column).
            start_y (int): The starting Y-coordinate (row).
            direction (str): 'horizontal' or 'vertical'.

        Returns:
            bool: True if the word can be placed, False otherwise.
        """
        word_length = len(word)
        intersection_count = 0  # Count how many valid intersections occur

        # --- CRITICAL CHECK: Ensure start coordinates are not negative ---
        if start_x < 0 or start_y < 0:
            return False

        if direction == 'horizontal':
            # 1. Out of bounds check (end of word)
            if start_x + word_length > self.width:
                return False

            # 2. Check cells along the word's path and surrounding perpendicular cells
            for i in range(word_length):
                x = start_x + i
                y = start_y

                # Ensure coordinates are within grid bounds before accessing
                if not (0 <= x < self.width and 0 <= y < self.height):
                    return False

                current_grid_char = self.solution_grid[y][x]

                # If the cell is occupied by an existing letter
                if current_grid_char != '#':
                    # A. Check for direct conflict: If existing letter doesn't match new word's letter
                    if current_grid_char != word[i]:
                        return False
                    # B. If it matches, it's a potential intersection point.
                    intersection_count += 1
                else:  # The cell is currently empty ('#')
                    # C. If the cell is empty, ensure its perpendicular neighbors are also empty.
                    # Check cell above
                    if y > 0 and self.solution_grid[y - 1][x] != '#':
                        return False
                    # Check cell below
                    if y < self.height - 1 and self.solution_grid[y + 1][x] != '#':
                        return False

            # 3. Check horizontal boundaries (cells immediately before and after the word)
            if start_x > 0 and self.solution_grid[start_y][start_x - 1] != '#':
                return False
            if start_x + word_length < self.width and self.solution_grid[start_y][start_x + word_length] != '#':
                return False

        elif direction == 'vertical':
            # 1. Out of bounds check (end of word)
            if start_y + word_length > self.height:
                return False

            # 2. Check cells along the word's path and surrounding perpendicular cells
            for i in range(word_length):
                x = start_x
                y = start_y + i

                # Ensure coordinates are within grid bounds before accessing
                if not (0 <= x < self.width and 0 <= y < self.height):
                    return False

                current_grid_char = self.solution_grid[y][x]

                # If the cell is occupied by an existing letter
                if current_grid_char != '#':
                    # A. Check for direct conflict: If existing letter doesn't match new word's letter
                    if current_grid_char != word[i]:
                        return False
                    # B. If it matches, it's a potential intersection point.
                    intersection_count += 1
                else:  # The cell is currently empty ('#')
                    # C. If the cell is empty, ensure its perpendicular neighbors are also empty.
                    # Check cell to the left
                    if x > 0 and self.solution_grid[y][x - 1] != '#':
                        return False
                    # Check cell to the right
                    if x < self.width - 1 and self.solution_grid[y][x + 1] != '#':
                        return False

            # 3. Check vertical boundaries (cells immediately before and after the word)
            if start_y > 0 and self.solution_grid[start_y - 1][start_x] != '#':
                return False
            if start_y + word_length < self.height and self.solution_grid[start_y + word_length][start_x] != '#':
                return False

        # For a word to be placed, it must either be the first word (no intersections yet)
        # or it must have at least one valid intersection with an existing word.
        if not self.placed_words and intersection_count == 0:  # First word can be placed anywhere
            return True
        elif self.placed_words and intersection_count == 0:  # Subsequent words MUST intersect
            return False  # If there are already words, and this one doesn't intersect, it's invalid.

        return True  # If all checks pass and there are valid intersections (if not first word)

    def _place_word(self, word_dict, start_x, start_y, direction):
        """
        Places a word onto the grid at the specified position and direction.
        Assumes _can_place_word has already verified it's possible.
        """
        word = word_dict['word']
        word_length = len(word)

        if direction == 'horizontal':
            for i in range(word_length):
                self.solution_grid[start_y][start_x + i] = word[i]
                self.grid[start_y][start_x + i] = ' '  # Empty space for user input
        elif direction == 'vertical':
            for i in range(word_length):
                self.solution_grid[start_y + i][start_x] = word[i]
                self.grid[start_y + i][start_x] = ' '  # Empty space for user input

        self.placed_words.append({
            'word': word,
            'clue': word_dict['clue'],
            'start_x': start_x,
            'start_y': start_y,
            'direction': direction,
            'number': len(self.placed_words) + 1
        })

    def generate_puzzle(self):
        """
        Attempts to generate the crossword puzzle by placing words on the grid.
        """
        # Sort words by length in descending order to place longer words first
        self.words.sort(key=lambda x: len(x['word']), reverse=True)

        for word_dict in self.words:
            word = word_dict['word']
            placed = False

            # Store valid directions for the current word
            possible_directions = []
            if len(word) <= self.width:
                possible_directions.append('horizontal')
            if len(word) <= self.height:
                possible_directions.append('vertical')

            if not possible_directions:
                print(f"Word '{word}' is too long to fit horizontally or vertically. Skipping.")
                continue

            # If no words are placed yet, try random positions for the first word.
            if not self.placed_words:
                for _ in range(self.width * self.height * 50):
                    direction = random.choice(possible_directions)

                    if direction == 'horizontal':
                        max_x = self.width - len(word)
                        if max_x < 0: continue
                        start_x = random.randint(0, max_x)
                        start_y = random.randint(0, self.height - 1)
                    else:  # vertical
                        max_y = self.height - len(word)
                        if max_y < 0: continue
                        start_x = random.randint(0, self.width - 1)
                        start_y = random.randint(0, max_y)

                    if self._can_place_word(word, start_x, start_y, direction):
                        self._place_word(word_dict, start_x, start_y, direction)
                        placed = True
                        break
            else:
                # For subsequent words, try to find an intersection point.
                possible_placements = []
                for p_word in self.placed_words:
                    for char_idx_new, char_new in enumerate(word):
                        for char_idx_old, char_old in enumerate(p_word['word']):
                            if char_new == char_old:  # Found a potential intersection
                                # Calculate potential start_x, start_y, and direction for the new word
                                if p_word['direction'] == 'horizontal' and 'vertical' in possible_directions:
                                    potential_start_x = p_word['start_x'] + char_idx_old
                                    potential_start_y = p_word['start_y'] - char_idx_new

                                    if potential_start_x >= 0 and potential_start_y >= 0:
                                        if self._can_place_word(word, potential_start_x, potential_start_y, 'vertical'):
                                            possible_placements.append(
                                                (word_dict, potential_start_x, potential_start_y, 'vertical'))
                                elif p_word['direction'] == 'vertical' and 'horizontal' in possible_directions:
                                    potential_start_x = p_word['start_x'] - char_idx_new
                                    potential_start_y = p_word['start_y'] + char_idx_old

                                    if potential_start_x >= 0 and potential_start_y >= 0:
                                        if self._can_place_word(word, potential_start_x, potential_start_y,
                                                                'horizontal'):
                                            possible_placements.append(
                                                (word_dict, potential_start_x, potential_start_y, 'horizontal'))

                random.shuffle(possible_placements)
                for placement_info in possible_placements:
                    word_to_place, sx, sy, direct = placement_info
                    if self._can_place_word(word_to_place['word'], sx, sy, direct):
                        self._place_word(word_to_place, sx, sy, direct)
                        placed = True
                        break

                # If no ideal intersection placement found, fall back to random placement attempts
                if not placed:
                    for _ in range(self.width * self.height * 50):
                        direction = random.choice(possible_directions)

                        if direction == 'horizontal':
                            max_x = self.width - len(word)
                            if max_x < 0: continue
                            start_x = random.randint(0, max_x)
                            start_y = random.randint(0, self.height - 1)
                        else:  # vertical
                            max_y = self.height - len(word)
                            if max_y < 0: continue
                            start_x = random.randint(0, self.width - 1)
                            start_y = random.randint(0, max_y)

                        if self._can_place_word(word, start_x, start_y, direction):
                            self._place_word(word_dict, start_x, start_y, direction)
                            placed = True
                            break

            if not placed:
                print(f"Could not place word: {word}")

    def display_puzzle(self):
        """
        Prints the current state of the crossword grid to the console.
        """
        print("\nCrossword Puzzle (Console View - for debugging):")
        for row in self.grid:
            print(" ".join(cell if cell != '#' else '■' for cell in row))

        print("\nPlaced Words (and their starting positions):")
        if not self.placed_words:
            print("No words were successfully placed in the puzzle.")
        for p_word in self.placed_words:
            print(f"- {p_word['number']}. {p_word['word']} ({p_word['direction']}): "
                  f"Start Row {p_word['start_y']}, Col {p_word['start_x']} - {p_word['clue']}")


# --- Enhanced Pygame GUI Implementation ---

class CrosswordGUI:
    """
    A Pygame-based GUI for displaying and playing the crossword puzzle.
    """

    def __init__(self, puzzle_instance, cell_size=35, margin=20):
        """
        Initializes the Pygame GUI.
        """
        pygame.init()

        self.puzzle = puzzle_instance
        self.cell_size = cell_size
        self.margin = margin

        # Calculate screen dimensions
        grid_width = self.puzzle.width * self.cell_size + 2 * self.margin
        clues_width = 400  # Fixed width for clues panel
        self.screen_width = grid_width + clues_width
        self.screen_height = max(600, self.puzzle.height * self.cell_size + 2 * self.margin)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Interaktives Kreuzworträtsel")

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.BLUE = (100, 150, 255)
        self.GREEN = (100, 255, 100)
        self.RED = (255, 100, 100)
        self.YELLOW = (255, 255, 100)
        self.LIGHT_BLUE = (200, 220, 255)

        # Define fonts
        self.font_large = pygame.font.Font(None, int(self.cell_size * 0.6))
        self.font_small = pygame.font.Font(None, int(self.cell_size * 0.3))
        self.font_clues = pygame.font.Font(None, 18)
        self.font_title = pygame.font.Font(None, 24)

        # User input grid (what the user has typed)
        self.user_grid = [['' for _ in range(self.puzzle.width)] for _ in range(self.puzzle.height)]

        # Selected cell and word
        self.selected_cell = None
        self.selected_word = None
        self.selected_direction = None

        # Scroll position for clues
        self.clues_scroll = 0

    def get_word_at_cell(self, row, col):
        """
        Returns all words that pass through the given cell.
        """
        words_at_cell = []
        for word_info in self.puzzle.placed_words:
            start_x, start_y = word_info['start_x'], word_info['start_y']
            word_len = len(word_info['word'])
            direction = word_info['direction']

            if direction == 'horizontal':
                if (row == start_y and start_x <= col < start_x + word_len):
                    words_at_cell.append(word_info)
            elif direction == 'vertical':
                if (col == start_x and start_y <= row < start_y + word_len):
                    words_at_cell.append(word_info)

        return words_at_cell

    def get_next_cell_in_word(self, current_row, current_col, word_info):
        """
        Returns the next cell in the word direction, or None if at the end.
        """
        start_x, start_y = word_info['start_x'], word_info['start_y']
        direction = word_info['direction']
        word_len = len(word_info['word'])

        if direction == 'horizontal':
            next_col = current_col + 1
            if next_col < start_x + word_len:
                return (current_row, next_col)
        elif direction == 'vertical':
            next_row = current_row + 1
            if next_row < start_y + word_len:
                return (next_row, current_col)

    def get_cell_at_pos(self, mouse_pos):
        """
        Returns the grid coordinates of the cell at the given mouse position.
        """
        x, y = mouse_pos
        if x < self.margin or y < self.margin:
            return None

        col = (x - self.margin) // self.cell_size
        row = (y - self.margin) // self.cell_size

        if 0 <= col < self.puzzle.width and 0 <= row < self.puzzle.height:
            if self.puzzle.grid[row][col] != '#':  # Only selectable if it's a playable cell
                return (row, col)
        return None

    def select_cell(self, row, col):
        """
        Selects a cell and determines the active word and direction.
        """
        self.selected_cell = (row, col)

        # Find words that pass through this cell
        words_at_cell = self.get_word_at_cell(row, col)

        if words_at_cell:
            # If we have a previously selected word and it's still valid, keep it
            if (self.selected_word and self.selected_word in words_at_cell):
                pass  # Keep current selection
            else:
                # Select the first word (or prioritize horizontal/vertical based on preference)
                self.selected_word = words_at_cell[0]
                self.selected_direction = self.selected_word['direction']
        else:
            self.selected_word = None
            self.selected_direction = None

    def get_previous_cell_in_word(self, current_row, current_col, word_info):
        """
        Returns the previous cell in the word direction, or None if at the beginning.
        """
        start_x, start_y = word_info['start_x'], word_info['start_y']
        direction = word_info['direction']

        if direction == 'horizontal':
            prev_col = current_col - 1
            if prev_col >= start_x:
                return (current_row, prev_col)
        elif direction == 'vertical':
            prev_row = current_row - 1
            if prev_row >= start_y:
                return (prev_row, current_col)

        return None
        """
        Returns the grid coordinates of the cell at the given mouse position.
        """
        x, y = mouse_pos
        if x < self.margin or y < self.margin:
            return None

        col = (x - self.margin) // self.cell_size
        row = (y - self.margin) // self.cell_size

        if 0 <= col < self.puzzle.width and 0 <= row < self.puzzle.height:
            if self.puzzle.grid[row][col] != '#':  # Only selectable if it's a playable cell
                return (row, col)
        return None

    def draw_grid(self):
        """
        Draws the crossword grid with user input and visual feedback.
        """
        for row_idx in range(self.puzzle.height):
            for col_idx in range(self.puzzle.width):
                x = self.margin + col_idx * self.cell_size
                y = self.margin + row_idx * self.cell_size

                cell_value = self.puzzle.grid[row_idx][col_idx]
                user_value = self.user_grid[row_idx][col_idx]
                solution_value = self.puzzle.solution_grid[row_idx][col_idx]

                # Determine cell color based on state
                if cell_value == '#':  # Blocked cell
                    color = self.BLACK
                elif (row_idx, col_idx) == self.selected_cell:  # Selected cell
                    color = self.YELLOW
                elif (self.selected_word and
                      self._is_cell_in_word(row_idx, col_idx, self.selected_word)):  # Highlighted word
                    color = self.LIGHT_BLUE
                elif user_value and user_value.upper() == solution_value:  # Correct letter
                    color = self.GREEN
                elif user_value and user_value.upper() != solution_value:  # Wrong letter
                    color = self.RED
                else:  # Empty playable cell
                    color = self.WHITE

                # Draw cell
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, self.BLACK, (x, y, self.cell_size, self.cell_size), 1)

                # Draw word numbers
                if cell_value != '#':
                    # Check if this is the start of a word
                    for word_info in self.puzzle.placed_words:
                        if word_info['start_x'] == col_idx and word_info['start_y'] == row_idx:
                            num_surface = self.font_small.render(str(word_info['number']), True, self.BLACK)
                            self.screen.blit(num_surface, (x + 2, y + 2))

                    # Draw user input
                    if user_value:
                        text_surface = self.font_large.render(user_value.upper(), True, self.BLACK)
                        text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        self.screen.blit(text_surface, text_rect)

    def _is_cell_in_word(self, row, col, word_info):
        """
        Checks if a cell is part of the given word.
        """
        start_x, start_y = word_info['start_x'], word_info['start_y']
        word_len = len(word_info['word'])
        direction = word_info['direction']

        if direction == 'horizontal':
            return (row == start_y and start_x <= col < start_x + word_len)
        elif direction == 'vertical':
            return (col == start_x and start_y <= row < start_y + word_len)

        return False

    def draw_clues(self):
        """
        Draws the clues panel on the right side of the screen.
        """
        clues_x = self.puzzle.width * self.cell_size + 2 * self.margin + 10
        clues_y = 20

        # Title
        title_surface = self.font_title.render("FRAGEN:", True, self.BLACK)
        self.screen.blit(title_surface, (clues_x, clues_y))
        clues_y += 40

        # Separate horizontal and vertical clues
        horizontal_clues = [w for w in self.puzzle.placed_words if w['direction'] == 'horizontal']
        vertical_clues = [w for w in self.puzzle.placed_words if w['direction'] == 'vertical']

        # Draw horizontal clues
        if horizontal_clues:
            subtitle = self.font_title.render("Waagerecht:", True, self.BLACK)
            self.screen.blit(subtitle, (clues_x, clues_y))
            clues_y += 25

            for word_info in sorted(horizontal_clues, key=lambda x: x['number']):
                clue_text = f"{word_info['number']}. {word_info['clue']}"
                # Word wrap for long clues
                words = clue_text.split(' ')
                lines = []
                current_line = []

                for word in words:
                    test_line = ' '.join(current_line + [word])
                    if self.font_clues.size(test_line)[0] < 380:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]

                if current_line:
                    lines.append(' '.join(current_line))

                for line in lines:
                    if clues_y < self.screen_height - 30:
                        clue_surface = self.font_clues.render(line, True, self.BLACK)
                        self.screen.blit(clue_surface, (clues_x, clues_y))
                        clues_y += 20

            clues_y += 15

        # Draw vertical clues
        if vertical_clues:
            subtitle = self.font_title.render("Senkrecht:", True, self.BLACK)
            self.screen.blit(subtitle, (clues_x, clues_y))
            clues_y += 25

            for word_info in sorted(vertical_clues, key=lambda x: x['number']):
                clue_text = f"{word_info['number']}. {word_info['clue']}"
                # Word wrap for long clues
                words = clue_text.split(' ')
                lines = []
                current_line = []

                for word in words:
                    test_line = ' '.join(current_line + [word])
                    if self.font_clues.size(test_line)[0] < 380:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]

                if current_line:
                    lines.append(' '.join(current_line))

                for line in lines:
                    if clues_y < self.screen_height - 30:
                        clue_surface = self.font_clues.render(line, True, self.BLACK)
                        self.screen.blit(clue_surface, (clues_x, clues_y))
                        clues_y += 20

    def handle_key_input(self, key, unicode_char):
        """
        Handles keyboard input for the selected cell with automatic advancement.
        """
        if self.selected_cell is None:
            return

        row, col = self.selected_cell

        if key == pygame.K_BACKSPACE:
            # Clear current cell and move to previous cell in word
            self.user_grid[row][col] = ''
            if self.selected_word:
                prev_cell = self.get_previous_cell_in_word(row, col, self.selected_word)
                if prev_cell:
                    self.selected_cell = prev_cell

        elif key == pygame.K_DELETE:
            # Just clear current cell, don't move
            self.user_grid[row][col] = ''

        elif key == pygame.K_SPACE:
            # Skip to next cell without entering anything
            if self.selected_word:
                next_cell = self.get_next_cell_in_word(row, col, self.selected_word)
                if next_cell:
                    self.selected_cell = next_cell

        elif key == pygame.K_TAB:
            # Switch between horizontal and vertical word at current position
            words_at_cell = self.get_word_at_cell(row, col)
            if len(words_at_cell) > 1:
                current_index = words_at_cell.index(self.selected_word) if self.selected_word in words_at_cell else -1
                next_index = (current_index + 1) % len(words_at_cell)
                self.selected_word = words_at_cell[next_index]
                self.selected_direction = self.selected_word['direction']

        elif key == pygame.K_LEFT:
            # Move left (only in horizontal words)
            if self.selected_word and self.selected_word['direction'] == 'horizontal':
                prev_cell = self.get_previous_cell_in_word(row, col, self.selected_word)
                if prev_cell:
                    self.selected_cell = prev_cell

        elif key == pygame.K_RIGHT:
            # Move right (only in horizontal words)
            if self.selected_word and self.selected_word['direction'] == 'horizontal':
                next_cell = self.get_next_cell_in_word(row, col, self.selected_word)
                if next_cell:
                    self.selected_cell = next_cell

        elif key == pygame.K_UP:
            # Move up (only in vertical words)
            if self.selected_word and self.selected_word['direction'] == 'vertical':
                prev_cell = self.get_previous_cell_in_word(row, col, self.selected_word)
                if prev_cell:
                    self.selected_cell = prev_cell

        elif key == pygame.K_DOWN:
            # Move down (only in vertical words)
            if self.selected_word and self.selected_word['direction'] == 'vertical':
                next_cell = self.get_next_cell_in_word(row, col, self.selected_word)
                if next_cell:
                    self.selected_cell = next_cell

        elif unicode_char and unicode_char.isalpha():
            # Enter letter and automatically move to next cell
            self.user_grid[row][col] = unicode_char.upper()

            # Automatically advance to next cell in the selected word
            if self.selected_word:
                next_cell = self.get_next_cell_in_word(row, col, self.selected_word)
                if next_cell:
                    self.selected_cell = next_cell

    def check_completion(self):
        """
        Checks if the puzzle is completed correctly.
        """
        for row in range(self.puzzle.height):
            for col in range(self.puzzle.width):
                if self.puzzle.grid[row][col] != '#':  # Playable cell
                    user_char = self.user_grid[row][col]
                    solution_char = self.puzzle.solution_grid[row][col]
                    if not user_char or user_char.upper() != solution_char:
                        return False
        return True

    def run(self):
        """
        Runs the main Pygame event loop.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        cell = self.get_cell_at_pos(event.pos)
                        if cell:
                            self.select_cell(cell[0], cell[1])

                elif event.type == pygame.KEYDOWN:
                    self.handle_key_input(event.key, event.unicode)

                    # Check for completion after each input
                    if self.check_completion():
                        print("Glückwunsch! Kreuzworträtsel gelöst!")

            # Draw everything
            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_clues()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


# --- Main execution block ---
if __name__ == "__main__":
    # Create and generate the crossword puzzle
    puzzle = CrosswordPuzzle(width=15, height=12)

    # Add words with their clues (German clues for German audience)
    puzzle.add_word("APPLE", "A red or green fruit")
    puzzle.add_word("RIVER", "A natural flowing watercourse")
    puzzle.add_word("MOUNTAIN", "A large natural elevation of the earth's surface")
    puzzle.add_word("CITY", "A large town")
    puzzle.add_word("SUN", "The star at the center of our solar system")
    puzzle.add_word("MOON", "Earth's natural satellite")
    puzzle.add_word("WATER", "Clear liquid we drink")
    puzzle.add_word("TREE", "Plant with a trunk and branches")
    puzzle.add_word("BIRD", "Animal that can fly")
    puzzle.add_word("HOUSE", "A building where people live")
    puzzle.add_word("SCHOOL", "Place where children learn")
    puzzle.add_word("TEACHER", "Person who gives lessons")
    puzzle.add_word("FISH", "Animal that lives in water")
    puzzle.add_word("DOG", "Common pet that barks")
    puzzle.add_word("MILK", "White liquid from cows")
    puzzle.add_word("BREAD", "Food made from flour")
    puzzle.add_word("CAR", "Vehicle with four wheels")
    puzzle.add_word("ROAD", "Path for cars to drive on")
    puzzle.add_word("CHAIR", "Something you sit on")
    puzzle.add_word("BOOK", "Set of written pages")
    puzzle.add_word("PRECIPITATION", "When the moisture in the air fell down to the ground")
    puzzle.add_word("ARCHIPELAGO", "A group or chain of islands.")
    puzzle.add_word("CATALYST", "A substance that speeds up a chemical reaction without being consumed.")
    puzzle.add_word("HORIZON", "The line at which the Earth’s surface and the sky appear to meet.")
    puzzle.add_word("PHOTOSYNTHESIS", "The process by which green plants use sunlight to make food.")
    puzzle.add_word("MOSAIC",
                    "A picture or pattern produced by arranging together small pieces of stone, tile, or glass.")
    puzzle.add_word("ORBIT", "The curved path of a celestial object around a star, planet, or moon.")
    puzzle.add_word("CARAVAN", "A group of people, especially traders or pilgrims, traveling together across a desert.")
    puzzle.add_word("TIMBERLINE", "The altitude above which trees cannot grow.")
    puzzle.add_word("DELTA", "A landform at the mouth of a river where it splits into several outlets.")
    puzzle.add_word("ISOTOPE", "Atoms of the same element with different numbers of neutrons.")
    puzzle.add_word("TSUNAMI", "A long high sea wave caused by an underwater earthquake or volcano.")
    puzzle.add_word("PENINSULA", "A piece of land almost surrounded by water or projecting into a body of water.")
    puzzle.add_word("EQUATOR", "An imaginary line around the Earth equally distant from the poles.")
    puzzle.add_word("FOSSIL", "The remains or impression of a prehistoric organism preserved in rock.")
    puzzle.add_word("OASIS", "A fertile spot in a desert where water is found.")
    puzzle.add_word("MONSOON", "A seasonal prevailing wind in the region of South and Southeast Asia.")
    puzzle.add_word("TUNDRA", "A vast, flat, treeless Arctic region where the subsoil is permanently frozen.")
    puzzle.add_word("CENSUS", "An official count or survey of a population.")

    puzzle.generate_puzzle()
    puzzle.display_puzzle()

    # Create and run the interactive GUI
    gui = CrosswordGUI(puzzle, cell_size=35)
    gui.run()