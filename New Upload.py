import streamlit as st
from datetime import datetime
from pathlib import Path
from mysql.connector import Error
import base64
import classes as cl
import css_strings as cs

st.set_page_config(layout='wide', page_title='Beyond Heavens',
                   initial_sidebar_state='collapsed')

est_connection = cl.EstablishConnection()
connection = est_connection.database_connection()


def validate_current_name(filename):
    existing_records = fetch_existing_files()
    existing_filenames = [Path(record_file_name[0]).stem for
                          record_file_name in existing_records]
    return filename in existing_filenames


def fetch_existing_files():
    try:
        cursor = connection.cursor()
        records_query = "SELECT filename, content FROM videos"
        cursor.execute(records_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except Error as e:
        st.error(f"Error: {e}")
    return []


def edit_file_name(filename):
    # Create new file name with current date
    now = datetime.now()
    new_file_name = (file_name + '-' + str(now.month) +
                     '-' + str(now.day) + '-' + str(now.hour)
                     + str(now.minute))
    return new_file_name


# Create table to store video files
def create_video_table():
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


# Insert uploaded video file into database
def insert_video(file_name, encoded_content_str):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO videos (filename, content) VALUES (%s, %s)"
        cursor.execute(insert_query, (file_name, encoded_content_str))
        connection.commit()
        cursor.close()
        st.success(f"Video '{file_name}' inserted successfully")
    except Error as e:
        st.error(f"Error: {e}")


st.title('Upload a recorded video!')

uploaded_file = st.file_uploader("Browse files", type=['mp4', 'avi', 'mov'],
                                 key='file_picker', label_visibility='hidden')

css = cs.browse_files_btn_css

st.markdown(css, unsafe_allow_html=True)

if uploaded_file is not None:
    # Create videos table
    create_video_table()

    # Extract file name and content
    file_name = Path(uploaded_file.name).stem
    file_content = uploaded_file.read()

    # Validate if filename exists or not
    name_exists = validate_current_name(file_name)
    if name_exists:
        file_name = edit_file_name(file_name)

    encoded_content = base64.b64encode(file_content)
    encoded_content_str = encoded_content.decode('utf-8')

    insert_video(file_name, encoded_content_str)