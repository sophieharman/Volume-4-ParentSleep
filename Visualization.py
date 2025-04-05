import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Parent and Baby Awake Times")

# Colors
WHITE = (255, 255, 255)
DAY_COLOR = (255, 255, 200)  # Light yellow for day
NIGHT_COLOR = (50, 50, 100)  # Dark blue for night
EYE_COLOR = (0, 0, 0)  # Black for eyes
PACIFIER_COLOR = (0, 128, 128)  # Light pink for the pacifier
SUN_COLOR = (255, 255, 0)  # Yellow for the sun
MOON_COLOR = (200, 200, 200)  # Light gray for the moon
HAIR_COLOR = (50, 25, 0)  # Brown hair color

# Set up the clock
clock = pygame.time.Clock()

# Baby and Parent positions
baby_pos = (200, 150)  # Position of the baby
parent_pos = (400, 150)  # Position of the parent

def draw_baby(awake):
    # Baby head
    pygame.draw.circle(screen, (255, 204, 204), baby_pos, 40)  # Baby body color
    # Baby eyes or dash (depending on awake status)
    if awake:
        pygame.draw.circle(screen, EYE_COLOR, (baby_pos[0] - 15, baby_pos[1] - 10), 5)  # Left eye
        pygame.draw.circle(screen, EYE_COLOR, (baby_pos[0] + 15, baby_pos[1] - 10), 5)  # Right eye
    else:
        # Draw a dash for the eyes if the baby is asleep
        font = pygame.font.Font(None, 36)
        dash_text = font.render("-", True, EYE_COLOR)
        screen.blit(dash_text, (baby_pos[0] - 15, baby_pos[1] - 10))  # Left eye dash
        screen.blit(dash_text, (baby_pos[0] + 5, baby_pos[1] - 10))  # Right eye dash

    # Pacifier
    pacifier_base_pos = (baby_pos[0], baby_pos[1] + 30)  # Position of the pacifier
    pygame.draw.circle(screen, PACIFIER_COLOR, pacifier_base_pos, 8)  # Pacifier base
    pygame.draw.line(screen, PACIFIER_COLOR, pacifier_base_pos, (baby_pos[0], baby_pos[1] + 45), 3)  # Pacifier stem

    # Draw a hair curl on the baby (small spiral)
    pygame.draw.arc(screen, HAIR_COLOR, (baby_pos[0] - 25, baby_pos[1] - 50, 30, 30), 0, 3.14, 3)  # Baby hair curl

def draw_parent(awake):
    # Parent head
    pygame.draw.circle(screen, (255, 204, 204), parent_pos, 50)  # Parent body color
    # Parent eyes or dash (depending on awake status)
    if awake:
        eye_radius = 7
        pygame.draw.circle(screen, EYE_COLOR, (parent_pos[0] - 20, parent_pos[1] - 20), eye_radius)  # Left eye
        pygame.draw.circle(screen, EYE_COLOR, (parent_pos[0] + 20, parent_pos[1] - 20), eye_radius)  # Right eye
    else:
        # Draw a dash for the eyes if the parent is asleep
        font = pygame.font.Font(None, 36)
        dash_text = font.render("-", True, EYE_COLOR)
        screen.blit(dash_text, (parent_pos[0] - 20, parent_pos[1] - 20))  # Left eye dash
        screen.blit(dash_text, (parent_pos[0] + 10, parent_pos[1] - 20))  # Right eye dash

def draw_clock(time_step):
    # Convert the time_step to 12-hour format
    hour = time_step % 12
    if hour == 0:  # Handle the case where hour = 0 (i.e., midnight or noon)
        hour = 12
    
    # Determine AM or PM
    period = "AM" if time_step % 24 < 12 else "PM"  # Ensure 24-hour cycle is used for AM/PM logic
    
    # Display time in 12-hour format
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"{hour:02}:00 {period}", True, (0, 0, 0))
    screen.blit(time_text, (250, 20))

def draw_sun_moon(time_step):
    if 8 <= time_step % 24 <= 22:  # Daytime (8:00 AM to 10:00 PM)
        # Draw the sun during daytime
        pygame.draw.circle(screen, SUN_COLOR, (screen_width - 50, 50), 30)  # Sun in the top left corner
    else:  # Nighttime (other hours)
        # Draw the moon during nighttime
        pygame.draw.circle(screen, MOON_COLOR, (screen_width - 50, 50), 30)  # Moon in the top left corner

# Function to draw sleep counters
def draw_sleep_counters(baby_sleep_total, parent_sleep_total):
    # Display the counters in the bottom left corner
    font = pygame.font.Font(None, 30)
    baby_sleep_text = font.render(f"Baby Sleep: {baby_sleep_total} hours", True, (0, 0, 0))
    parent_sleep_text = font.render(f"Parent Sleep: {parent_sleep_total} hours", True, (0, 0, 0))
    
    # Position the text
    screen.blit(baby_sleep_text, (7, screen_height - 70))  # Baby counter
    screen.blit(parent_sleep_text, (7, screen_height - 30))  # Parent counter


def main(baby_list, parent_list):
    time_step = 0  # Time step (in hours, 0-23)
    baby_sleep_total = 0
    parent_sleep_total = 0
    
    # Extend lists to match 24 hours if necessary
    while len(baby_list) < 24:
        baby_list.extend(baby_list)  # Extend list to 24 hours
    while len(parent_list) < 24:
        parent_list.extend(parent_list)  # Extend list to 24 hours
    
    while True:
        # Determine day or night based on time_step (8:00 AM - 10:00 PM is daytime)
        if 8 <= time_step % 24 <= 22:
            screen.fill(DAY_COLOR)  # Daytime background
        else:
            screen.fill(NIGHT_COLOR)  # Nighttime background
        
        # Draw the sun or moon based on the time
        draw_sun_moon(time_step)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get awake status from binary lists for the current time_step (wrap around if end of list is reached)
        baby_awake = baby_list[time_step % len(baby_list)] == 0  # 0 means awake, 1 means asleep
        parent_awake = parent_list[time_step % len(parent_list)] == 0  # 0 means awake, 1 means asleep

        # Count the number of hours slept up until the current time step
        if baby_awake == 0:  # Baby is asleep
            baby_sleep_total += 1
        if parent_awake == 0:  # Parent is asleep
            parent_sleep_total += 1
        
        # Draw the baby and parent based on their awake status
        draw_baby(baby_awake)
        draw_parent(parent_awake)

        # Draw the clock
        draw_clock(time_step)

        # Draw the sleep counters
        draw_sleep_counters(baby_sleep_total, parent_sleep_total)

        # Update the display
        pygame.display.update()

        # Increment the time step (wrap around after the last time step)
        time_step += 1

        # Reset the counters after 24 hours (without affecting the AM/PM logic)
        if time_step % 24 == 0:
            baby_sleep_total = 0
            parent_sleep_total = 0

        # Control frame rate (1 FPS for 1 hour per tick)
        clock.tick(1)

if __name__ == "__main__":
    # Example binary lists for baby and parent (1 = asleep, 0 = awake)
    baby_list = [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]
    parent_list = [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0]
    
    main(baby_list, parent_list)

