#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  duplicate or close to duplicate file finder
  should determine file type and using interpreter read in file and check against all other files
  so each file would be compared against all others,
  files already checked would be tracked and not compared or compared against again
  making the search faster and faster the more files it processes.
  - added compedity would be to check by specific file ownership

  create groups of different file types to make searching faster by searching only files of the same type

  -what about files with the same name?

  the report at the end should list files with
    - greater similarity than 75%
    - and then the preferred file for each dupe set being the latest dated file
    
"""
import docx2txt  # pip install docx2txt
#import PyPDF2  # pip install PyPDF2
"""
if file type == doc or docx
my_text = docx2txt.process("test.docx")
print(my_text)

if type iso or any other archive type check md5 only

"""
import os, sys
from pwd import getpwuid #for getting user name of files
from itertools import chain
result = ''
search_path = ''
paths = []
sys.path.insert(0,'/Users/blainekuhn/Git/Python/md5-check/')
from check_md5 import   check_files
dic = {}

def check_for_dupes(*args):
  global search_path, dic
  search_path = args[0]
  path_verifier(search_path)
  print("returned")
  print(paths)
  print(search_path)
  dic = check_files(search_path, 'log_file')
  #print(dic)
  file_recurse(dic)
#  search_path = input("Please enter the path to search from. ")
  # verify path is actually a path and exit with message if not.
  if os.path.isfile(search_path):
    sys.exit(print("This is a single file, it's hard to find duplicates in a single file."))
  else:
    pass  # call function 'file_recurse()' to add all files to a list
    # file_recurse(search_path)


def path_verifier(search_path):  #works great
  if search_path[0:2] == './' or search_path[0] == '/':
    return search_path
  else:
    print("%s is not a path.  A path starts with './' or '/'." % search_path)
    sys.exit(print("Error in path_verifier"))


#check_for_dupes('./README.md')

def file_typer():
  import os
  pass


"""
TIP:
  create a list
    lst = ["kathryn", "katie", "katrina"]
  Pop them one by one by alphabetical order
    lst.pop(min(lst).index(min(lst)))
