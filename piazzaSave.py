from piazza_api import Piazza
import time
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def clean(str):
  return  cleanhtml(str.replace('&#43;', '+').replace('&#96;', '`').replace('\\', '\\\\').replace('&#64;', '@').replace('&amp;', '&').replace('&#34;', "''").replace('&#39;', "'").replace('&gt;', "\\textgreater{}").replace('&lt;', "\\textless{}").replace('&', '\\&').replace('#', '\\#').replace('_', '\_').replace('$', '\$').replace('^', '\^{}'))
  
p = Piazza()
p.user_login()
class_id = "CLASSID"
course_piazza = p.network(class_id)

posts = []

feed = course_piazza.get_feed(limit=2, offset=0)
cids = [post['id'] for post in feed["feed"]]
for cid in cids:
  time.sleep(3)
  p = course_piazza.get_post(cid)
  print(p)
  posts.append(p)

text = ""
print ("Working...")
for post in reversed(list(posts)):
  subject = clean(post['history'][0]['subject'])
  text += "\\section*{" + str(post['nr']) + ": " + subject + "}\n"
  if len(post['children']) > 0:
    text += "\\subsection*{Question}\n"
    text += clean(post['history'][0]['content']) + "\n"
    for child in post['children']:
      if 'history' in child:
        if child['type'] == 's_answer':
          text += "\\subsection*{Student Answer}\n"
          text += clean(child['history'][0]['content']) + "\n" 
        elif child['type'] == 'i_answer':
          text += "\\subsection*{Instructor Answer}\n"
          text += clean(child['history'][0]['content']) + "\n" 
      elif child['type'] == 'followup':
        text += "\\subsection*{Followup}\n"
        text += clean(child['subject']) + "\n" 
        for inner_child in child['children']:
          if inner_child['type'] == 'feedback':
            text += "\\subsubsection*{Feedback}\n"
            text += clean(inner_child['subject']) + "\n" 
  elif 'no_answer' in post and post['no_answer'] == 1:
    text += "\\subsection*{Question}\n"
    text += clean(post['history'][0]['content']) + "\n"
    text += "\\subsection*{**No Answer**}\n"
  elif clean(post['history'][0]['content']) != "":
    text += "\\subsection*{Note}\n"
    text += clean(post['history'][0]['content']) + "\n"
print(text)
f = open("piazza-" + class_id + ".txt", "w+")
f.write(text)
f.close()
