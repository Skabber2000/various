from flask import Flask, request, send_file, render_template, jsonify, session
import qrcode
import io
from game import Game, Team

app = Flask(__name__)
app.secret_key = 'knights-vs-assassins-secret-key-12345'

# Store active games in memory (in production, use a database)
games = {}

@app.route('/generate', methods=['GET', 'POST'])
def generate_qr_code():
    if request.method == 'POST':
        # Handle POST request with JSON data
        data = request.json
        product_name = data.get('product_name')
        production_number = data.get('production_number')
        batch_release_date = data.get('batch_release_date')
    elif request.method == 'GET':
        # Handle GET request with query parameters
        product_name = request.args.get('product_name')
        production_number = request.args.get('production_number')
        batch_release_date = request.args.get('batch_release_date')
    
    if not all([product_name, production_number, batch_release_date]):
        return "Missing required fields", 400

    qr_data = f"Product name: {product_name}\nProduction: {production_number}\nBatch release date: {batch_release_date}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

# Game routes
@app.route('/')
def index():
    """Serve the game page"""
    return render_template('game.html')

@app.route('/shock-pulse-lab')
def shock_pulse_lab():
    """Serve the shock pulse lab page"""
    return render_template('shock_pulse_lab.html')

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Create a new game"""
    game = Game()
    session_id = request.remote_addr + str(len(games))
    games[session_id] = game
    session['game_id'] = session_id
    return jsonify(game.get_state())

def get_current_game():
    """Get the current game from session"""
    game_id = session.get('game_id')
    if game_id and game_id in games:
        return games[game_id]
    return None

@app.route('/api/game/state', methods=['GET'])
def get_state():
    """Get current game state"""
    game = get_current_game()
    if not game:
        return jsonify({'error': 'No active game'}), 404
    return jsonify(game.get_state())

@app.route('/api/game/move', methods=['POST'])
def move_unit():
    """Move a unit"""
    game = get_current_game()
    if not game:
        return jsonify({'error': 'No active game'}), 404

    data = request.json
    from_x = data.get('from_x')
    from_y = data.get('from_y')
    to_x = data.get('to_x')
    to_y = data.get('to_y')

    unit = game.board.get_unit(from_x, from_y)
    if not unit:
        return jsonify({'success': False, 'message': 'No unit at source position'})

    if unit.team != game.current_turn:
        return jsonify({'success': False, 'message': 'Not your turn'})

    success = game.board.move_unit(unit, to_x, to_y)
    if success:
        return jsonify({'success': True, 'state': game.get_state()})
    else:
        return jsonify({'success': False, 'message': 'Invalid move'})

@app.route('/api/game/attack', methods=['POST'])
def attack():
    """Attack with a unit"""
    game = get_current_game()
    if not game:
        return jsonify({'error': 'No active game'}), 404

    data = request.json
    attacker_x = data.get('attacker_x')
    attacker_y = data.get('attacker_y')
    defender_x = data.get('defender_x')
    defender_y = data.get('defender_y')

    attacker = game.board.get_unit(attacker_x, attacker_y)
    defender = game.board.get_unit(defender_x, defender_y)

    if not attacker or not defender:
        return jsonify({'success': False, 'message': 'Invalid units'})

    if attacker.team != game.current_turn:
        return jsonify({'success': False, 'message': 'Not your turn'})

    result = game.attack(attacker, defender)
    if result['success']:
        return jsonify({'success': True, 'result': result, 'state': game.get_state()})
    else:
        return jsonify(result)

@app.route('/api/game/end-turn', methods=['POST'])
def end_turn():
    """End the current turn"""
    game = get_current_game()
    if not game:
        return jsonify({'error': 'No active game'}), 404

    game.end_turn()
    return jsonify({'success': True, 'state': game.get_state()})

@app.route('/api/game/ai-turn', methods=['POST'])
def ai_turn():
    """Let AI take its turn"""
    game = get_current_game()
    if not game:
        return jsonify({'error': 'No active game'}), 404

    actions = game.ai_take_turn()
    game.end_turn()

    return jsonify({'success': True, 'actions': actions, 'state': game.get_state()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
