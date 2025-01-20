import pytest
from src.masks import get_mask_card_number, get_mask_account


#@pytest.fixture
#def card_num():
#    return [('Visa Super Puper 1234567890123456'),
#            ('Visa Super 1234567890123456'),
#            ('Visa 1234567890123456')]

#@pytest.mark.parametrize('card_num, expected', [('Visa Super Puper 1234567890123456'),
#                                                ('Visa Super 1234567890123456'),
#                                                ('Visa 1234567890123456')])

def test_get_mask_card_number():
    assert get_mask_card_number('Visa Super Puper 1234567890123456') == 'Visa Super Puper 1234 56** **** 3456'


def test_get_mask_card_number_len():
    with pytest.raises(ValueError, match='Неверный формат карты'):
        get_mask_card_number('Visa Super Puper 12345678901234')


def test_get_mask_account():
    assert get_mask_account('Счет 12345678901234567890') == 'Счет **7890'

def test_get_mask_account_len():
    with pytest.raises(ValueError, match='Неверный формат счета'):
        get_mask_account('Счет 1234567890123456789')
