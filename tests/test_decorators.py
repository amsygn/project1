from src.decorators import log


@log()
def my_function(x, y):
    return x + y


def test_my_function(capsys):
    my_function(1, 2)
    content = capsys.readouterr()
    assert "my_function ok" in content.out


def test_my_function_error(capsys):
    try:
        my_function(1)
    except Exception as e:
        content = capsys.readouterr()
        assert f"my_function error: {type(e).__name__}. Inputs: {x, y}, kwargs:", "{}\n" in content.out
