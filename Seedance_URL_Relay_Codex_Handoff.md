# SW Assisted Extension: Seedance 2.0 + URL Relay Migration Protocol

协议定位：本文件是 SW 体系的援助式延展迁移指令，用于把「即梦2.0 / Seedance 2.0 视频生成」与「SW media uploader 图片/视频中转策略」接入目标 Codex 工作流。  
适用范围：目标项目已有自己的即梦/Seedance 工作流、或只需要最小化安装视频生成与公网 URL 中转能力。  
边界声明：只迁移 `seedance-2-video` 与 `url-relay` 能力，不引入完整 SW 工作室框架，不改变目标项目原有创意、分镜、提示词或管理体系。

接入方在自己的 Codex 对话里使用：

```text
请读取这个 MD，把 SW URL Relay 中转策略接入我的即梦/Seedance skill。先问我必要问题，再按我的选择安装或合并。
```

## 给目标 Codex 的执行目标

你要帮助接入方完成一件事：让目标即梦/Seedance 工作流可以使用 SW media uploader，把本地参考图/视频转成公网 URL，再交给 Seedance/Ark 抓取。

你不能做这些事：

- 不要安装或复制完整 SW 工作室框架。
- 不要覆盖目标项目现有即梦 skill，除非接入方明确同意。
- 不要把 `ARK_API_KEY`、上传 token、`.env`、私密配置写入仓库或 skill 文件。
- 不要在缺 token、缺上传地址、权限错误时自动切到第三方临时中转。
- 不要把 Catbox/Litterbox 的临时链接说成“自有服务器”。

## 接入前必须询问

请先向接入方询问以下问题，等待回答后再执行：

1. 你是要「合并到现有即梦 skill」，还是「安装独立最小工具包」？
2. 如果要合并到现有即梦 skill，请提供它的文件夹位置，或至少提供现有 runner 脚本路径；没有路径不能开始合并。
3. 你是否已经有 `ARK_API_KEY` 和 SW media uploader 上传 token？不要直接把 key 发到公开仓库。
4. 临时中转策略是否启用？推荐：`auto`，即自有服务器不可用时才使用 Litterbox 24h。

如果接入方说“你定”，默认选择：

- 优先询问现有即梦 skill 位置；如果接入方没有现有 skill 或不给路径，则创建独立最小工具包。
- 配置文件使用本机私密路径：`~/.config/sw-media-uploader/config.json`。
- `temporary_fallback`: `auto`
- `litterbox_time`: `24h`

## 必须给到的中转配置

SW media uploader 配置如下，真实 token 由接入方通过安全渠道提供，不写入仓库：

```json
{
  "upload_url": "http://123.56.255.86/upload",
  "public_base": "http://123.56.255.86/u",
  "token": "<paste-private-upload-token-here>",
  "max_bytes": 209715200,
  "temporary_fallback": "auto",
  "litterbox_time": "24h"
}
```

说明：

- `upload_url` 是上传入口。
- `public_base` 是下游 AI 工具可访问的公网文件前缀。
- `token` 是上传 token，只能进入本机私密配置。
- `temporary_fallback=auto` 表示先用自有服务器；只有自有服务器连接失败、超时、502/5xx 等服务器侧失败时，才用临时中转。
- `litterbox_time=24h` 表示 Litterbox 临时链接保留 24 小时。

## 推荐文件结构

如果接入方选择独立最小工具包，请创建或复制：

```text
seedance-2-video/
  SKILL.md
  agents/openai.yaml
  references/ark-seedance-api.md
  scripts/seedance_task.py
  scripts/install_employee_key.sh

url-relay/
  SKILL.md
  agents/openai.yaml
  scripts/url_relay.py
```

如果目标项目已有即梦 skill，请优先合并：

```text
existing-seedance-skill/
  SKILL.md
  scripts/<existing seedance runner>
  url-relay/
    SKILL.md
    scripts/url_relay.py
```

合并时只接入 URL Relay 能力，不重写目标项目已有提示词、工作流、UI 或项目规则。

## URL Relay 行为规范

下游工具需要公网 URL，但接入方提供的是本地文件时：

```text
local image/video file -> SW media uploader -> public URL -> Seedance/Ark
```

优先级必须是：

