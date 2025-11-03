from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Game parameters
GRID_SIZE = 3
TOTAL_TILES = GRID_SIZE * GRID_SIZE
WINNING_ORDER = [f'tile_{i // GRID_SIZE}_{i % GRID_SIZE}.png' for i in range(TOTAL_TILES)]
WINNING_ORDER[-1] = 'blank' # The last tile is the empty space

# Server-side game state
game_state = []
is_solved = False

def create_shuffled_board():
    global game_state, is_solved
    
    # Create a solvable puzzle board
    tiles = WINNING_ORDER[:-1]
    random.shuffle(tiles)
    tiles.append('blank')
    
    game_state = tiles
    is_solved = False

def check_win():
    # Check if the current order of tiles matches the winning order
    return game_state == WINNING_ORDER

@app.route('/')
def index():
    create_shuffled_board()
    return render_template('index.html', game_state=game_state, grid_size=GRID_SIZE)

@app.route('/move/<int:tile_index>')
def move(tile_index):
    global is_solved, game_state
    
    if is_solved:
        return jsonify({'message': 'Puzzle is already solved!', 'is_solved': True})
    
    # Check for valid move (adjacent to blank tile)
    blank_index = game_state.index('blank')
    
    # Valid moves are horizontal or vertical
    can_move = (abs(tile_index - blank_index) == 1 and tile_index // GRID_SIZE == blank_index // GRID_SIZE) or \
               (abs(tile_index - blank_index) == GRID_SIZE)
    
    if can_move:
        # Swap the tile and the blank space
        game_state[tile_index], game_state[blank_index] = game_state[blank_index], game_state[tile_index]
        is_solved = check_win()
    
    return jsonify({'game_state': game_state, 'is_solved': is_solved})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
