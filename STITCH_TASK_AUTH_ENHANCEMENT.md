# Stitch Task: Authentication & User Profile Enhancement

## Context
The current authentication system in the `lunar-loot` repository is a simple "Spacetag" identity stored in the Streamlit `session_state`. There is no persistent user registration, password protection, or cloud-based storage for user profiles and high scores.

## Affected Files
- `catching_moonrocks.py`: Main application loop and UI state management.
- `enhanced_features.py`: Logic for saving/loading high scores (currently local JSON).
- `high_scores.json`: Current local storage for high scores.

## Current Functions & Logic

### `catching_moonrocks.py`
- **Session State Initialization**: Initializes `st.session_state.spacetag` to an empty string.
- **Identity Input**: Uses `st.text_input` in the `title` state to allow users to enter a "Spacetag" (username).
- **State Management**: Uses `st.session_state.game_state` to transition between screens (intro, about, title, level_start, playing, level_complete, level_failed, game_complete).
- **In-Game Display**: Shows the Spacetag in the HUD and on the mission briefing screen.

### `enhanced_features.py`
- **`save_high_score(spacetag, score, level)`**: Appends a score entry to `high_scores.json` and sorts the top 10.
- **`load_high_scores()`**: Reads scores from the local JSON file.

## Current UI/UX Flow
1. **Intro Screen**: Large logo with "Begin Game" and "About" buttons.
2. **Title Screen**: "Spacetag" text input, mission objectives, and "Start Game" button.
3. **Mission Briefing (`level_start`)**: Displays current level, sector name, and "Begin Mission" button.
4. **Gameplay (`playing`)**: Interactive MediaPipe hand-tracking session with HUD (Score, Level, Time, Spacetag).
5. **Level Results**: "Level Complete" or "Level Failed" screens with score summaries and (for failure) a "Space Selfie" download option.

---

## Task: Authentication & Persistence Enhancement

### Objective
Implement a robust authentication system that replaces the ephemeral Spacetag with persistent user accounts. This enhancement should allow users to sign up, log in with a password, and have their progress/high scores saved across sessions.

### Requirements

#### 1. Database Integration
- Replace the local `high_scores.json` with a database solution (e.g., SQLite for local, or a cloud provider like Supabase/Firebase for production).
- Define a `users` table/collection: `id`, `username` (unique), `password_hash`, `created_at`.
- Define a `scores` table/collection: `id`, `user_id`, `score`, `level`, `timestamp`.

#### 2. Enhanced UI Logic
- **Login/Sign-up Screen**: Create a new `auth` state in `catching_moonrocks.py`.
- Users must authenticate before reaching the `title` screen.
- Provide toggles between "Login" and "Sign-up" modes.
- Implement password hashing (e.g., using `bcrypt` or `hashlib`).

#### 3. Persistent Sessions
- Update `session_state` to store a `user_id` and `authenticated` boolean.
- Ensure the `spacetag` is automatically populated from the logged-in user's profile.
- Implement a "Logout" button in the `title` or `intro` screens.

#### 4. Global Leaderboard
- Update `load_high_scores` in `enhanced_features.py` to fetch from the database.
- Create a dedicated "Hall of Fame" screen accessible from the `intro` or `title` states to display global rankings.

### Technical Implementation Details
- **Encryption**: Use a secure hashing algorithm for passwords. Never store plain-text passwords.
- **API/Client Separation**: Ensure database calls are abstracted into `enhanced_features.py` to keep `catching_moonrocks.py` focused on the frontend/Streamlit logic.
- **Error Handling**: Add visual feedback for failed login attempts (e.g., "Invalid username or password").
