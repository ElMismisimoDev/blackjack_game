import random
import os
import time
import keyboard

# Variables ###################################################

deck = []
winner = None

CARDS = range(2, 14)
TYPES = {
    "C": "Clubs",
    "H": "Hearts",
    "S": "Spades",
    "D": "Diamonds"
}

# Class User (Jugador) ########################################

class User:

    def __init__(self, name):
        
        self.name = name
        self.hand = []
        self.value = 0
        self.is_playing = True

    def choose_card(self):
    
        card = deck[random.randrange(len(deck))]
        deck.remove(card)
        return card
    
    def get_card_value(self, card):
        
        cardValue = ""
        for ch in card:
            if ch.isdigit():
                cardValue += str(ch)

        return int(cardValue)

    def card_name(self, card: str):
        
        type = ""
        number = ""
        cardName = ""

        for ch in card:
            if ch.isdigit():
                number += ch
            elif ch.isalpha():
                type += TYPES[ch]
        if number == "13": #El numero 13 es para los ases.
            cardName = "Ace of " + type
        else:
            cardName = number + " of " + type

        return cardName

    def bet(self):
        
        global winner

        card = self.choose_card()
        cardName = self.card_name(card)

        # Identificar el tipo de carta para mostrarla (solo para el player).

        if self.name == "player":
            print(" Card: " + cardName)
        

        # Añadir la carta a la mano y sumar el valor de esta.

        self.hand.append(cardName)
        self.value += self.get_card_value(card)


        # Calcular si la mano ya vale 21 o se pasa de 21.

        if self.value == 21:
            self.is_playing = False
        elif self.value > 21:
            
            if self.name == "player":
                print("\n\n Oops! It seems you got above 21...")
                self.is_playing = False
                winner = "dealer"
            else:
                self.is_playing = False


    def end(self):
        self.is_playing = False

    def should_hit(self): # Solo para la IA.
        """
        Devuelve True si el dealer pide carta, False si se planta.
        """

        # si tiene 18 o más -> siempre se planta
        if self.value >= 18:
            return False

        # probabilidad de plantarse aumenta con el valor
        # ejemplo: a 12 -> 10% de plantarse, a 17 -> 70%
        plantarse_prob = (self.value - 11) * 0.15  # escala lineal aprox.
        plantarse_prob = max(0, min(plantarse_prob, 1))  # limitar 0–1

        # lanzar un dado probabilístico
        if random.random() < plantarse_prob:
            return False  # se planta
        else:
            return True   # pide carta

    def play(self): #Funcion solo para la IA.

        if self.should_hit():
            self.bet()
        else:
            self.end()

# Users #######################################################

player = User("player")
dealer = User("dealer")

# Functions ###################################################

def create_deck():
    for type in TYPES:
        for card in CARDS:
            deck.append(type + str(card))

def restart():
    
    global deck
    global winner
    global player
    global dealer

    deck = []
    winner = None
    player = User("player")
    dealer = User("dealer")

    os.system('cls')
    create_deck()

# Program #####################################################

os.system('cls')
create_deck()

while True:
   
    if dealer.is_playing and dealer.name != winner:
        dealer.play()
    else:
        dealer.is_playing = False

    if player.is_playing:

        # Primero muestra la baraja del jugador.

        if len(player.hand) == 0:
            print("\n PLAYER'S CARDS:")
            print(" - None")
        else:
            print("\n PLAYER'S CARDS:")
            for card in player.hand:
                print(" - " + card)

        print("\n -------------------------------------------------------------")

        # Pregunta por la opcion del jugador.

        playerChoice = str(input("\n Pick a option:\n\n - Bet\n - Quit\n\n"))
        os.system('cls')
        
        if playerChoice.lower() == "bet":
            print("\n ##############################################################\n")
            player.bet()
            print("\n ##############################################################\n")

            time.sleep(3.0)
            os.system('cls')

        elif playerChoice.lower() == "quit":
            player.end()
            print("\n ##############################################################\n")
            print("                            Loading...                             ")
            print("\n ##############################################################\n")

            time.sleep(2.5)
            os.system('cls')

        else:
            print(" Invalid Option. Stoping program!\n")
            exit()
    



    
    # Results ###################################################################

    if player.is_playing == False and dealer.is_playing == False:
        
        # Calcular los resultados si no hay todavia un ganador definido.

        if winner == None:
            if player.value > dealer.value or dealer.value > 21:
                winner = "player"
            elif player.value == dealer.value:
                winner = None
            else:
                winner = "dealer"



        print("\n ------------------------ END OF THE GAME ------------------------\n\n")
        print("\n ############################### Cards ###########################\n")
        
        print("  Player's Cards:\n")
        for card in player.hand:
            print(" - " + card)

        print("\n  Dealer's Cards:\n")
        for card in dealer.hand:
            print(" - " + card)

        print("\n ############################### Score ############################\n")

        if winner == "player":
            print(" Player: " + str(player.value) + " Winner!")
            print(" Dealer: " + str(dealer.value) + " Loser...!")
        elif winner == "dealer":
            print(" Player: " + str(player.value) + " Loser...!")
            print(" Dealer: " + str(dealer.value) + " Winner!")
        else:
            print(" Player: " + str(player.value) + " Tie...!")
            print(" Dealer: " + str(dealer.value) + " Tie...!")


        print("\n ---------------------- Press Space to continue ----------------------")

        keyboard.wait("space")
        os.system('cls')

        while True:
            option = str(input(" Play again? (y/n): "))

            if option.lower() == "y":
                restart()
                break
            elif option.lower() == "n":
                exit()
            else:
                print(" Invalid Option. Stoping program!\n")
                exit()
