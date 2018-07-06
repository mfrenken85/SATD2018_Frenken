# SATD2018
CAPITA project by Mark Frenken on SATD.

## How to use
### 1. Set up the database.
Either use the Maldonado database or create a new database and create the required tables specified in tables.sql.
### 2. Extract comments from a project using srcML.
Some have already been included in the the projects folder.
### 3. Insert comments to database.
In py_scripts/ you can find extract_comments.py
### 4. Populate treated_commenttext.
populate_treated_commenttext.py
### 5. Classify comments manually.
Use the labeling_turorial.md found in documentation/.
### 6. Run classify_comments.py to check performance of the classifier.
Results are stored in classifier/output/. 
- classified_seq.test
- output.txt
- results.txt
