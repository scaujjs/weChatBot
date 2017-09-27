#coding:utf-8
import sys
import urllib2
import urllib
reload(sys)
sys.setdefaultencoding( "utf-8" )

while(1):
    url="http://www.tuling123.com/openapi/api"
    apiKey="51dab4681bdc49d6ab0b2c30835e70a9"
    content = raw_input("Please input your name:\n")
    postdata=dict(key=apiKey,info=content,userid="12345678")
    postdata=urllib.urlencode(postdata)
    request = urllib2.Request(url,postdata)
    response=urllib2.urlopen(request)
    print response.read()