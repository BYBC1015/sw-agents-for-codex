# Kling legacy API reference

Archived compatibility reference for explicit `--api-version legacy` use. API Keys may authenticate legacy requests directly as Bearer credentials; AK/SK-generated JWTs are also supported for legacy only. For current requests, read [kling-api.md](kling-api.md). Old `/v1` payloads, `model_name`, angle-bracket reference tokens and `succeed` status are not the current API schema. Legacy model availability may change; Kling 1.6 is announced for retirement on 2026-09-15.

Source verified from the official Kling AI document page:

- `https://klingai.com/document-api/quickStart/productIntroduction/overview`
- `https://klingai.com/document-api/apiReference%2FcommonInfo`
- `https://klingai.com/document-api/apiReference%2Fmodel%2FtextToVideo`
- `https://klingai.com/document-api/apiReference%2Fmodel%2FimageToVideo`
- `https://klingai.com/document-api/apiReference%2Fmodel%2FmultiImageToVideo`
- `https://klingai.com/document-api/apiReference%2Fmodel%2FOmniVideo`
- `https://klingai.com/document-api/apiReference%2FcallbackProtocol`
- `https://klingai.com/document-api/apiReference%2FrateLimits`

## Base URL

Official current China-region base URL:

```text
https://api-beijing.klingai.com
```

The docs state the older `https://api.klingai.com` domain changed to `https://api-beijing.klingai.com` for China-region servers.

## Auth

Credentials:

- `AccessKey`
- `SecretKey`

JWT:

- Header: `{"alg":"HS256","typ":"JWT"}`
- Payload:
  - `iss`: AccessKey
  - `exp`: current Unix time + 1800 seconds
  - `nbf`: current Unix time - 5 seconds
- Signature: HMAC SHA256 with SecretKey

Request header:

```text
Authorization: Bearer <JWT>
Content-Type: application/json
```

## Status

Task status values:

- `submitted`
- `processing`
- `succeed`
- `failed`

Result video URL path:

```text
data.task_result.videos[0].url
```

Generated image/video URLs may be cleaned after 30 days. Download or transfer successful results.

## Text To Video

Create:

```text
POST /v1/videos/text2video
```

Query one:

```text
GET /v1/videos/text2video/{task_id}
```

List:

```text
GET /v1/videos/text2video?pageNum=1&pageSize=30
```

Common payload fields:

- `model_name`: optional, examples include `kling-v2-6`, `kling-v3`.
- `prompt`: required for normal single-shot generation.
- `negative_prompt`: optional, max 2500 chars.
- `multi_shot`: optional boolean. If true, `prompt` is ignored and `multi_prompt` is used.
- `shot_type`: `customize` or `intelligence`; required when `multi_shot=true`.
- `multi_prompt`: array of `{index, prompt, duration}`. Max 6 shots, each prompt max 512 chars, durations sum to total duration.
- `sound`: `on` or `off`.
- `cfg_scale`: 0-1; not supported by `kling-v2.x`.
- `mode`: `std`, `pro`, or `4k` where model supports it.
- `camera_control`: optional object, not compatible with every model/mode.
- `aspect_ratio`: `16:9`, `9:16`, `1:1`.
- `duration`: string seconds. V3 supports 3-15 seconds; v2.6 commonly supports 5/10 and some modes.
- `watermark_info`: `{"enabled": boolean}`.
- `callback_url`: optional.
- `external_task_id`: optional, unique per user.

## Image To Video

Create:

```text
POST /v1/videos/image2video
```

Query one:

```text
GET /v1/videos/image2video/{task_id}
```

List:

```text
GET /v1/videos/image2video?pageNum=1&pageSize=30
```

Common payload fields:

- `model_name`: optional, examples include `kling-v2-6`, `kling-v3`.
- `image`: first-frame/reference image. URL or raw Base64, no `data:image/...` prefix.
- `image_tail`: optional tail-frame image. URL or raw Base64, no prefix.
- `prompt`: required for normal single-shot generation.
- `negative_prompt`: optional.
- `multi_shot`, `shot_type`, `multi_prompt`: same multi-shot rules as text-to-video.
- `element_list`: optional reference subject IDs, max 3.
- `voice_list`: optional voice IDs, max 2; mutually exclusive with `element_list`.
- `sound`: `on` or `off`.
- `mode`: `std`, `pro`, or `4k` where supported.
- `duration`: string seconds.
- `callback_url`, `external_task_id`, `watermark_info`: optional.

