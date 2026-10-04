def get_range_for_difficulty(difficulty: str):
    """
    Return the range of numbers the secret can be in for a difficulty.

    Args:
        difficulty: "Easy", "Normal" or "Hard".

    Returns:
        A tuple (low, high) with the inclusive range. Easy is 1 to 20,
        Normal is 1 to 100, Hard is 1 to 50. Any other value falls back
        to 1 to 100.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# FIX: I found that huge and negative numbers were accepted; Claude added the
# range check in app.py instead of here, because app.py knows the difficulty
# range
def parse_guess(raw: str):
    """
    Turn the text the player typed into a whole-number guess.

    Args:
        raw: the text from the guess input box.

    Returns:
        A tuple (ok, guess_int, error_message):
        - ok is True if the input is a whole number, otherwise False.
        - guess_int is the number, or None if the input is not valid.
        - error_message explains what is wrong ("Enter a guess.",
          "That is not a number." or "Please enter a whole number."),
          or None if the input is valid.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # FIX: I asked for only whole numbers to count; Claude found decimals like
    # 50.5 were cut down to 50 and added the "Please enter a whole number."
    # error, checked by a pytest test
    try:
        value = int(raw)
    except Exception:
        try:
            float(raw)
        except Exception:
            return False, None, "That is not a number."
        return False, None, "Please enter a whole number."

    return True, value, None


# FIX: I found while playing that the hints were inverted; I pointed Claude
# to this function, it swapped the messages, and pytest tests confirm them
def check_guess(guess, secret):
    """
    Compare a guess to the secret number.

    Args:
        guess: the player's guess.
        secret: the secret number.

    Returns:
        A tuple (outcome, message):
        - outcome is "Win", "Too High" or "Too Low".
        - message is the hint shown to the player, for example
          "Go LOWER!" when the guess is too high.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


# UI: I asked Claude to add Hot/Cold emojis to the hints, based on how close
# the guess is compared to the difficulty range
def get_temperature(guess, secret, low, high):
    """
    Describe how close a guess is to the secret as Hot, Warm or Cold.

    Args:
        guess: the player's guess.
        secret: the secret number.
        low: the lowest number in the difficulty's range.
        high: the highest number in the difficulty's range.

    Returns:
        "🔥 Hot!" if the guess is within 10% of the range from the secret,
        "🌡️ Warm" if it is within 25%, and "🧊 Cold" if it is further away.
    """
    distance = abs(guess - secret)
    range_size = high - low + 1

    if distance <= range_size * 0.10:
        return "🔥 Hot!"
    if distance <= range_size * 0.25:
        return "🌡️ Warm"
    return "🧊 Cold"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update the score after a guess.

    Args:
        current_score: the score before this guess.
        outcome: "Win", "Too High" or "Too Low".
        attempt_number: which attempt this guess was.

    Returns:
        The new score. A win adds more points the fewer attempts it took
        (at least 10), and wrong guesses usually subtract 5 points.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
