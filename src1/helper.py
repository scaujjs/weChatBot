##print "heo"

#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import time



NAMEINDEX=0
CONTENTINDEX=1
FROMWHOM=2
TOWHOM=3
TIME=4

ME="me"
YOU="you"
RANGE=30
THREHOLD=5

def sleepForUpdate(i):
    k=i*i*i
    time.sleep(0.05*k)


##merge message
def processReply(replys):
    newReplys=list()
    i=0
    while(i<=len(replys)-1):
        name=replys[i][NAMEINDEX]
        step=0
        groupContents=list()
        groupContents.append(replys[i][CONTENTINDEX])
        while(True):
            if i<len(replys)-1 and name==replys[i+1+step][NAMEINDEX]:
                groupContents.append(replys[i+1+step][CONTENTINDEX])
                step+=1
            else:
                break
        i=i+1+step
        newReplys.append((name,groupContents))

    return newReplys

def filterNewMessageIreceived(messages):
    newMessages=list()
    for message in messages:
        if message[2]==YOU:
            newMessages.append(message)

    return newMessages




test=True
if test:
    content=[[1,"2"],[1,"3"],[2,"3"],[1,"3"]]
    print processReply(content)