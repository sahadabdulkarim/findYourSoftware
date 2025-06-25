import os
import mysql.connector
import time
from mysql.connector import Error
from dotenv import load_dotenv

def create_connection():
    """Creating database connection to the MySQL container with retries."""
    connection = None
    attempts = 10
    while attempts > 0:
        try:
            load_dotenv()
            
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT')),
                database=os.getenv('DB_DATABASE'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            if connection.is_connected():
                print("Seed script successfully connected to the database")
                return connection
        except Error as e:
            print(f"Seed script connection error: {e}. Retrying in 5 seconds...")
            attempts -= 1
            time.sleep(5)
            
    print("Seed script could not connect to the database after several attempts.")
    return None

def setup_database(connection):
    """Create the software table and insert the initial data."""
    cursor = connection.cursor()
    try:
        print("Dropping existing 'software' table if it exists...")
        cursor.execute("DROP TABLE IF EXISTS software")

        print("Creating 'software' table...")
        create_table_query = """
        CREATE TABLE software (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            industry VARCHAR(255),
            team_size VARCHAR(255),
            platform VARCHAR(255),
            features TEXT,
            price VARCHAR(50),
            tags VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'software' created successfully.")

        software_data = [
            (1, 'Notion', 'General', 'Small/Medium', 'Web', 'Notes, Collaboration', 'Free', 'productivity, notes'),
            (2, 'Jira', 'Tech', 'Medium/Large', 'Web', 'Issue Tracking, Agile Boards', '$$$', 'project management'),
            (3, 'Figma', 'Design', 'Solo/Small', 'Web', 'UI Design, Prototyping', '$$', 'design, collaboration'),
            (4, 'Salesforce', 'Marketing', 'Enterprise', 'Web, Mobile', 'CRM, Sales Automation', '$$$$', 'crm, sales'),
            (5, 'VS Code', 'Tech', 'Solo', 'Desktop', 'Coding, Extensions, Git', 'Free', 'ide, code'),
            (6, 'QuickBooks', 'Finance', 'Small/Medium', 'Desktop, Web', 'Accounting, Invoicing', '$$$', 'accounting, finance'),
            (7, 'Moodle', 'Education', 'Medium/Large', 'Web', 'Course Management, Quizzes', '$$', 'lms, education'),
            (8, 'Canva', 'Marketing', 'Solo/Small', 'Web, Mobile', 'Graphic Design, Templates', 'Free', 'design, marketing'),
            (9, 'Trello', 'General', 'Small/Medium', 'Web, Mobile', 'Kanban Boards, Task Management', 'Free', 'project management, kanban'),
            (10, 'SAP ERP', 'Finance', 'Enterprise', 'Desktop, Web', 'Finance, Inventory, HR', '$$$$', 'enterprise, erp'),
            (11, 'Asana', 'Tech', 'Small/Medium', 'Web, Mobile', 'Project Tracking, Workflows', '$$', 'task management'),
            (12, 'Adobe XD', 'Design', 'Solo', 'Desktop', 'UI/UX Design, Prototyping', '$$', 'design'),
            (13, 'GitHub', 'Tech', 'Solo/Small', 'Web', 'Repos, CI/CD, Team Collaboration', 'Free', 'devops, version control'),
            (14, 'FreshBooks', 'Finance', 'Solo/Small', 'Web', 'Invoicing, Time Tracking', '$$', 'accounting, small business'),
            (15, 'Zoom', 'General', 'All Sizes', 'Web, Desktop', 'Video Conferencing, Chat', 'Free', 'communication')
        ]

        print("Inserting data into 'software' table...")
        insert_query = """
        INSERT INTO software (id, name, industry, team_size, platform, features, price, tags) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, software_data)
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

    except Error as e:
        print(f"Error during database setup: {e}")
        connection.rollback()
    finally:
        cursor.close()

if __name__ == '__main__':
    db_connection = create_connection()
    if db_connection:
        setup_database(db_connection)
        db_connection.close()
        print("Database connection closed.")

