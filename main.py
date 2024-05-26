import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Pad")

# Define colors
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define button properties
button_width = 140
button_height = 140
margin = 10
middle_distance = WIDTH / 2 - button_width - button_width / 2

# Define fonts
font = pygame.font.Font(None, 48)
clicked_numbers_font_size = 72 
large_font = pygame.font.Font(None, clicked_numbers_font_size)

# Predefined code and max length
correct_code = "1234"
max_length = len(correct_code)

# Initial vertical offset for button pad
vertical_offset = button_height + margin

# Add submit button
submit_button = {'label': 'Submit', 'pos': (middle_distance + 2 * button_width + 2 * margin, 3 * button_height + 4 * margin + vertical_offset)}

# Define button positions and labels
buttons = [
    {'label': '1', 'pos': (middle_distance, margin + vertical_offset)},
    {'label': '2', 'pos': (middle_distance + button_width + margin, margin + vertical_offset)},
    {'label': '3', 'pos': (middle_distance + 2 * button_width + 2 * margin, margin + vertical_offset)},
    {'label': '4', 'pos': (middle_distance, button_height + 2*margin + vertical_offset)},
    {'label': '5', 'pos': (middle_distance + button_width + margin, button_height + 2 * margin + vertical_offset)},
    {'label': '6', 'pos': (middle_distance + 2 * button_width + 2 * margin, button_height + 2 * margin + vertical_offset)},
    {'label': '7', 'pos': (middle_distance, 2 * button_height + 3 * margin + vertical_offset)},
    {'label': '8', 'pos': (middle_distance + button_width + margin, 2 * button_height + 3 * margin + vertical_offset)},
    {'label': '9', 'pos': (middle_distance + 2 * button_width + 2 * margin, 2 * button_height + 3 * margin + vertical_offset)},
    {'label': '0', 'pos': (middle_distance + button_width + margin, 3 * button_height + 4 * margin + vertical_offset)},
    {'label': 'Delete', 'pos': (middle_distance, 3 * button_height + 4 * margin + vertical_offset)},
    submit_button
]

# Store clicked numbers
clicked_numbers = ""
unlocked = False
incorrect = False
incorrect_time = 0

def draw_button(screen, label, pos, color=GREY, text_color=WHITE):
    rect = pygame.Rect(pos[0], pos[1], button_width, button_height)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text = font.render(label, True, text_color)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    return rect

def draw_background(screen):
    screen.fill(BLACK)

# Main loop
running = True
while running:
    draw_background(screen)
    
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
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Press Enter to submit
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
        screen.blit(unlocked_text, (WIDTH / 2 - unlocked_text.get_width() / 2, HEIGHT / 2))
    else:
        for button in buttons:
            draw_button(screen, button['label'], button['pos'])
        draw_button(screen, submit_button['label'], submit_button['pos'], color=ORANGE)

        # Render the clicked numbers
        clicked_text = large_font.render(clicked_numbers if len(clicked_numbers) == max_length else clicked_numbers + "_"*(max_length-len(clicked_numbers)), True, ORANGE)
        screen.blit(clicked_text, (middle_distance + button_width+margin+button_width/2-(clicked_text.get_width()/2), margin * 8))

        # Show "Incorrect" message for a few seconds if the code is wrong
        if incorrect:
            incorrect_text = font.render("Incorrect", True, RED)
            screen.blit(incorrect_text, (middle_distance + button_width+margin+button_width/2-(incorrect_text.get_width()/2), incorrect_text.get_height() / 2))
            if time.time() - incorrect_time > 2:  # Show message for 2 seconds
                incorrect = False

    pygame.display.flip()

pygame.quit()
sys.exit()
