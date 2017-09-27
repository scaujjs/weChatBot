
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import time
import helper
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




class ChatBot:
    contactsManager=dict()

    def __init__(self,brain):
        bot=webdriver.Firefox()
        self.bot =bot
        bot.get("https://wx.qq.com/")
        self.communicationWithOne=Communication.Communication("danger",self)
        self.brain=brain


        while (1):
            ##self.showQRcode()

            ##if not self.isElementExist("//div[@id='search_bar']"):
            if not self.is_element_visible((By.XPATH,"//div[@id='search_bar']")):
###                 print("請掃描二維碼並點擊確認")
                time.sleep(1)
            else:
                break
 ##       print("login suscessfully")

    def showQRcode(self):
        pass


    ##information should contains
    ## gender, type,,IdentifyName, region

    ## W for Weman M for man F for fileassistenser
    ## G for group P for people F for fileassistenser
    ##
    ## identifyName should be unique, However here we dont judge whether there r two same name
    def updateContact(self):
        informationOfContacts=list()


        ##this block used to switch to contact list
        xpathForContacts = '//h4[@class="contact_title ng-binding ng-scope"]'
        self.bot.find_element_by_class_name("web_wechat_tab_friends").click()
        i=1
        while(i):
            i=i+1
            if self.isVisibleAndContainsText((By.XPATH, xpathForContacts), "群组"):
                ##print "loading finished"
                break
            else:
                helper.sleepForUpdate(i)
                ##print "still loading"



        ##this block is used to read information of all contacts one by one, and return the list of inform
        flag=True
        while(flag):
            self.bot.find_element_by_class_name("web_wechat_tab_friends").send_keys(Keys.DOWN)
            i=1
            while(i):
                ## Warning here I use i>10 as the condition the end the update process
                if(i>3):
                    flag=False
                    break
                time.sleep(0.05)
                xpathForLoadContact="//p[@class='value ng-binding']";
                xpathForActiveName="//div[@class='ng-isolate-scope active']//div[@class='info']"
                nameToCheck=self.bot.find_element_by_xpath(xpathForActiveName).text;
                print(nameToCheck)
                i=i+1
                if self.isVisibleAndContainsText((By.XPATH, xpathForLoadContact),nameToCheck):
                    print "loading information of this contact finished"


                    xpathForGenderW="//i[@class='web_wechat_women']"
                    xpathForGenderM="//i[@class='web_wechat_men']"

                    if self.is_element_visible((By.XPATH,xpathForGenderM)):
                        gender='M'
                    elif self.is_element_visible((By.XPATH, xpathForGenderW)):
                        gender='W'
                    else:
                        gender='F'


                    ##maybe here we need a English version
                    beizhun="备注："
                    fileAssistant="文件传输助手"

                    xpathForType= "//div[@class='meta_area']/div[@class='meta_item'][1]/label"


                    typeString=self.bot.find_element_by_xpath(xpathForType).text
                    if typeString==beizhun:
                        if nameToCheck==fileAssistant:
                            type='F'
                        else:
                            type='H'
                    else:
                        type='G'

                    xpathForRegion="//div[@class='meta_area']/div[@class='meta_item ng-scope']/p"
                    if self.is_element_visible((By.XPATH,xpathForRegion)):
                        region=self.bot.find_element_by_xpath(xpathForRegion).text
                    else:
                        region='';

                    identifyName=nameToCheck



                    item=[gender,type,identifyName,region]
                    if len(informationOfContacts)==0:
                        informationOfContacts.append(item)
                    elif identifyName==informationOfContacts[-1][-2]:
                        pass
                    else:
                        informationOfContacts.append(item)
                    break
                else:
                    helper.sleepForUpdate(i)
                    ##print "still loading information of contact"


        return informationOfContacts



    def sendMessages(self,list):

        for (targetContact,text) in list:
            self.sendMessage(targetContact,text)

    ## should return the result

    def sendMessage(self,targetContact,textlist):
        self.switchToChatAreaBySearch(targetContact)
        while(1):
            if(self.isVisibleAndContainsText((By.XPATH,"//a[@class='title_name ng-binding']"),targetContact)):
                break
            else:
                helper.sleepForUpdate(1)
                print("waiting show up")


        editArea = self.bot.find_element_by_xpath("//pre[@id='editArea']")
        editArea.click()
        for text in textlist:
            editArea.send_keys(text)
            self.bot.find_element_by_xpath("//a[@class='btn btn_send']").click()
        self.bot.find_element_by_class_name("web_wechat_tab_friends").click()


    def listenToNewMessage(self):
        pass

    def isVisibleAndContainsText(self,element,text):
        return (self.is_element_visible(element) and self.is_element_contain_the_text(element,text))

    def isElementExist(self, element):
        flag = True

        try:
            self.bot.find_element_by_xpath(element)

            return flag
        except:
            flag = False
            return flag

    def is_element_contain_the_text(self,element,text):

        try:
            the_element = EC.text_to_be_present_in_element(element,text)
            assert the_element(self.bot)
            flag = True
        except:
            flag = False
        return flag


    def is_element_visible(self, element):

        try:
            the_element = EC.visibility_of_element_located(element)
            assert the_element(self.bot)
            flag = True
        except:
            flag = False
        return flag


    def testSelector(self):
        self.bot.find_element_by_class_name("web_wechat_tab_friends").click()
        print self.bot.find_elements(By.XPATH,"//h4[@class='nickname ng-binding']")[0]
        page=self.bot.page_source
        result=Selector(text=page).xpath("//h4[@class='nickname ng-binding']").extract()
        if result:
            print "not right way"
        else:
            print "its ok"
        print len(result)
        print(repr(result).decode('unicode-escape'))


    ## swithch to chat by search
    def switchToChatAreaBySearch(self,name):
        serach_box = self.bot.find_element_by_xpath("//div[@id='search_bar']")
        serach_box.click()
        serach_box.send_keys(name)


        while (1):
            page = self.bot.page_source
            xpackShowUp = "//div[@class='contacts scrollbar-dynamic scroll-content']//h4[@class='nickname ng-binding']"

            if len(Selector(text=page).xpath(xpackShowUp)) > 0:
                ##   print "not right way..."

                break
            else:
                helper.sleepForUpdate(1)
                ##print("waiting contact show up in searhBOX")
        self.bot.find_element_by_xpath("//div[@id='search_bar']").send_keys(Keys.DOWN)
        self.bot.find_element_by_xpath(xpackShowUp).send_keys(Keys.ENTER)
