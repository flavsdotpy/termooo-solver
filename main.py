import logging
import time
from optparse import OptionParser
from unidecode import unidecode


PROHIBITED_CHARACTERS = [".", ",", "'"]


def config_logger():
    formatter = logging.Formatter(
        "[%(levelname)s][%(asctime)s][%(filename)-15s][%(lineno)4d][%(threadName)10s] - %(message)s"
    )
    formatter.converter = time.gmtime

    channel = logging.StreamHandler()
    channel.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel("INFO")
    logger.addHandler(channel)


def load_words(word_size: int = 5, language: str = "portuguese"):
    logging.info(f"Language: {language} Word size: {word_size}")
    words = list()
    with open(f"./resources/{language}.txt", "r") as fin:
        words = [unidecode(line.rstrip().lower()) for line in fin]
        for prohibited_character in PROHIBITED_CHARACTERS:
            words = [word for word in words if prohibited_character not in word]
    words_for_length = [word for word in words if len(word) == word_size]
    return words_for_length


def parse_options():
    parser = OptionParser()
    parser.add_option(
        "-e", "--excluded", dest="excluded",
        help="excluded characters, comma separated", metavar="EXCLUDED"
    )
    parser.add_option(
        "-i", "--included", dest="included",
        help="included characters, comma separated in the format `char-pos`, for positions they do not belong to",
        metavar="INCLUDED"
    )
    parser.add_option(
        "-x", "--exact_positions", dest="exact_positions",
        help="exact positions characters, comma separated in the format `char-pos`", metavar="EXACT"
    )
    parser.add_option(
        "-s", "--word_size", dest="word_size",
        help="size of the word", metavar="SIZE",
        default=5
    )
    parser.add_option(
        "-l", "--language", dest="language",
        help="language of the word", metavar="LANGUAGE",
        default="portuguese"
    )
    (options, _) = parser.parse_args()
    return options


def parse_char_coords_tuple(positions_str):
    coords_tuples = list()
    split_str = positions_str.split(",")
    for element in split_str:
        positions_ref = element.split("-")
        coords_tuples.append((positions_ref[0], positions_ref[1]))
    return coords_tuples


def run_excluded_filter(words, excluded_characters):
    filtered = words
    for character in excluded_characters:
        filtered = [word for word in filtered if character not in word]
    return filtered


def run_included_filter(words, included_characters_coords):
    filtered = words
    for character, not_position in included_characters_coords:
        filtered = [
            word for word in filtered
            if character in word
            and word[int(not_position)-1] != character
        ]
    return filtered


def run_exact_filter(words, exact_characters_coords):
    filtered = words
    for character, position in exact_characters_coords:
        filtered = [word for word in filtered if word[int(position)-1] == character]
    return filtered


def main():
    config_logger()
    logging.info("Started processing...")
    options = parse_options()

    logging.info("Loading words...")
    words = load_words(options.word_size, options.language)
    logging.info("Words loaded!")

    excluded_characters = options.excluded.split(",") if options.excluded else []
    logging.info(f"Excluded characters {excluded_characters}")

    included_characters_coords = parse_char_coords_tuple(options.included) if options.included else []
    logging.info(f"Included characters {included_characters_coords}")

    exact_characters_coords = parse_char_coords_tuple(options.exact_positions) if options.exact_positions else []
    logging.info(f"Exact characters positions: {exact_characters_coords}")

    words = run_excluded_filter(words, excluded_characters)
    words = run_included_filter(words, included_characters_coords)
    words = run_exact_filter(words, exact_characters_coords)

    logging.info(f"The correct word may be: {words}")
    logging.info("Finished processing!!!")


if __name__ == "__main__":
    main()
