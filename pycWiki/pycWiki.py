# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import urllib
import urllib2
import requests
import cookielib
import json
import ssl

from collections import OrderedDict


class pycWiki:

    def __init__(self, url='', username='', password='', domain=''):

        self.wiki_url = url
        self.username = username
        self.password = password
        self.domain = domain

        self.token_id = ''
        self.session_id = ''

        self.format_data = 'json'
        self.cj = cookielib.CookieJar()

        self.login_status = False

    def wiki_order_data(self,data):
        """
        Method to order the argument passed to Mediawiki API
        # based on wiki decumentation 'token' should be in the last index
        data: json data
        return: ordered dict
        """
        last_field = 'token'
        if last_field in data:
            keys = [k for k in data.keys() if not k == last_field]
            keys.append(last_field)
        else:
            keys = data.keys()

        ordered = OrderedDict((k, data[k]) for k in keys)
        return ordered

    #def wiki_request(self, data, storecookie=False,):
    #
    #    completedata = data
    #    completedata['format'] = self.format_data
    #    ordereddata = self.wiki_order_data(completedata)
    #    requests.packages.urllib3.disable_warnings()
    #    output = requests.post(url=self.wiki_url, data=ordereddata, verify=False, cookies=self.cj)
    #
    #    if storecookie == True:
    #        self.cj = output.cookies
    #
    #    return output

    def wiki_request2(self,data):
        """
        Main method to send request to mediawiki
        data: json data
        return: output from mediawiki APi,json format
        """
        if 'create_default_context' in dir(ssl):
          ctx = ssl.create_default_context()
          ctx.check_hostname = False
          ctx.verify_mode = ssl.CERT_NONE
          opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.HTTPSHandler(context = ctx))
        else:
          opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.HTTPSHandler())

        urllib2.install_opener(opener)

        completedata = data
        completedata['format'] = self.format_data
        ordereddata = self.wiki_order_data(completedata)
        encodeddata = urllib.urlencode(ordereddata)
        # print encodeddata
        #req = urllib2.Request(wiki_url, encodeddata)
        #rsp = urllib2.urlopen(req, context=ctx)
        rsp = opener.open(self.wiki_url, encodeddata)
        content = rsp.read()
        # print content
        return content



    def wiki_login(self):
        
        ## 1st Login
        #data = {'action':'login','lgname':self.username,'lgdomain':self.domain,'lgpassword':self.password}
        data = {
            'action':'query',
            'meta':'tokens',
            'type':'login'
            }
        resp_json = json.loads(self.wiki_request2(data))
        login_token = resp_json['query']['tokens']['logintoken']

        data = {
            'action': 'login',
            'lgname': self.username,
            'lgpassword': self.password,
            'lgtoken': login_token
            }
        resp_json = json.loads(self.wiki_request2(data))


        # ## 2nd Token Login
        # #data = {'action':'login','lgname':self.username,'lgdomain':self.domain,'lgpassword':self.password, 'lgtoken':self.token_id}
        # #resp_json = json.loads(self.wiki_request2(data))
        # #print resp_json
        if not resp_json['login']['result'] == "Success":
            print("login failed")
            self.login_status = False
        else:
            self.login_status = True

    def wiki_logout(self):
        if self.login_status == True:
            data = {'action':'logout'}
            resp_json = json.loads(self.wiki_request2(data))
            self.login_status = False
        else:
            print("user not logged in")

    def wiki_getPage(self, page_name):
        data = {'action': 'query', 'titles':page_name, 'prop':'revisions','rvprop':'content'}
        resp_json =  json.loads(self.wiki_request2(data))
        return resp_json

    def wiki_getEditBasetimestamp(self,page_name):
        data = {'action': 'query','prop':'revisions', 'titles':page_name, 'rvprop':'timestamp'}
        resp_json =  json.loads(self.wiki_request2(data))
        page_id =  resp_json['query']['pages'].keys()[0]
        base_timestamp = resp_json['query']['pages'][page_id]['revisions'][0]['timestamp']
        return base_timestamp

    def wiki_getToken(self, page_name):
        data = {'action': 'query','meta':'tokens'}
        resp_json =  json.loads(self.wiki_request2( data))
        token_id = resp_json['query']['tokens']["csrftoken"]
        return token_id

    def wiki_postPage(self, page_name,summary, content, section=0):
        basetimestamp = self.wiki_getEditBasetimestamp(page_name)
        tokenedit = self.wiki_getToken(page_name)
        data = {'action': 'edit', 'title':page_name,
                'basetimestamp':basetimestamp, 'text':content,
                'section':section, 'summary':summary, 'token':tokenedit}
        resp_json =  json.loads(self.wiki_request2(data))
        if "captcha" in resp_json["edit"].keys():
            captcha_question =  resp_json["edit"]["captcha"]["question"]
            captcha_question = captcha_question.replace(u'\u2122',"+-1*").replace(u'−',"+-1*").strip()
            captcha_answer = eval(captcha_question)
            captcha_id =  resp_json["edit"]["captcha"]["id"].strip()
            data["captchaid"] = captcha_id
            data["captchaword"] = captcha_answer
            resp_json =  json.loads(self.wiki_request2(data))

        return resp_json

    def wiki_dict2wikitable(self,content, header=None):
        ## set header
        if header is None:
            header = content[0].keys()
        lstHeader = [ '! %s\n' %(hd) for hd in header]
        strheader = '{| class="wikitable sortable"\n|-\n' + "".join(lstHeader)
        ## set content
        strrow = ""
        for eachcontent in content:
            lstcont = [ "| %s \n" %(eachcontent[v]) for v in header]
            strrow += '|- \n' + ''.join(lstcont)
        ## set footer
        strfooter = "|}\n"
        return "%s%s%s" %(strheader,strrow,strfooter)

    def wiki_wikitable2dict(self,content):
        ## parsing content
        stripcontent = content.strip().replace("|}","").replace('{| class="wikitable sortable"\n|-\n!','')
        dlist = stripcontent.split('|-')
        dkey = [x.strip() for x in dlist[0].split('! ')]
        dWiki = []
        for d in dlist[1:]:
            dval = d.strip().split('| ')
            dval.pop(0)
            dd = {}
            for i in range(0,len(dkey)):
                dd[str(dkey[i].strip())] = str(dval[i].strip())
            dWiki.append(dd)
        return dWiki

    def wiki_extractContent(self,jsoncontent):
        return str(jsoncontent['query']['pages'][jsoncontent['query']['pages'].keys()[0]]['revisions'][0]['*'])
