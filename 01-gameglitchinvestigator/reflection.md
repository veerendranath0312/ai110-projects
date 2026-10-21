# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran it, the game looked finished: a title, a difficulty setting in the sidebar, an input box, Submit and New Game buttons, and a "Developer Debug Info" panel that shows the secret. Playing it didn't work. I started by guessing 20, and every hint told me to "Go HIGHER!", so I kept moving away from the secret, which turned out to be 13. Nothing showed up as an error in the console, so every bug was silent and I could only find them by comparing what the game said with what it should have said. The two bugs I noticed first were that **the hints were backwards** and that **New Game didn't really restart the game** after a win or loss. More bugs turned up once those were fixed (see the log below).

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                                                      | Expected Behavior                                                       | Actual Behavior                                                                                                                                                                                                                                                                                                             | Console Output / Error                                                                                                          | Suspected Code Location                                                                                                                                       |
| ---------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Secret is 13. Guess 20, then keep guessing higher numbers. | 20 is above 13, so the hint should say "Go LOWER!"                      | Every guess shows "📈 Go HIGHER!" and moves me further from 13. The game correctly decides the guess is "Too High", but `check_guess` in `app.py` attaches the wrong message: "Too High" says "Go HIGHER!" and "Too Low" says "Go LOWER!".                                                                                  | No error. The wrong message is shown silently.                                                                                  | `app.py` lines 37–47, in `check_guess`: the "Go HIGHER!" and "Go LOWER!" messages are swapped.                                                                |
| Secret is 13. Guess 9 on two attempts in a row.            | 9 is below 13, so both guesses should get the same "Too Low" result.    | The result changes between attempts. On even-numbered attempts `app.py` turns the secret into text (`str(secret)`), so the comparison is done letter by letter: `"9" > "13"` is true, and 9 is treated as "Too High". On odd attempts it's compared as a number and treated as "Too Low".                                   | No error. The `TypeError` from comparing a number with text is caught by `except TypeError`, so nothing appears in the console. | `app.py` lines 158–159: `secret = str(st.session_state.secret)` on even attempts, plus the `except TypeError` fallback in `check_guess` (lines 42–47).        |
| Win or lose a game, then click "New Game 🔁".              | A fresh game starts and I can guess again.                              | The game still says "You already won" or "Game over" and won't take guesses. The New Game button resets `attempts` and `secret` but never sets `status` back to `"playing"`, so the app stops early. It also doesn't clear `score` or `history`, and it always picks the new secret from 1 to 100, whatever the difficulty. | No error. `st.stop()` ends the page quietly.                                                                                    | `app.py` lines 134–138, the `if new_game:` block: `status`, `score` and `history` are never reset, and `random.randint(1, 100)` ignores the difficulty range. |
| Submit the guess box empty (or type "abc") several times.  | An empty or invalid guess shows an error and doesn't use up an attempt. | Every empty submit lowers "Attempts left", and it keeps going past 0 into negative numbers. The game never ends, because the "out of attempts" check only runs for valid guesses.                                                                                                                                           | No error in the console. The page shows "Enter a guess." while the attempts counter keeps dropping.                             | `app.py`, the `if submit:` block: `st.session_state.attempts += 1` runs before `parse_guess` checks the input, so invalid input is counted as an attempt.     |
| Type a guess, then click "New Game 🔁".                    | The game restarts with an empty guess box.                              | The old guess is still in the input box after the new game starts.                                                                                                                                                                                                                                                          | No error.                                                                                                                       | `app.py`, the `if new_game:` block: it resets the game data but never clears the text box's saved value (`guess_input_{difficulty}` in `st.session_state`).   |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**AI tools used:** Claude Code (Anthropic), in agent mode inside VS Code. I described what I saw while playing, and Claude read the code, explained the cause, proposed a fix plan, edited the files and ran the tests. I approved each step before it moved on.

**A correct AI suggestion: putting the guess box in a form**

