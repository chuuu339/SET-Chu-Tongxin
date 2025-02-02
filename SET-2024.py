import pygame
import sys
import itertools
from random import shuffle
import time

# Initialize Pygame
pygame.init()

# Constants for window size and colors
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 750  # Adjusted height to fit everything
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SET Game")

# Custom Colors
COLOR1 = (167, 118, 124)  # #B43332 with 30% alpha for transparency
COLOR2 = (93, 123, 111)  # #174D86 with 30% alpha
COLOR3 = (249, 210, 145, 77)  # #F9D291 with 30% alpha
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHADOW_COLOR = (200, 200, 200)
SELECTED_COLOR = (230, 230, 250)  # Light contrasting color for selection

# Card dimensions and spacing
card_width, card_height = 150, 190  # Adjusted card size for symbols
card_spacing = 40  # Increased spacing for better layout
start_x = (WINDOW_WIDTH - (card_width * 3 + card_spacing * 2)) // 2  # Center horizontally
start_y = 80  # Adjusted start point for better layout
corner_radius = 20
shadow_offset = 5

# Create a card class
class Card:
    def __init__(self, number, symbol, color, shading):
        self.number = number
        self.symbol = symbol
        self.color = color
        self.shading = shading
        self.selected = False

    def __repr__(self):
        return f"{self.number} {self.color} {self.shading} {self.symbol}"

# Constants for card arrangement
rows, cols = 3, 4  # Three rows, four columns

# Calculate starting positions for centering cards
start_x = (WINDOW_WIDTH - (card_width * cols + card_spacing * (cols - 1))) // 2
start_y = (WINDOW_HEIGHT - (card_height * rows + card_spacing * (rows - 1))) // 2

# Function to generate a deck of cards
def generate_deck():
    numbers = [1, 2, 3]
    symbols = ['oval', 'triangle', 'diamond']
    colors = [COLOR1, COLOR2, COLOR3]
    shadings = ['solid', 'transparent', 'open']
    deck = [Card(number, symbol, color, shading) for number in numbers for symbol in symbols for color in colors for shading in shadings]
    shuffle(deck)
    return deck

# Check if three cards form a SET
def is_set(card1, card2, card3):
    conditions = [
        (card1.number == card2.number == card3.number or len({card1.number, card2.number, card3.number}) == 3),
        (card1.symbol == card2.symbol == card3.symbol or len({card1.symbol, card2.symbol, card3.symbol}) == 3),
        (card1.color == card2.color == card3.color or len({card1.color, card2.color, card3.color}) == 3),
        (card1.shading == card2.shading == card3.shading or len({card1.shading, card2.shading, card3.shading}) == 3),
    ]
    return all(conditions)

# Find all possible sets in the given cards
def find_all_sets(cards):
    all_sets = []
    for card1, card2, card3 in itertools.combinations(cards, 3):
        if is_set(card1, card2, card3):
            all_sets.append((card1, card2, card3))
    return all_sets

# Find one set in the given cards
def find_one_set(cards):
    for card1, card2, card3 in itertools.combinations(cards, 3):
        if is_set(card1, card2, card3):
            return card1, card2, card3
    return None

# Draw a single card on the screen
def draw_card(card, x, y):
    # Draw shadow for 3D effect
    pygame.draw.rect(screen, SHADOW_COLOR, (x + shadow_offset, y + shadow_offset, card_width, card_height), border_radius=corner_radius)
    # Draw selected background if selected
    card_color = SELECTED_COLOR if card.selected else WHITE
    pygame.draw.rect(screen, WHITE, (x, y, card_width, card_height), border_radius=corner_radius)
    pygame.draw.rect(screen, BLACK, (x, y, card_width, card_height), 2, border_radius=corner_radius)
    if card.selected:
        pygame.draw.rect(screen, SELECTED_COLOR, (x, y, card_width, card_height), 0, border_radius=corner_radius)
    draw_symbols(card, x, y)

