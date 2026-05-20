# Video Motion And Edit Prompt Rules

Use this file only for detailed video prompts, Seedance/即梦 generation, camera movement design, one-take planning, special motion effects, or edit-rhythm refinement. Do not load it for ordinary project startup.

## Prompt Split

Video generation prompts and edit notes are not the same.

- Generation prompt: one continuous clip, one camera path, one action beat, clear start/end frame.
- Edit note: where cuts, transitions, subtitles, sound, and rhythm happen after clips exist.

Default rule: if the user wants multiple cuts, create separate shot prompts plus an edit plan. Do not force a multi-cut sequence into one generation prompt.

## Motion Primitives

| Intent | Prompt Language | Best Use |
| --- | --- | --- |
| Stable observation | `locked-off camera, subject movement creates the action` | premium, documentary, product clarity |
| Reveal | `slow push-in from medium shot to close-up over 4 seconds` | emotional focus, hook |
| Context expansion | `pull-out from close-up to wide shot, revealing the full environment` | place reveal, scale |
| Travel with subject | `tracking shot parallel to subject, constant distance, stable horizon` | walking, driving, process |
| Space scan | `slow truck left-to-right, foreground passes across lens` | environment, exhibition, market |
| Focus shift | `rack focus from foreground object to background subject` | attention transfer |
| Hero emphasis | `low-angle slow push-in, rim light, subject occupies 60% frame, hold final pose` | product/person hero shot |
| Unease | `subtle handheld drift, imperfect horizon, slow push-in` | tension, realism |
| Energy | `whip pan transition, fast motion blur, lands on new subject position` | action, short video hook |
| Scale | `crane up from subject to wide overhead view` | city, event, landscape |
| Product orbit | `controlled 20-degree arc around product, shape remains stable` | product detail |
| Dream/Memory | `slow floating camera, shallow depth, softened highlights` | emotional montage |

## One-Take / Oner

Use only when the user asks for "一镜到底", "one take", "long take", or a continuous camera move.

### Rules

- State `single continuous shot, no visible cuts`.
- Keep duration realistic for the tool. For AI generation, prefer 5-10 seconds per clip.
- Plan 2-4 action beats inside one path, not a full film sequence.
- Use foreground wipes, door frames, or body passes only if hidden cuts are acceptable. If not, say no hidden cuts.
- Lock subject continuity: face, clothes, props, scene geometry, light direction.

### Template

```text
Single continuous shot, [duration], [ratio].
Start: [shot size, subject position, environment].
Beat 1: camera [movement] as subject [action].
Beat 2: camera passes [foreground/object] and reveals [new information].
Beat 3: camera settles into [final shot size/composition].
Movement: one smooth path from [point A] to [point B], no jump cut, no sudden scene change.
Continuity: same subject, same costume, same lighting direction, stable background geometry.
Avoid: teleporting camera, morphing face/body, extra people, flicker, unreadable text, watermark.
```

## Bullet-Time / Time-Slice Feel

Do not ask for a copyrighted franchise look. Describe the effect technically.

```text
near-frozen action at the peak moment, camera performs a 180-degree orbit around the subject, background particles and cloth motion appear slowed, subject remains anatomically stable, time-ramp from normal speed into slow motion then back, no scene change
```

Use sparingly. It is high-risk for deformation and usually needs a strong reference frame or a very simple subject.

## Hero Shot

Use for product, character, campaign key image, or title reveal.

```text
low-angle medium close-up, subject occupies 60% of the frame, slow push-in over 3 seconds, strong rim light from behind, subtle foreground depth, final half-second hold for impact, clean background, no generated text
```

## Edit Techniques

Use these in edit plans, not as overloaded video-generation prompts.

| Technique | Use | Note |
| --- | --- | --- |
| Hard cut | clean information change | best for fast social edits |
| Cut on action | hide transition in movement | keep direction/action continuous |
| Match cut | connect similar shapes/motions | needs two planned frames |
| Smash cut | sudden contrast | use for comedy/shock/hook |
| Jump cut | compress time or create energy | avoid if continuity must feel smooth |
| Montage | compress process | build as shot list, not one prompt |
| Cross-cutting | parallel actions | needs separate scenes and clear time relation |
| J-cut / L-cut | audio leads or trails picture | specify in edit plan/audio notes |
| Whip-pan transition | energetic scene bridge | generate ending/starting motion separately |
| Speed ramp | emphasize impact | specify normal -> slow -> normal timing |

## Prompt Upgrade Examples

Vague:

```text
镜头炫一点，一镜到底，英雄感。
```

Controlled:

```text
Single continuous 8-second shot, 16:9. Start in a low-angle medium shot, subject centered and occupying 45% of the frame. Camera slowly pushes in while arcing 20 degrees clockwise; subject steps forward once and raises the product to chest height. Rim light outlines the shoulders, background stays darker and simple. End in a medium close-up, subject occupies 65%, hold final pose for 0.5 seconds. No visible cuts, no face/body deformation, no generated text, no logo.
```

Vague:

```text
子弹时间，酷一点。
```

Controlled:

```text
6-second action beat. Start at normal speed as the subject throws a small object upward. At the peak moment, motion slows dramatically; the camera orbits 180 degrees around the subject while the object and dust particles appear nearly frozen. Return to normal speed as the object lands. Keep one subject, stable anatomy, same costume, same background, no extra limbs, no sudden scene change.
```

## Low-Token Use

- For normal video prompt requests, use only the compact template in `Prompt_Spec_Rules.md`.
- Load this file only when the user asks for motion/edit precision, one-take, bullet-time, hero shot, or Seedance/AI video execution.
- For revisions, output only the changed motion/edit parameters.

## Source Links

- Camera movement reference: https://www.studiobinder.com/camera-shots/camera-movements/
- Shot size/framing reference: https://www.studiobinder.com/blog/ultimate-guide-to-camera-shots/
- Film cut technique reference: https://www.adobe.com/creativecloud/video/post-production/cuts-in-film.html
- J-cut / L-cut editing reference: https://helpx.adobe.com/premiere-pro/using/perform-j-and-l-cuts.html
