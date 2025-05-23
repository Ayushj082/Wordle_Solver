import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, make_response, render_template
from dataclasses import dataclass
import string, json, sys, random
from wordle_solver import WorldSolverMultiList

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@dataclass
class SolverAPIParameters:
    # Compute absolute paths relative to the location of index.py
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    opener_word_list_file_path: str = os.path.join(base_dir, "english_words_opener.txt")
    full_word_list_file_path: str = os.path.join(base_dir, "english_words_full.txt")
    max_suggested_words: int = 10
    logging_enabled: bool = True

def write_log(log):
    if SolverAPIParameters.logging_enabled:
        print(log)

def handle_tries(ui_tries, word_length, exclude_plurals=True, shuffle_suggested_words=False, visit=None):
    if isinstance(ui_tries, list):
        tries = [(attempt["word"].lower(), attempt["symbols"]) for attempt in ui_tries if "word" in attempt and "symbols" in attempt]
        solver_multi = WorldSolverMultiList(
            [SolverAPIParameters.opener_word_list_file_path, SolverAPIParameters.full_word_list_file_path],
            word_length=word_length,
            exclude_plurals=exclude_plurals
        )
        solver_multi.max_try_indexes_for_lists = [2, sys.maxsize]

        if any(letter not in string.ascii_lowercase for attempt in tries for letter in attempt[0]):
            return make_response(jsonify(error="Invalid characters in word(s)"), 400)

        if any(symbol not in solver_multi.solvers[0].permitted_input_symbols for attempt in tries for symbol in attempt[1]):
            return make_response(jsonify(error="Invalid symbols in pattern(s)"), 400)

        if any(len(attempt[0]) != word_length or len(attempt[1]) != word_length for attempt in tries):
            return make_response(jsonify(error="Invalid word/symbol length"), 400)

        solver_multi.tries = tries
        solver_multi.update_pattern_paramters()
        results = solver_multi.get_suggested_words()
        suggestions = results.words[:SolverAPIParameters.max_suggested_words]

        if shuffle_suggested_words:
            random.shuffle(suggestions)

        return jsonify({
            "word_list": results.word_list_file_path,
            "suggested_words": suggestions
        })

    return make_response(jsonify(error="Invalid request format"), 400)

@app.route("/api", methods=["POST", "OPTIONS"])
def api_handler():
    if request.method == "OPTIONS":
        return ("", 204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600"
        })

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify(error="Invalid or missing JSON"), 400)

    response = handle_tries(data, word_length=5)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")

def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)