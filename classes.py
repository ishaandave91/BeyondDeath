import os
import time
import streamlit as st
import mysql.connector
from mysql.connector import Error
from io import BytesIO
import base64


# Create MySQL database connection
class EstablishConnection:
    def __init__(self, host="localhost", user="root", password="justdo!t",
                 database="local_data"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def database_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            st.error(f"Error: {e}")
        return None


class Upload:
    def __init__(self):
        self.uploaded_file = st.file_uploader(" ", type=['mp4', 'avi', 'mov'],
                                              key='file_picker')

        css = '''
            <style>
                [data-testid='stFileUploader'] {
                    width: max-content;
                }
                [data-testid='stFileUploader'] section {
                    padding: 0;
                    float: left;
                }
                [data-testid='stFileUploader'] section > input + div {
                    display: none;
                }
                [data-testid='stFileUploader'] section + div {
                    float: right;
                    padding-top: 0;
                }

            </style>
            '''

        st.markdown(css, unsafe_allow_html=True)

        if self.uploaded_file is not None:
            # Extract file name and content
            self.file_name = self.uploaded_file.name
            file_content = self.uploaded_file.read()
            encoded_content = base64.b64encode(file_content)
            self.encoded_content_str = encoded_content.decode('utf-8')

            # Initiate connection to database
            est_connection = EstablishConnection()
            self.connection = est_connection.database_connection()

            self.insert_video()

    # Create table to store video files
    def create_video_table(self):
        try:
            cursor = self.connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS videos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                content LONGBLOB
            )
            """
            cursor.execute(create_table_query)
            self.connection.commit()

            # After table is created, insert the video
            insert_query = "INSERT INTO videos (filename, content) VALUES (%s, %s)"
            cursor.execute(insert_query, (self.file_name, self.encoded_content_str))
            self.connection.commit()
            cursor.close()
            self.connection.close()
            st.success(f"Video '{self.file_name}' inserted successfully")
        except Error as e:
            st.error(f"Error: {e}")

    # Insert uploaded video file into database
    def insert_video(self):
        try:
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO videos (filename, content) VALUES (%s, %s)"
            cursor.execute(insert_query, (self.file_name, self.encoded_content_str))
            self.connection.commit()
            cursor.close()
            self.connection.close()
            st.success(f"Video '{self.file_name}' inserted successfully")
        except Error as e:
            if e.errno == 1146:             # error number 1146 = table does not exist
                self.create_video_table()
            else:
                st.error(f"Error: {e}")


class Record:
    pass


class ViewUploaded:
    def __init__(self):
        # Initiate connection to database
        est_connection = EstablishConnection()
        self.connection = est_connection.database_connection()

        total_videos = self.count_existing_files()
        if total_videos > 0:
            st.title("Your Uploaded files:")
            self.existing_records = self.extract_records()
            self.render_video()

    def count_existing_files(self):
        try:
            cursor = self.connection.cursor()
            count_query = "SELECT count(*) FROM videos"
            cursor.execute(count_query)
            row_count = cursor.fetchall()[0][0]
            cursor.close()
            return row_count
        except Error as e:
            st.error(f"Error: {e}")
        return 0

    def extract_records(self):
        try:
            cursor = self.connection.cursor()
            records_query = "SELECT filename, content FROM videos"
            cursor.execute(records_query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error: {e}")
        return []

    def render_video(self):
        for filename, content in self.existing_records:
            st.write(filename)
            try:
                decoded_content = base64.b64decode(content)
                st.video(decoded_content, format="video/mp4", start_time=0)
            except Exception as e:
                st.error(f"Error encoding video content: {e}")
                return None


class Watch:
    pass


class RemoveFiles:
    pass
