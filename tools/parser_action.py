import json
import sys

filename = sys.argv[1]
f = open(filename,'r')
jd = json.load(f)
f.close()

#print(jd.get("actions")[1].get("id"))
#print(len(jd.get("actions")))
for i in jd.get("actions"):
    #print(i.get("type"))
    #if(0):
    if(i.get("type")=="addAttachmentToCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("attachment").get("name")+"\",",end='')
        if( data.get("attachment").get("url") != None):
            print("\""+data.get("attachment").get("url")+"\"")
        else:
            print("")
    #if(0):
    if(i.get("type")=="addMemberToBoard"):
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                i.get("data").get("board").get("name")+"\",\""+
                i.get("member").get("fullName")+"\",")
    #if(0):
    if(i.get("type")=="addMemberToCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                i.get("member").get("fullName")+"\",")
    #if(0):
    if(i.get("type")=="commentCard"):
        data = i.get("data")
        text = data.get("text").replace("\n","\\n")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("list").get("name")+"\",\""+
                text+"\"")
    #if(0):
    if(i.get("type")=="copyCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("list").get("name")+"\",\""+
                data.get("cardSource").get("name")+"\"")
    #if(0):
    if(i.get("type")=="copyCommentCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("cardSource").get("name")+"\"")
    #if(0):
    if(i.get("type")=="createBoard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\"")
    #if(0):
    if(i.get("type")=="createCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("list").get("name")+"\"")
    #if(0):
    if(i.get("type")=="createList"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("list").get("name")+"\"")
    #if(0):
    if(i.get("type")=="deleteAttachmentFromCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("attachment").get("name")+"\"")
    #if(0):
    if(i.get("type")=="removeMemberFromCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("member").get("name")+"\"")
    #if(0):
    if(i.get("type")=="updateBoard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\"",end='')
        if( data.get("list") != None):
            if( data.get("list").get("name") != None):
                print(",\""+data.get("list").get("name")+"\"")
            else:
                print("")
        else:
            print("")
    #if(0):
    if(i.get("type")=="updateCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\"",end='')
        if( data.get("list") != None):
            if( data.get("list").get("name") != None):
                print(",\""+data.get("list").get("name")+"\"")
            else:
                print("")
        else:
            print("")
    #if(0):
    if(i.get("type")=="updateCheckItemStateOnCard"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("card").get("name")+"\",\""+
                data.get("checklist").get("name")+"\",\""+
                data.get("checkItem").get("name")+"\"")
    #if(0):
    if(i.get("type")=="updateList"):
        data = i.get("data")
        print("\""+i.get("date")+"\",\""+i.get("type")+"\",\""+
                i.get("memberCreator").get("fullName")+"\",\""+
                data.get("board").get("name")+"\",\""+
                data.get("list").get("name")+"\"")


