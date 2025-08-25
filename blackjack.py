import random
import os
import time
import keyboard

# Variables ###################################################

deck = []
has_game_started = False
winner = None

money = 5000
bet_money = 0
takenLoans = 0

CARDS = range(2, 14)
TYPES = {
    "C": "Clubs",
    "H": "Hearts",
    "S": "Spades",
    "D": "Diamonds"
}

# Width = 100, Height = 30 

WIDTH = 100
HEIGHT = 30
os.system("mode con: cols=" + str(WIDTH) + " lines=" + str(HEIGHT))

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

    def giveCard(self): # Se llama a esta funcion cuando se hace un "hit".
        
        global winner

        card = self.choose_card()
        cardName = self.card_name(card)

        # Identificar el tipo de carta para mostrarla (solo para el player).

        if self.name == "player" and has_game_started:
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


    def stand(self):
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
            self.giveCard()
        else:
            self.stand()

# Users #######################################################

player = User("player")
dealer = User("dealer")

UsersList = [player, dealer]

# Functions ###################################################

def loading_print(seconds: float): 

    '''Funcion que simula una animacion de "Cargando". Dura los segundos que
    se indiquen como argumento.'''

    print("\n ##############################################################\n")
    print("                            Loading...                             ")
    print("\n ##############################################################\n")
    time.sleep(seconds)
    os.system('cls')


def create_deck():
    for type in TYPES:
        for card in CARDS:
            deck.append(type + str(card))

def choose_bet():

    global money
    global bet_money

    while True:
    
        try:
            bet_money = int(input("Select the quantity you want to bet.\nYour money: " + str(money) + "$\n\n"))
            os.system('cls')
    
            if bet_money > 0 and bet_money <= money:

                print("You are gonna bet " + str(bet_money) + "$")
                choice = str(input("Are you sure? (y/n): "))
                os.system('cls')

                if choice.lower() == "y":

                    money -= bet_money 
                    print("Okay. The game is about to start.")
                    time.sleep(2.0)
                    os.system('cls')
                    break
                elif choice.lower() == "n":

                    os.system('cls')
                    continue
                else:

                    print("Error! Invalid option. Try again.")
                    time.sleep(2.0)
                    os.system('cls')
                    continue
            elif bet_money <= 0:

                print("Well sir, we dont accept that quantity. Try again please.")
                time.sleep(2.0)
                os.system('cls')
                continue
            elif bet_money > money:

                print("Sir, you dont have that money. Try again please.")
                time.sleep(2.0)
                os.system('cls')
                continue
        
        except ValueError:

            os.system('cls')
            print("Error! Invalid option. Try again.")
            time.sleep(2.0)
            os.system('cls')
            continue

def loan():
    '''Evento que ocurre cuando al jugador no le queda dinero al reiniciar la partida.
    Se le da la opcion de pedir un prestamo y si accede, se suma uno al contador de prestamos.'''

    global money
    global takenLoans
    
    print("It seems you dont have any money left sir.")
    time.sleep(2.0)
    print("Howewer, we offer you the option to take a loan.")
    time.sleep(2.0)
    print("Worth of 5000$")
    time.sleep(2.5)

    os.system('cls')
    while True:

        option = str(input("Do you want to take the loan sir? (y/n):\n\n"))
        os.system('cls')

        if option.lower() == "y":
            
            money += 5000
            takenLoans += 1
            print("Good. Here's your money sir. Enjoy")
            time.sleep(2.0)
            os.system('cls')
            break
        elif option.lower() == "n":

            print("In that case, this is the end of the game sir.")
            time.sleep(1.5)
            print("Have a great night")
            time.sleep(1.5)
            exit()
        else:
            print(" Invalid Option. Try again.\n")
            time.sleep(2.0)
            os.system('cls')
            continue



    


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
    if money <= 0:
        loan()

    start()

def introduction():

    print("Hello")
    time.sleep(1.5)
    print("You're about to play blackjack, you know the rules right?")
    time.sleep(2.5)
    print("The objective is to get the closest possible to 21 with your cards. Easy")
    time.sleep(2.5)
    print("If you get above 21, you lose.")
    time.sleep(2.0)
    os.system('cls')
    print("Do you need more tips?")
    #Por hacer...

def start():

    global has_game_started

    choose_bet() # Elegimos la cantidad que queremos apostar.

    loading_print(2.5)

    create_deck() # Creamos la baraja para poder repartir las cartas.

    for user in UsersList: # Repartimos las cartas.
        for x in range(2):
            user.giveCard()

    has_game_started = True

# Program #####################################################








os.system('cls')
start()

while True:
   
    if dealer.is_playing and dealer.name != winner:
        dealer.play()
    else:
        dealer.is_playing = False

    if player.is_playing:

        # Primero muestra el titulo del juego, prestamos, el dinero del jugador y su apuesta.

        loan_label = "Loans: " + str(takenLoans)
        money_label = "Money: " + str(money) + "$"
        bet_label = "Bet: " + str(bet_money) + "$"

        print("BLACKJACK" + loan_label.rjust(WIDTH - 9)) #Se le resta menos 9 porque es la cantidad de letras que tiene "BLACKJACK".
        print(money_label.rjust(WIDTH))
        print(bet_label.rjust(WIDTH))

        # Luego muestra la baraja del jugador.

        print("\n PLAYER'S CARDS:")
        for card in player.hand:
            print(" - " + card)

        print("\n -------------------------------------------------------------")

        # Pregunta por la opcion del jugador.

        playerChoice = str(input("\n Pick a option:\n\n - Hit\n - Stand\n\n"))
        os.system('cls')
        
        if playerChoice.lower() == "hit":
            print("\n ##############################################################\n")
            player.giveCard()
            print("\n ##############################################################\n")

            time.sleep(3.0)
            os.system('cls')

        elif playerChoice.lower() == "stand":
            player.stand()
            loading_print(2.5)
            os.system('cls')

        else:
            print(" Invalid Option. Stoping program!\n")
            exit()
    



    
    # Results ###################################################################

    if player.is_playing == False and dealer.is_playing == False:
        
        # Indicar que el juego termino.
        has_game_started = False

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
            
            bet_money *= 2 #Se duplica lo apostado.

            print(" Player: " + str(player.value) + " Winner!")
            print(" Dealer: " + str(dealer.value) + " Loser...!")
        elif winner == "dealer":

            bet_money = 0 #El dealer se queda con la apuesta.

            print(" Player: " + str(player.value) + " Loser...!")
            print(" Dealer: " + str(dealer.value) + " Winner!")
        else:
            # Empate. Se devuelve la apuesta.

            print(" Player: " + str(player.value) + " Tie...!")
            print(" Dealer: " + str(dealer.value) + " Tie...!")

        money += bet_money # Se le da la apuesta (ya sea duplicada, tal cual estaba o cero.)

        print("\n ---------------------- Press Space to continue ----------------------")

        keyboard.wait("space")
        os.system('cls')

        loading_print(1.0)
        os.system('cls')

        while True:
            option = str(input("Do you want to play again sir? (y/n): "))

            if option.lower() == "y":
                restart()
                break
            elif option.lower() == "n":
                exit()
            else:
                print(" Invalid Option. Stoping program!\n")
                exit()
