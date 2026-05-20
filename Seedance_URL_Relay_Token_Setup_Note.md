# Seedance 2.0 URL Relay Token Setup Note

本文件用于说明：在 Codex 工作流里调用即梦2.0 / Seedance 2.0 时，为什么有时需要配置 SW URL Relay token，以及需要填写什么。

## 需要填写什么

需要填写的是：

```text
SW URL Relay upload token
```

它不是 Ark key。

区别如下：

```text
Ark key
= 调用即梦2.0 / Seedance 2.0 生成视频的 API key

SW URL Relay token
= 把本地图片/视频上传到 SW media uploader 中转服务器时使用的上传凭证
```

## 为什么需要 URL Relay

Seedance / Ark API 通常不能直接读取本地电脑路径，例如：

```text
C:\Users\...\reference.png
```

它需要公网可访问的图片或视频 URL，例如：

```text
http://123.56.255.86/u/xxxx.png
```

所以本地参考图的标准流程是：

```text
本地参考图
-> SW URL Relay 上传
-> 得到公网 URL
-> Seedance / Ark 读取公网 URL
-> 提交视频生成
```

## 图片已经上传到 Codex 客户端，还需要吗

结论：**如果要通过 Codex 脚本/API 调用 Seedance，通常仍然需要。**

原因是：

```text
图片上传到 Codex 客户端
= Codex 可以查看、分析、写提示词

图片有公网 URL
= Seedance / Ark API 可以抓取并作为参考图
```

这两件事不是一回事。

### 仍然需要 URL Relay 的情况

- 图片只是上传到了 Codex 对话里。
- 图片在本地电脑上，路径类似 `C:\...\image.png`。
- Codex 要通过 `seedance_task.py` 或类似 API runner 调用 Seedance。
- Seedance 参数需要 `image_url`，但当前只有本地文件或 Codex 附件。

这时需要 URL Relay 把图片变成公网 URL。

### 不需要 URL Relay 的情况

- 已经有一个公网可访问图片 URL，例如 `https://...jpg`。
- 直接在即梦网页端手动上传图片，不通过 Codex 脚本/API。
- 只让 Codex 看图、分析图、写提示词，不提交 Seedance 生成。
- 目标工作流使用自己的对象存储、OSS、COS、S3 或其他公网图床。

## 配置命令

优先使用用户级 skill 路径：

```powershell
python "$env:USERPROFILE\.codex\skills\url-relay\scripts\url_relay.py" setup --upload-url http://123.56.255.86/upload --public-base http://123.56.255.86/u --temporary-relay-fallback auto --litterbox-time 24h
```

如果用户级 skill 不存在，可以使用项目内路径：

```powershell
python "C:\Users\Administrator\Documents\New project\url-relay\scripts\url_relay.py" setup --upload-url http://123.56.255.86/upload --public-base http://123.56.255.86/u --temporary-relay-fallback auto --litterbox-time 24h
```

执行后，终端会要求输入：

```text
Relay token:
```

这里粘贴 SW URL Relay 的上传 token。

## 配置保存位置

token 会保存到本机私密配置：

```text
~/.config/sw-media-uploader/config.json
```

不要把这个文件提交到 Git。

不要把 token 写入：

- `SKILL.md`
- `README.md`
- `.env` 示例
- 提示词
- 对话交付文档
- Git 仓库

## 验证命令

配置后运行：

```powershell
python "$env:USERPROFILE\.codex\skills\url-relay\scripts\url_relay.py" doctor
```

如果用户级路径不存在，用项目内路径验证：

```powershell
python "C:\Users\Administrator\Documents\New project\url-relay\scripts\url_relay.py" doctor
```

## 使用逻辑

当需要把本地参考图交给 Seedance 时：

```powershell
python "$env:USERPROFILE\.codex\skills\url-relay\scripts\url_relay.py" upload --file .\reference.png
```

成功后会返回类似：

```json
{
  "ok": true,
  "url": "http://123.56.255.86/u/xxxx.png",
  "relay": "sw-media-uploader"
}
```

把返回的 `url` 交给 Seedance 的 `image_url` 参数即可。

## 临时中转说明

当前策略是：

1. 优先使用 SW media uploader。
2. 如果已有公网 URL，直接使用已有 URL。
3. 如果 SW media uploader 连接失败、超时或服务器 5xx，并且配置允许 fallback，才使用 Litterbox/Catbox 临时中转。
4. 如果是 token 缺失、权限错误、上传地址错误或本机配置错误，不自动 fallback，必须先修复配置。

标准提示：

```text
SW media uploader unavailable; temporary relay fallback used: litterbox.
```

## 一句话解释

Codex 客户端能看到图片，不代表 Seedance / Ark API 能抓到图片。
如果通过 Codex 脚本调用 Seedance，并且参考图不是公网 URL，就需要 URL Relay token 把图片上传成公网 URL。
