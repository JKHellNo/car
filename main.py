import pygame
import sys
from pygame import mixer
import math

# Initialize pygame
pygame.init()
mixer.init()

# Set up the display
screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height+100))
pygame.display.set_caption("Car Selection Menu")

# Load text and font
font = pygame.font.Font(None, 74)
player_text = font.render("Select A Car", True, (0, 255, 255))

# Load music and sounds
pygame.mixer.music.load('car_music.mp3')
pygame.mixer.music.set_volume(0.005)
pygame.mixer.music.play(-1, 0.0, 5000)

# Load the image containing the 8 cars
car_image = pygame.image.load('imgs/cars.png').convert_alpha()
start_button_image = pygame.image.load('imgs/start_btn.png').convert_alpha()
button_width, button_height = 100, 50
start_button_image= pygame.transform.scale(start_button_image, (button_width, button_height))
menu_background=pygame.image.load('imgs/menu_background.png').convert_alpha()
menu_background=pygame.transform.scale(menu_background, (screen_width, screen_height+100))

# Define the number of rows and columns of cars in the image
rows = 2
cols = 4

# Get the size of each car based on the image dimensions
image_width, image_height = car_image.get_size()
car_width = image_width // cols
car_height = image_height // rows
spacing_x= 50
grid_width=car_width+spacing_x
car_screen_width, car_screen_height = (screen_width-(cols * (grid_width))-spacing_x)//2+spacing_x, (screen_height-((rows-1) * car_height))//2

# Create a list to store the subsurfaces of each car
car_subsurfaces = []

# Loop through the rows and columns to extract each car
for row in range(rows):
    for col in range(cols):
        # Calculate the position and create the subsurface for each car
        x = col * car_width
        y = row * car_height
        car_subsurface = car_image.subsurface((x, y, car_width, car_height))
        car_subsurfaces.append(car_subsurface)

# Main game loop
action = False
selected_index = None
running = True
while running and not action:   #running and action false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on a car
            mouse_x, mouse_y = event.pos
            # Check if the click is within the grid of cars
            if 0 <= (mouse_x-car_screen_width) < cols * (grid_width) and 0 <= (mouse_y-car_screen_height) < rows * car_height:
                col_clicked = (mouse_x-car_screen_width) // grid_width
                row_clicked = (mouse_y-car_screen_height) // car_height
                index_clicked = row_clicked * cols + col_clicked
                if index_clicked < len(car_subsurfaces):
                    selected_index = index_clicked
            # Check if the user clicked on the start button
            elif (screen_width-button_width)//2 <= mouse_x <= (screen_width-button_width)//2 + button_width and screen_height*(4/5) <= mouse_y <= screen_height*(4/5) + button_height:
                if selected_index is not None:
                    action = True
  
    # Drawing assets
    screen.blit(menu_background, (0,0)) # background
    screen.blit(player_text, (200, 85)) # player text
    screen.blit(start_button_image, ((screen_width-button_width)//2, screen_height*(4/5))) # start button

    # Draw the grid of cars on the screen
    for i, car_surface in enumerate(car_subsurfaces):
        row = i // cols
        col = i % cols
        screen.blit(car_surface, (col * (grid_width) + car_screen_width, row * car_height + car_screen_height))

    # Highlight the selected car (if any)
    if selected_index is not None:
        width_offset, grid_width_offset, box_width_offset, height_offset=5,3,2,5
        car_position_width = car_screen_width-width_offset + (selected_index%4)*(grid_width+grid_width_offset) 
        car_position_height = car_screen_height + (selected_index//4)*(car_height+height_offset)
        pygame.draw.rect(screen, (255, 0, 0), (car_position_width, car_position_height, car_width+box_width_offset, car_height), 4)  

    # Update the display
    pygame.display.flip()

#loading image asserts for the main game loop
race_track=pygame.image.load('imgs/race-track.png').convert_alpha()
race_track=pygame.transform.scale(race_track, (screen_width, screen_height+100))
track_border=pygame.image.load('imgs/race-track-border.png').convert_alpha()
track_border=pygame.transform.scale(track_border, (screen_width, screen_height+100))
track_mask=pygame.mask.from_surface(track_border)
selected_car = car_subsurfaces[selected_index]
race_car = pygame.transform.scale(selected_car, (car_width//2.8, car_height//2.8))
car_mask = pygame.mask.from_surface(race_car)

# Initialize a variable to track the car's movement direction
car_direction = 1  # 1 for forward, -1 for backward
visual_angle=0
physics_angle=visual_angle+90
car_x, car_y = screen_width//2, screen_height//2  # Initial car position in middle
rotation_speed = screen_height * 0.0018 # Define the car rotation speed (in degrees per frame)
movement_speed = 0
speed = screen_width * 0.000015
deceleration = 0.95  # Deceleration factor (higher = less deceleration)
max_speed = screen_width * 0.0008

# Load restart button
restart_button = pygame.image.load('imgs/restart_btn.png').convert_alpha()
restart_button = pygame.transform.scale(restart_button, (40, 40))

# Function to reset car position and state
def reset_car():
    global car_x, car_y, movement_speed, visual_angle, physics_angle
    car_x, car_y = screen_width//2, screen_height//2
    movement_speed = 0
    visual_angle = 0
    physics_angle = visual_angle + 90

# Function to rotate the car image around its center
def rotate_car(angle):
    return pygame.transform.rotate(race_car, angle)

# Function to move the car forward based on its angle
def move_car_forward(x, y, angle, distance):
    angle_rad = math.radians(angle)  # Convert angle to radians
    new_x = x + distance * math.cos(angle_rad)
    new_y = y - distance * math.sin(angle_rad)  # Negative sign as the y-axis is inverted in Pygame
    return new_x, new_y

#running and action true
while running and action:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if restart button was clicked
            mouse_x, mouse_y = event.pos
            if 0 <= mouse_x <= 40 and 0 <= mouse_y <= 40:
                reset_car()

    
    keys = pygame.key.get_pressed()
    # Apply natural deceleration when no movement keys are pressed
    if not (keys[pygame.K_w] or keys[pygame.K_s]):
        movement_speed *= deceleration
    if keys[pygame.K_w]:
        movement_speed += speed
        movement_speed = min(movement_speed + speed, max_speed)
    if keys[pygame.K_s]:
        movement_speed -= speed
        movement_speed = max(movement_speed - speed, -max_speed)
    if keys[pygame.K_a]:
        visual_angle += rotation_speed
        physics_angle += rotation_speed  # Adjust physics angle accordingly
    if keys[pygame.K_d]:
        visual_angle -= rotation_speed
        physics_angle -= rotation_speed  # Adjust physics angle accordingly
    
    # Rotate the car image and Draw the rotated car image at its updated position
    rotated_car = rotate_car(visual_angle)
    rotated_car_width, rotated_car_height = rotated_car.get_size()
    car_x, car_y = move_car_forward(car_x, car_y, physics_angle, movement_speed) # Move the car forward

    screen.blit(race_track, (0,0))
    screen.blit(restart_button, (0, 0))  # Draw restart button
    screen.blit(rotated_car, (car_x - rotated_car_width // 2, car_y - rotated_car_height // 2))

    # Check for collision with the track
    offset = (car_x - rotated_car_width // 2 - 0, car_y - rotated_car_height // 2 - 0)
    collision_point = track_mask.overlap(car_mask, offset)

    if collision_point and movement_speed != 0:
        # Handle collision, move the car backward (bounce)
        movement_speed *= -0.8
        car_x, car_y = move_car_forward(car_x, car_y, physics_angle, movement_speed * car_direction)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()                                                                           
sys.exit()