from flask import Flask, request, jsonify
from players import get_all_players
from predictions import win_prediction, total_points_prediction, number_of_games_prediction
from predictions import games_decided_by_extra_points_prediction, third_game_winner_prediction
from scraper import scrape_data, update_player_list
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/api/players', methods=['GET'])
def players():
    query_parameters = request.args
    if 'update' in query_parameters:
        update_player_list()
    response = jsonify(get_all_players())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


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
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/scrape', methods=['GET'])
def scrape():
    response = jsonify("Scrape not performed")
    start_date = None
    end_date = None
    rank_range = None
    query_parameters = request.args
    if 'start' in query_parameters:
        start_date = query_parameters.get('start')
    if 'end' in query_parameters:
        end_date = query_parameters.get('end')
    if 'rank' in query_parameters:
        rank_range = query_parameters.get('rank')
    if start_date and end_date:
        scrape_data(start_date, end_date, rank_range)
        response_text = "Scrape performed from " + start_date + " to " + end_date
        if rank_range is not None:
            response_text = response_text + " for ranks " + rank_range
        response = jsonify(response_text)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
