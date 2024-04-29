from flask import Blueprint, render_template

tictactoe = Blueprint('tictactoe', __name__)

@tictactoe.route('/tictactoe')
def tictactoe_game():
    return render_template('tictactoe.html')
