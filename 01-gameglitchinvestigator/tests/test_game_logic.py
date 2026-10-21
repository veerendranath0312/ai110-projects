# FIX: Tests updated with Claude Code to unpack check_guess's (outcome, message) result
# and to cover the hint-direction and text-comparison bugs.
from logic_utils import check_guess

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

def test_too_high_guess_says_go_lower():
    # Bug 1: secret is 13 and guess is 20, so the hint should tell the player to go lower
    outcome, message = check_guess(20, 13)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_guess_says_go_higher():
    # Bug 1: secret is 13 and guess is 5, so the hint should tell the player to go higher
    outcome, message = check_guess(5, 13)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_single_digit_guess_compared_as_number():
    # Bug 2: comparing as text gives "9" > "13", so 9 was wrongly treated as too high
    outcome, message = check_guess(9, 13)
    assert outcome == "Too Low"
