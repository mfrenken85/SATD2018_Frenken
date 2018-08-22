import psycopg2

####################################################################################################
# SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS #
####################################################################################################

# Script merges subsequent line comments

# To use this script, correctly set the variables in this section

# Database login
dbhost = 'localhost'
dbport = '5432'
dbname = 'postgres'
username = 'postgres'
password = '111111'

# Specify the projectname to be inserted in comment_class table
project_name = "android-oss"  # Example: "android-oss"

# Set to True for inserting into the database, set to False for printing the queries
insert_into_db = False

####################################################################################################
####################################################################################################

try:
    connection = None

    # connect to the database
    connection = psycopg2.connect(host=dbhost, port=dbport, database=dbname, user=username, password=password)
    cursor = connection.cursor()

    print("Finised")

except Exception as e:
    print(e)
    raise e