- **What the AI suggested:** After an empty guess showed an error, typing a number and clicking "Submit Guess" only cleared the error; it didn't check my guess. Claude explained that clicking the button while still typing makes Streamlit rerun twice: once when the text box loses focus (saving the text, with `submit` still `False`) and again for the click. It suggested wrapping the text input and the Submit button in `st.form` so the typed value and the click arrive in the same rerun.
- **Why it was correct:** Claude reproduced my exact symptom in Streamlit's test tool by simulating "typing only": the error cleared, no hint appeared and attempts didn't change. That matched what I saw, so the explanation fit the evidence instead of being a guess.
- **How I verified it:** Claude said its test tool couldn't recreate the browser timing, so I tested it myself in the browser: an empty guess, then a number, then one click on Submit. The hint now appears on the first click. Pressing Enter also submits now.

**A suggestion I did not accept as written**

_TODO: fill this in with a real example. Ideas from this session: Claude's Step 3 fix restarted `attempts` at 1 to match startup, which kept the bug where Easy ends after 5 guesses instead of 6; or a fix whose layout or approach you'd change._

- **What the AI suggested:**
- **Why I rejected or changed it:**
- **How I verified my version:**

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**How I decided a bug was really fixed:** I counted a bug as fixed only when two things were true: a check that failed (or would have failed) before the fix passed afterwards, and the game behaved correctly when I played the same steps that showed the bug. We fixed one bug at a time and ran `pytest` after each fix, so a new change couldn't quietly break an earlier one.

**Tests I ran:**

- **pytest:** First we moved the game logic into `logic_utils.py` so it could be tested. The original tests only checked the outcome ("Too High"), not the message, which is why they never caught the backwards hints. We added tests for that: `check_guess(20, 13)` must say LOWER and `check_guess(5, 13)` must say HIGHER. We also added `check_guess(9, 13)`, which must be "Too Low" because, compared as text, `"9" > "13"`. Final result: `6 passed`.
- **Streamlit's test tool (`AppTest`):** Claude used it to play the app from a script with the secret set to 13. It showed that 9 is now treated as "Too Low" on every attempt (the score dropped by 5 each time instead of going up and down), that New Game after a win or loss gives a playable game with score 0 and an empty history, and that 10 empty submits leave "Attempts left" unchanged. It also showed something pytest can't: on Easy the game ended after 5 guesses instead of 6, a bug that's still open.
- **Playing in the browser:** After the hint fix, guesses moved toward the secret correctly. Playing is also how I found the bugs where empty guesses drove attempts negative, the input box wasn't cleared, and Submit needed two clicks. I confirmed the Submit fix in the browser myself.

**How AI helped with testing:** Claude suggested testing the hint message, not just the outcome, and explained why the original tests missed bug 1. It was also clear about the limits of each test. The `check_guess(9, 13)` test can't catch `app.py` turning the secret into text, and its test tool can't recreate the browser's timing, so for those it told me to rely on the app test and on my own play-through.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

A Streamlit app is a Python script that runs again from top to bottom every time you interact with it: click a button, type in a box, change a dropdown. That's a "rerun". Because the whole script restarts, ordinary variables are wiped out every time, so `st.session_state` acts like the app's memory: a dictionary that survives reruns, where this game keeps the secret, attempts, score and history. Buttons are tricky because `st.button` is only `True` during the one rerun caused by its click. That's why the Submit bug happened: leaving the text box caused its own rerun before the click, and in that rerun `submit` was `False`. Many of the bugs came down to state, too: New Game forgot to reset `status`, and the input box keeps its own value in session state, so clearing it meant removing that key.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**A habit to reuse:** Fix one bug at a time, and for each one: reproduce it, make the smallest change, add a test that checks the actual behavior (the message, not just the outcome), play through it again, then commit. Working in small steps made each fix easy to understand and to check, and when something new broke I knew which change caused it. Asking the AI for a plan first and approving one step at a time kept me in control of what changed.

**What I'd do differently:** I'd question the AI's choices more instead of just accepting them. For example, in the New Game fix it chose to restart attempts at 1 "to match startup", which kept the bug where you get one guess fewer than allowed. I'd also test in the real browser earlier, because the AI's test tool couldn't reproduce the Submit bug that I found by playing.

**How my thinking changed:** AI-generated code can look finished and run without a single error and still be wrong in several places, because none of these bugs crashed; they just gave wrong answers. Now I treat AI code as a draft that I have to prove works by testing and playing it, not as something that's correct because it runs.
