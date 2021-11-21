from flask import Flask, request, jsonify, render_template
from players import get_all_players
from predictions import win_prediction, total_points_prediction, number_of_games_prediction
from predictions import games_decided_by_extra_points_prediction, first_game_winner_prediction
from users import user_exists
from player_statistics import get_player_stats, get_vs_stats
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": ["https://ping-pong-king-666.uc.r.appspot.com"]}})
# "http://localhost:4200",
# "https://ping-pong-king-666.uc.r.appspot.com"


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
        if prediction == "FIRST_GAME":
            response = first_game_winner_prediction(first_player, second_player)
        if prediction == "EXTRA_POINTS":
            response = games_decided_by_extra_points_prediction(first_player, second_player)
        if prediction == "ALL":
            response = list()
            response.append(win_prediction(first_player, second_player))
            response.append(total_points_prediction(first_player, second_player))
            response.append(number_of_games_prediction(first_player, second_player))
            response.append(first_game_winner_prediction(first_player, second_player))
            response.append(games_decided_by_extra_points_prediction(first_player, second_player))

    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/players', methods=['GET'])
def players():
    response = jsonify(get_all_players())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# @app.route('/api/scrape', methods=['POST'])
# def scrape():
#     failed = False
#     response = jsonify("Scrape not performed")
#     query_parameters = request.form
#     try:
#         start_idx = int(query_parameters.get('start'))
#         end_idx = int(query_parameters.get('end'))
#         tournament = query_parameters.get('tournament')
#     except:
#         failed = True
#
#     if not failed:
#         fetch_tournament(tournament, start_idx, end_idx)
#         response_text = "Scrape performed from " + str(start_idx) + " to " + str(end_idx) + \
#                         " for tournament " + tournament
#         response = jsonify(response_text)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
#
# @app.route('/api/user', methods=['POST'])
# def user():
#     failed = False
#     response = jsonify("User not found")
#     query_parameters = request.get_json()
#     try:
#         email = str(query_parameters['email'])
#     except:
#         failed = True
#     if not failed:
#         if user_exists(email):
#             response_text = "User already exists " + str(email)
#             response = jsonify(response_text)
#         else:
#             add_user(email)
#             response_text = "User created " + str(email)
#             response = jsonify(response_text)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
#
# @app.route('/api/genstats', methods=['POST'])
# def generate_player_stats():
#     failed = False
#     response = jsonify("Scrape not performed")
#     query_parameters = request.form
#     try:
#         start_timestamp = int(query_parameters.get('start'))
#         end_timestamp = int(query_parameters.get('end'))
#     except:
#         failed = True
#
#     if not failed:
#         generate_player_statistics(start_timestamp, end_timestamp)
#         response_text = "Generated player statistic data from timestamp " + \
#                         str(start_timestamp) + " to " + str(end_timestamp)
#         response = jsonify(response_text)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
#
@app.route('/api/single_player_stats', methods=['GET'])
def single_player_stats():
    response = jsonify("Not a valid player")
    query_parameters = request.args
    if 'p1' in query_parameters:
        first_player = query_parameters.get('p1')
        response = jsonify(get_player_stats(first_player))
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/vs_stats', methods=['GET'])
def vs_stats():
    response = jsonify("Not a valid player")
    query_parameters = request.args
    if 'p1' in query_parameters and 'p2' in query_parameters:
        first_player = query_parameters.get('p1')
        second_player = query_parameters.get('p2')
        response = jsonify(get_vs_stats(first_player, second_player))
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/user/', methods=['POST'])
def user():
    failed = False
    response = jsonify("User not authorized")
    query_parameters = request.get_json()
    try:
        email = str(query_parameters['email'])
    except:
        failed = True
    if not failed:
        if user_exists(email):
            response_text = "User authorized - " + str(email)
            response = jsonify(response_text)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
