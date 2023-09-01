import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
CHARACTER_SIZE = 50
NUM_CHARACTERS = 50
SQUARE_SIZE = 7  # Adjust this value to control the size of the square arrangement

# Colors
WHITE = (255, 255, 255)

# Create a screen with hardware acceleration
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Yo-Kai Watch Wibble Wobble')

# Load character images with a transparent background
character_images = [pygame.image.load(f'wibwob{i}.png').convert_alpha() for i in range(1, 3)]
wallpaper = pygame.image.load('wallpaper.png').convert()

# Load the close button image and scale it to 64x64 pixels
close_button = pygame.image.load('close.png')
close_button = pygame.transform.scale(close_button, (64, 64))
close_button_rect = close_button.get_rect()
close_button_rect.topright = (SCREEN_WIDTH - 10, 10)  # Position the close button in the top-right corner

# Create a class for characters
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image_index):
        super().__init__()
        self.image = character_images[image_index]
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image_index = image_index  # Store the image index to identify characters
        self.dragging = False  # Indicates whether the character is being dragged

    def update(self):
        if self.dragging:
            # Move the character with the mouse
            self.rect.center = pygame.mouse.get_pos()

# Create a sprite group for characters
all_characters = pygame.sprite.Group()

# Calculate the number of characters per side of the square
characters_per_side = int(math.sqrt(NUM_CHARACTERS))

# Calculate the size of the gap between characters in the square
gap_size = (SCREEN_WIDTH - (characters_per_side * CHARACTER_SIZE)) // (characters_per_side + 1)

# Create characters in a square arrangement
for row in range(characters_per_side):
    for col in range(characters_per_side):
        x = (col + 1) * gap_size + col * CHARACTER_SIZE
        y = (row + 1) * gap_size + row * CHARACTER_SIZE
        image_index = random.randint(0, len(character_images) - 1)
        character = Character(x, y, image_index)
        all_characters.add(character)

# Load background music
pygame.mixer.music.load('music.mp3')

# Play background music in a loop
pygame.mixer.music.play(-1)  # -1 means to loop indefinitely

# Main game loop
clock = pygame.time.Clock()
dragged_character = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                x, y = event.pos
                clicked_characters = [character for character in all_characters.sprites() if character.rect.collidepoint(x, y)]
                if clicked_characters:
                    dragged_character = clicked_characters[0]
                    dragged_character.dragging = True

            # Check if the close button is clicked
            if close_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            if dragged_character is not None and dragged_character.dragging:
                # Move the dragged character with the mouse
                dragged_character.rect.center = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged_character is not None and dragged_character.dragging:
                # Stop dragging the character
                dragged_character.dragging = False
                for character in all_characters.sprites():
                    if character != dragged_character and character.image_index == dragged_character.image_index:
                        if character.rect.colliderect(dragged_character.rect):
                            # Check if the dropped character overlaps with a character of the same image
                            all_characters.remove(character)
                            all_characters.remove(dragged_character)
                dragged_character = None

    screen.blit(wallpaper, (0, 0))

    all_characters.draw(screen)

    # Draw the close button
    screen.blit(close_button, close_button_rect)

    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS
