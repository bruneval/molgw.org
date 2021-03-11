import sys, os, subprocess, shutil

subprocess.run(['mkdocs', 'build','--clean'])
shutil.copyfile('site/articles/index.html','site/articles/old.html')
f = open('site/articles/old.html','r')
fnew = open('site/articles/index.html','w')
for line in f:
    if 'List to be filled here' not in line:
        fnew.write(line)
    else:
        f2 = open('articles.html','r')
        for line2 in f2:
            fnew.write(line2)
        f2.close()
            

f.close()
fnew.close()
os.remove('site/articles/old.html')

