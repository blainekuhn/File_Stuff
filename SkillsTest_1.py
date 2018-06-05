

"""
  This problem was in a test I had once.  I was to see how many characters off the words are from being
  a palindrome
"""

m = 'abba'
n = 'abba'

o = 'abdba'
p = 'abdda'

e = 'this is a string'
f = 'dhis  s a strin '

count = [0]
s = 0

def return_it(a,b):
  global count, s
  if a == b:
    print("a:%s and \nb:%s" % (a, b))
    return 0

  if len(a) >= len(b):
    count[0]+= (len(a) - len(b))
    s = len(a)
    
  if  len(a) < len(b):
    count[0]+= (len(b) - len(a))
    s = len(b)

  print(s, count[0])

  for d in range(s-count[0]):
    if a[d] == b[d]:
      pass
    else:
      count[0] += 1
  print(a)
  print(b)
  print(count[0])
  return count[0]
  
return_it(o,p)
