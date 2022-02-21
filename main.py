import logging
import time
from optparse import OptionParser
from unidecode import unidecode


def config_logger():
    formatter = logging.Formatter(
        "[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s"
    )
    formatter.converter = time.gmtime

    channel = logging.StreamHandler()
    channel.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel('INFO')
    logger.addHandler(channel)


def parse_options():
    parser = OptionParser()
    parser.add_option("-e", "--excluded", dest="excluded",
                      help="excluded characters, comma separated", metavar="EXCLUDED")
    parser.add_option("-i", "--included", dest="included",
                      help="included characters, comma separated", metavar="INCLUDED")
    parser.add_option("-x", "--exact_positions", dest="exact_positions",
                      help="exact positions characters, comma separated in the format `char-position`", metavar="EXACT")
    (options, _) = parser.parse_args()
    return options


def get_exact_characters(exact_positions):
    exact_position_characters = dict()
    exact_positions_list = exact_positions.split(',')
    for e in exact_positions_list:
        positions_ref = e.split('-')
        exact_position_characters[positions_ref[0]] = positions_ref[1]
    return exact_position_characters


def run_excluded_filter(words, excluded_characters):
    filtered = words
    for chararacter in excluded_characters:
        filtered = [word for word in filtered if chararacter not in word]
    return filtered


def run_included_filter(words, included_characters):
    filtered = words
    for chararacter in included_characters:
        filtered = [word for word in filtered if chararacter in word]
    return filtered


def run_exact_filter(words, exact_position_characters):
    filtered = words
    for character, position in exact_position_characters.items():
        filtered = [word for word in filtered if word[int(position)-1] == character]
    return filtered


def main():
    config_logger()
    logging.info('Started processing...')
    options = parse_options()

    logging.info('Loading words...')
    words = list()
    with open('./5_chars_words.txt', 'r') as fin:
        words = [unidecode(line.rstrip().lower()) for line in fin]
    logging.info('Words loaded!')

    excluded_characters = options.excluded.split(',') if options.excluded else []
    logging.info(f'Excluded characters {excluded_characters}')

    included_characters = options.included.split(',') if options.included else []
    logging.info(f'Included characters {included_characters}')

    exact_characters = get_exact_characters(options.exact_positions) if options.exact_positions else []
    logging.info(f'Exact characters positions: {exact_characters}')

    words = run_excluded_filter(words, excluded_characters)
    words = run_included_filter(words, included_characters)
    words = run_exact_filter(words, exact_characters)

    logging.info(f'The correct word may be: {words}')
    logging.info('Finished processing!!!')


if __name__ == '__main__':
    main()
