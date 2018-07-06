# SATD2018
CAPITA project by Mark Frenken on SATD.

## How to use
### 1. Set up the database.
Use the Maldonado database or create a new database with the required tables specified in the database section below.
### 2. Set up the database.
Use the Maldonado database or create a new database with the required tables specified in the database section below.
### 3. Extract comments from a project using srcML.
3.1. Download and install srcML: https://www.srcml.org
3.2. Use srcML to store the entire project

Command: srcml android-oss -o android-oss.xml

Some have already been included in the the projects folder.
### 4. Insert comments to database.
In py_scripts/ you can find extract_comments.py
### 5. Populate treated_commenttext.
populate_treated_commenttext.py
### 6. Classify comments manually.
Use the labeling_turorial.md found in documentation/.
### 7. Run classify_comments.py to check performance of the classifier.
Results are stored in classifier/output/. 
- classified_seq.test
- output.txt
- results.txt

## Database
