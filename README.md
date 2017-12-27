# Overview
This Library is used to Get and Post Wiki content to mediawiki framework. 
This library works on self hosted and public mediawiki.

bug: For now this library only works on existing page

# Installation
1. Install python-pip
```
$ sudo apt install python-pip
```
2. Clone repo
```
$ git clone https://github.com/icesourceg/pycWiki.git
```

3. Install requirements and install package
```
$ cd pycWiki
$ pip install -r requirements
$ sudo python setup.py install
```

# Usage Example
## Login
```
from pycWiki import pycWiki
oWiki = pycWiki.pycWiki()
oWiki.username = "icesourceg25"
oWiki.domain = ""
oWiki.wiki_url = "https://www.mediawiki.org/w/api.php"
oWiki.password = "Pranata25"
oWiki.wiki_login()

'''


## Get Page
```
... # login

json_output = oWiki.wiki_getPage("User:Icesourceg25")
print json_output

output:
{u'batchcomplete': u'', u'query': {u'pages': {u'729872': {u'ns': 2, u'pageid': 729872, u'revisions': [{u'*': u'My pAge', u'contentmodel': u'wikitext', u'contentformat': u'text/x-wiki'}], u'title': u'User:Icesourceg25'}}}}

```

## Post Page
```
... # login

pagename = "User:Icesourceg25"
summary = "This is for summary"
content = "This is the content for my Page"
section = 0

output = oWiki.wiki_postPage(pagename, summary, content, section)
print output

output:
{u'edit': {u'pageid': 729872, u'title': u'User:Icesourceg25', u'newtimestamp': u'2017-12-27T17:42:13Z', u'contentmodel': u'wikitext', u'result': u'Success', u'oldrevid': 2600875, u'newrevid': 2664614}}


```

# 

# Errors
1. Unsupported locale setting
```
Traceback (most recent call last):
  File "/usr/bin/pip", line 11, in <module>
    sys.exit(main())
  File "/usr/lib/python2.7/dist-packages/pip/__init__.py", line 215, in main
    locale.setlocale(locale.LC_ALL, '')
  File "/usr/lib/python2.7/locale.py", line 581, in setlocale
    return _setlocale(category, locale)
locale.Error: unsupported locale setting

```
* Fix
```
$ export LC_ALL=C
```
