# srcml command:  srcml FP2-Launcher -o fp2-launcher.xml

#fill database per class in comment_class
# fill db per comment in processed_comment

import psycopg2

# etree extension for line numbers
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

# Database login variables
password = "111111"#sys.argv[1]
username = 'postgres'
dbname = 'postgres'

# load element tree
tree = etree.parse('fp2-launcher.xml')
root = tree.getroot()

project_name = "fp2-launcher"

try:
    connection = None

    # connect to the database
    connection = psycopg2.connect(host='localhost', port='5432', database=dbname, user=username, password=password)
    cursor = connection.cursor()

    file_counter = 0

    # get proper key for comment_class
    cursor.execute("select max(id) from comment_class")
    cl_key = cursor.fetchone()[0]

    # get proper key for processed_comment
    cursor.execute("select max(id) from processed_comment")
    comment_key = cursor.fetchone()[0]

    for file in root.iter("{http://www.srcML.org/srcML/src}unit"):
        # Prevent iterating over files with Nonetype name
        if file.get('filename')!= None:
            file_name = str(file.get('filename'))
            file_path = "FP2-Launcher/src/"

            # Only include files from the src folder
            if file_name[:len(file_path)] == file_path:
                file_counter += 1

                # For correct line numbering
                pkg = file.find("{http://www.srcML.org/srcML/src}package")
                if pkg != None:
                    file_start = pkg.sourceline
                else:
                    file_start = file.sourceline

                # Set end line of file
                file_end = file_start + (len(etree.tostring(file).strip().splitlines()) - 1)

                # Check if file starts with comment, for correct line numbering
                add_lines = 1
                if file[0].tag == "{http://www.srcML.org/srcML/src}comment":
                    add_lines += (len(etree.tostring(file[0]).strip().splitlines()))+1

                # Iterate over classes in file.
                for cl in file.iter("{http://www.srcML.org/srcML/src}class"):
                    # Prevent iterating over classes with Nonetype name
                    if cl.find('{http://www.srcML.org/srcML/src}name') != None:
                        # Class name, start line, end line
                        cl_name = cl.find('{http://www.srcML.org/srcML/src}name').text
                        cl_start = cl.sourceline - file_start + add_lines
                        cl_end = cl_start + (len(etree.tostring(cl).strip().splitlines()) - 1)

                        # Increment comment_class table key, will be decremented if no comments are found
                        cl_key += 1

                        # Check if class contains comments
                        comment_found = False

                        # Iterate over methods
                        for method in cl.iter("{http://www.srcML.org/srcML/src}function"):
                            # Method name, start line, end line
                            method_name = method.find('{http://www.srcML.org/srcML/src}name').text
                            method_start = method.sourceline - file_start + add_lines
                            method_end = method_start + (len(etree.tostring(method).strip().splitlines()) - 1)

                            # Container for all comments of this method
                            method_comments = []

                            # Check for preceding comments
                            prevItem = method.getprevious()
                            while prevItem != None:
                                if prevItem.tag == "{http://www.srcML.org/srcML/src}comment":
                                    method_comments.append(prevItem)
                                    prevItem = prevItem.getprevious()
                                else:
                                    break

                            # Sort preceding comments by sourceline
                            method_comments.sort(key=lambda x: x.sourceline)

                            # Method body
                            method_block = method.find('{http://www.srcML.org/srcML/src}block')

                            # Check for comments in method body
                            for comment in method_block.iter("{http://www.srcML.org/srcML/src}comment"):
                                method_comments.append(comment)

                            # Iterate over comments and insert
                            for comment in method_comments:
                                # Comment was found
                                comment_found = True

                                comment_text = comment.text.replace('\'','').replace('\"', '')
                                comment_text_treated = " ".join(comment_text .lower().replace('\n','').replace('\r\n', '').replace('\r', '').replace('\t', '').replace('//','').replace('/**','').replace('*/','').replace('/*','').replace('*','').replace(',','').replace(':','').replace('...','').replace(';','').split())
                                comment_type = comment.get('type')
                                comment_format = comment.get('format')
                                comment_start = comment.sourceline - file_start + add_lines
                                comment_end = comment_start + (len(etree.tostring(comment).strip().splitlines()) - 1)

                                # Increment comment_key
                                comment_key += 1

                                # Insert into processed_comment
                                query = str(
                                    "insert into processed_comment (id,commentclassid,startline,endline,commenttext,type,description,classification,treated_commenttext) values (" +
                                    str(comment_key) + "," +
                                    str(cl_key) + "," +
                                    str(comment_start) + "," +
                                    str(comment_end) + ",'" +
                                    comment_text + "','" +
                                    comment_type + "','" +
                                    method_name + "','" +
                                    "UNKNOWN" + "','" +
                                    comment_text_treated + "')"
                                )
                                cursor.execute(query)
                                connection.commit()
                                #print(query)

                        # insert class into comment_class
                        if comment_found:
                            query = str(
                                "insert into comment_class (id,projectname,filename,classname,startline,endline) values (" +
                                str(cl_key)+ ",'" +
                                project_name + "','" +
                                file_name + "','" +
                                cl_name + "'," +
                                str(cl_start) + "," +
                                str(cl_end) + ")"
                            )
                            cursor.execute(query)
                            connection.commit()
                            #print(query)
                        else:
                            # Decrement key since no class was added.
                            cl_key -= 1
    print("Finised")

except Exception as e:
    print(e)
    raise e