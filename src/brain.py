
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re

import time
import helper
import bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
## warming!!!  i'm not clear about the mchanism about EC.... it may cause problems late...
## only Chinaese Version
## warming!! some people's name contains emoj
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import Communication

import urllib,urllib2
import json

class Brain:


    def __init__(self):
        self.wechatBot=bot.ChatBot(self)


    def getReplyFromTuring(self,messageList):
        url = "http://www.tuling123.com/openapi/api"
        apiKey = "51dab4681bdc49d6ab0b2c30835e70a9"
        replys=list()
        for message in messageList:
            content=message[helper.CONTENTINDEX]
            postdata = dict(key=apiKey, info=content, userid="12345678")
            postdata = urllib.urlencode(postdata)
            request = urllib2.Request(url, postdata)
            response = urllib2.urlopen(request)
            replyContent=json.load(response)[u'text']


            reply=(message[helper.NAMEINDEX],replyContent)
            replys.append(reply)

            replys=helper.processReply(replys)

            return replys

    def chatWithTuringOne(self,name):
        newCommunication = Communication.Communication(name, self.wechatBot)
        while(True):
            self.wechatBot.switchToChatAreaBySearch(name)
            newMessages = newCommunication.readRecentMessage()
            newMessages = helper.filterNewMessageIreceived(newMessages)


            if(len(newMessages)!=0):
                replys = self.getReplyFromTuring(newMessages)
                self.sendMessage(replys)

    def updateContactList(self):
        pass

    def sendMessage(self,replys):
        self.wechatBot.sendMessages(replys)

    def generateDataBase(self,contactList):
        pass

    def cnvertNameToID(self,username):
        pass


alpha=Brain()
alpha.chatWithTuringOne(u"")
