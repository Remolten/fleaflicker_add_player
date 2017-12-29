import mechanize
import sys
import datetime
import time

def main():
    # Stores player_id's to add/drop and at what priority
    # [{'add': 1111, 'drop': 2222, 'priority': 1}]
    transactions = []
    
    # Check for correct command line arguments
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        raise 'Usage: python add.py user password player_data_file'
        
    try:
        with open(sys.argv[3]) as player_data_file:
            for transaction in player_data_file:
                if not transaction.isspace():
                    add_player_id = transaction.split('?')[1].split('=')[1].split('&')[0]
                    drop_player_id = transaction.split('?')[1].split('=')[2].split(' ')[0]
                    priority = transaction.split(' ')[1]

                    transactions.append({'add_player_id': add_player_id, 'drop_player_id': drop_player_id, 'priority': priority})

    except:
        raise Exception('Incorrectly formatted input file. Please paste only paste the urls of your desired transactions')
        
    # Sort the transactions by priority
    transactions.sort(key=lambda transaction: transaction['priority'])
    
    # Create a new browser instance
    browser = mechanize.Browser()
    
    # Go to the login page
    browser.open('http://fleaflicker.com/nfl/login')
    # Get the login form
    browser.select_form(nr=0)
    browser.form['email'] = sys.argv[1]
    browser.form['password'] = sys.argv[2]
    browser.submit()
    
    # Holds the time for waivers
    next_wed_time = datetime.datetime.utcnow()
    
    # If today is Wednesday and it is pass waivers time, set to next week
    if next_wed_time.weekday() == 2 and next_wed_time.hour >= 13:
        next_wed_time.replace(hour=0)
        next_wed_time += datetime.timedelta(days=7)
    
    # Iterate until we find the next Wednesday
    for i in range(6):
        if next_wed_time.weekday() != 2:
            # Increment by one day
            next_wed_time += datetime.timedelta(days=1)
            
    # Set next_wed_time to the correct time of day with a slight offset
    next_wed_time.replace(hour=13, minute=0, second=3)
    
    print(next_wed_time)
    print(datetime.datetime.utcnow())
            
    # Sleep until it is time to add the players
    time.sleep((next_wed_time - datetime.datetime.utcnow()).total_seconds())
    
    # Go to each player url and add them
    for transaction in transactions:
        browser.open('http://www.fleaflicker.com/nfl/leagues/68975/players/confirm?toAddPlayerId={0}&toDropPlayerId={1}'.format(transaction['add_player_id'], transaction['drop_player_id']))
        browser.select_form(nr=0)
        #browser.submit()
    
if __name__ == '__main__':
    main()