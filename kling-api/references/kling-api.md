# Kling current API reference

Verified against official documentation on **2026-09-11**. Current API Key endpoints differ from the [legacy API](kling-api-legacy.md).

## Official sources

- [Overview](https://klingai.com/document-api/guides/get-started/overview)
- [Quick start](https://klingai.com/document-api/guides/get-started/quick-start)
- [Authentication](https://klingai.com/document-api/api/get-started/authentication)
- [Kling 3.0 text-to-video](https://klingai.com/document-api/api/video/3-0-omni/text-to-video)
- [Kling 3.0 image-to-video](https://klingai.com/document-api/api/video/3-0-omni/image-to-video)
- [Kling 3.0 Omni](https://klingai.com/document-api/api/video/3-0-omni/video-omni)
- [Account usage](https://klingai.com/document-api/api/assets/account-usage)

Navigation groups ordinary 3.0 and 3.0 Omni together; ordinary video endpoints still use `kling-3.0`. Do not derive endpoint spelling from documentation URLs.

## Authentication and routes

China base: `https://api-beijing.klingai.com`. Other regions: `https://api-singapore.klingai.com`. Use the account's region; SW is configured for China. Set `Authorization: Bearer <API Key>` and `Content-Type: application/json`. API Keys support both current and legacy models per the guide; AK/SK JWTs support legacy interfaces only. The runner keeps current and legacy payloads separate.

| Action | Method and path |
| --- | --- |
| Ordinary Kling 3.0 from text | `POST /text-to-video/kling-3.0` |
| Ordinary Kling 3.0 from images | `POST /image-to-video/kling-3.0` |
| Kling 3.0 Omni | `POST /omni-video/kling-3.0-omni` |
| Query tasks | `GET /tasks?task_ids=<id>` |
| Query by external ID | `GET /tasks?external_task_ids=<id>` |
| List tasks, read-only | `POST /tasks`, e.g. `{"limit":1}` |
| Free resource-pack/auth check | `GET /account/costs?start_time=<ms>&end_time=<ms>` |

The task ID parameters are mutually exclusive; multiple IDs are comma-separated. The account query is explicitly free, QPS ≤1, with required Unix-millisecond start/end times. Resource-pack quantities may lag 12 hours. An empty list does not establish cash balance or model permission.

## Ordinary Kling 3.0

```json
{
  "prompt": "A calm product shot with a slow camera push-in.",
  "settings": {
    "multi_shot": false,
    "audio": "off",
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "duration": 5
  }
}
```

- `duration`: integer 3–15 seconds, default 5.
- `resolution`: `720p`, `1080p`, `4k`. Official default 720p; SW defaults to 1080p, matching its earlier pro default.
- `audio`: `native` or `off`, default off.
- `multi_shot`: boolean. Official default true; SW explicitly uses false for one selected clip.
- Text `aspect_ratio`: `16:9`, `9:16`, `1:1`.
- Prompt maximum 3072 characters; official guidance recommends ≤2500.
- Optional `options` contains supported task options, including `external_task_id`, `callback_url`, and `watermark_info`.

Image generation replaces the top-level prompt with `contents`:

```json
{
  "contents": [
    {"type": "prompt", "text": "The camera slowly approaches the subject."},
    {"type": "first_frame", "url": "https://example.com/start.png"},
    {"type": "last_frame", "url": "https://example.com/end.png"}
  ],
  "settings": {"multi_shot": false, "audio": "off", "resolution": "1080p", "duration": 5}
}
```

First frame required, last frame optional; tail-only input is not supported. Images: URL or raw Base64; jpg/jpeg/png, ≤50MB, both dimensions ≥300px, aspect ratio 0.4–2.5. Legacy's old 10MB limit does not apply to current images.

## Omni reference versus editing

Current contents types include `prompt`, `refer_image`, `first_frame`, `last_frame`, `element`, `feature_video`, `base_video`. Assign reference assets an `id`, then cite `@id` in the prompt. The runner uses IDs such as `video_1` and `image_1`.

```json
{
  "contents": [
    {"type": "prompt", "text": "参考 @video_1 的运镜节奏，生成雨夜街道场景。"},
    {"type": "feature_video", "url": "https://example.com/reference.mp4", "id": "video_1"}
  ],
  "settings": {"resolution": "1080p", "audio": "off", "multi_shot": true}
}
```

`feature_video` guides a new clip and requires `audio=off`. The runner follows the official example with `multi_shot=true` by default for feature reference. The English schema restricts this to true, while the Chinese wording is less explicit; use the documented true setting for this mode.

`base_video` edits the supplied clip. Explicitly name requested changes and preserved elements. Audio may be `original` or `off`; native audio, first/end frames, and multi-shot are unsupported.

The official video examples omit duration and aspect ratio; the runner follows that convention for base-video edits. Current documentation does not explicitly guarantee exact source timing/dimension inheritance. Treat preservation as a requested constraint and check the result.

Video inputs: URL only, mp4/mov, ≤200MB, 3–15.5 seconds, both dimensions 700–4553px, total pixels ≤8,294,400, aspect ratio 0.4–2, frame rate 24–60fps. Output is 24fps. At most one video. There is no documented local-path, video-Base64, or multipart upload field; local videos need an authorized upload workflow first.

Image/subject counts depend on the combination. With a video, at most one video-character subject is supported; video-character subjects and reference images cannot be combined. Consult the linked Omni schema for complex combinations rather than assuming a universal seven-image allowance.

## Task lifecycle

Submission uses an object under data: `{"code":0,"data":{"id":"task-id","status":"submitted"}}`.

Queries return an **array**:

```json
{
  "code": 0,
  "data": [{
    "id": "task-id",
    "status": "succeeded",
    "outputs": [{"type": "video", "url": "https://example.com/result.mp4", "duration": "5.04"}]
  }]
}
```

Current statuses: `submitted`, `processing`, `succeeded`, `failed`. Legacy uses `succeed` and different result fields. Download `outputs[].url` where `type=video`. The service retains generated files for 30 days. Record `api_version` with a task so resuming uses the appropriate query parser.
