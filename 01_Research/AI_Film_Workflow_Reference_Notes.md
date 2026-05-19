# AI Film Workflow Reference Notes

Status: saved as reference only. Not yet absorbed into SW runtime rules.
Date: 2026-05-19
Source topic: PJ Ace thread on Gossip Goblin / The Patchwright workflow, plus public discussion and user screenshots.

## Why This Matters

The main lesson is that strong AI films are not made by one clever prompt or one tool. The quality comes from accumulated world-building, deliberate shot control, human editorial judgment, and many small visual decisions that most creators skip.

## Saved Lessons

1. Story bible before tools
   - A long-running world, recurring characters, custom language, custom alphabet, props, and visual history do heavy lifting.
   - For SW, this may later become a `World Bible` or project memory pattern.

2. Script first
   - Start from story, characters, scene purpose, and emotional beats.
   - Prompts and tools should serve the script, not replace it.

3. Visual exploration follows story beats
   - Explore locations by narrative zones: penthouse, ship, city airspace, street, market, workshop, etc.
   - Each location should have its own plate/texture/color pass before animation.

4. Push past AI defaults
   - Avoid generic outputs even if they look acceptable.
   - Replace default rooms, props, costumes, and layouts with designed choices.

5. Tool roles are separate
   - Midjourney-style tools: broad aesthetic exploration and strange visual possibility.
   - Banana-style tools: image repair, character insertion, continuity stitching, frame-level compositing.
   - Seedance/Kling-style tools: animate already-designed frames or shots.
   - Do not let a generation tool skip writing, design, storyboard, or edit decisions.

6. Hero shots first, then connective tissue
   - Lock a few key frames that define lighting, color, tone, and composition.
   - Use those anchors to derive intermediate shots instead of designing every frame from zero.

7. Character coverage matrix
   - Do not rely on one master sheet.
   - Generate close-up, medium, wide, rear, action, expression, and lighting-matched variants for each major character.

8. Frame-by-frame control
   - Avoid relying on multi-shot or omni-ref for important scenes.
   - Build and animate single shots/frames when control matters.

9. Annotated image notes
   - Complex scenes may need paint-over notes: arrows, blocking, cables, motion direction, subject placement.
   - Text prompt plus annotated visual reference can beat text-only prompting.

10. Human voice matters
   - Discernible dialogue should use real voice actors when possible.
   - AI visuals still need human performance rhythm, casting, and sound direction.

11. Editor is a core AI film role
   - AI film cohesion happens in the edit because shots are generated in separate silos.
   - A dedicated editor who understands AI failure modes may be more important than another prompt specialist.

12. Grade early, polish late
   - Bake most lighting and color into still frames before animation.
   - Final color grade should unify discrepancies, not rescue the whole look.

13. Grain and texture fight AI waxiness
   - Grain is no longer only a trick to hide artifacts.
   - It adds grit, reduces plastic surfaces, and makes spaces feel physical.

14. Sound is the glue
   - Score, SFX, footsteps, metal clanks, room tone, crowd texture, and transitions bind separate clips into one film.
   - Sound design should not be treated as an afterthought.

15. The unseen 99 percent creates belief
   - Custom mug, kettle, background creature, signage, cables, shelf objects, and barely visible glyphs matter.
   - Viewers may not name these details, but they feel the difference.

## Possible Future SW Absorption

Do not implement automatically yet. Candidate upgrades:

- Add a premium AI film pipeline:
  `World Bible -> Script -> Hero Frames -> Character Coverage -> Location Plates -> Annotated Frame Notes -> Prompt Director -> Banana Stitching -> Seedance/Kling Animation -> Voice/Sound -> Edit -> Grade/Grain -> Final Review`
- Add a `Hero Shot Lock` checkpoint before video generation.
- Add a `Character Coverage Matrix` checklist for recurring characters.
- Add an `Annotated Frame Notes` option for difficult shots.
- Strengthen `edit-director`, `sound-designer`, and `colorist` in AI film projects.
- Keep video generation tools as post-prompt execution only.

## Sources

- https://en.rattibha.com/thread/2054567105924899147
- https://www.thedaringcreatives.com/the-work-hidden-inside-gossipgoblins-worlds/
- https://www.theguardian.com/technology/2026/may/14/gossip-goblin-ai-film-making-new-era-hollywood
- User-provided screenshots from the PJ Ace thread.
