#!/usr/bin/python
 
import os
import time
 
#-----globals-----
#player = "omxplayer -o hdmi"
player = "vlc -f"
ShouldUpdateAllowlist = False
RetryNum = 1 #number of times to retry each stream connection
 
print ("Starting twitch queue. Press ^C to cancel...")
time.sleep(3)
 
if ShouldUpdateAllowlist:
        #Delete and check for updated list
        print ("Refreshing streamer allowlist")
        os.system('rm -f allowlist.txt')
        updateURL = "https://raw.githubusercontent.com/stuartsoft/twitchqueue/main/allowlist.txt"
        os.system('wget -q -O allowlist.txt %s' %(updateURL))
 
#load the allowlist of stream urls
with open("allowlist.txt","r") as f:
        AllowList = f.readlines()
f.close()
 
if len(AllowList) == 0:
        print ("Allowlist is empty. Exiting...")
        exit()
else:
        print ("Discovered %d allowlist streamers" % (len(AllowList)))
 
#trim off newline of each element
for i in range(0,len(AllowList)):
        AllowList[i] = AllowList[i].rstrip('\n')
 
CurrentStream = 0 #index of stream currently being displayed
 
print ("\nLooking for online streamers...")
 
while True:#continue looping through allowlist of streamers
        if os.name == 'nt':#Windows
                os.system('livestreamer --retry-open %d twitch.tv/%s best -p "%s"' %(RetryNum,AllowList[CurrentStream],player))
        else:#not windows
                os.system('livestreamer --retry-open %d twitch.tv/%s best -np "%s"' %(RetryNum,AllowList[CurrentStream],player))
        #halts script here while livestreamer is running ^^^^^
 
        CurrentStream+=1
        if CurrentStream == len(AllowList):#loop back around to the first streamer
                CurrentStream = 0
                print ("\ntwitch.tv/%s appears to be offline. Trying twitch.tv/%s\n" % (AllowList[len(AllowList)-1],AllowList[CurrentStream]))
        else:  
                print ("\ntwitch.tv/%s appears to be offline. Trying twitch.tv/%s\n" % (AllowList[CurrentStream-1],AllowList[CurrentStream]))