def main():
    # Holds the value of the user entered url and priority
    url = 'Fleaflicker'
    
    try:
        # Open the data file to be written to
        with open('players.dat', 'w') as player_data_file:
            # Get the first url from input
            print('Please enter the Fleaflicker transaction url and priority separated by a space')
            url = raw_input()
            
            # Run until the user enters whitespace only
            while not url.isspace():
                # Parse player_id's from the url
                # http://www.fleaflicker.com/nfl/leagues/68975/players/confirm?toAddPlayerId=11&toDropPlayerId=11 1
                try:
                    add_player_id = url.split('?')[1].split('=')[1].split('&')[0]
                    drop_player_id = url.split('?')[1].split('=')[2].split(' ')[0]
                    player_data_file.write('{0} {1} {2}'.format(add_player_id, drop_player_id, url.split(' ')[1]))
                except:
                    print('Url incorrectly formatted or file writing error')
                    return
                    
                print('Please enter the Fleaflicker transaction url and priority separated by a space')
                url = raw_input()
                
    except IOError:
        raise IOError

if __name__ == '__main__':
    main()