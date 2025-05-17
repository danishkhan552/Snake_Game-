import random
from tkinter import *

# Game settings
GAME_WIDTH = 700          # Width of the game window
GAME_HEIGHT = 700         # Height of the game window
SPEED = 100               # Speed of the snake's movement (lower is faster)
SPACE_SIZE = 50           # Size of each snake segment and food block
BODY_PARTS = 3            # Initial size of the snake
SNAKE_COLOR = "#00FF00"  # Color of the snake
FOOD_COLOR = "#FF0000"   # Color of the food
BACKGROUND_COLOR = "#000000"  # Background color of the game window


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS       # Set the initial body size of the snake
        self.coordinates = []             # List to store the coordinates of each snake segment
        self.squares = []                 # List to store the actual rectangle objects representing each segment

        # Initialize the snake at (0,0) with a default length
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create the snake segments as rectangles on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        # Generate a random position for the food within the game boundaries
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]  # Store the food coordinates

        # Create a food item as an oval on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    # Get the current head coordinates of the snake
    x, y = snake.coordinates[0]

    # Update the head coordinates based on the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add the new head position to the snake
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1  # Increase the score
        score_label.config(text=f"Score: {score}")  # Update the score label
        canvas.delete("food")  # Remove the eaten food
        food = Food()  # Create a new food item
    else:
        # Remove the last segment to simulate movement
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions (with walls or itself)
    if check_collisions(snake):
        game_over()  # End the game if a collision occurs
    else:
        window.after(SPEED, next_turn, snake, food)  # Continue the game loop


def change_direction(new_direction):
    # Prevent the snake from reversing direction
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    # Check if the snake hits the wall
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if the snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    # Clear the canvas and display the game over message
    canvas.delete(ALL)
    game_over_label.config(text="GAME OVER")


# Initialize the main window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

# Create the main game frame
main_frame = Frame(window)
main_frame.pack(side=LEFT)

# Create the game canvas
canvas = Canvas(main_frame, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Create the sidebar for score and game over message
sidebar_frame = Frame(window)
sidebar_frame.pack(side=RIGHT, fill=Y)

# Score label
score_label = Label(sidebar_frame, text=f"Score: {score}", font=('consolas', 40))
score_label.pack()

# Game over label
game_over_label = Label(sidebar_frame, font=('consolas', 40), text="", fg="red")
game_over_label.pack()

# Center the window on the screen
window.update()
window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{(window.winfo_screenwidth()//2) - (window.winfo_width()//2)}+{(window.winfo_screenheight()//2) - (window.winfo_height()//2)}")

# Set up the key bindings for direction changes
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize the snake and food
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Run the main event loop
window.mainloop()
