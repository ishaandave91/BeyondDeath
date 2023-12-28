import os
from datetime import datetime
from pathlib import Path
import streamlit as st
import mysql.connector
from mysql.connector import Error
from io import BytesIO
import base64
import css_strings as cs


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


class ValidateFilename():
    def __init__(self, filename):
        self.filename = filename
        est_connection = EstablishConnection()
        self.connection = est_connection.database_connection()
        self.existing_records = self.fetch_existing_files()
        self.name_exists = self.validate_current_name()

    def fetch_existing_files(self):
        try:
            cursor = self.connection.cursor()
            records_query = "SELECT filename, content FROM videos"
            cursor.execute(records_query)
            records = cursor.fetchall()
            cursor.close()
            return records
        except Error as e:
            st.error(f"Error: {e}")
        return []

    def validate_current_name(self):
        existing_filenames = [Path(record_file_name[0]).stem for record_file_name in self.existing_records]
        return self.filename in existing_filenames


class Upload:
    def __init__(self):
        self.uploaded_file = st.file_uploader("Browse files", type=['mp4', 'avi', 'mov'],
                                              key='file_picker',
                                              label_visibility='hidden')

        css = cs.browse_files_btn_css

        st.markdown(css, unsafe_allow_html=True)

        if self.uploaded_file is not None:
            # Extract file name and content
            self.file_name = Path(self.uploaded_file.name).stem
            file_content = self.uploaded_file.read()

            # Validate if filename exists or not
            validate_upload_filename = ValidateFilename(self.file_name)
            name_exists = validate_upload_filename.name_exists
            if name_exists:
                self.file_name = self.edit_file_name()

            encoded_content = base64.b64encode(file_content)
            self.encoded_content_str = encoded_content.decode('utf-8')

            # Initiate connection to database
            est_connection = EstablishConnection()
            self.connection = est_connection.database_connection()

            self.insert_video()

    def edit_file_name(self):
        # Create new file name with current date
        now = datetime.now()
        new_file_name = (self.file_name + '-' + str(now.month) +
                         '-' + str(now.day) + '-' + str(now.hour)
                         + str(now.minute))
        return new_file_name

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
            self.connection.close()
        else:
            self.connection.close()

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
            cursor.close()
            return records
        except Error as e:
            st.error(f"Error: {e}")
        return []

    def render_video(self):
        for filename, content in self.existing_records:
            try:
                button_name = filename
                watch_btn_key = f'watch_btn_{filename}'
                watch_button_clicked = st.button(f"Watch: {button_name}", use_container_width=True,
                                                 key=watch_btn_key)
                if watch_button_clicked:
                    decoded_content = base64.b64decode(content)
                    video_frame = st.video(decoded_content, format="video/mp4", start_time=0)
                    close_btn_key = f'close_vid_{filename}'
                    close_button_clicked = st.button("Close", use_container_width=True,
                                                     key=close_btn_key)
                    if close_button_clicked:
                        del close_button_clicked
                        del video_frame
            except Exception as e:
                st.error(f"Error encoding video content: {e}")
                return None


class Watch:
    pass


class RemoveFiles:
    pass
