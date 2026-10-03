# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

### What did the game look like the first time I ran it, and what bugs did I notice?

The first time I ran the game, it looked like a normal number guessing game: a title, a sidebar to choose the difficulty, a box to type my guess, and buttons to submit or start a new game. But once I started playing, I noticed that many things did not work correctly. The "Go Higher" and "Go Lower" hints were backwards, so they pointed me in the wrong direction. The game also told me I was out of attempts while I still had one try left. On top of that, typing letters still used up an attempt, and after winning, clicking "New Game" did not actually let me play again.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Typed `kfadjgdfghf` and clicked "Submit Guess" | The game shows an error and does not count it as an attempt, because it is not a valid input | The game showed the error, but it still used up one of my attempts | On screen: "That is not a number." No console error |
| Typed `43095702347873234` and `-24356452054095` and clicked "Submit Guess" | The game shows an error message, because these numbers are outside the allowed range | The game accepted them as normal guesses and showed "Go HIGHER!" / "Go LOWER!" hints | On screen: "📈 Go HIGHER!" / "📉 Go LOWER!" No console error |
| Won a game, then clicked "New Game" and typed a new guess | The game fully restarts: history is cleared and I can play again | The attempts reset to 8 and the secret number changed, but the old history stayed and typing a guess did nothing | On screen: "You already won. Start a new game to play again." No console error |

### Where Each Bug Comes From in the Code

- **Invalid input uses up an attempt:** in `app.py`, `st.session_state.attempts += 1` runs as soon as "Submit Guess" is clicked, before `parse_guess` checks whether the input is valid. So even text like "kfadjgdfghf" counts as an attempt.
- **Out-of-range numbers are accepted:** in `logic_utils.py`, `parse_guess` only checks that the input can be turned into a number. It never checks the allowed range (like 1 to 100), so huge or negative numbers are treated as normal guesses.
- **The game can't restart after a win:** in `app.py`, winning sets `st.session_state.status = "won"`, but the "New Game" button only resets `attempts` and `secret`. It never sets `status` back to `"playing"` or clears `history`. Because the status is still `"won"`, the app hits `st.stop()` before it can read any new guess.

### Game Run Trace

Terminal output when I ran the game:

```
(.venv) PS C:\Users\user4\Desktop\ai110-module1show-gameglitchinvestigator-starter> python -m streamlit run app.py
2026-10-03 15:06:34.834 Uvicorn server started on :::8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.14.0.2:8501
```

#### A problem I faced while playing (proof the game was run)

When I typed letters ("kfadjgdfghf"), the game correctly showed "That is not a number." However, it still counted that as one of my attempts. Invalid input shouldn't cost an attempt.

### Fixed Bug #1: Invalid input used up an attempt

I moved `attempts += 1` in `app.py` so it only runs after the input is confirmed valid.

### Fixed Bug #2: One attempt was missing

The counter in `app.py` started at `1`. I changed it to `0`, so each difficulty now gets its full attempts.

**Checked:** letters no longer cost an attempt, and each difficulty allows its full number of guesses.

### Fixed Bug #3: Fixing the inverted hints

In `check_guess` in `logic_utils.py`, the messages were swapped. I changed it so a guess that is too high now says "Go LOWER!" and a guess that is too low says "Go HIGHER!".

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

### Which AI tools did I use on this project?

I mainly used Claude Code inside VS Code, running the Claude Opus 5 model. I also used a free AI model, GPT5-6 Luna, to help me organize my prompts and explain some things to me, so I would not run out of credits on Claude Code.

### An AI suggestion that was correct

I usually work with JavaScript, and while playing the game I noticed that the input box let me type numbers above 100, text, and negative numbers. My first idea was to fix this by blocking invalid keystrokes directly in the browser. What I forgot is that this would require JavaScript to control the input. The AI caught this and explained that adding JavaScript to a Streamlit app is possible, but it would be over-complicated for this assignment, so a simple error message in Python is the better fit. I agreed this was the correct approach.

### An AI explanation of a bug

I asked Claude to explain why the game could not be restarted after a win. After I won and clicked "New Game", the attempts reset and a new secret number appeared, but the old history stayed and typing a new guess did nothing. Claude explained that the "New Game" button resets the attempts and the secret number but forgets to set `status` back to `"playing"` and to clear `history`. Because the status is still `"won"`, the app shows "You already won. Start a new game to play again." and calls `st.stop()`, which stops the app before it can read any new guess. This also explained why refreshing the page fixed it: a refresh starts a new session where `status` starts as `"playing"` again.

### An AI suggestion I did not accept

Claude listed "the score goes negative" as a bug. I rejected it, because losing points for wrong guesses makes sense in a guessing game, so a negative score is not a problem. I removed it from my bug list and kept the score logic as it is.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
