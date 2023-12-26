import streamlit as st
import mysql.connector
from mysql.connector import Error
import base64


# Establish MySQL database connection
def database_connection(host="localhost", user="root", password="justdo!t",
                 database="local_data"):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
    return None


# Create video table if not exists
def create_video_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS videos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255),
            content LONGBLOB
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except Error as e:
        st.error(f"Error: {e}")


# Insert uploaded video into database
def insert_video(connection, file_name, encoded_content_str):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO videos (filename, content) VALUES (%s, %s)"
        cursor.execute(insert_query, (file_name, encoded_content_str))
        connection.commit()
        cursor.close()
        st.success(f"Video '{file_name}' inserted successfully")
    except Error as e:
        st.error(f"Error: {e}")


# Retrieve all videos from the database
def get_all_videos(connection):
    try:
        cursor = connection.cursor()
        select_query = "SELECT filename, content FROM videos"
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except Error as e:
        st.error(f"Error: {e}")
    return []


# Streamlit UI
st.set_page_config(layout="wide", page_title='Video App')
st.title('Upload and Watch Videos')

# Upload video files
uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov'], key='file_picker')

# Establish database connection
connection = database_connection()

# Check if the 'videos' table exists, if not, create it
if connection is not None:
    create_video_table(connection)

# Handle file upload and video insertion
if uploaded_file is not None:
    # Get file name
    file_name = uploaded_file.name

    # Read the uploaded file content
    file_content = uploaded_file.read()

    # Encode the file content
    encoded_content = base64.b64encode(file_content)
    encoded_content_str = encoded_content.decode('utf-8')

    # Insert video into the database
    insert_video(connection, file_name, encoded_content_str)

# Display 'Watch' buttons for each uploaded video
for filename, content in get_all_videos(connection):
    st.write(filename)
    watch_button = st.button(f"Watch {filename}")

    if watch_button:
        try:
            # Decode the base64-encoded content
            decoded_content = base64.b64decode(content)

            # Display the video
            st.video(decoded_content, format="video/mp4", start_time=0)
        except Exception as e:
            st.error(f"Error displaying video: {e}")

# Close the database connection
if connection is not None:
    connection.close()
