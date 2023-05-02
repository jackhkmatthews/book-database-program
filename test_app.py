import sys
from io import StringIO

from app import menu


def test_menu(monkeypatch):
    user_input = "2\n"
    expected_output = """
              \nProgramming books
              \r1) add book
              \r2) View all books
              \r3) Search for book
              \r4) Book analysis
              \r5) Exit\nWhat would you like to do? """
    with monkeypatch.context() as m:
        m.setattr("sys.stdin", StringIO(user_input))
        captured_output = StringIO()
        sys.stdout = captured_output

        result = menu()

        assert result == "2"
        assert captured_output.getvalue() == expected_output
