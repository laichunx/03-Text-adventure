import sys, logging, json

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def render():
    ''' Display the current location '''
    return True

def update():
    ''' Update our location, if posible, etc. '''
    return True

def check_input():
    ''' get user input '''
    response = input('What would you like to do? ')
    return response

def main():
    game = {}
    with open('zork.json') as json_file:
        game = json.load(json_file)
    # Your game goes here!

    current = 'WHOUS'

    quit = False

    while not quit:
        # render
        render()
        # check input
        check_input()
        # update
        update()
    return True



#if we are running this from the command line, run main
if __name__ == '__main__':
	main()