import os
import time
import pandas as pd
from celery import Celery
from mysql.connector import Error, connect
from dotenv import load_dotenv

# Configure Celery
# It reads the broker and backend URLs from the environment variables we set in docker-compose
celery_app = Celery(
    'tasks',
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND")
)

# Load environment variables for the worker
load_dotenv()

def get_db_connection_for_task():
    """A dedicated DB connection function for the Celery worker."""
    # This includes retry logic to ensure the worker can connect
    attempts = 5
    while attempts > 0:
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
            print(f"Worker connection error: {e}. Retrying...")
            attempts -= 1
            time.sleep(5)
    return None

@celery_app.task
def find_recommendation_task(user_input):
    """The background task that runs the scoring logic."""
    print(f"Received task for user input: {user_input}")
    
    # Simulate a long-running task
    time.sleep(5)

    industry = user_input.get('industry')
    team_size = user_input.get('team_size')
    platform = user_input.get('platform')
    preferred_features = user_input.get('features', '').lower()

    conn = get_db_connection_for_task()
    if not conn:
        raise Exception("Database connection failed in worker.")

    try:
        query = "SELECT * FROM software"
        df = pd.read_sql(query, conn)
    finally:
        if conn.is_connected():
            conn.close()

    df['score'] = 0
    keywords = [keyword.strip() for keyword in preferred_features.split(',') if keyword.strip()]

    for i, row in df.iterrows():
        score = 0
        if industry and industry in row['industry']: score += 3
        elif 'General' in row['industry']: score += 1
        if team_size and team_size in row['team_size']: score += 2
        elif 'All Sizes' in row['team_size']: score += 1
        if platform and platform in row['platform']: score += 1
        if keywords:
            search_text = f"{row['features']} {row['tags']}".lower()
            for keyword in keywords:
                if keyword in search_text:
                    score += 4
        df.at[i, 'score'] = score
    
    qualified_software = df[df['score'] > 0]
    
    if not qualified_software.empty:
        max_score = qualified_software['score'].max()
        best_matches = qualified_software[qualified_software['score'] == max_score]
        recommendation = best_matches.sample(n=1).iloc[0].to_dict()
        response_message = f"Based on your preferences, we recommend: {recommendation['name']}. It's a great tool for {recommendation['features'].lower()}."
        return {"recommendation": recommendation, "message": response_message}
    else:
        fallback = df[df['name'] == 'Notion'].iloc[0].to_dict()
        response_message = "We couldn't find a perfect match, but you might like Notion. It's a versatile tool for general productivity."
        return {"recommendation": fallback, "message": response_message}
