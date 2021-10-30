from flask import Flask, request, jsonify, render_template
from players import get_all_players
from predictions import win_prediction, total_points_prediction, number_of_games_prediction
from predictions import games_decided_by_extra_points_prediction, third_game_winner_prediction
from predictions import money_line_prediction
from machine_learning.tennis import fetch_tournament
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/predictions', methods=['GET'])
def predictions():
    response = "Not yet implemented"
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
            response = win_prediction(first_player, second_player)
        if prediction == "TOTAL_POINTS":
            response = total_points_prediction(first_player, second_player)
        if prediction == "NUMBER_OF_GAMES":
            response = number_of_games_prediction(first_player, second_player)
        if prediction == "THIRD_GAME":
            response = third_game_winner_prediction(first_player, second_player)
        if prediction == "EXTRA_POINTS":
            response = games_decided_by_extra_points_prediction(first_player, second_player)
        if prediction == "ALL":
            response = list()
            response.append(win_prediction(first_player, second_player))
            response.append(total_points_prediction(first_player, second_player))
            response.append(number_of_games_prediction(first_player, second_player))
            response.append(third_game_winner_prediction(first_player, second_player))
            response.append(games_decided_by_extra_points_prediction(first_player, second_player))
            response.append(money_line_prediction(first_player, second_player))

    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/players', methods=['GET'])
def players():
    query_parameters = request.args
    response = jsonify(get_all_players())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/scrape', methods=['POST'])
def scrape():
    failed = False
    response = jsonify("Scrape not performed")
    query_parameters = request.form
    try:
        start_idx = int(query_parameters.get('start'))
        end_idx = int(query_parameters.get('end'))
        tournament = query_parameters.get('tournament')
    except:
        failed = True

    if not failed:
        fetch_tournament(tournament, start_idx, end_idx)
        response_text = "Scrape performed from " + str(start_idx) + " to " + str(end_idx) + \
                        " for tournament " + tournament
        response = jsonify(response_text)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
