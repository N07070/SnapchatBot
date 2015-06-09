#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
fbstory bot - a snapchat bot for the school of the Francs-Bourgeois
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

credit = """\n
|---------------------------------------------------------|
|                    * FbStoryBot V3*                     |
|                       by N07070                         |
|---------------------------------------------------------|"""
class FbStoryBot(SnapchatBot):

    # Acceuillir l'utilisateur
    def on_friend_add(self, friend):
        self.log("\n"+str(friend)+" has added me !\n")
      	self.send_snap(friend, Snap.from_file('resources/auto_welcome.png'))
        self.log("I have "+str(len(bot.get_friends()))+" friends !\n")

        
    # Dire au revoir si il nous supprime
    def on_friend_delete(self, friend):
        self.log("\n"+str(friend)+" does not want me anymore...\n")
        self.send_snap(friend, Snap.from_file('resources/adieu.png'))
        self.delete_friend(friend)
        self.log("I have "+str(len(bot.get_friends()))+" friends !\n")

    # Ajout d'une story
    def on_snap(self, sender, snap):
        snap.save(None,"snapbot_saves")
        self.log("[RETRACTED]")
        try:
            self.post_story(snap)
            self.log("Posted the snap in the story !")
        except: 
            self.send_snap(sender, Snap.from_file('resources/erreur.png'))
            self.log("Error while trying to post the snap...")
            pass
        try:
            if sender != args.username:    
                self.send_snap([sender], snap)
            self.log("Sent the snap back to the user !")
        except:
            pass


    # Envoie d'un message 
    def message(self, text, friend):
        os.system('convert -size 1080x1920 -background "#2C3539" -gravity Center -fill grey -pointsize 80 label:"'+str(text)+'" image.jpg')
        self.send_snap(friend, Snap.from_file('image.jpg'))
        os.system('rm image.jpg')
        self.log('Sent the message : ' + str(text) + ' ')
        
if __name__ == '__main__':
    parser = ArgumentParser('FbStory Bot')
    parser = ArgumentParser('Reflector Bot')
    parser.add_argument('-u', '--username', required=True, type=str,
                        help='Username of the account to run the bot on'
                        )
    parser.add_argument('-p', '--password', required=True, type=str,
                        help='Password of the account to run the bot on'
                        )
    parser.add_argument('-msg', required=False, type=str,
                        help='Messenge you want to send yourself.')
    parser.add_argument('-user', required=False, type=str, help='The user you want to the send the message to; needs to existe.')

    args = parser.parse_args()

    bot = FbStoryBot(args.username, args.password)
    #Lister tout les utilisateurs puis le nombre d'utilisateurs.
    bot.log(credit)
    bot.log("I have "+str(len(bot.get_friends()))+" friends !")
    
    if args.msg and args.user:
        if args.user == "all" or args.user == "All":
            friends_list = bot.get_friends()
            for friends in friends_list:
                print(friends)
                time.sleep(0.1)
                bot.message(args.msg, friends)
            
        else:
            bot.message(args.msg,args.user)
    else:
        bot.log("You need to provide a valid message and username.")

    
    bot.listen()
