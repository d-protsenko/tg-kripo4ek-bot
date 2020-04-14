from argparse import ArgumentParser
import logging


def parse_arguments():
    parser = ArgumentParser(description='telegram bot')
    parser.add_argument('-n', '--n',
                        type=str,
                        dest='number',
                        default='1',
                        help='number'
                        )
    return parser.parse_args()


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.log(logging.DEBUG, "main started")
    return 0


if __name__ == '__main__':
    args = parse_arguments()

