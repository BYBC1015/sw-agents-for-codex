# Aesthetic Decision Index

Last updated: 2026-05-25

This is SW's compact, low-token decision layer for visual taste. It is safe to read during normal project work because it stores only distilled aesthetic profiles, not image files.

## Decision Rule

- If the user gives project-local visual references, use those first.
- If the user does not specify a visual style, select one profile below based on project goal, audience, medium, and emotional tone.
- Use one profile as the main direction and at most one fallback.
- Convert the profile into neutral production language before prompts or design execution.
- Do not copy exact film frames, named director signatures, logos, character designs, typography, or proprietary layouts.

## Profiles

| Profile | Best For | Visual Levers | Avoid | Source Lane |
| --- | --- | --- | --- | --- |
| restrained-human-realism | local tourism, public-interest stories, founder stories, documentary brand films, grounded city life | observational blocking, natural light, imperfect surfaces, medium-wide context, lived-in color, quiet pauses | glossy stock cleanliness, overdesigned props, perfect AI skin, generic smiling montage | Daily Selected, Jia Zhangke lane, Magnum/documentary sources |
| monumental-cinematic-scale | tech launches, destination films, sci-fi, architecture, desert/landscape scale, premium hero visuals | tiny human vs vast environment, low horizon, long lens compression or wide establishing scale, dust/haze, controlled silhouettes, restrained palette | busy fantasy clutter, neon overload, random spacecraft detail, generic "epic" contrast | Dune / Denis Villeneuve lane, Film HQ set |
| award-drama-interior-tension | prestige storytelling, institutional films, serious brand films, emotional narrative scenes | layered foreground/background, practical interior light, restrained camera, motivated shadows, precise blocking, negative space | melodramatic expressions, obvious spotlighting, shallow prop symbolism | Oscar HQ frame set |
| urban-night-texture | nightlife, markets, youth culture, cyber/city atmosphere, music video texture | wet surfaces, mixed practical light, signage glow, haze, compressed streets, dense background life, selective color accents | random cyberpunk cliches, unreadable clutter, fake rain sheen, over-saturated blue/purple | Film HQ set, Motion/video source lane |
| warm-commercial-lifestyle | beverage, retail, campus, community, light social content, product-in-hand stories | energetic sunlight, clear product visibility, candid gestures, clean faces, simple background rhythm, optimistic color | over-polished advertising faces, plastic skin, fake handwritten text, chaotic crowding | Daily Selected, brand/design source lane |
| lyrical-animation-color | animation references, family films, emotional fantasy, stylized storyboards, character moments | clear silhouette, readable staging, strong color grouping, shape language, expressive negative space, simple value structure | noisy texture, photoreal detail overload, muddy midtones, unmotivated sparkle | Oscar Animated lane, open HQ color/material studies |
| minimal-premium-editorial | high-end posters, decks, luxury/service brands, restrained pitch visuals | generous white/quiet space, controlled type hierarchy, tactile detail crops, soft contrast, intentional asymmetry | empty "luxury" sameness, beige monotone, tiny unreadable type, decorative filler | BP&O, The Brand Identity, typography source lane |
| historical-material-realism | historically sensitive visuals, period atmosphere, museums, cultural content after user enables checks | era-appropriate material, construction logic, patina, weathering, grounded props, visible craft, restrained palette | mixed dynasties/eras, fantasy armor, fake calligraphy, modern fasteners, generic "ancient" sets | Historical consultant plus HQ/open study lanes |
| uncanny-folklore-horror | eerie character sheets, local legends, supernatural storyboards, suspense posters | asymmetry, damp texture, partial occlusion, low-key light, pale skin/value contrast, negative space, restrained gore | jump-scare tropes, excessive blood, random horror symbols, unreadable monster detail | Character/scene board references plus film frame lane |
| high-energy-board-sequence | social ads, beverage/product storyboards, nine-shot boards, action rhythm | clear beat-to-beat continuity, hero product frames, simple captions, varied shot size, fast readable gestures, bright contrast | too many micro-actions in one frame, inconsistent wardrobe/product, model-generated text reliance | Visual development board rules, Daily Selected, commercial references |

## Selection Heuristics

| User Cues | Default Pick |
| --- | --- |
| 真实, 人味, 城市烟火, 文旅, 纪录片感, grounded realism, lived-in city | restrained-human-realism |
| 大片, 史诗, 沙丘, 宏大, 未来但克制, vast landscape, monumental scale | monumental-cinematic-scale |
| 高级叙事, 电影短片, 严肃, 压迫感, 内心戏, prestige drama, interior tension | award-drama-interior-tension |
| 夜市, 霓虹, 潮流, 地下, 湿润, 赛博, wet night street, practical neon | urban-night-texture |
| 饮料, 新品, 年轻, 轻松, 阳光, 社交平台, product lifestyle, sunny candid | warm-commercial-lifestyle |
| 动画, 角色, 童话, 家庭, 可爱但高级, animation staging, clear silhouette | lyrical-animation-color |
| 高端, 克制, 品牌感, PPT提案, 极简, premium editorial, restrained deck | minimal-premium-editorial |
| 朝代, 考据, 博物馆, 历史准确, period material, historical accuracy | historical-material-realism only after historical check is enabled |
| 怪谈, 民俗, 恐怖, 诡异, 潮湿, folklore horror, uncanny atmosphere | uncanny-folklore-horror |
| 一张分镜板, 九宫格, 15秒, 广告分镜, beat board, commercial sequence | high-energy-board-sequence |

## Handoff Template

```text
aesthetic_profile:
visual_levers:
reference_lane:
locked_constraints:
avoid:
next_role:
```

## Deep Reference Entry Points

- Master library: `01_Research/HQ_Aesthetic_References/HQ_Aesthetic_Master_Index.md`
- Storage and relocation: `01_Research/HQ_Aesthetic_References/Aesthetic_Library_Config.md`
- User daily selections: `01_Research/Aesthetic_Daily_Selected/Daily_Selected_Index.md`
- Source discovery: `01_Research/Aesthetic_Reference_Archive/High_Level_Aesthetic_Repositories.md`
- Prompt refinement: `Prompts/Image_Aesthetic_Prompt_Reference.md`
- Motion/edit refinement: `Prompts/Video_Motion_Edit_Prompt_Rules.md`