1. 使用 SW media uploader。
2. 如果接入方已经有公网 URL，直接使用该 URL。
3. 如果 SW media uploader 连接失败、超时或返回服务器侧错误，并且接入方允许 fallback，使用 Litterbox/Catbox 临时中转。
4. 如果是 token 缺失、上传地址缺失、权限错误、本机配置错误，不要 fallback，提示接入方修复配置。
5. 拿不到公网 URL 时，不要提交真实 Seedance 生成。

必须在 fallback 时提示接入方：

```text
SW media uploader unavailable; temporary relay fallback used: litterbox.
```

## 私密配置安装命令

Windows PowerShell：

```powershell
python url-relay/scripts/url_relay.py setup --upload-url http://123.56.255.86/upload --public-base http://123.56.255.86/u --temporary-relay-fallback auto --litterbox-time 24h
```

macOS / Linux：

```bash
python url-relay/scripts/url_relay.py setup --upload-url http://123.56.255.86/upload --public-base http://123.56.255.86/u --temporary-relay-fallback auto --litterbox-time 24h
```

执行时让接入方粘贴上传 token。输入应隐藏；保存位置默认是：

```text
~/.config/sw-media-uploader/config.json
```

这个文件不要加入 Git。

## 即梦 / Seedance Key 安装命令

如果使用本工具包里的 `seedance_task.py`：

```powershell
python seedance-2-video/scripts/seedance_task.py setup-key
```

或：

```bash
python seedance-2-video/scripts/seedance_task.py setup-key
```

保存位置默认是：

```text
~/.config/codex-seedance-2-video/secrets.json
```

这个文件也不要加入 Git。

## 接入现有即梦 Skill 的最小补丁要求

如果目标项目已有 Seedance runner，请按下面合同改造，不要照抄完整 SW：

开始前必须先拿到并确认以下至少一项：

- 现有即梦 skill 文件夹路径
- 现有 Seedance runner 脚本路径
- 现有项目根目录，并且能在其中找到即梦/Seedance 相关文件

如果接入方无法提供路径，停止合并方案，改为询问是否创建独立最小工具包。

1. 新增本地文件参数，例如：

```text
--image-file ./reference.png
```

2. 在提交 Ark/Seedance 任务前，检测本地文件并调用：

```text
python url-relay/scripts/url_relay.py upload --file ./reference.png
```

3. 读取返回 JSON 里的 `url`：

```json
{
  "ok": true,
  "url": "http://123.56.255.86/u/xxxx.png",
  "relay": "sw-media-uploader",
  "expires_hint": null
}
```

4. 把这个公网 URL 写入 Seedance/Ark 的 `image_url` 字段。

5. 如果返回：

```text
SW media uploader unavailable
```

并且接入方允许 fallback，则用：

```text
python url-relay/scripts/url_relay.py upload --file ./reference.png --temporary-relay-fallback auto --litterbox-time 24h
```

6. 如果上传失败且没有公网 URL，不要提交真实生成任务。

## 验证命令

先检查中转配置：

```powershell
python url-relay/scripts/url_relay.py doctor
```

再检查即梦环境：

```powershell
python seedance-2-video/scripts/seedance_task.py doctor
```

测试本地文件中转：

```powershell
python url-relay/scripts/url_relay.py upload --file ./reference.png
```

测试即梦 dry-run，不消耗生成额度：

```powershell
python seedance-2-video/scripts/seedance_task.py dry-run --prompt "5秒，参考图主体轻微转头，镜头缓慢推进，柔和电影光，无文字，无logo。" --image-file ./reference.png
```

真实生成前必须让接入方确认。

## 标准使用方式

有公网图时：

```powershell
python seedance-2-video/scripts/seedance_task.py run --prompt-file video_prompt.txt --image-url https://example.com/reference.png --output-dir outputs/seedance-test
```

只有本地图时：

```powershell
python seedance-2-video/scripts/seedance_task.py run --prompt-file video_prompt.txt --image-file ./reference.png --output-dir outputs/seedance-test
```

## 最终说明模板

集成完成后，请回复接入方：

```text
已接入 SW URL Relay 中转策略。

当前优先级：
1. SW media uploader: http://123.56.255.86/u
2. 已有公网 URL
3. 自有服务器连接失败时，按配置 fallback 到 Litterbox 24h

配置文件保存在本机私密路径，不进入仓库。
真实 Seedance 生成前仍需要确认，因为它会消耗额度。
```
