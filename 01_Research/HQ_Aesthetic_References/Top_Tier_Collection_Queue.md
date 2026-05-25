# Top-Tier Aesthetic Collection Queue

Last updated: 2026-05-25

Use this queue to expand the local aesthetic library without turning it into a random inspiration dump. Add images only after the storage root is confirmed or the portable root variables are set.

## Collection Standard

- Choose only references with unusually strong composition, light, color, texture, blocking, typography, motion rhythm, or production-design value.
- Prefer fewer, better images over broad scraping.
- Store high-quality local study files under ignored `images/` folders; commit only indexes, source links, and distilled lessons.
- Record source URL, work/title, quality tier, visual lesson, and safe extraction rule.
- Do not use collection entries as "copy this"; translate them into neutral visual language.

## Priority Lanes

| Priority | Lane | Why It Matters | First Sources |
| ---: | --- | --- | --- |
| 1 | Canonical cinema grammar | Gives SW reliable default taste when a user says "you decide" | BFI Sight and Sound, FilmGrab, Criterion essays, ASC articles |
| 2 | Contemporary cinematography | Keeps prompts from looking like generic AI film stills | American Cinematographer, ShotDeck/Frameset when available, director/cinematographer interviews |
| 3 | Chinese realism and urban texture | Supports local tourism, city, documentary, government/client proposal work | Jia Zhangke lane, documentary/photo sources, Daily Selected |
| 4 | Animation staging and color | Supports animation, character boards, family content, stylized storyboards | Oscar Animated winners, animation art books/articles, open HQ color studies |
| 5 | Commercial/product/lifestyle | Supports posters, short ads, beverages, retail, social content | Daily Selected, Directors Library, STASH, Motionographer, brand-design archives |
| 6 | Typography and editorial systems | Supports posters, PPT/decks, title cards, brand worlds | Fonts In Use, BP&O, The Brand Identity, Typewolf |
| 7 | Production-design sheets | Supports character sheets, scene sheets, props, wardrobe continuity | User references, concept-art boards, production design interviews |

## Current Next Batches

| Batch | Target | Output | Notes |
| --- | --- | --- | --- |
| 2026-05-cinema-canon | 30 additional canon films | 3-5 frames each plus distilled grammar | Start with films not already represented in Oscar/Dune/Jia lanes. |
| 2026-05-commercial-motion | 20 top commercial/music-video references | contact sheet plus motion/edit lessons | Prioritize director-level references and practical production lessons. |
| 2026-05-character-scene-sheets | 20 character/scene/prop boards | board examples plus layout rules | Keep as visual-development reference; do not merge into prompt rules until tested. |
| 2026-05-typography-editorial | 30 poster/deck/title-card references | typography hierarchy notes | Useful for PPT/deck and poster systems. |
| 2026-05-25-expanded-targets | 74 curated targets | tracked target map first, raw images later | See `Aesthetic_Expansion_Queue_2026_05_25.md`; collect only after storage root and review workflow are ready. |

## External Source Starters

| Source | Use | Link |
| --- | --- | --- |
| BFI Sight and Sound | canonical cinema discovery | https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time |
| American Cinematographer | cinematography technique and interviews | https://theasc.com/ |
| Criterion | essays, restorations, director context | https://www.criterion.com/current |
| Oscars | official award film discovery | https://www.oscars.org/oscars/ceremonies |
| FilmGrab | frame study and contact-sheet source | https://film-grab.com/ |
| Motionographer | motion and title-design research | https://motionographer.com/ |
| STASH | commercial animation and VFX references | https://www.stashmedia.tv/ |
| Art of the Title | title sequence and typography-in-motion research | https://www.artofthetitle.com/ |
| Fonts In Use | typography behavior and context | https://fontsinuse.com/ |
| BP&O | brand and packaging design systems | https://bpando.org/ |

## Before Downloading A Large Batch

1. Run `python tools/aesthetic_library_doctor.py`.
2. Confirm the active storage root has enough space.
3. Save images under ignored `images/` folders.
4. Generate contact sheets for human review.
5. Add or update only the tracked index and distilled lessons.
