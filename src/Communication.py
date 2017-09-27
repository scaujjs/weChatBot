
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from selenium.webdriver.common.keys import Keys
import time
import helper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from datetime import datetime
import copy



## the format of message [messageContnet,time,fromWho,toWho]
class Communication:
    activeRate=0
    history=list()
    newMessage=list()
    ##idenyified
    def __init__(self,indentified,chatBot):
        self.identified=indentified
        self.bot=chatBot

    def add(self,messageContent,time,fromWho,toWho):
        self.history.append((messageContent,time,fromWho,toWho))


    def search(self,checkedMessages):
        for i in range(len(self.history)):
            pass

    ##before call this function make sure the bot is in the workplace
    ##the make the question simplify and my work easier, assume a person will not send
    def readRecentMessage(self):
        serach_box = self.bot.bot.find_element_by_xpath("//div[@id='search_bar']")
        serach_box.click()
        serach_box.send_keys('wenjianchuanshuzhushou')
        '''
        chuxian
        dianjidyige
        '''
        while(1):
            if(self.bot.isVisibleAndContainsText((By.XPATH,"//h4[@class='contact_title ng-binding ng-scope first']"),"好友")):
                break
            else:
                helper.sleepForUpdate(1)
                ##print("waiting show up")
        page = self.bot.bot.page_source
        self.bot.bot.find_element_by_xpath("//div[@class='contact_item on']").send_keys(Keys.ENTER)


        ##those two are list of the messages
        xpathForAll="//pre[contains(@class,'js_message_plain ng-binding')]/text()"
        xpathForSent="//div[contains(@class,'message ng-scope me')]//pre[@class='js_message_plain ng-binding']/text()"
        xpathForReceived="//div[contains(@class,'message ng-scope you')]//pre[@class='js_message_plain ng-binding']/text()"
        messagesInChat=Selector(text=page).xpath(xpathForAll).extract()
        messagesIsent=Selector(text=page).xpath(xpathForSent).extract()
        messagesIreceived=Selector(text=page).xpath(xpathForReceived).extract()


        if len(messagesInChat)!=len(messagesIsent)+len(messagesIreceived):
            while(1):
                print "error:"
                time.sleep(1)
                print(repr(messagesInChat).decode('unicode-escape'))
                print(repr(messagesIsent).decode('unicode-escape'))
                print(repr(messagesIreceived).decode('unicode-escape'))

        messages=list()
        indexOfSent=0
        indexOfReceied=0
        print "message in chat"
        print len(messagesInChat)
        print
        for i in range(len(messagesInChat)):
            if indexOfSent<=len(messagesIsent)-1 and messagesInChat[i]==messagesIsent[indexOfSent]:
                indexOfSent=indexOfSent+1
                message=[self.identified,messagesInChat[i],helper.ME,helper.YOU,datetime.now()]
                messages.append(message)
            else:
                indexOfReceied+=1
                message = [self.identified,messagesInChat[i],helper.YOU, helper.ME,datetime.now()]
                messages.append(message)

        self.reduceReplicationAndAddTohistory(messages)

        return self.moveNewToOld()


    def moveNewToOld(self):
##        print "hitory beofre"
##        print(repr(self.history).decode('unicode-escape'))
        messagesToProcess=list()
        for i in range(len(self.newMessage)):
            messagesToProcess.append(copy.deepcopy(self.newMessage[i]))
            self.history.append(copy.deepcopy(self.newMessage[i]))
        self.newMessage=list()

##        print "hitory after"
        print(repr(self.history).decode('unicode-escape'))
        print len(self.history)
        print
##        print "after the self.newMessage should be empty"
##        print len(self.newMessage)

        return messagesToProcess



    def reduceReplicationAndAddTohistory(self,messages):


        position=-1
        if len(self.history)==0:
            pass

        elif len(self.history)<=helper.THREHOLD:
            position=0

        elif len(self.history)<helper.RANGE:
            for i in range(len(self.history)):

                if position!=-1:
                    break
                if self.isTwoMessageTheSame(self.history[i],messages[0]) :
                    flag=True
                    for j in range(helper.THREHOLD):
                        if self.isTwoMessageTheSame(self.history[i+j],messages[j]) :
                            pass
                        else:
                            flag=False
                            break
                    if flag:
                        position=i

        else:
            for i in range(helper.RANGE):
                if position != -1:
                    break
                if self.isTwoMessageTheSame(self.history[-helper.RANGE+i], messages[0]):
                    flag = True
                    for j in range(helper.THREHOLD):
                        if self.isTwoMessageTheSame(self.history[-helper.RANGE+i+j],messages[j]):
                            pass
                        else:
                            flag=False
                            break
                    if flag:
                        position=len(self.history)-helper.RANGE+i


        if position==-1:
            self.newMessage=messages
        else:
            print "here is the reduce function"


            length=len(self.history)-position

            lengthOfNewMessages=len(messages)-length

            if lengthOfNewMessages<0:
                while(1):
                    print lengthOfNewMessages
                    helper.sleepForUpdate(5)
                    print "eror"
            print "is the wrong one happen here before"
            print len(self.newMessage)
            for i in range(lengthOfNewMessages):
                self.newMessage.append(messages[length+i])

 ##           print "length"
 ##           print length
 ##           print "lengthOfNewMessages"
 ##           print lengthOfNewMessages
 ##           print "is the wrong one happen here"
 ##           print len(self.newMessage)



    def isTwoMessageTheSame(self,message1,message2):
        flag=True

        for i in range(len(message1)-1):
            if message1[i]==message2[i]:
                continue
            else:
                flag=False
                break

        return flag



