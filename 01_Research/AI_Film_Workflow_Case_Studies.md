# AI Film Workflow Case Studies

Status: saved as research reference only. Not yet absorbed into SW runtime rules.
Date: 2026-05-19
Scope: public AI short-film / AI-assisted short-film workflow lessons, excluding the previously saved Gossip Goblin / The Patchwright notes.

## Executive Takeaways

1. AI film quality comes from workflow design, not one model.
2. The strongest projects still start with script, story, theme, or a sharp visual premise.
3. Video generation is usually a shot generator, not a director.
4. The edit is where AI fragments become cinema.
5. Human sound, voice, music, VFX, color, and curation remain decisive.
6. Many strong AI shorts are designed around AI's limits instead of fighting them.
7. The best workflows use AI differently by stage: ideation, still frames, style exploration, animation, VFX repair, sound, and finishing.

## Case 1: Air Head / shy kids / Sora

Reputation:
- One of the most visible early Sora short films.
- Valued because it felt like an indie short rather than only a tech demo.

Workflow notes:
- Started from a simple iconic premise: a man with a yellow balloon head.
- The team had a script and voiceover, but stayed flexible in the edit because generated outputs varied.
- Sora produced many short clips; the final used selected fragments.
- The production behaved like documentary editing: gather footage, then find the usable story and rhythm.
- Post-production mattered: color grading, retiming, VFX cleanup, balloon color fixes, unwanted element removal, music, and sound.
- Extra generations were used during editing to fill gaps.

Lessons:
- Design characters and symbols AI can hold consistently.
- Treat generated video as raw footage, not final footage.
- Expect a high waste ratio; build time for selects.
- Prompting does not replace VFX, color, sound, or editorial judgment.
- Use generation again during post when the edit reveals missing connective tissue.

Potential SW absorption:
- Add an `AI Footage Selects` step.
- Add an expected waste ratio before video generation.
- Strengthen `edit-director` and `review-producer` for AI video projects.

## Case 2: Runway GEN:48 / Gabe Michael Workflow

Reputation:
- Useful because the maker publicly documented a 48-hour AI film workflow.
- Strong practical lessons for short-deadline AI film production.

Workflow notes:
- Used AI for ideation, but filtered everything through personal taste and original intent.
- Generated many visual concepts, then selected one direction instead of chasing every possible option.
- Built character sheets and style tests before final animation.
- Split backgrounds and characters like a traditional 2D animation workflow.
- Created an animatic early.
- Rebuilt the film more than once during the deadline to solve structure and continuity.
- For difficult shots, reverse-engineered how the shot would be made in real production, then adapted that process to AI tools.

Lessons:
- Use AI brainstorming, but do not outsource taste.
- Animatic first reduces waste.
- Layered animation thinking still works with AI: background, character, foreground, camera, edit.
- Fast deadlines need ruthless scope control.
- The best prompt may come from understanding physical production, not prompt syntax.

Potential SW absorption:
- Add `Animatic First` for AI video projects.
- Add `Layer Split` guidance for character/background workflows.
- Add a `How would this be shot for real?` diagnostic question for hard shots.

## Case 3: Critterz / Chad Nelson / DALL-E

Reputation:
- Often cited as an early AI-assisted animated short that combined generative images with traditional film craft.

Workflow notes:
- AI was used heavily for visual development and backgrounds/characters.
- Traditional human production roles still mattered: writing, animation, voice, editing, music, and sound.
- The project proved that AI images are only one department inside a film pipeline.

Lessons:
- AI can accelerate visual invention but does not remove the need for writing and performance.
- Use AI image generation to create a world fast, then bring in traditional craft to make it watchable.
- Voice and animation timing carry emotional credibility.

Potential SW absorption:
- Keep `scriptwriter`, `edit-director`, and `sound-designer` active even when image generation is strong.
- Treat image generation as production design support, not the whole film.

## Case 4: Thank You For Not Answering / Paul Trillo

Reputation:
- Frequently discussed as an artist-led AI short using Runway and AI voice/audio tools.
- Important because the film's dreamlike form matches AI's strengths.

Workflow notes:
- Built from a personal emotional premise rather than a generic AI showcase.
- Used AI video generation for surreal, memory-like visuals.
- Embraced some AI instability because it served the film's tone.
- Combined generated visuals with voice, edit rhythm, and post choices.

Lessons:
- Pick stories where AI artifacts can become part of the style.
- AI is strong for memory, dream, abstraction, surreal transition, and unstable subjectivity.
- If a film needs precise realism, the workflow cost rises sharply.

Potential SW absorption:
- Add a `Fit story to medium` check before AI video generation.
- Add a style lane for dream/memory/subjective films where controlled instability is acceptable.

## Case 5: The Frost / Waymark

Reputation:
- Early widely shared AI-generated short with clear public discussion around process and limitations.
- Useful as a workflow and limitation case, even when not universally admired as cinema.

Workflow notes:
- Used a written script, then generated still images for scenes.
- Animated stills with AI tools and assembled them into a short.
- The uncanny, frozen, surreal quality became part of the result.
- Human emotion and subtle acting remained weak points.

