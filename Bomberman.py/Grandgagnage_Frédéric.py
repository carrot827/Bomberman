# -*- coding: utf-8 -*-

#suite du travail! 09 aout 2020

import random    #De base
import datetime  #De base

import os        #Fonctionnalité couleur
import threading #Fonctionnalité couleur


    # Afficher les scors passés
class See :
    def __init__(self):
        self.data = data

    @staticmethod
    def read():
        print("\n--- Historique des parties ---")
        try :
            if (os.stat("data.txt").st_size == 0) : #Si le fichier est vide, il n'y a aucune partie à afficher
                print("Il faut y jouer pour savoir pourquoi on y joue :-)")
            else :
                with open ("data.txt","r") as file :
                    for line in file :
                        print(line)
                
        except FileNotFoundError : #Si on veut consulter avec un fichier non présent
            print("Il faut y jouer pour savoir pourquoi on y joue :-)")

        finally :
            input("\nAppuyez sur ENTER pour retourner au menu")
            Game.menu()


    # Les musiques du jeu
class Music :
    def __init__(self):
        self.musique = musique

    @staticmethod
    def music_start():
        os.startfile(r"Music\start.mp3")

    @staticmethod
    def music_menu():
        os.startfile(r"Music\menu.mp3")
        
    @staticmethod
    def music_battle():
        os.startfile(r"Music\battle.mp3")
        
    @staticmethod
    def music_regle():
        os.startfile(r"Music\regles.mp3")

    @staticmethod
    def music_draw():
        os.startfile(r"Music\draw.mp3")

    @staticmethod
    def music_winner():
        os.startfile(r"Music\winner.mp3")

    @staticmethod
    def sound_drug():
        os.startfile(r"Music\drug.mp3")

    @staticmethod
    def sound_exit():
        os.startfile(r"Music\exit.mp3")
    

class Player :
    def __init__(self, name, points = 0, start = (0,0), drop = False, dead = False, keyboard_key = {'z':(-1,0), 'q':(0,-1),'s':(1,0),'d':(0,1)}):
        self.name = name
        self.points = points
        self.position = start
        self.drop = drop
        self.dead = dead
        self.nbdrug = 0
        self.keyboard_key = keyboard_key
        self.bomb = []

    def playerisdead(self):
        self.dead = True
        
# Touches poser une bombe
    def drop_bomb(self):
        key_bomb = input("Poser une bombe? ")
        if key_bomb == 'e' or key_bomb == 'p':
            print("Bombe placée")
            drop = True
            return drop

    # Déposer des bombes
    def pop_bomb(self):
        new_bomb = self.position
        if (self.drop_bomb()) and (new_bomb not in self.bomb):
            self.bomb.append(new_bomb)


    # Mouvements des joueurs
    def move (self) :
        key = input("Déplacement: ")
        while key not in self.keyboard_key.keys() :
            key = input("Déplacement: ")
        
        move = self.keyboard_key[key]
        self.position = (self.position[0] + move[0], self.position[1] + move[1])
        

