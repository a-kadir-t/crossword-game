import pygame
import random


# --- Your existing CrosswordPuzzle class ---
class CrosswordPuzzle:
    """
    A class to represent and generate a crossword puzzle.

    Attributes:
        width (int): The width of the crossword grid.
        height (int): The height of the crossword grid.
        grid (list of list of str): The 2D list representing the crossword grid.
                                     Empty cells are represented by an empty string or '#'.
        words (list of str): A list of words to be placed in the puzzle.
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
        self.words = []
        self.placed_words = []

    def add_word(self, word):
        """
        Adds a word to the list of words to be placed in the puzzle.
        Also performs an initial check to ensure the word can fit on the grid at all.
        """
        word_upper = word.upper()
        # A word must be able to fit either horizontally or vertically
        if len(word_upper) <= self.width or len(word_upper) <= self.height:
            self.words.append(word_upper)
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
            # Uncomment the line below for detailed debugging of why words are not placed.
            # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y}, {start_x}) - Negative start coordinates.")
            return False

        if direction == 'horizontal':
            # 1. Out of bounds check (end of word)
            if start_x + word_length > self.width:
                # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y}, {start_x}) - Out of bounds horizontally.")
                return False

            # 2. Check cells along the word's path and surrounding perpendicular cells
            for i in range(word_length):
                x = start_x + i
                y = start_y

                # Ensure coordinates are within grid bounds before accessing (redundant with initial checks but safe)
                if not (0 <= x < self.width and 0 <= y < self.height):
                    # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Cell out of grid bounds during iteration.")
                    return False

                current_grid_char = self.grid[y][x]

                # If the cell is occupied by an existing letter
                if current_grid_char != '#':
                    # A. Check for direct conflict: If existing letter doesn't match new word's letter
                    if current_grid_char != word[i]:
                        # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Character mismatch ('{current_grid_char}' != '{word[i]}').")
                        return False
                    # B. If it matches, it's a potential intersection point.
                    intersection_count += 1
                else:  # The cell is currently empty ('#')
                    # C. If the cell is empty, ensure its perpendicular neighbors are also empty.
                    # This prevents words from being placed immediately adjacent (parallel) to others.
                    # Check cell above
                    if y > 0 and self.grid[y - 1][x] != '#':
                        # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Conflict with cell above (perpendicular touch).")
                        return False
                    # Check cell below
                    if y < self.height - 1 and self.grid[y + 1][x] != '#':
                        # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Conflict with cell below (perpendicular touch).")
                        return False

            # 3. Check horizontal boundaries (cells immediately before and after the word)
            # These cells must be empty to prevent "extending" existing horizontal words.
            if start_x > 0 and self.grid[start_y][start_x - 1] != '#':
                # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y}, {start_x-1}) - Conflict with cell before word.")
                return False
            if start_x + word_length < self.width and self.grid[start_y][start_x + word_length] != '#':
                # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y}, {start_x+word_length}) - Conflict with cell after word.")
                return False

        elif direction == 'vertical':
            # 1. Out of bounds check (end of word)
            if start_y + word_length > self.height:
                # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y}, {start_x}) - Out of bounds vertically.")
                return False

            # 2. Check cells along the word's path and surrounding perpendicular cells
            for i in range(word_length):
                x = start_x
                y = start_y + i

                # Ensure coordinates are within grid bounds before accessing (redundant but safe)
                if not (0 <= x < self.width and 0 <= y < self.height):
                    # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Cell out of grid bounds during iteration.")
                    return False

                current_grid_char = self.grid[y][x]

                # If the cell is occupied by an existing letter
                if current_grid_char != '#':
                    # A. Check for direct conflict: If existing letter doesn't match new word's letter
                    if current_grid_char != word[i]:
                        # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Character mismatch ('{current_grid_char}' != '{word[i]}').")
                        return False
                    # B. If it matches, it's a potential intersection point.
                    intersection_count += 1
                else:  # The cell is currently empty ('#')
                    # C. If the cell is empty, ensure its perpendicular neighbors are also empty.
                    # Check cell to the left
                    if x > 0 and self.grid[y][x - 1] != '#':
                        # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Conflict with cell left (perpendicular touch).")
                        return False
                    # Check cell to the right
                    if x < self.width - 1 and self.grid[y][x + 1] != '#':
                        # print(f"DEBUG: Rejected '{word}' ({direction}) at ({y}, {x}) - Conflict with cell right (perpendicular touch).")
                        return False

            # 3. Check vertical boundaries (cells immediately before and after the word)
            # These cells must be empty to prevent "extending" existing vertical words.
            if start_y > 0 and self.grid[start_y - 1][start_x] != '#':
                # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y-1}, {start_x}) - Conflict with cell before word.")
                return False
            if start_y + word_length < self.height and self.grid[start_y + word_length][start_x] != '#':
                # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y+word_length}, {start_x}) - Conflict with cell after word.")
                return False

        # For a word to be placed, it must either be the first word (no intersections yet)
        # or it must have at least one valid intersection with an existing word.
        # This helps build a connected puzzle.
        if not self.placed_words and intersection_count == 0:  # First word can be placed anywhere
            return True
        elif self.placed_words and intersection_count == 0:  # Subsequent words MUST intersect
            # print(f"DEBUG: Rejected '{word}' ({direction}) at ({start_y}, {start_x}) - No intersection found for non-first word.")
            return False  # If there are already words, and this one doesn't intersect, it's invalid.

        return True  # If all checks pass and there are valid intersections (if not first word)

    def _place_word(self, word, start_x, start_y, direction):
        """
        Places a word onto the grid at the specified position and direction.
        Assumes _can_place_word has already verified it's possible.
        """
        word_length = len(word)
        if direction == 'horizontal':
            for i in range(word_length):
                self.grid[start_y][start_x + i] = word[i]
        elif direction == 'vertical':
            for i in range(word_length):
                self.grid[start_y + i][start_x] = word[i]

        self.placed_words.append({
            'word': word,
            'start_x': start_x,
            'start_y': start_y,
            'direction': direction
        })

    def generate_puzzle(self):
        """
        Attempts to generate the crossword puzzle by placing words on the grid.
        This is a simple greedy algorithm that tries to place words randomly.
        A more sophisticated algorithm would involve backtracking and scoring.
        """
        # Sort words by length in descending order to place longer words first
        self.words.sort(key=len, reverse=True)

        for word in self.words:
            placed = False

            # Store valid directions for the current word
            possible_directions = []
            if len(word) <= self.width:
                possible_directions.append('horizontal')
            if len(word) <= self.height:
                possible_directions.append('vertical')

            if not possible_directions:
                print(f"Word '{word}' is too long to fit horizontally or vertically. Skipping.")
                continue  # Skip this word if it can't fit in any direction

            # If no words are placed yet, try random positions for the first word.
            if not self.placed_words:
                # Greatly increased tries for first word to ensure placement in a reasonable spot
                for _ in range(self.width * self.height * 50):
                    direction = random.choice(possible_directions)

                    if direction == 'horizontal':
                        max_x = self.width - len(word)
                        if max_x < 0: continue  # Should not happen due to prior check, but defensive
                        start_x = random.randint(0, max_x)
                        start_y = random.randint(0, self.height - 1)
                    else:  # vertical
                        max_y = self.height - len(word)
                        if max_y < 0: continue  # Defensive check
                        start_x = random.randint(0, self.width - 1)
                        start_y = random.randint(0, max_y)

                    if self._can_place_word(word, start_x, start_y, direction):
                        self._place_word(word, start_x, start_y, direction)
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

                                    # Ensure proposed coordinates are valid before checking can_place_word
                                    if potential_start_x >= 0 and potential_start_y >= 0:
                                        if self._can_place_word(word, potential_start_x, potential_start_y, 'vertical'):
                                            possible_placements.append(
                                                (word, potential_start_x, potential_start_y, 'vertical'))
                                elif p_word['direction'] == 'vertical' and 'horizontal' in possible_directions:
                                    potential_start_x = p_word['start_x'] - char_idx_new
                                    potential_start_y = p_word['start_y'] + char_idx_old

                                    # Ensure proposed coordinates are valid before checking can_place_word
                                    if potential_start_x >= 0 and potential_start_y >= 0:
                                        if self._can_place_word(word, potential_start_x, potential_start_y,
                                                                'horizontal'):
                                            possible_placements.append(
                                                (word, potential_start_x, potential_start_y, 'horizontal'))

                random.shuffle(possible_placements)  # Shuffle to add randomness to placement
                for placement_info in possible_placements:
                    word_to_place, sx, sy, direct = placement_info
                    # Re-check can_place_word because the grid state might have changed or other words placed
                    if self._can_place_word(word_to_place, sx, sy, direct):
                        self._place_word(word_to_place, sx, sy, direct)
                        placed = True
                        break

                # If no ideal intersection placement found, fall back to random placement attempts
                if not placed:
                    # Greatly increased tries for fallback random placement
                    for _ in range(self.width * self.height * 50):
                        direction = random.choice(possible_directions)  # Only choose valid directions

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
                            self._place_word(word, start_x, start_y, direction)
                            placed = True
                            break

            if not placed:
                print(f"Could not place word: {word}")

    def display_puzzle(self):
        """
        Prints the current state of the crossword grid to the console.
        (This method is mostly for debugging, as Pygame will handle display)
        """
        print("\nCrossword Puzzle (Console View - for debugging):")
        for row in self.grid:
            print(" ".join(cell if cell != '#' else ' ' for cell in row))

        print("\nPlaced Words (and their starting positions):")
        if not self.placed_words:
            print("No words were successfully placed in the puzzle.")
        for p_word in self.placed_words:
            print(f"- {p_word['word']} ({p_word['direction']}): "
                  f"Start Row {p_word['start_y']}, Col {p_word['start_x']}")


# --- Pygame GUI Implementation ---

class CrosswordGUI:
    """
    A Pygame-based GUI for displaying the crossword puzzle.
    """

    def __init__(self, puzzle_instance, cell_size=40, margin=20):
        """
        Initializes the Pygame GUI.

        Args:
            puzzle_instance (CrosswordPuzzle): An instance of the generated crossword puzzle.
            cell_size (int): The size (width and height) of each square cell in pixels.
            margin (int): Margin around the puzzle grid in pixels.
        """
        pygame.init()

        self.puzzle = puzzle_instance
        self.cell_size = cell_size
        self.margin = margin

        # Calculate screen dimensions based on puzzle size and cell size
        self.screen_width = self.puzzle.width * self.cell_size + 2 * self.margin
        self.screen_height = self.puzzle.height * self.cell_size + 2 * self.margin + 50  # Extra space for controls/info later

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Crossword Puzzle")

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRID_COLOR = (150, 150, 150)  # Light gray for grid lines
        self.LETTER_COLOR = (50, 50, 50)  # Dark gray for letters
        self.BACKGROUND_COLOR = (240, 240, 240)  # Off-white background

        # Define font for letters
        self.font = pygame.font.Font(None, int(self.cell_size * 0.7))  # Font size based on cell size

    def draw_grid(self):
        """
        Draws the crossword grid, including cells and letters.
        """
        # Fill the background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Iterate through the grid to draw cells and letters
        for row_idx in range(self.puzzle.height):
            for col_idx in range(self.puzzle.width):
                x = self.margin + col_idx * self.cell_size
                y = self.margin + row_idx * self.cell_size

                cell_value = self.puzzle.grid[row_idx][col_idx]

                # Draw cell background
                if cell_value == '#':  # Empty/blackout cell
                    pygame.draw.rect(self.screen, self.BLACK, (x, y, self.cell_size, self.cell_size))
                else:  # Playable cell
                    pygame.draw.rect(self.screen, self.WHITE, (x, y, self.cell_size, self.cell_size))
                    # Draw letter if present
                    if cell_value != ' ':  # Not an intentionally blank space, but a letter
                        text_surface = self.font.render(cell_value, True, self.LETTER_COLOR)
                        text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        self.screen.blit(text_surface, text_rect)

                # Draw cell borders
                pygame.draw.rect(self.screen, self.GRID_COLOR, (x, y, self.cell_size, self.cell_size), 1)

    def run(self):
        """
        Runs the main Pygame event loop.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid()  # Redraw the grid in each frame
            pygame.display.flip()  # Update the full display Surface to the screen

        pygame.quit()  # Uninitialize Pygame modules


