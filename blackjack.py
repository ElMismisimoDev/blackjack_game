import random
import os
import time
import keyboard
import msvcrt

# Variables ###################################################

deck = []
has_game_started = False
winner = None

money = 5000
bet_money = 0
takenLoans = 0

CARDS = range(1, 14)
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
        self.aceCards = 0

    def reset(self):

        self.hand = []
        self.value = 0
        self.is_playing = True
        self.aceCards = 0

    def choose_card(self):
    
        card = deck[random.randrange(len(deck))]
        deck.remove(card)
        return card
    
    def get_card_value(self, card):
        
        cardValue = 0
        number = ""

        for ch in card:
            if ch.isdigit():
                number += ch

        if number == "1": # El 1 es el Ace.
            cardValue = 11
            self.aceCards += 1
        elif number in ("11", "12", "13"):
            cardValue = 10
        else:
            cardValue += int(number)        

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
        if number == "1": #El numero 1 es para los ases.
            cardName = "Ace of " + type
        elif number == "11":
            cardName = "Jack of " + type
        elif number == "12":
            cardName = "Queen of " + type
        elif number == "13":
            cardName = "King of " + type
        else:
            cardName = number + " of " + type

        return cardName

    def giveCard(self): # Se llama a esta funcion cuando se hace un "hit".
        
        global winner

        card = self.choose_card()
        cardName = self.card_name(card)

        # Identificar el tipo de carta para mostrarla (solo para el player).

        if self.name == "player":
            
            print("\n ##############################################################\n")
            print(" Card: " + cardName)
        

        # Añadir la carta a la mano y sumar el valor de esta.

        self.hand.append(cardName)
        self.value += self.get_card_value(card)


        # Calcular si la mano ya vale 21 o se pasa de 21.

        while True: # Un bucle que termina cuando se realizan todas las comprobaciones.

            if self.value == 21:
                
                if self.name == "player":
                    print("\n\n It seems you got a total of 21!!!")
                    self.is_playing = False
                    break
                else:
                    self.is_playing = False
                    break
                    
            elif self.value > 21:

                if self.aceCards > 0:

                    self.aceCards -= 1
                    self.value -= 10
                    continue
                else:

                    if self.name == "player":
                        print("\n\n Oops! It seems you got above 21...")
                        self.is_playing = False
                        winner = "dealer"
                        break
                    else:
                        self.is_playing = False
                        break
            else:
                break

        if self.name == "player":
            print("\n ##############################################################\n")
            time.sleep(3.0)
            os.system('cls')
    
        
        return
                    
    def stand(self):
        self.is_playing = False

    def double_down(self):

        global money
        global bet_money

        money -= bet_money
        bet_money *= 2

        print("You are doubling your bet for a total value of " + str(bet_money) + "$")
        time.sleep(2.0)
        print("You have " + str(money) + "$ left.")
        
        time.sleep(3.5)
        os.system('cls')

        self.giveCard()
        self.stand()

    def should_hit(self): # Solo para la IA.
        """
        (Solo para la IA) Devuelve True si el dealer pide carta, False si se planta.
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

def clean_buffer():
    """
    Limpia el buffer de entrada
    """
    while msvcrt.kbhit(): msvcrt.getch()

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

            clean_buffer()
            bet_money = int(input("Select the quantity you want to bet.\nYour money: " + str(money) + "$\n\n"))
            os.system('cls')
    
            if bet_money > 0 and bet_money <= money:

                print("You are gonna bet " + str(bet_money) + "$")
                print("Are you sure? (y/n): ")

                while True:
                    
                    if keyboard.is_pressed("y"):

                        os.system('cls')

                        money -= bet_money 
                        print("Okay. The game is about to start.")

                        time.sleep(2.0)
                        os.system('cls')
                        return
                    elif keyboard.is_pressed("n"):

                        os.system('cls')
                        break

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

        print("Do you want to take the loan sir? (y/n):\n\n")

        while True:

            if keyboard.is_pressed("y"):

                os.system('cls')

                money += 5000
                takenLoans += 1
                print("Good. Here's your money sir. Enjoy")

                time.sleep(2.0)
                os.system('cls')
                return
            elif keyboard.is_pressed("n"):

                os.system('cls')

                print("In that case, this is the end of the game sir.")
                time.sleep(1.5)
                print("Have a great night")
                time.sleep(1.5)

                exit()

def introduction():

    print("Hello")
    time.sleep(2.0)
    print("You're about to play blackjack, you know the rules right?")
    time.sleep(2.0)
    print("The objective is to get the closest possible to 21 with your cards. Simple.")
    time.sleep(2.5)
    print("If you get above 21, you lose.")
    time.sleep(3.5)
    os.system('cls')
    
    print("Sir, do you need me to explain how Blackjack works? (y/n)")

    while True:

        if keyboard.is_pressed("y"):

            os.system('cls')

            time.sleep(2.0)
            print("I, the dealer, will deal 2 cards to both you and me.")
            time.sleep(2.0)
            print("Each card has a value, his number.")
            time.sleep(1.5)
            print("Except for some cards, like the Jack, the Queen and the King, which have a value of 10.")
            time.sleep(2.5)
            print("And also there's a special card, the Ace, which has both values: 11 and 1")
            time.sleep(2.0)
            print("If for any reason you get above 21, the Ace will have a value of 1, instead of 11.")

            time.sleep(3.0)

            print("\nWhen playing, you will have 3 options: Hit, Stand and Double") #Actualizar si se meten mas opciones.
            time.sleep(2.0)
            print("\nIf you choose the 'hit' option, I will give you another card. Simple.\nHowewer, if you get above 21, you will immediately lose.")
            time.sleep(2.5)
            print("\nIf you choose the 'stand' option, you will stop playing and you will keep the total value of all your cards.")
            time.sleep(2.5)
            print("\nIf you choose the 'double down' option, you will double your bet and you will get another card and immediately stand.\n")
            time.sleep(2.5)
            print("The game continues until someone loses or both you and me choose to 'stand'.")
            time.sleep(2.0)
            print("The player that get closer to 21, wins.")

            time.sleep(2.5)
            print("\n ---------------------- Press Space to continue ----------------------")
            
            keyboard.wait('space')
            os.system('cls')
            break

        elif keyboard.is_pressed("n"):
            
            os.system('cls')

            print("Nice. Let's start in that case.")

            time.sleep(2.0)
            os.system('cls')
            break
    

def start():

    global has_game_started

    choose_bet() # Elegimos la cantidad que queremos apostar.

    loading_print(2.5)

    create_deck() # Creamos la baraja para poder repartir las cartas.

    for user in UsersList: # Repartimos las cartas.
        for x in range(2):
            user.giveCard()

    has_game_started = True

def restart():
    
    global deck
    global winner
    global UsersList

    deck = []
    winner = None

    for user in UsersList:
        user.reset()

    os.system('cls')
    if money <= 0:
        loan()

    start()













# Program #####################################################

introduction()

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

        print("\n Pick a option:\n\n 1. Hit\n 2. Stand\n 3. Double Down\n\n")
        
        while True:

            if keyboard.is_pressed("1"):

                os.system('cls')
                
                player.giveCard()
                break
    
            elif keyboard.is_pressed("2"):
                
                os.system('cls')
                
                player.stand()
                break

            elif keyboard.is_pressed("3"):

                os.system('cls')

                if money >= bet_money:
                    player.double_down()
                    break
                else:
                    print("Sorry sir, you dont have enough money left to double down.")
                    time.sleep(2.0)
                    print("Please, choose other option.")
                    time.sleep(2.0)
                    os.system('cls')
                    break

    

    
    # Results ###################################################################

    if player.is_playing == False and dealer.is_playing == False:
        
        loading_print(2.5)

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

        print("\nEarned Money: " + str(bet_money) + "$")
        print("Actual money: " + str(money) + "$")

        print("\n ---------------------- Press Space to continue ----------------------")

        keyboard.wait("space")
        os.system('cls')

        loading_print(1.0)

        print("Do you want to play again sir? (y/n): ")

        while True:
            
            if keyboard.is_pressed("y"):
                restart()
                break
            elif keyboard.is_pressed("n"):
                os.system('cls')
                print("Goodbye then.")
                time.sleep(1.5)
                exit()