class Game :  
    def __init__(self, player, player2, size=10):
        self.player = player
        self.player2 = player2
        self.board_size = size
        self.candies = []
        self.drug = []
        
    # Dessine le plateau
    def draw(self):
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("*",end=" ")
                elif (line,col) in self.drug :
                    print("▓",end=" ")
                elif (line,col) in self.player.bomb or (line,col) in self.player2.bomb :
                    print("Ó",end=" ")
                elif (line,col) == self.player.position :
                    if self.player.dead :
                        print("┼",end=" ")
                    else:
                        print("♥", end=" ")
                elif (line,col) == self.player2.position :
                    if self.player2.dead :
                        print("╬",end=" ")
                    else:
                        print("♣", end=" ")
                else : 
                    print(".",end=" ")
            print()


    # Affiche les couleurs liées au bonbon drogue
    def color(self):
        if couleurok:
            for i in range(0,35): #  35 = le temps de la musique
                os.system("color E")
                os.system("color D")
                os.system("color A")
                os.system("color 5")
            os.system("color F")
        else :
            print("Bha bravo Nils, tu es déchiré! T'es vraiment un sale petit con!")

    # Fait apparaitre un bonbon
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies :
            self.candies.append(new_candy)

    # Fait apparaitre de la drogue
    def pop_drug(self):
        new_drug = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_drug not in self.drug :
            self.drug.append(new_drug)
            
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            if self.player.dead is not True: # Un mort ne peux plus augmenter ses points, mais peut perturber l'autre joueur
                self.player.points += 1
            self.candies.remove(self.player.position)
            
        if self.player2.position in self.candies:
            if self.player2.dead is not True: # Un mort ne peux plus augmenter ses points
                self.player2.points += 1
            self.candies.remove(self.player2.position)

    def check_dead(self):
        if self.player.position in self.player.bomb:
            self.player.bomb.remove(self.player.position)
            self.player.playerisdead()
            print("Et ça fait bim bam boum")

        if self.player2.position in self.player2.bomb:
            self.player2.bomb.remove(self.player2.position)
            self.player2.playerisdead()
            print("Et ça fait bim bam boum")

    # Regarde si il y a de la drogue à prendre (et la prend) + start couleurs
    def check_drug(self):
        #Joueur 1
        if self.player.position in self.drug:
            if self.player.dead is not True: # Un mort ne peux plus augmenter ses points
                self.player.points += 5
                self.player.nbdrug += 1
            Music.sound_drug()
            threading.Thread(target=self.color).start()
            # Vérifie l'abus de drogue
            if self.player.nbdrug > 2 :
                self.player.points = 0
            self.drug.remove(self.player.position)
            
        #Joueur 2    
        if self.player2.position in self.drug:
            if self.player2.dead is not True: # Un mort ne peux plus augmenter ses points
                self.player2.points += 5
                self.player2.nbdrug += 1
            Music.sound_drug()
            threading.Thread(target=self.color).start()
            # Vérifie l'abus de drogue
            if self.player2.nbdrug > 2 :
                self.player2.points = 0
            self.drug.remove(self.player2.position)


    #Empêche les joueurs de sortir, ils seront téléportés
    def check_out(self):
        if self.player.position[0] not in range(self.board_size) or self.player.position[1] not in range(self.board_size):
            print("Stay at home! è_é")
            self.player.position = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
            
        if self.player2.position[0] not in range(self.board_size) or self.player2.position[1] not in range(self.board_size):
            print("Stay at home! è_é")
            self.player2.position = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
    
             
    # Joue une partie complète
    def play(self):
        print("--- Début de la partie ---")
        Music.music_battle()
        self.draw()
        
        end = Game.end_time(2,0) # Une partie dure deux minutes selon les règes
        now = datetime.datetime.today()
        
        while now < end :
            print("Au tour de", self.player.name, " (♥)!")
            self.player.pop_bomb()
            self.player.move()
            print("Au tour de", self.player2.name, " (♣)!")
            self.player2.pop_bomb()
            self.player2.move()
            self.check_candy()
            self.check_drug()
            self.check_dead()
            self.check_out()

                 
            if random.randint(1,3) == 1 :
                self.pop_candy()
                self.pop_drug()
                
            self.draw()
            
            now = datetime.datetime.today()
        
        
        print("----- Terminé -----")

        #Total des points et gagnant
        print("Le joueur 1,", self.player.name, "a", self.player.points, "points")
        print("Le joueur 2,", self.player2.name, "a", self.player2.points, "points\n")

        if self.player.points > self.player2.points :
            Music.music_winner()
            print(self.player.name, ", gagne!")
        elif self.player.points < self.player2.points :
            Music.music_winner()
            print(self.player2.name, ", gagne!")
        else :
            Music.music_draw()
            print("Egalité!")

#Fichier et enregistrement ----------------------------------
        date= str(datetime.datetime.today())

        with open ("data.txt", "a") as file :
            file.write("\nDate de la partie:\n")
            file.write(date)
            file.write("\n")
            file.write("\n")
            ptj1 = str(("Le joueur 1,", self.player.name, "a", self.player.points, "points"))
            file.write(ptj1)
            file.write("\n")
            ptj2 = str(("Le joueur 2,", self.player2.name, "a", self.player2.points, "points\n"))
            file.write(ptj2)
            file.write("\n")

            if self.player.points > self.player2.points :
                winj1= str((self.player.name, ", gagne!"))
                file.write("\n")
                file.write(winj1)
            elif self.player.points < self.player2.points :
                winj2= str((self.player2.name, ", gagne!"))
                file.write("\n")
                file.write(winj2)
            else :
                file.write("\n")
                file.write("Egalité!")    
            file.write("\n------------------------\n") 