Lessons:
- AI still-image-to-video workflows can create atmosphere quickly.
- They are weaker for nuanced human performance.
- Choose subject matter that tolerates uncanny faces, strange motion, or surreal tone.
- AI short films need honest expectation-setting about what is controlled and what is discovered.

Potential SW absorption:
- Add a `Performance Risk` gate for dialogue-heavy or subtle acting scenes.
- Recommend still-image-driven AI film for atmosphere, dream, montage, lore, or world-building more than intimate acting.

## Case 6: The Crow / Glenn Marshall

Reputation:
- Award-winning AI-assisted dance/animation short.
- Valuable because it uses AI as transformation over real human motion.

Workflow notes:
- Started from human dance/performance footage.
- Used machine learning to transform frames into painterly animated imagery.
- The human performance supplied motion logic and emotional rhythm.
- AI supplied visual transformation rather than inventing everything from nothing.

Lessons:
- Real performance is a powerful control source.
- AI can be better as a transformation layer than as a blank-slate generator.
- For dance, music videos, fashion, and experimental films, live action reference may solve continuity better than pure prompting.

Potential SW absorption:
- Add `Human Motion Source` as an option for movement-heavy AI films.
- Add `Transform footage` workflow alongside text/image-to-video workflows.

## Case 7: Hysteresis / Robert Seidel

Reputation:
- Not a conventional narrative short, but respected as an AI-assisted experimental animation and installation/film hybrid.

Workflow notes:
- Combined analog drawings, performance, projection, machine learning, and sound.
- The AI process acted like a feedback system rather than a one-click generator.
- The piece is strongest when the process itself becomes the visual language.

Lessons:
- Hybrid inputs can create a more personal visual signature than prompt-only work.
- Analog marks, drawings, scans, or physical performance can give AI a unique source texture.
- Experimental work benefits from designing a system, not just individual shots.

Potential SW absorption:
- Add `Personal Source Texture` to premium visual development: drawings, scans, handwriting, props, motion capture, analog marks.
- Add `System Aesthetic` for experimental projects.

## Case 8: Adobe / Native Foreign Style Hybrid Short Workflows

Reputation:
- Useful professional reference because several public AI film workflows show traditional film roles mixed with Firefly/Sora/Runway-style tools.

Workflow notes:
- Human concepts and hand-drawn or photographic references often came first.
- AI helped with boards, style exploration, temp shots, and generated inserts.
- Editing, grading, VFX, rights, music, and final polish remained standard production concerns.
- Teams organized work with boards and shot-management workflows rather than loose prompt piles.

Lessons:
- Professional AI film work needs asset organization.
- Boards and shot databases matter as much as prompts.
- Legal/consent/source-material decisions must be made early.
- AI can speed ideation, but final delivery still needs production discipline.

Potential SW absorption:
- Add `Shot Asset Database` / `Boards` guidance.
- Add consent and rights checks for personal photos, client assets, and brand material.

## Cross-Case Pattern

Recommended future premium AI film pipeline candidate:

```text
Story / Theme
-> World Bible or Project Memory
-> Script
-> Visual Premise
-> Character Coverage
-> Location / Plate Exploration
-> Hero Frames
-> Animatic
-> Tool-Specific Prompts
-> Single-Shot Generation
-> Selects
-> Edit
-> Voice / Music / Sound Design
-> VFX Repair
-> Color / Grain / Texture
-> Review
```

Do not absorb automatically yet. These are saved as reference material for a future SW AI-film upgrade.

## Candidate Rules To Consider Later

- Never generate a long AI film directly from one video prompt.
- Start with script or emotional premise.
- Lock hero frames before video generation.
- Use character coverage matrices for recurring characters.
- Use annotated image notes for complex blocking.
- Use an animatic before spending on many generated clips.
- Treat video generation as single-shot footage creation.
- Build a selects/review stage for generated clips.
- Keep sound and edit as first-class roles.
- Bake most grade into frames, then unify in final grade.
- Preserve human craft where it carries emotion: voice, music, edit, timing, performance reference.

## Sources

- https://www.fxguide.com/fxfeatured/actually-using-sora/
- https://nofilmschool.com/sora-ai-filmmaker-interview
- https://runwayml.com/customers/48-hours-to-generate-a-film
- https://runwayml.com/customer-stories/paul-trillo
- https://shots.net/news/view/how-paul-trillos-short-film-found-the-artist-within-ai
- https://www.thedrum.com/news/2023/08/16/waymark-filmmaker-josh-rubin-creating-the-first-generative-ai-film
- https://openai.com/index/critters/
- https://www.linkedin.com/pulse/behind-scenes-making-critterz-chad-nelson
- https://www.artnews.com/art-news/artists/glenn-marshall-the-crow-ai-generated-animated-video-1234652293/
- https://newatlas.com/technology/ai-generated-animation-the-crow-glenn-marshall/
- https://zkm.de/en/artwork/hysteresis
- https://hyperallergic.com/545428/hysteresis-robert-seidel/
- https://blog.adobe.com/en/publish/2024/10/21/filmmakers-embrace-generative-ai-in-first-of-kind-short-films-premiered-at-adobe-max
- https://blog.adobe.com/en/publish/2024/10/22/how-ai-powered-filmmaking-fueled-beta-earth-a-film-by-gabe-michael-made-with-adobe-firefly-video-model
