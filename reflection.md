# Reflection: Music Recommender Simulation

## Profile Comparison Notes

### High-Energy Pop vs. Chill Lofi Study

These two profiles represent opposite ends of the energy spectrum (0.85 vs 0.38) and completely different genres. The outputs reflect this cleanly: the pop profile surfaces high-BPM tracks (Sunrise City at 118 BPM, Gym Hero at 132 BPM), while the lofi profile clusters around low-BPM acoustic tracks (Library Rain at 72 BPM, Midnight Coding at 78 BPM). Score gaps also behave differently: the lofi profile produced tighter scores (7.46 / 7.44 for #1 and #2) because two songs matched all four criteria equally well. The pop profile had a large gap between #1 (6.46) and #2 (4.38) because only one song (Sunrise City) matched both genre and mood.

**Why this makes sense:** Lofi has a more coherent sonic identity than pop — fewer songs match it, but the ones that do match precisely. Pop is broader, so mood misses are more common even within the same genre.

### Chill Lofi Study vs. Deep Intense Rock

Both profiles have a clear, tightly defined "vibe" — they just sit at opposite poles. The rock profile returned Storm Runner at #1 (6.48) with a near-perfect score, very similar in structure to the lofi profile's #1. However, the falloff was steeper: #3 (Iron Teeth) scored 3.43, while the lofi profile's #3 scored 5.47. This is because the lofi catalog has three songs (Library Rain, Midnight Coding, Focus Flow), while rock has only one (Storm Runner). After that one song, the rock user is being served songs that share only mood or energy — not genre.

**Why this makes sense:** Having only 1 song per genre means the system exhausts its best matches quickly. This is a dataset limitation, not a logic flaw — but it shows how catalog size directly affects recommendation quality.

### High-Energy Pop vs. Conflicted Listener

This comparison shows the system's biggest weakness. The pop profile and the conflicted profile both request high energy (0.85 and 0.90), yet their top 5 lists share almost no overlap. The pop profile gets energetic pop and k-pop tracks; the conflicted profile gets Spacewalk Thoughts (ambient, energy 0.28) as #1.

To explain this to a non-programmer: imagine you hired a music librarian and told them "I love ambient music, but I want high-energy songs tonight." The librarian, following strict rules, finds your favorite section first (ambient), grabs the only ambient album in stock (Spacewalk Thoughts), and hands it to you — even though it's a quiet, meditative record. They followed your genre preference to the letter and ignored the contradiction. That's exactly what this system does. The genre weight (3.0 points) is so strong that it overrides the energy mismatch.

**Why Gym Hero keeps showing up for Happy Pop users:** Gym Hero is a pop song with energy 0.93, danceability 0.88, and mood "intense" — not "happy." For a happy pop user, it earns 3.0 genre points but misses the 2.0 mood bonus. Yet it still ranks #2 every time because no other pop song in the catalog has both happy mood and high energy *except* Sunrise City. The system is correct — Gym Hero is the second-best available pop song — but a human listener might find it jarring to get an intense workout track when they asked for happy music.

## Weight Shift Experiment

**Setup:** Genre weight changed from 3.0 → 1.5. Energy weight changed from 1.5 → 3.0.

**Result for High-Energy Pop:** Neon Petals (k-pop) jumped from #3 to #2, bumping Gym Hero down to #4. A k-pop song outranked a pop song once genre was less dominant.

**What this tells us:** The original weights encode a judgment call — genre is the most important signal. That may be reasonable (most people don't cross genre lines easily), but it means that any song not in the user's preferred genre is severely penalized regardless of how well it matches on every other dimension. Lowering the genre weight created more diverse, cross-genre results, which felt more like "songs in the right vibe" rather than "songs in the right box."

The right weights depend on what you're trying to optimize for. If your goal is comfort and familiarity, high genre weight makes sense. If your goal is discovery and surprise, lower genre weight produces better results.
