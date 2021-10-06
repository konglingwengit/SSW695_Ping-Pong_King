from flask import Flask, request, jsonify
from players import get_all_players
from predictions import win_prediction, total_points_prediction, number_of_games_prediction
from predictions import games_decided_by_extra_points_prediction, third_game_winner_prediction
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/api/players', methods=['GET'])
def players():
    return jsonify(get_all_players())


@app.route('/api/predictions', methods=['GET'])
def predictions():
    return_data = "Not yet implemented"
    first_player = None
    second_player = None
    query_parameters = request.args
    if 'prediction' in query_parameters:
        prediction = query_parameters.get('prediction')
        if 'p1' in query_parameters:
            first_player = query_parameters.get('p1')
        if 'p2' in query_parameters:
            second_player = query_parameters.get('p2')
        if prediction == "WINNER":
            return_data = win_prediction(first_player, second_player)
        if prediction == "TOTAL_POINTS":
            return_data = total_points_prediction(first_player, second_player)
        if prediction == "NUMBER_OF_GAMES":
            return_data = number_of_games_prediction(first_player, second_player)
        if prediction == "THIRD_GAME":
            return_data = third_game_winner_prediction(first_player, second_player)
        if prediction == "EXTRA_POINTS":
            return_data = games_decided_by_extra_points_prediction(first_player, second_player)
    return return_data


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
