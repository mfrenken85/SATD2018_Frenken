#!/usr/bin/python

import psycopg2

####################################################################################################
# SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS #
####################################################################################################

# Script originally from https://github.com/maldonado/tse2015_td_identification, modified by Mark Frenken
# This script populates the treated_commenttext column in processed_comment table.
# treated_commenttext is required for using serialized_classifier_tenfold.ser.gz.

# Database login
dbhost = 'localhost'
dbport = '5432'
dbname = 'postgres'
username = 'postgres'
password = '111111'

# Set to True for updating the database, set to False for printing the queries
insert_into_db = False

####################################################################################################
####################################################################################################


# connect to the database 
connection = psycopg2.connect(host=dbhost, port=dbport, database=dbname, user=username, password=password)
cursor = connection.cursor()

cursor.execute("select commenttext, id from processed_comment")
processed_comment_list = cursor.fetchall()

formatted_comment_list = []
formatted_comment_id_list = []

for processed_comment in processed_comment_list:
    formatted_comment = " ".join(processed_comment[0].lower().replace('\n','').replace('\r\n', '').replace('\r', '').replace('\t', '').replace('//','').replace('/**','').replace('*/','').replace('/*','').replace('*','').replace(',','').replace(':','').replace('...','').replace(';','').split())
    formatted_comment_list.append(formatted_comment)
    formatted_comment_id_list.append(processed_comment[1])

print('inserting data ...')
largest_id = 0
progress_counter = 0
total_comments = len(formatted_comment_id_list)
for x in range(0, total_comments):
    progress_counter = progress_counter + 1
    query = str("update processed_comment set treated_commenttext = '" + formatted_comment_list[x] + "' where id = " + str(formatted_comment_id_list[x]))
    if insert_into_db:
        cursor.execute(query)
        connection.commit()
    else:
        print(query)
    print(str(progress_counter) + ' out of : ' + str(total_comments))
print('done')