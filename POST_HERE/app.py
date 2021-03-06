"""app factory"""

from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from .functions import jsonConversion, transform_get, list_subreddits
import joblib
from .models import Post_Model, Username_Model
import pymongo


load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)
    # Allow CORS from the above domain on all routes

    loadcv = joblib.load('tf.joblib')
    loaddf = joblib.load('tfarray.joblib')
    loaddf = loaddf.todense()

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/subreddit', methods=['POST'])
    def get_subreddits():
        """this is the route the Frontend makes requests to"""
        submission = request.get_json(force=True)
        model_input = jsonConversion(submission)
        model_output = transform_get(model_input, loadcv, loaddf)
        subreddit_list = list_subreddits(model_output)

        return jsonify(subreddit_list)

    @app.route('/subreddit_test', methods=['POST'])
    def get_subreddits_test():
        """this route lets us test the model directly in the Flask app"""
        title, text, link = sorted([request.values['title'],
                                    request.values['text'],
                                    request.values['link']])
        submission = {"title": title, "text": text, "link": True if link == 'T' else False}
        model_input = jsonConversion(submission)
        model_output = transform_get(model_input, loadcv, loaddf)
        subreddit_list = list_subreddits(model_output)

        return jsonify(subreddit_list)

    @app.route('/username', methods=['POST'])
    def from_username(name=None):
        """route made in preparation for the possible stretch goal"""
        name = name or request.values['user_name']
        model = Username_Model(name=name)
        prediction = model.predict()
        output = list_subreddits(prediction)

        return jsonify(output)

    return app
