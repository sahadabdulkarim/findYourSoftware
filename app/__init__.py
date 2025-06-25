import os
import pandas as pd
from flask import Flask, jsonify, request, render_template 
from flask_cors import CORS
from mysql.connector import Error, connect
from dotenv import load_dotenv

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
    def recommend():
        """
        The main recommendation endpoint. It expects a JSON payload
        with user preferences and returns the best software match.
        
        FINAL LOGIC:
        - Implements a scoring system.
        - Adds keyword matching for features and tags.
        """
        # 1. Get user input from the request
        user_input = request.get_json()
        if not user_input:
            return jsonify({"error": "Invalid input"}), 400

        industry = user_input.get('industry')
        team_size = user_input.get('team_size')
        platform = user_input.get('platform')
        preferred_features = user_input.get('features', '').lower()

        # 2. Fetch all software data from the database
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        try:
            query = "SELECT * FROM software"
            df = pd.read_sql(query, conn)
        except Exception as e:
            return jsonify({"error": f"Could not retrieve data: {e}"}), 500
        finally:
            if conn.is_connected():
                conn.close()

        # 3. scoring logic
        
        df['score'] = 0
        
        keywords = [keyword.strip() for keyword in preferred_features.split(',') if keyword.strip()]

        for i, row in df.iterrows():
            score = 0
            
            # Score for Industry
            if industry and industry in row['industry']:
                score += 3
            elif 'General' in row['industry']:
                score += 1
            
            # Score for Team Size
            if team_size and team_size in row['team_size']:
                score += 2
            elif 'All Sizes' in row['team_size']:
                score += 1
            
            # Score for Platform
            if platform and platform in row['platform']:
                score += 1

            # Score for Keyword Matching
            if keywords:
                # Combine the software's features and tags into one string
                search_text = f"{row['features']} {row['tags']}".lower()
                for keyword in keywords:
                    if keyword in search_text:
                        score += 4 # High score for each keyword match!
            
            df.at[i, 'score'] = score
            
        qualified_software = df[df['score'] > 0]
        
        if not qualified_software.empty:
            max_score = qualified_software['score'].max()
            best_matches = qualified_software[qualified_software['score'] == max_score]
            recommendation = best_matches.sample(n=1).iloc[0].to_dict()
            response_message = f"Based on your preferences, we recommend: {recommendation['name']}. It's a great tool for {recommendation['features'].lower()}."
            return jsonify({
                "recommendation": recommendation,
                "message": response_message
            })
        else:
            fallback_recommendation = df[df['name'] == 'Notion'].iloc[0].to_dict()
            response_message = "We couldn't find a perfect match, but you might like Notion. It's a versatile tool for general productivity."
            return jsonify({
                "recommendation": fallback_recommendation,
                "message": response_message
            })



    return app
