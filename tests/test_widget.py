import pytest

from src.widget import mask_account_card, get_date


@pytest.fixture
def account_num():
    return 'Счет 12345678901234567890'


def test_mask_account(account_num) -> None:
    assert mask_account_card(account_num) == 'Счет **7890'


@pytest.fixture
def card_num():
    return 'Visa Super 1234567890123456'


def test_mask_card(card_num) -> None:
    assert mask_account_card(card_num) == 'Visa Super 1234 56** **** 3456'


def test_mask_account_card_wrong_data(card_num) -> None:
    with pytest.raises(ValueError, match='Неверный формат данных'):
        mask_account_card('Visa Super 12345678901234')


def test_get_date() -> None:
    assert get_date('2018-06-30T02:08:58.425572') ==  '30.06.2018'


