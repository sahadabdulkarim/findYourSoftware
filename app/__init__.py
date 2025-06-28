import os
import pandas as pd
from flask import Flask, jsonify, request, render_template 
from flask_cors import CORS
from mysql.connector import Error, connect
from dotenv import load_dotenv
from tasks import find_recommendation_task, celery_app


def create_app():
    """Creating and configuring an instance of the Flask application."""
    app = Flask(__name__, template_folder='../templates')
    
    CORS(app) 
    load_dotenv()

    def get_db_connection():
        try:
            conn = connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT')),
                database=os.getenv('DB_DATABASE'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    @app.route('/')
    def index():
        """Render the main frontend page."""
        return render_template('index.html')

    @app.route('/recommend', methods=['POST'])
    def start_recommendation_task():
        """
        This endpoint NO LONGER calculates the recommendation.
        It starts the background task and immediately returns a task ID.
        """
        user_input = request.get_json()
        # Dispatch the task to the Celery worker
        task = find_recommendation_task.delay(user_input)
        # Return the ID of the task so the frontend can check its status
        return jsonify({"task_id": task.id}), 202

    @app.route('/tasks/<task_id>', methods=['GET'])
    def get_task_status(task_id):
        """
        This endpoint is polled by the frontend to get the status
        of a background task.
        """
        task = celery_app.AsyncResult(task_id)
        response = {
            'state': task.state,
        }
        if task.state == 'SUCCESS':
            response['result'] = task.info
        elif task.state == 'FAILURE':
            response['result'] = str(task.info) # Return error message as string
        return jsonify(response)



    return app
