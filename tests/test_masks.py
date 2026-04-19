import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number('1234567890123456') == '1234 56** **** 3456'


def test_get_mask_account() -> None:
    assert get_mask_account('12345678901234567890') == '**7890'