# Function to draw symbols on a card
def draw_symbols(card, x, y):
    symbol_size = min(card_width, card_height) - 100  # Ensure symbols do not overlap or go outside the card

    positions = []
    if card.number == 1:
        positions = [(x + card_width // 2, y + card_height // 2)]
    elif card.number == 2:
        positions = [
            (x + card_width // 2, y + card_height // 3),
            (x + card_width // 2, y + 2 * card_height // 3)
        ]
    elif card.number == 3:
        positions = [
            (x + card_width // 2, y + card_height // 4),
            (x + card_width // 4, y + 3 * card_height // 4),
            (x + 3 * card_width // 4, y + 3 * card_height // 4)
        ]

    for pos in positions:
        draw_symbol(screen, card.symbol, card.color, card.shading, pos, symbol_size, symbol_size)

# Function to draw a specific symbol
def draw_symbol(surface, symbol, color, shading, position, width, height):
    x, y = position
    stripe_width = 2  # Stripe width
    stripe_spacing = 6  # stripe spacing

    if symbol == 'oval':
        rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        if shading == 'solid':  # solid colour filling
            pygame.draw.ellipse(surface, color[:3], rect)
        elif shading == 'open':  # No fill, border only
            pygame.draw.ellipse(surface, color[:3], rect, 2)
        elif shading == 'transparent':  # Stripe Fill
            # Building transparent surfaces to draw stripes
            s = pygame.Surface((width, height), pygame.SRCALPHA)
            for i in range(-height, height, stripe_spacing):
                pygame.draw.line(s, color[:3], (i, 0), (i + height, height), stripe_width)
            mask_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.ellipse(mask_surface, (255, 255, 255, 255), (0, 0, width, height))
            s.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            surface.blit(s, rect.topleft)
            pygame.draw.ellipse(surface, color[:3], rect, 2)  # Drawing Borders
           

    elif symbol == 'triangle':
        points = [
            (x, y - height // 2),
            (x - width // 2, y + height // 2),
            (x + width // 2, y + height // 2)
        ]
        if shading == 'solid':  # solid colour filling
            pygame.draw.polygon(surface, color[:3], points)
        elif shading == 'open':  # No fill, border only
            pygame.draw.polygon(surface, color[:3], points, 2)
        elif shading == 'transparent':  # Stripe Fill
            # Creating a transparent surface to draw stripes
            s = pygame.Surface((width, height), pygame.SRCALPHA)
            for i in range(-height, height, stripe_spacing):
                pygame.draw.line(s, color[:3], (0, i), (width, i + width), stripe_width)
           # Create a mask to limit the stripe range
            mask_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.polygon(mask_surface, (255, 255, 255, 255), [(p[0] - x + width // 2, p[1] - y + height // 2) for p in points])
            s.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            surface.blit(s, (x - width // 2, y - height // 2)) 
    

    elif symbol == 'diamond':
        points = [
            (x, y - height // 2),
            (x + width // 2, y),
            (x, y + height // 2),
            (x - width // 2, y)
        ]
        if shading == 'solid':  # solid colour filling
            pygame.draw.polygon(surface, color[:3], points)
        elif shading == 'open':  # No fill, border only
            pygame.draw.polygon(surface, color[:3], points, 2)
        elif shading == 'transparent':  # Stripe Fill
            # Creating a transparent surface to draw stripes
            s = pygame.Surface((width, height), pygame.SRCALPHA)
            for i in range(-height, height, stripe_spacing):
                pygame.draw.line(s, color[:3], (0, i), (width, i + width), stripe_width)
            # Create a mask to limit the stripe range
            mask_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.polygon(mask_surface, (255, 255, 255, 255), [(p[0] - x + width // 2, p[1] - y + height // 2) for p in points])
            s.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            surface.blit(s, (x - width // 2, y - height // 2))
            pygame.draw.polygon(surface, color[:3], points, 2)  # Drawing Borders

# Draw scoreboard and timer
def draw_scoreboard(player_score, computer_score, remaining_time):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Player: {player_score}  Computer: {computer_score}", True, BLACK)
    timer_text = font.render(f"Time Left: {remaining_time}s", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(timer_text, (WINDOW_WIDTH - 200, 20))

# Display a temporary message
def display_message(text):
    font = pygame.font.SysFont(None, 40)
    message = font.render(text, True, BLACK)
    screen.blit(message, (WINDOW_WIDTH // 2 - message.get_width() // 2, 20))
    pygame.display.flip()
    pygame.time.wait(1000)

def display_time_menu():
    font = pygame.font.SysFont('Arial', 48, bold=True)
    title_font = pygame.font.SysFont('Arial', 60)
    times = [30, 60, 90]
    text_surfaces = [font.render(f"{t} seconds", True, BLACK) for t in times]
    title_surface = title_font.render("Please select the game difficulty", True, BLACK)
    screen.fill((245, 245, 245))
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 50))

    buttons = []
    for i, txt in enumerate(text_surfaces):
        text_width, text_height = txt.get_size()
        button_rect = pygame.Rect(WINDOW_WIDTH // 2 - text_width // 2 - 10, 150 + i * 100, text_width + 20, text_height + 20)
        buttons.append((button_rect, times[i]))

    while True:
        for button_rect, _ in buttons:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (210, 210, 230), button_rect)  # Button hover color
            else:
                pygame.draw.rect(screen, (230, 230, 250), button_rect)  # Button normal color
            pygame.draw.rect(screen, (100, 100, 120), button_rect, 3)  # Button border

        for i, txt in enumerate(text_surfaces):
            screen.blit(txt, (buttons[i][0].x + 10, buttons[i][0].y + 10))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, time in buttons:
                    if button_rect.collidepoint(event.pos):
                        return time  # Return the selected time immediately
                    
import pygame
import sys
import itertools
from random import shuffle
import time

# Initialize Pygame
pygame.init()

# Constants for window size and colors
# (Ensure all initial definitions and constants are above this code)
...

def draw_button(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action:
            action() 
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

# Card dimensions and spacing, and the rest of your setup
...
import pygame
import sys

# Initialize Pygame
pygame.init()

# Window and color settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 750
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SET Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (93, 123, 111)  # Aesthetic green
BUTTON_HOVER_COLOR = (167, 118, 124)  # Aesthetic red

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def draw_button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()  # Action is a function to be called when the button is clicked
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


# Main function call and the rest of your game logic follows


# Main game logic

def main():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Welcome to SET Game", largeText)
        TextRect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 3))
        screen.blit(TextSurf, TextRect)

        button_width = 250
        button_height = 50
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_y = (WINDOW_HEIGHT - button_height) // 2

        draw_button("Start Game", button_x, button_y, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, game_loop)

        pygame.display.update()
        pygame.time.Clock().tick(15)

def main():
    # Display the time selection menu and get the selected time
    time_limit = display_time_menu()  #  Calling the time selection menu

    # Initialization of play variables
    deck = generate_deck()
    table_cards = deck[:12]
    selected_cards = []
    player_score, computer_score = 0, 0
    timer = pygame.time.Clock()
    elapsed_time = 0

    # The main loop of the game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a card is clicked
                mouse_x, mouse_y = event.pos
                for index, card in enumerate(table_cards):
                    card_x = start_x + (card_width + card_spacing) * (index % cols)
                    card_y = start_y + (card_height + card_spacing) * (index // cols)
                    if card_x < mouse_x < card_x + card_width and card_y < mouse_y < card_y + card_height:
                        card.selected = not card.selected
                        if card.selected:
                            selected_cards.append(card)
                        else:
                            selected_cards.remove(card)

                        # Check if three cards are selected
                        if len(selected_cards) == 3:
                            if is_set(selected_cards[0], selected_cards[1], selected_cards[2]):
                                player_score += 1
                                display_message("You Win!")
                                for card in selected_cards:
                                    table_cards.remove(card)
                                table_cards += deck[:3]
                                deck = deck[3:]
                                selected_cards.clear()
                                elapsed_time = 0  # Reset timer after finding a set
                            else:
                                display_message("Try again!")
                                for card in selected_cards:
                                    card.selected = False
                                selected_cards.clear()

        # Check for no SETs immediately
        if not find_one_set(table_cards):
            table_cards = table_cards[3:] + deck[:3]
            deck = deck[3:]
            elapsed_time = 0

        # Check time limit
        elapsed_time += timer.tick(90) / 1000  # Convert milliseconds to seconds
        remaining_time = max(0, time_limit - int(elapsed_time))
        if elapsed_time >= time_limit: 
            screen.fill(WHITE)
            display_message("Time's up! Computer's turn.")
            computer_set = find_one_set(table_cards)
            if computer_set:
                computer_score += 1
                for card in computer_set:
                    table_cards.remove(card)
                table_cards += deck[:3]
                deck = deck[3:]
            else:
                table_cards = table_cards[3:] + deck[:3]
                deck = deck[3:]
            elapsed_time = 0

        # Draw the game
        screen.fill(WHITE)
        draw_scoreboard(player_score, computer_score, remaining_time)
        for index, card in enumerate(table_cards):
            card_x = start_x + (card_width + card_spacing) * (index % cols)
            card_y = start_y + (card_height + card_spacing) * (index // cols)
            draw_card(card, card_x, card_y)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Start the game
main()
