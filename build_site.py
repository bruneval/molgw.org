import sys, os, subprocess, shutil
import rispy

subprocess.run(['mkdocs', 'build','--clean'])
shutil.copyfile('site/articles/index.html','site/articles/old.html')


#
# Transform RIS file to html
#
filepath = "molgw_biblio.ris"
with open(filepath, 'r') as bibliography_file:
    entries = rispy.load(bibliography_file)

print("{} entries found in the RIS file".format(len(entries)))

fhtml = open('out.html','w')
fhtml.write("<ol reversed>\n\n")
for entry in entries:
    #debug
    #for k in entry.keys():
    #    print(k,entry[k])
    string = '    <li>\n        '
    try:
        authors = entry['first_authors'] + entry['authors']
    except:
        authors = entry['authors']
    for i,author in enumerate(authors):
        last_name   = author.split(',')[0]
        first_names = author.split(',')[1]
        initials = ''
        for n in first_names.split(" "):
            if len(n) > 0:
                initials +=  n[0] + '. '
        #if i == len(entry['authors'])-1:
        #    string += initials + last_name + " "
        #else:
        #    string += initials + last_name + ", "
        string += initials + last_name + ", "
    try:
        string += entry['journal_name'] 
    except:
        string += entry['alternate_title2'] 
    string += " <b>" + entry['volume'] + "</b>, "
    string +=         entry['start_page']
    year = entry['year'].split("/")[0]
    string += " (" + year + "). <br>\n"
    string += "        <a href=http://dx.doi.org/" + entry['doi'] + ">"
    try:
        string += entry['primary_title'] + "</a>\n"
    except:
        string += entry['title'] + "</a>\n"
    string += "    </li>\n\n"

    #print(string)
    fhtml.write(string)

#fhtml.write("</ol>\n")
fhtml.close()


#
# Merge the two html files for mkdocs and from rispy
#
f = open('site/articles/old.html','r')
fnew = open('site/articles/index.html','w')
for line in f:
    if 'List to be filled here' not in line:
        fnew.write(line)
    else:
        f2 = open('out.html','r')
        for line2 in f2:
            fnew.write(line2)
        f2.close()
        f2 = open('articles.html','r')
        for line2 in f2:
            fnew.write(line2)
        f2.close()
            

f.close()
fnew.close()
os.remove('site/articles/old.html')
os.remove('out.html')

