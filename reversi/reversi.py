import reversi_game
import reversi_console
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('reversi_type', help='reversi_type')

    args = parser.parse_args()
    if args.reversi_type == 'ENGINE':
        reversi_game.main()
    elif args.reversi_type == 'CONSOLE':
        reversi_console.main()
    else:
        print("WRONG INPUT")