'''
bot= webdriver.Firefox()
bot.get("https://wx.qq.com/")


time.sleep(10)



if(bot.find_element_by_id('search_bar')):
    print "find"

else:
    print "not"
serach_box=bot.find_element_by_xpath("//div[@id='search_bar']")

##time.sleep(0.5)
serach_box.send_keys(u'火星人')
time.sleep(0.5)
bot.find_element_by_xpath("//div[@class='contact_item on']").click()
##time.sleep(0.5)
editArea=bot.find_element_by_xpath("//pre[@id='editArea']")
editArea.click()
##time.sleep(0.1)
editArea.send_keys(u"主人問你在幹嗎呢")
##time.sleep(0.1)
bot.find_element_by_xpath("//a[@class='btn btn_send']").click()

'''
test0=False
if test0:
    bot=ChatBot()
    bot.sendMessage("danger",["haha"])



test=False
if test:
    bot=ChatBot()
    ##bot.updateContact()
    i=0
    while(1):
        bot.switchToChatAreaBySearch("huoxingren")
##        bot.bot.find_element_by_xpath("//div[@class='contact_item on']").send_keys(Keys.ENTER)
        messagesToProcess=bot.communicationWithOne.readRecentMessage()
        print "this is old"
        print(repr(bot.communicationWithOne.history).decode('unicode-escape'))
        print "this is new"
        print(repr(messagesToProcess).decode('unicode-escape'))
        bot.sendMessage('danger', (i,i+1))
        i=i+1
    ##bot.testSelector()
    ##informationOfContacts=bot.updateContact()

    ##print informationOfContacts
    ##print len(informationOfContacts)
    i=0
    flag=0
    while(flag):
        bot.sendMessage(u'火星人 小狐狸',u"主人讓我和你說ta會不說晚安就睡覺嗎？")
        i=i+1


'''
        while (1):

            page = bot.bot.page_source
            if len(Selector(text=page).xpath("//div[@class='contact_item on']"))==1:
                break
            else:
                helper.sleepForUpdate(1)
                print("waiting show up")

'''