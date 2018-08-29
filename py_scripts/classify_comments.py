import os
import psycopg2
import subprocess
from subprocess import PIPE

####################################################################################################
# SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS # SETTINGS #
####################################################################################################

# Script originally from https://github.com/maldonado/tse2015_td_identification, modified by Mark Frenken
# This script classifies comments using a serialized classifier.
# To use this script, correctly set the variables in this section

# Database login
dbhost = 'localhost'
dbport = '5432'
dbname = 'postgres'
username = 'postgres'
password = '111111'

# Specify the projectname as referred to in the database
project = "VocableTrainer-Android"  # Example: "android-oss"

####################################################################################################
####################################################################################################

loc_classifier = os.path.expanduser("../classifier/")
serialized_classifier = "serialized_classifier_tenfold.ser.gz"

execution_options = {1: {'DOCUMENTATION', 'DESIGN', 'DEFECT', 'IMPLEMENTATION', 'TEST', 'WITHOUT_CLASSIFICATION'},
                     2: {'DEFECT', 'WITHOUT_CLASSIFICATION'},
                     3: {'DESIGN', 'WITHOUT_CLASSIFICATION'},
                     4: {'DOCUMENTATION', 'WITHOUT_CLASSIFICATION'},
                     5: {'IMPLEMENTATION', 'WITHOUT_CLASSIFICATION'},
                     6: {'TEST', 'WITHOUT_CLASSIFICATION'},
                     7: {'UNKNOWN'}
}

# create the files used by the stanford classifier, train and test both.
def write_classifier_file(file_name, result):
    with open (file_name,'a') as classified_seq:
        for line in result:
            classified_seq.write("{0}\t{1}\t{2}\n".format(line[0], line[1].replace('\n','').replace('\r\n', '').replace('\r', ''), line[2]))
        classified_seq.close()

def write_output_file(file_name, output):
    with open (file_name,'a') as classified_seq:
        for line in output:
            classified_seq.write(line)
        classified_seq.close()

try:
    connection = None

    # connect to the database
    connection = psycopg2.connect(host=dbhost, port=dbport, database=dbname, user=username, password=password)
    cursor = connection.cursor()

    # Remove previous output files.
    subprocess.call(["rm", loc_classifier + "output/output.txt"])
    subprocess.call(["rm", loc_classifier + "output/results.txt"])
    subprocess.call(["rm", loc_classifier + "output/classified_seq.test"])

    for td_type in execution_options[7]: # For now just query UNKNOWN
        # When using serialized_classifier_tenfold.ser.gz, query a.treated_commenttext
        # When using serialized_classifier.ser.gz, query a.commenttext
        cursor.execute(
            "select a.classification, a.treated_commenttext, a.id from processed_comment a, comment_class b "
            "where a.commentclassid = b.id  and b.projectname like '%" + project + "%' and a.classification = '"+td_type+"'")
        write_classifier_file(loc_classifier + "output/classified_seq.test", cursor.fetchall())

    print("Analysis started for " + project)
    output = subprocess.Popen([
        "java -jar " + loc_classifier + "stanford-classifier.jar -loadClassifier " +
        loc_classifier + serialized_classifier + " -testFile " +
        loc_classifier + "output/classified_seq.test"],
        stdout=PIPE, stderr=PIPE, shell=True).communicate()
    #serialized_classifier.ser.gz

    print("Analysis finished")
    write_output_file(loc_classifier + "output/output.txt", output[0].strip().decode("utf-8"))
    write_output_file(loc_classifier + "output/results.txt", output[1].strip().decode("utf-8"))

except Exception as e:
    print(e)
    raise e