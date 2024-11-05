import random


JAPANESE_NUMBERS = {1: 'ICHI', 2: 'NI', 3: 'SAN', 4: 'SHI', 5: 'GO', 6: 'ROKU'}
HOUSE_FEE = 40
START_SUM = 5000


class Player:

    def __init__(self, cash=START_SUM):
        self.__cash = cash

    def get_cash(self):
        return self.__cash

    def bet(self, amount):
        self.__cash -= amount
        return amount

    def gain(self, amount):
        self.__cash += amount



class House:

    def __init__(self):
        self.__cash = START_SUM*2

    def get_cash(self):
        return self.__cash

    def gamble(self, player, amount, guess):
        result=(random.randint(1,6), random.randint(1,6))
        if sum(result)%2==0 and guess=='even':
            self.__cash -= amount-HOUSE_FEE
            player.gain((amount*2)-HOUSE_FEE)
            return result[0], result[1], True
        elif sum(result)%2==1 and guess=='odd':
            self.__cash -= amount-HOUSE_FEE
            player.gain((amount*2)-HOUSE_FEE)
            return (result[0], result[1], True)
        else:
            return (result[0], result[1], False)


def check_balance(player, house):
    if player.get_cash()<41:
        print('look who lost all his money! Remember: house always wins, come again.')
    elif house.get_cash()<1:
        print('wow. You actually managed to outplay the house, now you are blacklisted for your life')


if __name__ == '__main__':
    you=Player()
    house=House()
    while True:
        print(f'You have {you.get_cash()} mon. How much do you bet? (or QUIT)')
        while True:
            bet=input('> ')
            try:
                bet=int(bet)
            except ValueError:
                if bet=='q':
                    exit()
                print('Please enter a valid number.')
                continue
            if bet<HOUSE_FEE+1 or bet>you.get_cash():
                print(f'Please enter an amount bigger than {HOUSE_FEE} and lower than your balance.')
                continue
            break
        print('The dealer swirls the cup and you hear the rattle of dice.')
        print('The dealer slams the cup on the floor, still covering the dice and asks for your bet.')
        print('CHO (even) or HAN (odd)?')
        while True:
            guess=input('> ')
            if isinstance(guess, str):
                guess=guess.lower()
                if guess =='cho':
                    guess='even'
                    break
                elif guess =='han':
                    guess='odd'
                    break
                elif guess in ['even', 'odd']:
                    break
            else:
                print('CHO (even) or HAN (odd)?')
        print(f'The dealer lifts the cup to reveal:')
        res=house.gamble(you, you.bet(bet), guess)
        print(JAPANESE_NUMBERS[res[0]], '-', JAPANESE_NUMBERS[res[1]])
        print(res[0], '-', res[1])
        if res[2]:
            print(f'You won! You take {bet} mon. The house collects a {HOUSE_FEE} mon fee.')
        else:
            print(f'You lost. All your bet goes to the house')