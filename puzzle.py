import random


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

        # --- IMPORTANT NEW CHECKS: Ensure start coordinates are not negative ---
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

                current_grid_char = self.grid[y][x]

                # If the cell is occupied by an existing letter
                if current_grid_char != '#':
                    # A. Check for direct conflict: If existing letter doesn't match new word's letter
                    if current_grid_char != word[i]:
                        return False
                    # B. If it matches, it's a potential intersection point.
                    # We increment the count.
                    intersection_count += 1
                else:  # The cell is currently empty ('#')
                    # C. If the cell is empty, ensure its perpendicular neighbors are also empty.
                    # This prevents words from being placed immediately adjacent (parallel) to others.
                    if y > 0 and self.grid[y - 1][x] != '#':  # Cell above is occupied
                        return False
                    if y < self.height - 1 and self.grid[y + 1][x] != '#':  # Cell below is occupied
                        return False

            # 3. Check horizontal boundaries (cells immediately before and after the word)
            # These cells must be empty to prevent "extending" existing horizontal words.
            if start_x > 0 and self.grid[start_y][start_x - 1] != '#':
                return False
            if start_x + word_length < self.width and self.grid[start_y][start_x + word_length] != '#':
                return False

        elif direction == 'vertical':
            # 1. Out of bounds check (end of word)
            if start_y + word_length > self.height:
                return False

            # 2. Check cells along the word's path and surrounding perpendicular cells
            for i in range(word_length):
                x = start_x
                y = start_y + i

                current_grid_char = self.grid[y][x]

                # If the cell is occupied by an existing letter
                if current_grid_char != '#':
                    # A. Check for direct conflict: If existing letter doesn't match new word's letter
                    if current_grid_char != word[i]:
                        return False
                    # B. If it matches, it's a potential intersection point.
                    intersection_count += 1
                else:  # The cell is currently empty ('#')
                    # C. If the cell is empty, ensure its perpendicular neighbors are also empty.
                    if x > 0 and self.grid[y][x - 1] != '#':  # Cell to the left is occupied
                        return False
                    if x < self.width - 1 and self.grid[y][x + 1] != '#':  # Cell to the right is occupied
                        return False

            # 3. Check vertical boundaries (cells immediately before and after the word)
            # These cells must be empty to prevent "extending" existing vertical words.
            if start_y > 0 and self.grid[start_y - 1][start_x] != '#':
                return False
            if start_y + word_length < self.height and self.grid[start_y + word_length][start_x] != '#':
                return False

        # For a word to be placed, it must either be the first word (no intersections yet)
        # or it must have at least one valid intersection with an existing word.
        # This helps build a connected puzzle.
        if not self.placed_words and intersection_count == 0:  # First word can be placed anywhere
            return True
        elif self.placed_words and intersection_count == 0:  # Subsequent words MUST intersect
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
                for _ in range(self.width * self.height):  # Fewer tries for the first word
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
                # Iterate through existing placed words and try to connect.
                possible_placements = []
                for p_word in self.placed_words:
                    for char_idx_new, char_new in enumerate(word):
                        for char_idx_old, char_old in enumerate(p_word['word']):
                            if char_new == char_old:  # Found a potential intersection
                                # Calculate potential start_x, start_y, and direction for the new word
                                if p_word['direction'] == 'horizontal' and 'vertical' in possible_directions:
                                    # New word will be vertical, intersecting horizontally placed word
                                    potential_start_x = p_word['start_x'] + char_idx_old
                                    potential_start_y = p_word['start_y'] - char_idx_new

                                    if self._can_place_word(word, potential_start_x, potential_start_y, 'vertical'):
                                        possible_placements.append(
                                            (word, potential_start_x, potential_start_y, 'vertical'))
                                elif p_word['direction'] == 'vertical' and 'horizontal' in possible_directions:
                                    # New word will be horizontal, intersecting vertically placed word
                                    potential_start_x = p_word['start_x'] - char_idx_new
                                    potential_start_y = p_word['start_y'] + char_idx_old

                                    if self._can_place_word(word, potential_start_x, potential_start_y, 'horizontal'):
                                        possible_placements.append(
                                            (word, potential_start_x, potential_start_y, 'horizontal'))

                random.shuffle(possible_placements)  # Shuffle to add randomness to placement
                for placement_info in possible_placements:
                    word_to_place, sx, sy, direct = placement_info
                    # Re-check can_place_word because the grid state might have changed during random.shuffle
                    if self._can_place_word(word_to_place, sx, sy, direct):
                        self._place_word(word_to_place, sx, sy, direct)
                        placed = True
                        break

                # If no ideal intersection placement found, fall back to random placement attempts
                # This ensures words that don't easily intersect still have a chance to be placed,
                # provided they can fit.
                if not placed:
                    for _ in range(self.width * self.height * 2):  # Heuristic: try many times
                        direction = random.choice(possible_directions)  # Only choose valid directions

                        if direction == 'horizontal':
                            max_x = self.width - len(word)
                            # This check should ideally prevent the negative case, but good to be explicit
                            if max_x < 0: continue
                            start_x = random.randint(0, max_x)
                            start_y = random.randint(0, self.height - 1)
                        else:  # vertical
                            max_y = self.height - len(word)
                            # This check should ideally prevent the negative case, but good to be explicit
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
        """
        print("\nCrossword Puzzle:")
        for row in self.grid:
            print(" ".join(cell if cell != '#' else ' ' for cell in row))  # Display '#' as space

        print("\nPlaced Words (and their starting positions):")
        if not self.placed_words:
            print("No words were successfully placed in the puzzle.")
        for p_word in self.placed_words:
            print(f"- {p_word['word']} ({p_word['direction']}): "
                  f"Start Row {p_word['start_y']}, Col {p_word['start_x']}")


# --- Example Usage ---
if __name__ == "__main__":
    # Create a crossword puzzle instance
    puzzle = CrosswordPuzzle(width=20, height=15)  # Example size

    # Add some words
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
    puzzle.add_word("ARTIFICIALINTELLIGENCE")  # This word is longer than 20, so it will now be skipped

    # Generate the puzzle
    puzzle.generate_puzzle()

    # Display the puzzle
    puzzle.display_puzzle()

