# https://docs.python.org/3/library/xml.etree.elementtree.html
# http://lxml.de


# srcml command:  srcml FP2-Launcher -o fp2-launcher.xml

#fill database per class in comment_class
# fill db per comment in processed_comment

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

ns = {'srcml': 'http://www.srcML.org/srcML/src'}

tree = etree.parse('fp2-launcher.xml')
root = tree.getroot()

f = open('out.txt','w')
f.write('hello world \n')


# prints all comments within an element, including its children
def printAllCommentInfo (file, fileln, precommentlength) :
    for comment in file.iter("{http://www.srcML.org/srcML/src}comment"):
        ctext = comment.text
        ctype = comment.get('type')
        cformat = comment.get('format')
        clinenr = comment.sourceline - fileln + 1 + precommentlength
        cendlinenr = clinenr + (len(etree.tostring(comment).strip().splitlines()) - 1)
        nextElt = comment.getnext()
        print("type: ", ctype, ", format: ", cformat)
        f.write("type: "+str(ctype)+", format: "+str(cformat)+'\n')
        print("ln: ", clinenr, " to ", cendlinenr)
        f.write("ln: "+str(clinenr)+" to "+str(cendlinenr)+ '\n')
        print(ctext)
        f.write(ctext+'\n')
        print("")
        f.write('\n')

def printAllClasses (file, fileln, precommentlength) :
    i = 0
    for cl in file.iter("{http://www.srcML.org/srcML/src}class"):
        if cl.find('{http://www.srcML.org/srcML/src}name') != None:
            i+=1
            clName = cl.find('{http://www.srcML.org/srcML/src}name').text
            print(clName)
            print("number of classes: ",i)
            printAllMethods(cl, fileln, precommentlength)
            if i >1:
                print("WARNING!")


# finds methods within an element, including its childeren
def printAllMethods (file, fileln, precommentlength) :
    for method in file.iter("{http://www.srcML.org/srcML/src}function"):
        mname = method.find('{http://www.srcML.org/srcML/src}name').text
        mblock = method.find('{http://www.srcML.org/srcML/src}block')
        mlinenr = method.sourceline - fileln + 1 + precommentlength
        mendlinenr = mlinenr + (len(etree.tostring(method).strip().splitlines()) - 1)
        print("Method name: ", mname)
        f.write("Method name: "+mname+'\n')
        print("ln: ", mlinenr, " to ", mendlinenr)
        f.write("ln: "+str(mlinenr)+" to "+str(mendlinenr)+'\n')
        prevItemList = []
        #The siblings (or neighbours) of an element are accessed as next and previous elements
        prevItem = method.getprevious()
        getnextprev = 0
        while prevItem != None:
            if prevItem.tag == "{http://www.srcML.org/srcML/src}comment":
                getnextprev = getnextprev + 1
                prevItemList.append(prevItem)
                prevItem = prevItem.getprevious()
            else:
                print("Preceding comments: ", getnextprev)
                f.write("Preceding comments: "+ str(getnextprev)+'\n')
                break
        prevItemList.sort(key=lambda x: x.sourceline)
        for x in prevItemList:
            ctext = x.text
            ctype = x.get('type')
            cformat = x.get('format')
            clinenr = x.sourceline - fileln + 1 + precommentlength
            cendlinenr = clinenr + (len(etree.tostring(x).strip().splitlines()) - 1)
            print("type: ", ctype, ", format: ", cformat)
            f.write("type: " + str(ctype) + ", format: " + str(cformat) + '\n')
            print("ln: ", clinenr, " to ", cendlinenr)
            f.write("ln: " + str(clinenr) + " to " + str(cendlinenr) + '\n')
            print(ctext)
            f.write(ctext + '\n')
            print("")
            f.write('\n')
        print("Comments inside method block:")
        f.write("Comments inside method block:"+'\n')
        printAllCommentInfo(mblock, fileln, precommentlength)
        print("--------------------------------------------------------------")
        f.write('\n'+"--------------------------------------------------------------"+'\n')

# main loop
file_counter = 0
for file in root.iter("{http://www.srcML.org/srcML/src}unit"):
    filename = str(file.get('filename'))
    filepath = "FP2-Launcher/src/"
    if filename[:len(filepath)] == filepath :
        file_counter = file_counter+1
        print("==============================================================")
        f.write("=============================================================="+'\n')
        print("File name: ", file.get('filename'))
        f.write("File name: "+ file.get('filename')+'\n')
        pkg = file.find("{http://www.srcML.org/srcML/src}package")
        #pkgln = pkg.sourceline
        #fileln = file.sourceline
        if pkg != None:
            fileln = pkg.sourceline
        else:
            fileln = file.sourceline
        precommentlength = 0
        if file[0].tag == "{http://www.srcML.org/srcML/src}comment":
            precommentlength = (len(etree.tostring(file[0]).strip().splitlines()))
        print("Precomment length: ",precommentlength)
        #fileln = file.sourceline  #first comment before package always takes 1 line
        fileln_end = fileln + (len(etree.tostring(file).strip().splitlines()) - 1)
        print("ln: "," to ",fileln_end)
        f.write(str("ln: "+str(fileln)+" to "+str(fileln_end)+"\n"))
        print("--------------------------------------------------------------")
        f.write("--------------------------------------------------------------"+'\n')
        #printAllCommentInfo(file, fileln)
        printAllClasses(file, fileln, precommentlength)
        #printAllMethods(file, fileln, precommentlength)
        print("\n")
        f.write('\n')
print('PROJECT END')
f.write('PROJECT END'+'\n')
print("number of files: ",file_counter)
f.write("number of files: "+str(file_counter)+'\n')

f.close()

# obseravations on comment line numbers:
# It seems that block or javadocs lines are seen as single line
# problematic for comments at start of file, and javadoc comments before functions
# block comment src line indicates the final line, but not always.
# src lines on comments is unreliable.
# Once corrected for the comment at start of file, method srclines seem fine.