# --- Main execution block ---
if __name__ == "__main__":
    # Create and generate the crossword puzzle first
    puzzle = CrosswordPuzzle(width=20, height=15)  # You can adjust dimensions here

    # Add some words - feel free to add or remove words to test different layouts
    puzzle.add_word("PYTHON")
    puzzle.add_word("PROGRAMMING")
    puzzle.add_word("CROSSWORD")
    puzzle.add_word("DEVELOPER")
    puzzle.add_word("COMPUTER")
    puzzle.add_word("ALGORITHM")
    puzzle.add_word("LANGUAGE")
    puzzle.add_word("CODE")
    puzzle.add_word("ANACONDA")
    puzzle.add_word("KEYBOARD")
    puzzle.add_word("MOUSE")
    puzzle.add_word("MONITOR")
    puzzle.add_word("NETWORK")
    puzzle.add_word("INTERNET")
    puzzle.add_word("SCIENCE")
    puzzle.add_word("ENGINEERING")
    puzzle.add_word("DATA")
    puzzle.add_word("CLOUD")
    puzzle.add_word("SOFTWARE")  # Added a new word
    # puzzle.add_word("ARTIFICIALINTELLIGENCE") # This word is likely too long for current settings

    puzzle.generate_puzzle()
    puzzle.display_puzzle()  # Keep this for console debugging if needed

    # Create and run the Pygame GUI
    gui = CrosswordGUI(puzzle, cell_size=30)  # Adjust cell_size for larger/smaller squares
    gui.run()
