# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game purpose

A number guessing game built with Streamlit. The game picks a secret number in a range set by the difficulty (Easy 1–20, Normal 1–100, Hard 1–50). You guess, and the game tells you to go higher or lower until you find it or run out of attempts. Your score goes up for a quick win and down for wrong guesses.

### Bugs found and fixes applied

None of these bugs crashed the app or printed an error; they just made the game give wrong answers. Full reproduction steps are in the bug log in [reflection.md](reflection.md).

| #   | Bug                                                                                                                                                                               | Fix                                                                                                                                                     |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Backwards hints.** A guess that was too high said "Go HIGHER!", and a guess that was too low said "Go LOWER!".                                                                  | Swapped the messages in `check_guess`.                                                                                                                  |
| 2   | **Secret compared as text on every other attempt.** On even-numbered attempts the secret was turned into a string, so `"9" > "13"` was true and 9 counted as too high.            | Removed the `str()` conversion in `app.py` and the `except TypeError` fallback in `check_guess` that hid it. The secret is always compared as a number. |
| 3   | **New Game didn't restart the game.** After a win or loss the game stayed stuck on "You already won" / "Game over".                                                               | New Game now resets `status`, `score`, `history` and `attempts`, and picks the secret from the current difficulty's range, not always 1–100.            |
| 4   | **Empty guesses used up attempts.** "Attempts left" dropped on every empty or invalid submit and went into negative numbers.                                                      | Attempts now go up only for valid guesses.                                                                                                              |
| 5   | **New Game didn't clear the input box.** The last guess stayed in the box.                                                                                                        | New Game removes the text box's saved value from `st.session_state`.                                                                                    |
| 6   | **Submit needed two clicks after an error.** Typing a number and clicking Submit only cleared the old error, because leaving the text box caused its own rerun without the click. | Put the input box and Submit button in an `st.form`, so the typed guess and the click are sent together. Pressing Enter also submits.                   |

The game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) was also moved from `app.py` into `logic_utils.py` so it can be tested with pytest.

### Known issues (not fixed yet)

- "Attempts left" shows one fewer than allowed, because attempts start at 1. On Easy the game ends after 5 guesses instead of 6.
- The "Guess a number between 1 and 100" message ignores the difficulty.
- Hard uses 1–50, an easier range than Normal's 1–100.
- `update_score` gives +5 for a "Too High" guess on even-numbered attempts.
- Empty and invalid guesses are still added to the guess history.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app with `python -m streamlit run app.py` and pick a difficulty in the sidebar. The sidebar shows the range and how many attempts you get.
2. (Optional) Open "Developer Debug Info" to see the secret, for example 13.
3. Type a guess, for example 20, and click **Submit Guess 🚀** or press Enter. The hint says "📉 Go LOWER!" because 20 is above 13.
4. Guess 5. The hint says "📈 Go HIGHER!". Leaving the box empty and submitting shows "Enter a guess." without using up an attempt.
5. Guess 13. Balloons appear with "You won! The secret was 13." and your final score.
6. Click **New Game 🔁**. The input box is cleared, the score and history reset, and a new secret is picked from the current difficulty's range, so you can play again.

**Screenshot** _(optional)_: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest
============================= test session starts ==============================
platform darwin -- Python 3.12.4, pytest-9.1.1, pluggy-1.7.0
rootdir: .../01-gameglitchinvestigator
plugins: anyio-4.15.1
collected 6 items

tests/test_game_logic.py ......                                          [100%]

============================== 6 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
