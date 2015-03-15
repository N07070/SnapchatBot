#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
n0Bot - A bot for me, my friends and the world
Copyright (C) 2014  N07070

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Import the classes
from snapchat_bots import SnapchatBot, Snap
from argparse import ArgumentParser
import os, sys, time
sys.path.insert(0, '/media/HDD/Code/Python/SnapchatBot/snapchat_bots')
from utils import guess_type

credit = """\n
|---------------------------------------------------------|
|                    * n0bot V3.1 *                       |
|                       by N07070                         |
|---------------------------------------------------------|"""
class n0bot(SnapchatBot):

    # Say hi if the user added me
    def on_friend_add(self, friend):
        self.log(+str(friend)+" has added me !\n")
      	self.send_snap(friend, Snap.from_file('resources/auto_welcome.png'))
        self.log("\nI have "+str(len(bot.get_friends()))+" friends !\n")

        
    # Say goodbye if the user deleted me
    def on_friend_delete(self, friend):
        self.log(str(friend)+" does not want me anymore...\n")
        self.send_snap(friend, Snap.from_file('resources/adieu.png'))
        self.delete_friend(friend)
        self.log("I have "+str(len(bot.get_friends()))+" friends !\n")

    # To add the snap to the story, and watermark it with the username
    def on_snap(self, sender, snap):
        # Sauvegarde temporaire du snap
        if snap.media_type == 0:
            snap.save("temporaire.jpg")
            self.log("Saved the snap.")
        elif snap.media_type == 1 or snap.media_type == 2:
            snap.save("temporaire.mp4")
            self.log("Saved the snap.")
        else:
            self.log("I do not know which type of snap I got !")
        
        # If the snap is an image
        if snap.media_type == 0:
            os.system('convert temporaire.jpg -fill \'#FFF5EE\' -pointsize 20 -annotate +0+20 "'+str(sender)+'" image.jpg')
            try:
                self.post_story(Snap.from_file('image.jpg'))
                self.log("Posted the snap in the story !")
                try:
                    if sender != args.username:    
                        self.send_snap(sender, Snap.from_file('resources/recu.png'))
                        self.log("Validated the reception !")
                except:
                    pass
            except: 
                self.send_snap(sender, Snap.from_file('resources/erreur.png'))
                self.log("Error while trying to post the snap !")
                pass
            # os.system('rm image.jpg temporaire.jpg')
           
        # If the snap is a video
        elif snap.media_type == 1 or snap.media_type == 2 and os.path.getsize("temporaire") != 0:
            os.system('ffmpeg -i temporaire.mp4 -vf drawtext="fontfile=resources/Arial.ttf: text='+str(sender)+':fontcolor=dimgray@1.0:fontsize=00:x=00: y=00" -y output.mp4')
            try:
                self.post_story(Snap.from_file('output.mp4'))
                self.log("Posted the snap in the story !")
            except: 
                self.send_snap(sender, Snap.from_file('resources/erreur.png'))
                self.log("Error while trying to post the snap !")
                pass
            os.system('rm output.mp4 temporaire.mp4')
            try:
                if sender != args.username:    
                    self.send_snap(sender, Snap.from_file('resources/recu.png'))
                    self.log("Validated the reception !")
            except:
                pass
        
        # En cas d'erreur
        else:
            self.send_snap(sender, Snap.from_file('resources/erreur.png'))
            self.log("Error while trying to post the snap !")

    # To message someone or the message all the users 
    def message(self, text, friend):
        os.system('convert -size 1080x1920 -background "#2C3539" -gravity Center -fill grey -pointsize 80 label:"'+str(text)+'" image.jpg')
        self.send_snap(friend, Snap.from_file('image.jpg'))
        os.system('rm image.jpg')
        self.log('Sent the message : ' + str(text) + ' ')
    
    # To delete all the stories
    def clean_story(self):
        self.clear_stories()
        self.log("Deleted the story !")
        self.post_story(Snap.from_file('resources/deleted_story.png'))
        
        
        
if __name__ == '__main__':
    parser = ArgumentParser('n0bot')
    parser.add_argument('-u', '--username', required=True, type=str,help='Username of the account to run the bot on')
    parser.add_argument('-p', '--password', required=True, type=str,help='Password of the account to run the bot on')
    parser.add_argument('-msg', '--message', required=False, type=str,help='Text you want to send as a message')
    parser.add_argument('-user', '--recipient', required=False, type=str, help='The user you want to the send the message to; needs to existe')
    parser.add_argument('-d','--delete',required=False, help='If you want to delete the story of the bot')

    args = parser.parse_args()

    bot = n0bott(args.username, args.password)
    #Lister tout les utilisateurs puis le nombre d'utilisateurs.
    bot.log(credit)
    bot.log("I have "+str(len(bot.get_friends()))+" friends !")
    
    if args.message and args.recipient:
        if args.recipient == "all" or args.recipient == "All":
            friends_list = bot.get_friends()
            for friends in friends_list:
                print(friends)
                time.sleep(0.1)
                bot.message(args.message, friends)
            
        else:
            bot.message(args.message,args.recipient)
    else:
        bot.log("You need to provide a valid message and username to send a message.")
        
    if args.delete:
        bot.clean_story()

    
    bot.listen()
