from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug fix: the hints were inverted, a guess that is too high must say "Go LOWER!"
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug fix: the hints were inverted, a guess that is too low must say "Go HIGHER!"
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_letters_are_rejected():
    # Bug fix: letters are not a valid guess, so they show an error
    ok, guess, error = parse_guess("kfadjgdfghf")
    assert ok is False
    assert error == "That is not a number."

def test_decimal_is_rejected():
    # Bug fix: decimals like 50.5 used to be cut down to 50, now they show an error
    ok, guess, error = parse_guess("50.5")
    assert ok is False
    assert error == "Please enter a whole number."

def test_empty_input_is_rejected():
    # Edge case: clicking Submit Guess with an empty box should not count as a guess
    ok, guess, error = parse_guess("")
    assert ok is False
    assert error == "Enter a guess."

def test_symbols_are_rejected():
    # Edge case: an input with only symbols is not a number, so it shows an error
    ok, guess, error = parse_guess("@#$")
    assert ok is False
    assert error == "That is not a number."
