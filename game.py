import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
is_player=True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos,indicator):
        if indicator==0:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            if self.get_suit()=='S' or  self.get_suit()=='C':
                card_loc = (CARD_CENTER[0],CARD_CENTER[1])
            else:
                card_loc= (CARD_CENTER[0]+CARD_SIZE[0],CARD_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)     
                
                
# define hand class
class Hand:
    def __init__(self):
            # create Hand object
            self.in_hand=[]

    def __str__(self):
            # return a string representation of a hand
            s= ""
            for c in self.in_hand:
                s+=str(c)+ " "
            return s    
                

    def add_card(self, card):
            # add a card object to a hand
            self.in_hand.append(card)
            
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value=0
        is_ace=False
        for c in self.in_hand:
            value+=VALUES[c.get_rank()]
            if c.get_rank()=='A':
                is_ace=True
   
        if is_ace==True:
            if value+10<=21:
                  value+=10
        return value
        
        
   
    def draw(self, canvas, pos,ind):
        # draw a hand on the canvas, use the draw method for cards
        global is_player
        for c in self.in_hand:
            if is_player==True and self.in_hand.index(c)==0 and ind==1:
                c.draw(canvas,pos,1)
            else:    
                c.draw(canvas,pos,0)
            pos[0]+=CARD_SIZE[0]

            
            
 
 # define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck=[]
        for s in SUITS:
            for r in RANKS:
                c=Card(s,r)
                self.deck.append(c)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        c=random.choice(self.deck)
        self.deck.pop(self.deck.index(c))
        return c
    
    def __str__(self):
        # return a string representing the deck
        s=""
        for c in self.deck:
            s+=str(c)+" "     
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play,player,dealer,deck,is_player
    in_play = True
    is_player=True
    deck.shuffle()
    player=Hand()
    dealer=Hand()
    
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card()) 
   
 
def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global player,in_play,deck,outcome,score,is_player
    if in_play==True and is_player==True:
        if player.get_value()<=21:
            player.add_card(deck.deal_card())
            if player.get_value()>21:
                outcome="you have busted"
                in_play=False
                score-=1
            
    elif in_play==True and is_player==False:
            dealer.add_card(deck.deal_card())
            if dealer.get_value()>21:
                outcome="dealer has busted"
                in_play=False
                score+=1
      
       
         

        
            
def stand():  
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global dealer,in_play,deck,outcome,score,player,is_player
    is_player=False
    
    while dealer.get_value()<17 and in_play==True:
        hit()
    if in_play==True:
            if player.get_value()>dealer.get_value():
                outcome="you win"
                score+=1
                in_play=False
            else:
                outcome="you loose"
                score-=1
                in_play=False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global score,outcome,player,dealer
    canvas.draw_text("BLACKJACK",[100,100],40,"white")
    canvas.draw_text("score = "+str(score),[400,100],30,"black")
    
    
    canvas.draw_text("Dealer",[100,180],30,"black")
    canvas.draw_text(outcome,[350,180],30,"black")
    
    dealer.draw(canvas,[100,200],1)
    
    canvas.draw_text("Player",[100,380],30,"black")
    canvas.draw_text("Hit or Stand?",[350,380],30,"black")
    player.draw(canvas,[100,400],0)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

player=Hand()
dealer=Hand()
deck=Deck()

# get things rolling
deal()
frame.start()