"""

files_md5 = []
file_lst  = []
working_lst = []
lst = []
username = 'blainekuhn'
fileList = []
subdirList = []
count = [0,0,0]
dirlist = []
reverse_dic = {}
dupes = {}
md5_dupes = {}
L1, L2 = [], []
doc_text = []
f1 = ''
f2 = ''
R1 = 0.0
R2 = 0.0

def file_recurse(dic):
  global file_lst, files_md5, md5_dupes, fileList, subdirList, dirlist, count, lst, dupes, reverse_dic
  import os
#  s_path = os.path.join(os.getcwd(), s_path).split()[0] = os.path.abspath(s_path)
  # wootwoot, got that one in 1 try.
  #remove entries from dic that start with . _ or ~
  for k, v in dic.items():
    key = k.split('/')
    for a in key:
      if len(a) > 0:
        #print("this is a %s" % a)
        if a[0] == '.' or a[0] == '_' or a[0] == '~':
          lst.append(k)
  for a in lst:
    #print(a)
    dic.pop(a)
  print(len(lst))
  lst = []
  #now check dic for file ownership and remove those not owned by current user
  for k,v in dic.items():
    user = getpwuid(os.stat(k).st_uid).pw_name
    if not user == username:
      lst.append(k)
#      lst[k] = v
      #dic.popitem()  #causes dictionary size change during iteration - bad
      #print(user)
  for k in lst:
    dic.pop(k)
  print("$$$$$$$$$$$$$$$$$$$$$$$")
  lst = []
  # now the dictionary has only files owned by username and none are hidden, temporary
  # find duplicates by md5_sum as found by    dic = check_files(search_path, 'log_file')
  #get duplicates by md5_sum and call it md5_dupes
  for k,v in dic.items():
    reverse_dic.setdefault(v, set()).add(k)
  for k,v in reverse_dic.items():
    if len(v) > 1:
      md5_dupes[k]=list(v)
 # sys.exit()
#now remove the md5_dupes from dic
  print(len(dic.values()))
  for k,v in md5_dupes.items():
    for a in v:
      dic.pop(a)
  #now for the hard part - find out files with more than 80% words in common for each file in dic
  #This no reads all files - just need to builds lists to compare contents to each other
  for a in dic:
    file = a
    file = file.split('.')
    #print(len(file))
    if len(file) == 2:
      if file[1] == 'docx':
        with open(a, 'r') as f:
          data = docx2txt.process(a)
          doc_text.append((a,data))
          #print("#####",a,'\t', data)
    else:
      #print(a)
      with open(a, 'r') as f:
        #print(a)
        data = f.read()
        doc_text.append((a,data))
        #print("$$$$$$",a,'\t', data)

  for a in range(len(doc_text)):  #send the text of the doc not the doc name so. doc_text[a][1]
    file1 = doc_text[a][1]
    for b in range(1, len(doc_text)):
      print("\nFile1 is %s" % doc_text[a][0])
      file2 = doc_text[b][1]
      print("\nFile2 is %s" % doc_text[b][0])
      rate = find_80percent(file1, file2, doc_text[b])
      sys.exit()
  
    
    

def find_80percent(file1, file2, file):
  global L1, L2,f1, f2, R1, R2
  f1 = file1
  f2 = file2
  file = file[0]

  for w2 in f2.split():
    for w1 in f1.split():
      if w2 == w1:
          L2.append(w1)
          print("Comparing w1: '%s' to w2: %s" % (w1,w2))
      else:
          L1.append(w2)
    print("$$$$$$$$$")
    if len(L1) < len(L2):
      R2 = len(L1)/len(L2)
      #print("this is R1 %s"% R1)
    else:
      R1 = len(L2)/len(L1)
      #print("this is R2 %s"% R2)
    print("\t\t\t\tClearing L1 and L2")
    print("this is R1 %s"% R1)
    print("this is R2 %s"% R2)
    L1, L2 = [], []
    if R1 > R2:
      print("printing file %s" % file)
      lst.append((file,R1))
    else:
      lst.append((file,R2))

#*******************




  return md5_dupes
  sys.exit()


check_for_dupes('/Users/blainekuhn/Documents/1Job Hunt/LHH/ReWorked')

#check_for_dupes('/Users/blainekuhn/Git/Python/Basics')


def old_try():  #could eventually be usable??? Trying to make use of md5_checker to build file and md5 list
  for dirName, subdirList, fileList in os.walk(s_path):
    #print(len(fileList))
    fileList = [f for f in fileList if not f[0] == '.']
    subdirList = [d for d in subdirList if not d[0] == '.' or not d[0] == '_']
    dirlist = subdirList
    print("this is dirlist \t%s" % dirlist)
    print("this is subdirList \t%s\n" % subdirList)
    for d in subdirList:
      print("This is d %s" % d)
      print("this is subdirList %s" % subdirList)
      first_char = d[0]
      if first_char == '_' or first_char == '.':
        index = subdirList.index(d)
        print("----## %s \t%s" % (d, index))
        print(subdirList)
        print("\tThis directory was popped, %s" % dirlist.pop(index))
      else:
         count[1].append()

    print(subdirList)
    return subdirList
    sys.exit()
    working_lst = subdirList
     # for dirname in subdirList:
        
      
    print(len(subdirList))
 


    for fname in fileList:
      #print("the file name is %s" % fname)
      index = fileList.index(fname)
      #print("the file name is %s" % fileList[index])
      filename = os.path.join(dirName,fname)
      if username == getpwuid(os.stat(filename).st_uid).pw_name:
        #print("%%%%%%")
        file_lst.append(filename)
  working_lst = file_lst
  sys.exit(print("This is the END file_lst %s" % len(file_lst)))
  working_lst = file_lst
  for a in working_lst:
    index = file_lst.index(a)
    files_md5.append((file_lst[index], checksum_md5(file_lst[index])))
    #print(files_md5)
    for a, b in files_md5: #get md5_sum if files are same name     
      index = files_md5.index((a,b))
      #print("$$$checking is: %s" % (index))
      #files_md5.pop(files_md5.index((a,b)))
      for c, d in files_md5:
        if a != c and b == d:
  #        if b in c and a not in c:
            print("-----%s %s" % (a,b),(c,d))
            lst.append((a,b))
            print(len(lst))  #lst contains duplicate md5sums while files are in different folders

          
          
  print(len(files_md5))
  return files_md5






















