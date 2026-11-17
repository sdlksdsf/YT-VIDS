# YouTube Package — "The Last 53 Days of Rome"

> Everything needed to publish the video: title, description, tags, thumbnail, trailer, end screens, and the upload checklist.

---

## 1. Titles (A/B test these)

**Primary:** `The Last 53 Days of Rome: The Fall of Constantinople`
**Alt A:** `The Fall of Constantinople: The 53 Days That Ended the Roman Empire`
**Alt B:** `The ENTIRE History of the Fall of Constantinople Explained`
**Alt C:** `The 53 Days [No AI]` (only if the animation is genuinely hand-made)

**Why the primary works:** it promises a countdown (urgency), a number (concrete), and a name (Rome) that even people who know nothing about Byzantium recognize.

## 2. Description (copy-paste)

```
In 1453, a 21-year-old sultan and a dying emperor fought a 53-day war for the greatest city on Earth. This is the fall of Constantinople — the end of the Roman Empire.

For a thousand years, its walls had never been breached. Then came the cannon, the chain across the Golden Horn, the ships hauled over a hill, and one Tuesday morning that ended the Middle Ages.

⏱️ TIMESTAMPS
0:00 The Morning the World Died
1:00 The Dying Giant
5:00 The Throat-Cutter
10:00 Day 1 — The Guns Open Fire
12:00 Day 16 — 70 Ships Over the Hill
14:00 The War Underground
16:00 The Sky Turns Ominous
17:00 Day 53 — The Last Day
21:00 The Echo

📚 SOURCES
Wikipedia: Fall of Constantinople · Mehmed II · Constantine XI · Walls of Constantinople · Rumeli Hisarı · Orban · Giovanni Giustiniani · Johannes Grant · Hagia Sophia · Third Rome
Runciman, The Fall of Constantinople 1453 · Crowley, 1453 · Norwich, Byzantium: The Decline and Fall · Nicolle, Constantinople 1453 (Osprey) · Philippides & Hanak, The Siege of Constantinople in 1453
Primary: George Sphrantzes · Niccolò Barbaro's diary · Michael Critobulus · Doukas · Leonard of Chios · Tursun Beg

🎨 Every frame hand-drawn. 🗣️ Narrated by a human. No AI slop.

💬 Which empire should we end next?

⚠️ This video is for entertainment and education. Some details are simplified or disputed; the sources above are the place to start.
```

## 3. Tags

`fall of constantinople, constantinople 1453, byzantine empire, mehmed ii, constantine xi, ottoman empire, history of constantinople, fall of rome, end of the middle ages, animated history, history documentary, oversimplified, epic history tv, constantinople explained, byzantium, siege of constantinople, history channel, no ai`

## 4. Thumbnail

- **File:** `images/thumbnail.png`
- **Layout (every episode):** hero face left + hero face right + one visual hook in the middle + one huge title on top.
- **Title text (add in editor):** `THE LAST 53 DAYS OF ROME` — 3 lines max, thick sans, gold with a dark outline.
- **Rule:** one face, one number, one color. No clutter.

## 5. Trailer / promo cut (60–90 sec)

Record a separate fast-paced read of the cold open + the "70 ships over the hill" + the "last charge" beats, cut to music, with quick frame flashes. Post as a Short 4–7 days before the main upload, and again after.

**Shorts to cut from the video:**
1. "The cannon that ended the Middle Ages" (Orban's Great Bombard scene).
2. "The 4 ships that embarrassed a sultan" (April 20 convoy).
3. "The emperor who refused to run" (May 21 refusal + last charge).
4. "70 ships went over a hill" (April 22).
5. "The gate that may have decided everything" (Kerkoporta).

## 6. End screen & CTAs

- **0:00–0:15:** hook; no CTA.
- **~12:30:** mid-roll style verbal CTA (optional): "If you're enjoying this, subscribe — it helps more than you'd think."
- **22:00–end:** subscribe button + end card linking to the next episode poll.
- **Comment pin:** "Which empire should we end next: the Mongols, Rome itself, or the Aztecs?"

## 7. Upload checklist

- [ ] Title A/B set (primary + alt in the first 48h test).
- [ ] Thumbnail uploaded (custom, not auto).
- [ ] Description with timestamps + sources.
- [ ] Tags added.
- [ ] Captions: upload the narration transcript as the caption file (or let auto-captions sync, then polish).
- [ ] End screen + cards (next video, subscribe).
- [ ] Pinned comment with the poll.
- [ ] Shorts scheduled.
- [ ] Community post with a poll 24h before upload.

## 8. Production status

| Asset | Status |
|---|---|
| Script (v1) | ✅ approved |
| Narration audio | ✅ 12/12 chunks recorded (voice-00), 18:18 total |
| Thumbnail | ✅ selected |
| Character art | ✅ Mehmed, Constantine, Great Bombard |
| Background plates | ✅ 9 plates (walls, horn, camp, underground, Hagia Sophia, assault, eclipse, echo, two thrones) |
| Animatic | ✅ `animatic_full.mp4` — 12 scenes, 18:18, 1280×720, burned-in captions, synth score bed |
| Music/SFX | ✅ placeholder score bed mixed under narration (swap for licensed tracks at final mix) |
| Production dashboard | ✅ live at https://ytvids-static2.vercel.app (Supabase-backed) |
| Channel name | ⏳ you said you'll pick it later — placeholder "Echoes of Empires" in use |

## 9. Delivery log

- **Animatic:** `animatic_full.mp4` (18:18, 233 MB, h264 1280×720 + AAC). 12 narration clips over 12 generated plates, Ken-Burns motion, burned-in captions, synthesized drone + war-drum bed under the voice.
- **Dashboard:** deployed on Vercel (project `ytvids-static2`, framework vite, static output) at **https://ytvids-static2.vercel.app**. Pulls episode, scene and source rows from Supabase REST.
- **Repo:** `arena/1b17490e-yt-vids` — script, style bible, reference deep-dive, YouTube package, narration chunks + mp3s, art plates, dashboard source.
- **Google Drive:** folder "YT-VIDS" holds the three docs (deep dive, style bible, script).
- **Next:** full 2D animation pass (character rigging / scene motion), licensed music swap, final mix, then upload.
