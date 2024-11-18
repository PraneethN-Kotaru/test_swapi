import os
from traceback import print_tb

import pandas as pd

from src.models import Script

def read_and_insert_files_from_directory(directory_path, session):
    # Iterate through the directory and read files
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)

            # Read the file into a DataFrame, skipping the first line
            df = pd.read_csv(file_path, delimiter=" ", quotechar='"', header=None, skiprows=1, escapechar='\\')

            # Add the filename and first value (from each row) to the DataFrame as new columns
            df['script_name'] = filename
            df.columns = ['line_number', 'character', 'dialogue', 'script_name']
            # Insert rows into the database
            for _, row in df.iterrows():
                print(row)
                record = Script(**row.to_dict())
                session.add(record)

    # Commit all changes at once
    session.commit()