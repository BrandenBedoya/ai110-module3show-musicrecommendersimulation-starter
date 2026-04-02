# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use and Non-Intended Use

**Intended use:** VibeFinder is a content-based music recommender designed for classroom exploration of how recommendation algorithms work. Given a user's preferred genre, mood, and energy level, it scores a 20-song catalog and returns the top 5 matches. It is built to make the mechanics of weighted scoring visible and auditable — every recommendation includes an explanation of why it ranked where it did.

**Non-intended use:** This system should not be used as a real product for actual listeners. It makes several assumptions that would be harmful at scale: it treats each user as having a single fixed taste (real people's moods shift constantly), it cannot learn from feedback, it has no user privacy protections, it reflects a narrow Western pop-centric catalog, and its synthetic audio attributes were manually estimated rather than derived from real audio analysis. Using this system to make decisions about what real users are exposed to — especially in contexts involving personalization, advertising, or content gatekeeping — would be inappropriate.

---

## 3. How the Model Works

Every song in the catalog gets a relevance score based on how well it matches the user's preferences. Think of it like a judge at a cooking competition scoring each dish against a specific criteria list.

The scoring works like this: if a song's genre matches what the user wants, it earns the most points (3.0). If the mood also matches, it earns additional points (2.0). For energy level, the system rewards closeness — a song with energy very close to what the user wants scores up to 1.5 extra points, while a song far off scores close to zero. Finally, if the user likes acoustic sounds and a song is primarily acoustic, it gets a small bonus (1.0). All these points are added together, and the songs with the highest totals are recommended.

The system then sorts all 20 songs by their score from highest to lowest and returns the top 5.

---

## 4. Data

The catalog contains **20 songs** spanning 13 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, electronic, classical, country, metal, folk, reggae, k-pop, and blues. Moods include: happy, chill, intense, relaxed, focused, moody, motivated, romantic, euphoric, peaceful, nostalgic, and melancholic.

The original 10 songs were provided in the CodePath starter file. Ten additional songs were added manually to improve genre and mood diversity. The dataset reflects a Western, English-language popular music perspective — no Latin, Afrobeats, or world music genres are represented. The energy and acousticness values are synthetic estimates, not pulled from a real audio analysis API like Spotify's.

---

## 5. Strengths

- **Clear genre matches work well.** When a user profile aligns tightly with an available genre (e.g., lofi/chill or rock/intense), the top results feel intuitive and match musical expectation.
- **The acoustic bonus adds meaningful texture.** For the Chill Lofi Study profile, Spacewalk Thoughts (ambient, acousticness 0.92) bubbled up to #4 despite being the wrong genre, because mood + energy + acoustic bonus combined were enough to overcome the genre gap. That's a reasonable recommendation.
- **Transparent and auditable.** Every recommendation shows its exact score breakdown, so it's easy to understand why any song ranked where it did. Real systems (Spotify, YouTube) give you no such explanation.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** At 3.0 points, a genre match is worth more than a perfect mood + near-perfect energy combined in many cases. A user who prefers "lofi" will almost never see a jazz song that exactly matches their mood and energy, because the 3.0-point genre penalty is too large to overcome. This mirrors how real recommendation systems trap users in a "more of the same" loop.

**Mood labels are brittle strings.** "Chill" and "relaxed" are very similar emotions but get treated as completely different. A relaxed jazz track gets zero mood credit for a chill user, even though most listeners would consider them interchangeable. This is a direct consequence of using exact string matching instead of a semantic or vector-based comparison.

**The dataset skews toward specific moods.** "Happy" and "chill" appear multiple times in the 20-song catalog; moods like "euphoric," "melancholic," and "nostalgic" appear only once. A user asking for "euphoric" music can only ever mood-match a single song (Drop Everything), so most of their top 5 will be pulled by genre or energy alone.

**No diversity enforcement.** The ranking rule returns the top-k closest matches, which means results can cluster. For the Chill Lofi Study profile, three of the top five results were lofi songs — correct genre, but zero genre variety. A real system would inject occasional surprises to prevent listener fatigue.

**The "conflicted listener" problem.** When a user profile has internally conflicting preferences (ambient genre but high energy 0.9), the system resolves the conflict blindly — genre wins because it has the highest weight (3.0), so it returns Spacewalk Thoughts (ambient, energy 0.28) as #1 even though its energy is 0.62 away from the user's target. The system has no mechanism to detect or flag contradictory preferences.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Genre | Mood | Energy | Acoustic |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.85 | False |
| Chill Lofi Study | lofi | chill | 0.38 | True |
| Deep Intense Rock | rock | intense | 0.92 | False |
| Conflicted Listener | ambient | euphoric | 0.90 | True |

**What matched intuition:** Chill Lofi Study returned the two lofi/chill songs (Library Rain, Midnight Coding) as #1 and #2 with nearly identical scores (7.46 vs 7.44) — the tie-breaking was energy proximity alone. That felt correct.

**What was surprising:** For High-Energy Pop, Gym Hero (#2, 4.38) scored lower than expected. It's a pop/intense song at 0.93 energy — it matches genre but misses mood. The score gap between #1 (6.46) and #2 (4.38) shows how much the mood match (2.0 pts) matters. Without mood, Gym Hero drops 2 full points despite being a nearly perfect energy fit.

**Weight shift experiment:** Genre weight halved (3.0→1.5), energy weight doubled (1.5→3.0). For High-Energy Pop, Neon Petals (k-pop) jumped from #3 to #2, and Gym Hero dropped from #2 to #4. A k-pop song beat a pop song once genre became less dominant — showing the system is highly sensitive to weight calibration.

**Conflicted Listener edge case:** This profile exposed the system's inability to resolve contradictions. The user wants high energy (0.9) but also ambient genre, which only has one representative song with energy 0.28. The system returned that ambient song at #1 despite the massive energy mismatch, because 3.0 genre points outweighed the 0.57 energy score. A user receiving that recommendation would be confused.

---

## 8. Future Work

- **Semantic mood matching:** Replace string equality with a mood similarity table (e.g., "chill" and "relaxed" score 0.8 similarity instead of 0 or 1). This would dramatically improve results for users whose preferred mood doesn't have an exact catalog match.
- **Genre proximity groupings:** Similar to mood, grouping genres (e.g., lofi and ambient share a "low-energy chill" cluster) would allow better cross-genre recommendations without losing the importance of genre as a signal.
- **Contradiction detection:** If a user's energy preference is far from what their genre typically produces, surface a warning: "Your energy preference (0.9) is unusual for ambient music. Did you mean electronic?"
- **Diversity penalty:** After ranking, apply a light penalty to songs that are too similar to already-selected recommendations. This prevents the top 5 from being almost identical tracks.
- **Expanded catalog:** 20 songs is too small for genre-based scoring. With only 1–3 songs per genre, the system frequently falls back to energy-only matching for anything outside the top 3 genres.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight shift experiment was the clearest "aha" moment. Halving the genre weight from 3.0 to 1.5 and doubling the energy weight from 1.5 to 3.0 caused a k-pop song to outrank a pop song for a pop user. Nothing about the songs changed — only the policy embedded in the numbers changed. That's when it clicked that recommendation systems aren't discovering some objective truth about what you'll like; they're enforcing the designer's judgment about which signals matter more. Every Spotify "Discover Weekly" reflects someone's weight choices, not a neutral algorithm.

**How AI tools helped — and when I double-checked:** AI was genuinely useful for generating diverse song data quickly (getting 10 varied genres and moods into the CSV without manual research) and for reasoning through the scoring formula structure. The moments I had to override it: the initial import path in `main.py` was wrong (`from recommender import` instead of `from src.recommender import`) — AI generated code that matched the local context but broke when run as a module from the project root. Any time generated code involved file paths, module imports, or system-level execution, I verified it by actually running it rather than trusting it looked right.

**What surprised me about a simple algorithm feeling like recommendations:** The explanations made it feel real. When the system printed "genre match (+3.0) | mood match (+2.0) | energy proximity (+1.46)" for Sunrise City, it read like reasoning — like the system understood *why* it was suggesting that song. But it's just addition. There's no understanding happening. That gap between "looks like reasoning" and "is actually reasoning" is something real AI products exploit constantly, and it's easy to forget when you're on the receiving end of a smooth recommendation UI.

**What I'd try next:** The most impactful next step would be replacing exact string matching for genre and mood with a similarity table — so that "chill" and "relaxed" share 80% credit instead of 0%. That single change would make the system dramatically more useful for users whose preferred mood doesn't have an exact catalog match, without requiring any new data or infrastructure.
