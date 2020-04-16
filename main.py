from argparse import ArgumentParser
import logging
import bot


def parse_arguments():
    parser = ArgumentParser(description='telegram bot')
    parser.add_argument('-t', '--token',
                        type=str,
                        dest='token',
                        default='token',
                        help='tg bot token'
                        )
    return parser.parse_args()


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.log(logging.DEBUG, "main started")
    return 0


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    args = parse_arguments()
    bot.start()
