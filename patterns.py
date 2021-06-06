from itertools import product
from re import match


class PatternTooLong(Exception):
    def __init__(self, max_size: int, requested_size: int, block_size: int):
        self.message = f"The requested pattern size {requested_size} is larger than the maximum pattern size {max_size} using a block size of {block_size} "
        super().__init__(self.message)


class InvalidPattern(Exception):
    def __init__(self, supplied_pattern: str):
        self.message = f"The supplied pattern must match [A-Z]+.  What was supplied was {supplied_pattern}"
        super().__init__(self.message)


def create_pattern(pattern_len: int, block_size: int = 4) -> str:
    """
    :param pattern_len: The length of the final pattern you want.  it must be less than 24^block_size
    :param block_size: What block size should the pattern utilize.  When targeting DWORDS (x32 bit arch) chose 4, for QWORDS (x64 bit arch) choose 8.  Default 4
    :return: Returns a string of size pattern_len which has non-repeating blocks of size block_size
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    max_pattern_size = len(letters) ** block_size
    if pattern_len > max_pattern_size:
        raise PatternTooLong(max_size=max_pattern_size, requested_size=pattern_len, block_size=block_size)
    list_of_n_lists = [list(letters) for i in range(
        block_size)]  # creates a list of size i, where each element in the list is equivelent to list(letters)
    result = ""
    count = 0
    for char_tuple in product(*list_of_n_lists):
        result += ''.join(char_tuple)  # product yields a tuple of single characters.  we want ultimately a string.
        count += block_size
        if count >= pattern_len:  # are we done?
            break
    return result[:pattern_len]  # just in case pattern_len is not evenly divisible by block_size, we will need to trim


def find_pattern_offset(pattern_to_match):
    """
    :param pattern_to_match: The pattern to search for.  Must match the regex [A-Z]+
    :return: the offset, as an index, the pattern would be located if using the create_pattern function as the generator
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    block_size = len(pattern_to_match)  # the block size must be equal to len(pattern_to_match)
    if not match(f"[A-Z]+", pattern_to_match):
        raise InvalidPattern(supplied_pattern=pattern_to_match, block_size=block_size)
    list_of_n_lists = [list(letters) for i in range(block_size)]
    count = 0
    pattern_to_match = tuple(pattern_to_match)
    for char_tuple in product(*list_of_n_lists):
        if pattern_to_match == char_tuple:
            break
        else:
            count += block_size
    return count
