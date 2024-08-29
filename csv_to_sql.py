import pandas as pd
import os
import random, string, re # to generate random table name if necessary

def infer_sql_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'NUMERIC(10,2)'  # Defaulting to numeric with precision
    elif pd.api.types.is_string_dtype(dtype):
        return 'VARCHAR(255)'  # Defaulting to VARCHAR with length 255
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'TEXT'

def guess_table_name(csv_file):
    '''
    Create a table name from CSV file name and convert it to be table name
    allowed by slite3 documentation.
    '''
    # when in CSV file name there are letters too
    regex = re.compile('[^a-zA-Z]')
    table_name = csv_file.split("/")[-1].split(".")[0]
    table_name = regex.sub('', table_name)

    # when in CSV file name there aren't any letters
    if table_name == '':
        for _ in range(10):
            table_name += random.choice(string.ascii_lowercase)
    return table_name

def csv_to_sql(csv_file_path, actual_file_name) -> str:
    # Guess the table name from the CSV file name
    print(actual_file_name)
    table_name = guess_table_name(actual_file_name)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Check if any column has unique values across all rows
    primary_key_column = None
    for column in df.columns:
        if df[column].is_unique and df[column].notna().all():
            primary_key_column = column
            break
    
    # If no column has unique values, add an Id column and use it as the primary key
    if primary_key_column is None:
        df.insert(0, 'Id', range(1, len(df) + 1))
        primary_key_column = 'Id'
    
    # Generate the SQL schema
    sql_schema = f"CREATE TABLE {table_name}(\n"
    
    for column in df.columns:
        sql_type = infer_sql_type(df[column].dtype)
        if column == primary_key_column:
            sql_schema += f"   {column} {sql_type} NOT NULL PRIMARY KEY,\n"
        else:
            sql_schema += f"   {column} {sql_type},\n"
    
    # Remove the last comma and close the schema statement
    sql_schema = sql_schema.rstrip(",\n") + "\n);\n\n"
    
    # Generate the SQL data insertion statements
    sql_data = ""
    for _, row in df.iterrows():
        values = ', '.join(
            ["'{}'".format(str(value).replace("'", "''")) if not pd.isna(value) else 'NULL' for value in row]
        )
        sql_data += f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values});\n"
    
    # Determine the SQL file path in the current directory
    sql_file_name = f"{table_name}.sql"
    sql_file_path = os.path.join(os.getcwd(), sql_file_name)
    # print(sql_schema)
    # print(sql_data)
    # Write the schema and data to the SQL file
    with open(sql_file_path, 'w') as sql_file:
        sql_file.write(sql_schema)
        sql_file.write(sql_data)
    
    # Return the file path of the created SQL file
    return sql_file_path


#%%Test Functions
# csv_file_path = './Points Data - Sheet1.csv'
# csv_to_sql(csv_file_path = csv_file_path)