Image constraints:

- Format: `.jpg`, `.jpeg`, `.png`.
- File size: max 10 MB.
- Minimum dimensions: 300 px.
- Aspect ratio: between `1:2.5` and `2.5:1`.
- `image` and `image_tail` cannot both be empty.
- `image_tail`, motion brush masks, and `camera_control` are mutually exclusive.

## Multi Image To Video

Create:

```text
POST /v1/videos/multi-image2video
```

Query one:

```text
GET /v1/videos/multi-image2video/{task_id}
```

List:

```text
GET /v1/videos/multi-image2video?pageNum=1&pageSize=30
```

Common payload fields:

- `model_name`: default in docs is `kling-v1-6`.
- `image_list`: required, max 4 items, each `{ "image": "<url-or-base64>" }`.
- `prompt`: required, max 2500 chars.
- `negative_prompt`: optional.
- `mode`: `std` or `pro`.
- `duration`: `5` or `10`.
- `aspect_ratio`: `16:9`, `9:16`, `1:1`.
- `watermark_info`, `callback_url`, `external_task_id`: optional.

## Omni-Video

Create:

```text
POST /v1/videos/omni-video
```

Query one:

```text
GET /v1/videos/omni-video/{task_id}
```

List:

```text
GET /v1/videos/omni-video?pageNum=1&pageSize=30
```

Common payload fields:

- `model_name`: optional; official enum includes `kling-video-o1` and `kling-v3-omni`.
- `prompt`: optional in multi-shot customize mode, otherwise required. Omni prompts can reference assets with `<<<image_1>>>`, `<<<video_1>>>`, and `<<<element_1>>>`.
- `multi_shot`: optional boolean. If true, `shot_type` is required and `multi_prompt` is used for `customize`.
- `multi_prompt`: max 6 shots; each shot prompt max 512 chars; shot durations sum to total duration.
- `image_list`: optional reference images, scene/style references, or first/end frames. Items use `image_url`; optional `type` is `first_frame` or `end_frame`.
- `element_list`: optional subject library references with `element_id`.
- `video_list`: optional single public MP4/MOV URL. `refer_type=feature` uses the video as style/motion/camera reference; `refer_type=base` edits the supplied video.
- `mode`: `std`, `pro`, or `4k` where supported.
- `aspect_ratio`: `16:9`, `9:16`, `1:1`; not supported for video edit or first/end-frame image-to-video cases.
- `duration`: `3` to `15` seconds where supported; ignored for `refer_type=base` edits, which follow the input video duration.
- `sound`: `on` or `off`; official docs say it must be `off` when `video_list` is provided.
- `watermark_info`, `callback_url`, `external_task_id`: optional.

Omni-Video does not expose the normal `camera_control` object. Put camera instructions into the prompt, or use `video_list` with `refer_type=feature` when a movement reference is needed.

## Camera Control

`camera_control` is optional and model-dependent.

Preset `type` values include:

- `simple`
- `down_back`
- `forward_up`
- `right_turn_forward`
- `left_turn_forward`

For `type=simple`, configure exactly one non-zero field in `config`:

- `horizontal`: -10 to 10
- `vertical`: -10 to 10
- `pan`: -10 to 10
- `tilt`: -10 to 10
- `roll`: -10 to 10
- `zoom`: -10 to 10

## Rate Limits

Kling API concurrency is account-level and resource-pack dependent. Query APIs do not occupy generation concurrency. Running generation tasks occupy concurrency until they end, including failed tasks.

When over concurrency limit, the API may return:

```json
{
  "code": 1303,
  "message": "parallel task over resource pack limit"
}
```

Use queueing and exponential backoff instead of hammering task creation.

## Common Error Codes

- `401 / 1000-1004`: authorization missing, invalid, not yet valid, or expired.
- `429 / 1101`: account arrears.
- `429 / 1102`: prepaid resource pack exhausted or expired.
- `403 / 1103`: no permission for requested resource, interface, or model.
- `400 / 1200-1201`: invalid parameter.
- `404 / 1202`: invalid method.
- `404 / 1203`: resource or model not found.
- `400 / 1300-1301`: content or platform safety policy.
- `429 / 1302`: request too fast.
- `429 / 1303`: concurrency/resource pack limit.
- `429 / 1304`: IP allowlist policy.
- `500 / 5000`, `503 / 5001`, `504 / 5002`: server-side error, maintenance, or timeout.
