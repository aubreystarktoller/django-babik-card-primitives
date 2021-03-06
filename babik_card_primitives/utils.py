import re
from babik_card_primitives.exceptions import (
    InvalidCardNumber,
    IssuerNotRecognised
)


CARD_ISSUERS = [
    {
        'regex': re.compile(r'^4[0-9]{12,18}$'),
        'slug': 'visa',
        'name': 'Visa',
    },
    {
        'regex': re.compile(r'^5[1-5][0-9]{14}$'),
        'slug': 'mastercard',
        'name': 'MasterCard',
    },
]


def get_card_issuer(number):
    """
    Use a card's number to determine it's issuer
    """
    number = str(number)
    for issuer_data in CARD_ISSUERS:
        if issuer_data['regex'].match(number):
            return issuer_data['slug'], issuer_data['name']
    raise IssuerNotRecognised()


def card_number_luhn_test(number):
    """
    Use Luhn's algorithm to varify a credit card number
    """
    reverse_digit_list = [int(n) for n in str(number)][::-1]
    odd_sum = sum(n for n in reverse_digit_list[0::2])
    even_sum = sum(sum(divmod(n * 2, 10)) for n in reverse_digit_list[1::2])
    return (odd_sum + even_sum) % 10 == 0


whitespace_re = re.compile("\s+")
dash_re = re.compile("([0-9])-+([0-9])")
card_number_re = re.compile("^[0-9]+$")


def clean_card_number(raw_number):
    """
    Removes any whitespace and dashes from a card number, throws an
    InvalidCardNumber if there are not numeric characters remaining
    """
    whitespaced_stripped_number = whitespace_re.sub("", raw_number)
    number = dash_re.sub(r"\1\2", whitespaced_stripped_number)
    if card_number_re.match(number):
        return number
    else:
        raise InvalidCardNumber
