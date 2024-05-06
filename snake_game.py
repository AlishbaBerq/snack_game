import streamlit as st
import numpy as np
import time

# Game settings
width = 20
height = 20
snake_pos = [[width//2, height//2]]
food_pos = [np.random.randint(1, width), np.random.randint(1, height)]
score = 0
direction = 'RIGHT'
change_to = direction

# Game over function
def game_over():
    st.session_state['game_over'] = True
    st.balloons()

# Check if direction is valid
def is_valid_direction(main, against):
    if main == 'RIGHT' and not against == 'LEFT':
        return True
    if main == 'LEFT' and not against == 'RIGHT':
        return True
    if main == 'UP' and not against == 'DOWN':
        return True
    if main == 'DOWN' and not against == 'UP':
        return True
    return False

# Update the direction based on key presses
def update_direction():
    global direction, change_to
    if st.session_state['left']:
        change_to = 'LEFT'
    if st.session_state['right']:
        change_to = 'RIGHT'
    if st.session_state['up']:
        change_to = 'UP'
    if st.session_state['down']:
        change_to = 'DOWN'
    if is_valid_direction(change_to, direction):
        direction = change_to

# Update the snake's position
def update_snake():
    global snake_pos, food_pos, score
    # Update the position of the head of the snake
    if direction == 'RIGHT':
        snake_pos[0][0] += 1
    if direction == 'LEFT':
        snake_pos[0][0] -= 1
    if direction == 'UP':
        snake_pos[0][1] -= 1
    if direction == 'DOWN':
        snake_pos[0][1] += 1

    # Snake body growing mechanism
    # If the snake has eaten the food
    if snake_pos[0] == food_pos:
        score += 1
        food_pos = [np.random.randint(1, width), np.random.randint(1, height)]
        snake_pos.append(snake_pos[-1])

    # Move the snake body
    for i in range(len(snake_pos)-1, 0, -1):
        snake_pos[i] = list(snake_pos[i-1])

    # Check if snake has hit the boundaries
    if snake_pos[0][0] >= width or snake_pos[0][0] < 0 or snake_pos[0][1] >= height or snake_pos[0][1] < 0:
        game_over()

    # Check if snake has hit itself
    if snake_pos[0] in snake_pos[1:]:
        game_over()

# Rendering the snake and food
def render():
    # Create a blank canvas
    canvas = np.zeros((height, width))
    # Draw the snake
    for pos in snake_pos:
        canvas[pos[1]][pos[0]] = 1
    # Draw the food
    canvas[food_pos[1]][food_pos[0]] = 2
    # Display the canvas
    st.write('Score: %s' % score)
    st.image(canvas, width=500, channels='GRAY')

# Initialize the game state
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
    st.session_state['left'] = False
    st.session_state['right'] = False
    st.session_state['up'] = False
    st.session_state['down'] = False

# Placeholders for the direction buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button('Left', key='left', on_click=lambda: st.session_state.update({'left': True, 'right': False, 'up': False, 'down': False}))
with col2:
    st.button('Right', key='right', on_click=lambda: st.session_state.update({'left': False, 'right': True, 'up': False, 'down': False}))
with col3:
    st.button('Up', key='up', on_click=lambda: st.session_state.update({'left': False, 'right': False, 'up': True, 'down': False}))
with col4:
    st.button('Down', key='down', on_click=lambda: st.session_state.update({'left': False, 'right': False, 'up': False, 'down': True}))

# Main game loop
while not st.session_state['game_over']:
    update_direction()
    update_snake()
    render()
    time.sleep(0.1)
