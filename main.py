import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Pad")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define button properties
button_width = 100
button_height = 100
margin = 10

# Define font
font = pygame.font.Font(None, 48)

# Predefined code and max length
correct_code = "1234"
max_length = 4

# Initial vertical offset for button pad
vertical_offset = button_height + margin


# Add submit button
submit_button = {'label': 'Submit', 'pos': (2 * button_width + 3 * margin, 3 * button_height + 4 * margin + vertical_offset)}
# Define button positions and labels
buttons = [
    {'label': '1', 'pos': (margin, margin + vertical_offset)},
    {'label': '2', 'pos': (button_width + 2 * margin, margin + vertical_offset)},
    {'label': '3', 'pos': (2 * button_width + 3 * margin, margin + vertical_offset)},
    {'label': '4', 'pos': (margin, button_height + 2 * margin + vertical_offset)},
    {'label': '5', 'pos': (button_width + 2 * margin, button_height + 2 * margin + vertical_offset)},
    {'label': '6', 'pos': (2 * button_width + 3 * margin, button_height + 2 * margin + vertical_offset)},
    {'label': '7', 'pos': (margin, 2 * button_height + 3 * margin + vertical_offset)},
    {'label': '8', 'pos': (button_width + 2 * margin, 2 * button_height + 3 * margin + vertical_offset)},
    {'label': '9', 'pos': (2 * button_width + 3 * margin, 2 * button_height + 3 * margin + vertical_offset)},
    {'label': '0', 'pos': (button_width + margin + margin, 3 * button_height + 4 * margin + vertical_offset)},
    {'label': 'Delete', 'pos': (margin, 3 * button_height + 4 * margin + vertical_offset)},
    submit_button
]

# Store clicked numbers
clicked_numbers = ""
unlocked = False
incorrect = False
incorrect_time = 0

def draw_button(screen, label, pos, color=GREY):
    rect = pygame.Rect(pos[0], pos[1], button_width, button_height)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text = font.render(label, True, BLACK)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    return rect

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in buttons:
                rect = pygame.Rect(button['pos'][0], button['pos'][1], button_width, button_height)
                if rect.collidepoint(mouse_pos):
                    if button['label'] == 'Delete':
                        clicked_numbers = clicked_numbers[:-1]  # Remove last character
                    elif len(clicked_numbers) < max_length:
                        clicked_numbers += button['label']
                    print(f"Button {button['label']} pressed")
            submit_rect = pygame.Rect(submit_button['pos'][0], submit_button['pos'][1], button_width, button_height)
            if submit_rect.collidepoint(mouse_pos):
                if clicked_numbers == correct_code:
                    unlocked = True
                else:
                    incorrect = True
                    incorrect_time = time.time()
                    clicked_numbers = ""  # Clear the entered code if incorrect
                print("Submit button pressed")
        elif event.type == pygame.KEYDOWN:
            if event.unicode in '0123456789' and len(clicked_numbers) < max_length:
                clicked_numbers += event.unicode
                print(f"Key {event.unicode} pressed")
            elif event.key == pygame.K_RETURN:  # Press Enter to submit
                if clicked_numbers == correct_code:
                    unlocked = True
                else:
                    incorrect = True
                    incorrect_time = time.time()
                    clicked_numbers = ""  # Clear the entered code if incorrect
            elif event.key == pygame.K_BACKSPACE:
                clicked_numbers = clicked_numbers[:-1]  # Remove last character

    if unlocked:
        unlocked_text = font.render("Unlocked", True, GREEN)
        screen.blit(unlocked_text, (WIDTH // 2 - unlocked_text.get_width() // 2, HEIGHT // 2))
    else:
        for button in buttons:
            draw_button(screen, button['label'], button['pos'])
        draw_button(screen, submit_button['label'], submit_button['pos'], color=RED)

        # Render the clicked numbers
        clicked_text = font.render(clicked_numbers, True, BLACK)
        screen.blit(clicked_text, (margin+button_width, margin*3))

        # Show "Incorrect" message for a few seconds if the code is wrong
        if incorrect:
            incorrect_text = font.render("Incorrect", True, RED)
            screen.blit(incorrect_text, (margin+button_width, button_height-(2*margin)))
            if time.time() - incorrect_time > 1:  # Show message for 2 seconds
                incorrect = False

    pygame.display.flip()

pygame.quit()
sys.exit()