#Fichier et enregistrement ----------------------------------

        input("Appuyez sur ENTER pour retourner au menu principal")
        Game.menu()

    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end

#       Menu du jeu
    @staticmethod
    def menu():
        Music.music_menu()
 
        try :
            choix = int(input("1) Démarrer le jeu\n2) Règles du jeu\n3) Commandes\n4) Historique des parties\n5) Quitter le jeu\n\n- "))
            while (choix < 1 or choix > 5) :
                choix = int(input("1) Démarrer le jeu\n2) Règles du jeu\n3) Commandes\n4) Historique des parties\n5) Quitter le jeu\n\n- "))
            if choix == 1 :
                p = Player("Anne Smal")
                x = Player("Frédéric Grandgagnage", start=(9,9), keyboard_key = {'o':(-1,0),'k':(0,-1),'l':(1,0),'m':(0,1)})
                t = Game.asksize()
                g = Game(p, x, t)
                g.play()   
            elif choix == 2 :
                Music.music_regle()
                print("Règles du jeu\n\nLe but du jeu est de récolter le plus de bonbons en deux minutes.")
                print("Vous pouvez exploser votre adversaire avec des bombes afin de l'empêcher de gagner.")
                print("\nVous trouverez également certains bonbons moins catholiques.\nMalheur à ceux qui en abusent! :-)")
                print("\nMéfiez-vous des morts. Ceux-ci pourraient vous hanter . . .")
                input("\n\nAppuyez sur ENTER pour retourner au menu")
                Game.menu()
            elif choix == 3 :
                print("Comment jouer?\n")
                print("""Le joueur 1 se déplace avec zqsd et pose une bombe avec la touche "e" \n""")
                print("""Le joueur 2 se déplace avec oklm et pose une bombe avec la touche "p" """)
                input("\nAppuyez sur ENTER pour retourner au menu")
                Game.menu()
            elif choix == 4 :
                See.read()
            else :
                input("\nAppuyez sur enter pour quitter Bomberman.py")
                print("Fermeture ...")
                Music.sound_exit()
                exit()
        except ValueError:
            Game.menu()

        #Menu de démarrage du jeu
    @staticmethod
    def start():
        Music.music_start()

        print("    ____                  __                                        ")
        print("   / __ )____  ____ ___  / /_  ___  _____                           ")
        print("  / __  / __ \/ __ `__ \/ __ \/ _ \/ ___/                           ")
        print(" / /_/ / /_/ / / / / / / /_/ /  __/ /                               ")
        print("/_____/\____/_/ /_/ /_/_.___/\___/_/                     ____       ")
        print("                        ____ ___  ____ _____            / __ \__  __")
        print("                       / __ `__ \/ __ `/ __ \          / /_/ / / / /")
        print("                      / / / / / / /_/ / / / /    _    / ____/ /_/ / ")
        print("                     /_/ /_/ /_/\__,_/_/ /_/    (_)  /_/    \__, /  ")
        print("                                                           /____/")
 
        start = input("""\nAppuiez sur "Enter" pour lancer le jeu\n""")

        #Demande la taille du plateau 
    @staticmethod
    def asksize():
        print("Quel monde désirez-vous?")
        try :
            choix = int(input("1) Petit\n2) Moyen\n3) Grand\n- "))
            while (choix < 1 or choix > 3):
                choix = int(input("1) Petit\n2) Moyen\n3) Grand\n- "))
            if choix == 1:
                print("Monde 1")
                size = 10
                return size
            elif choix == 2:
                print("Monde 2")
                size = 12
                return size
            else:
                print("Monde 3")
                size = 18
                return size
        except ValueError :
            Game.menu()

if __name__ == "__main__" :
# Active ou non les couleurs --> l'IDE de Python ne supporte pas les couleur
    couleurok = False
    couleur = input("\n\n\nEtes-vous dans l'IDE de Python? un prof? ou même épileptique?\n\n(O)ui\n(N)on\n\n- ")
    if couleur.upper() == "O" :
        print("Bonjour Madame :x")
    else :
        couleurok = True
        
    Game.start()
    Game.menu()
