# HQ Aesthetic Master Index

Last updated: 2026-05-25

This is the master entry for high-resolution visual study references. Images and contact sheets are local-only and ignored by Git; tracked files store indexes, source links, quality tiers, and safe extraction rules.

## Current Library

| Library | Index | Scope | Local visual coverage | Best use |
| --- | --- | --- | --- | --- |
| Oscar HQ Frame Set | `01_Research/HQ_Aesthetic_References/Oscar_HQ_Frame_Set.md` | 30 Oscar Best Picture films | 94 frames; 30 HQ, 39 medium, 25 fallback small | Classical film language, blocking, light, palette, and award-film grammar |
| Film HQ Set 2026-05-24 | `01_Research/HQ_Aesthetic_References/Film_HQ_Reference_Set_2026_05_24.md` | 50 films: Dune / Denis Villeneuve, Jia Zhangke, Oscar Best Picture add-ons, Oscar Animated Feature | 126 frames; 30 HQ, 96 medium, 0 fallback small | Modern cinematic scale, Chinese realism, prestige drama, animation color and staging |
| Open HQ Study Set | `01_Research/HQ_Aesthetic_References/Open_HQ_Aesthetic_Study_Set.md` | Open-license Commons visual study set | 9 HQ images | Texture, material, light, environment, and composition study |
| Daily Selected Aesthetic Index | `01_Research/Aesthetic_Daily_Selected/Daily_Selected_Index.md` | User-supplied daily selected PDFs and candidate sheets | 100 extracted PDF images plus candidate review sheets | Personal taste calibration and daily visual vocabulary |
| High-Level Source Repository | `01_Research/Aesthetic_Reference_Archive/High_Level_Aesthetic_Repositories.md` | 30 external aesthetic sources and GitHub discovery hubs | 30 source preview cards | Finding new references without overloading one project |
| Aesthetic Decision Index | `01_Research/HQ_Aesthetic_References/Aesthetic_Decision_Index.md` | Compact profile layer for automatic visual-taste selection | no raw images | Default aesthetic choice when the user has not specified a look |
| Aesthetic Library Config | `01_Research/HQ_Aesthetic_References/Aesthetic_Library_Config.md` | Portable storage rules and environment variables | no raw images | Moving large local libraries to another disk |
| Top-Tier Collection Queue | `01_Research/HQ_Aesthetic_References/Top_Tier_Collection_Queue.md` | Curated future collection lanes | no raw images | Expanding the library without diluting quality |
| Aesthetic Expansion Queue 2026-05-25 | `01_Research/HQ_Aesthetic_References/Aesthetic_Expansion_Queue_2026_05_25.md` | 74 curated expansion targets across cinema, East Asian realism, animation, commercial/motion, typography, and production design | no raw images | Next high-quality collection map before downloading large batches |
| Interactive Browser Tech Notes | `01_Research/HQ_Aesthetic_References/Interactive_Aesthetic_Browser_Tech_Notes.md` | Evaluation notes for a future local image browser/review system | no raw images | Planning gallery, filtering, rating, and reject/keep workflows |

## Contact Sheet Entry Points

| Set | Contact sheets |
| --- | --- |
| Oscar HQ | `01_Research/HQ_Aesthetic_References/contact_sheets/oscar-hq-frames-01-10.jpg`, `oscar-hq-frames-11-20.jpg`, `oscar-hq-frames-21-30.jpg` |
| Film HQ 2026-05-24 | `01_Research/HQ_Aesthetic_References/contact_sheets/film-hq-set-2026-05-24-01-10.jpg` through `film-hq-set-2026-05-24-41-50.jpg` |
| Open HQ | `01_Research/HQ_Aesthetic_References/contact_sheets/open-hq-study-set-commons-featured.jpg` |
| Daily Selected | `01_Research/Aesthetic_Daily_Selected/contact_sheets/2026-05-19-contact-sheet.jpg` through `2026-05-24-contact-sheet.jpg` |

## Use Protocol

- Start with this file when the user asks for HQ aesthetic references, film visual study, moodboard calibration, or image/video prompt taste improvement.
- Choose one narrow source lane per task; do not load every index unless the user asks for broad research.
- For automatic SW project decisions, read `Aesthetic_Decision_Index.md` first and only open deeper indexes when the user asks for references or a moodboard.
- If a long-running project supplies `.sw/ASSETS.md`, `.sw/RULES.md`, `.sw/MEMORY.md`, or user-provided visual references, those project-local references override the global library.
- Use HQ and medium frames for close study. Use fallback-small rows only to understand historical coverage until better images are found.
- Extract visual language, not images: shot size, subject scale, lens feel, light direction, contrast, palette, set texture, atmosphere, blocking, typography behavior, and rhythm.
- Do not ask AI tools to copy named frames, named directors, exact layouts, logos, text, or proprietary graphic devices.
- Keep generated prompts source-neutral and project-specific.
- If image storage moves to another drive, use `Aesthetic_Library_Config.md` and `tools/aesthetic_library_doctor.py`; do not change tracked indexes to absolute local paths.

## Low-Token Selection Guide

| User intent | Read first | Optional second file |
| --- | --- | --- |
| User did not specify visual style; SW should decide | `Aesthetic_Decision_Index.md` | `HQ_Aesthetic_Master_Index.md` |
| Dune / large-scale sci-fi / monumental desert | `Film_HQ_Reference_Set_2026_05_24.md` | `High_Level_Aesthetic_Repositories.md` |
| Jia Zhangke / Chinese realism / city-life texture | `Film_HQ_Reference_Set_2026_05_24.md` | `Daily_Selected_Index.md` |
| Award-film visual grammar | `Oscar_HQ_Frame_Set.md` | `Film_HQ_Reference_Set_2026_05_24.md` |
| Animation color / family-film staging | `Film_HQ_Reference_Set_2026_05_24.md` | `Open_HQ_Aesthetic_Study_Set.md` |
| Personal daily moodboard | `Daily_Selected_Index.md` | `High_Level_Aesthetic_Repositories.md` |
| Material, light, and texture study | `Open_HQ_Aesthetic_Study_Set.md` | `Daily_Selected_Index.md` |
| Expand the library without downloading yet | `Aesthetic_Expansion_Queue_2026_05_25.md` | `Top_Tier_Collection_Queue.md` |
| Plan a future visual browser / reject workflow | `Interactive_Aesthetic_Browser_Tech_Notes.md` | `Aesthetic_Library_Config.md` |
