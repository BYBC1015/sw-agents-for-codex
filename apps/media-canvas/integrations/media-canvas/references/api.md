# 0.4.0 接口参考

CLI 完整路径：`{{CANVAS_ROOT}}\canvas_cli.py`。
示例中的 PID、CID、VERSION、NODE、TASK 均从真实读取结果替换。执行前缀为 `{{PYTHON}} -B -X utf8`。

```text
canvas_cli.py projects --query 项目名
canvas_cli.py --conversation CID binding
canvas_cli.py --conversation CID --project PID bind --body-file 绑定.json
canvas_cli.py --conversation CID --project PID open
canvas_cli.py --conversation CID --project PID project-handoff
canvas_cli.py --conversation CID --project PID packet --task T001
canvas_cli.py --conversation CID --project PID --binding-version VERSION ingest --body-file 导入.json
canvas_cli.py --conversation CID --project PID --binding-version VERSION create-task --body-file 任务.json
canvas_cli.py --conversation CID --project PID --binding-version VERSION claim T001
canvas_cli.py --conversation CID --project PID --binding-version VERSION result --body-file 结果.json
canvas_cli.py --conversation CID --project PID --binding-version VERSION project --body-file 项目信息.json
canvas_cli.py --conversation CID --project PID --binding-version VERSION version --body-file 取舍.json
canvas_cli.py --conversation CID --project PID --binding-version VERSION checkpoint --body-file 交接.json
canvas_cli.py --conversation CID --project PID handoff --checkpoint ID
```

`bind` body：`{"conversationId":"CID","projectId":"PID","expectedVersion":0,"label":"实际对话简称"}`。expectedVersion 取 binding 返回；不要拿项目 revision 代替。

`create-project` body：`{"requestId":"唯一编号","name":"项目名","goal":"项目目标"}`。

`ingest` body：`{"requestId":"唯一编号","files":[{"path":"绝对路径","title":"参考图","mode":"copy"}]}`。reference 保留路径；copy 复制到项目过程/导入素材，以内容散列避免覆盖。批量最多30项，全部登记成功后才提交。

`create-task` body：`{"requestId":"唯一编号","intent":"discuss","text":"讨论要求","nodeIds":["NODE"],"frameRange":"F100–120"}`。输入必须是当前项目真实素材/文字节点。执行任务 intent=execute；只适用于已授权的具体制作要求。

`result` body：`{"requestId":"唯一编号","task":"T001","text":"完整结果说明","files":[{"path":"实际输出文件","title":"新版本","mode":"reference","parentNode":"原素材节点"}]}`。任务先 claim；说明与输出一次提交为 review。纯讨论 files 为空。不要把中途日志写成完成结果。

`project` body：`{"expectedRevision":12,"goal":"目标","decisions":"已确认决定及依据","constraints":["锁定项"],"nextStep":"下一步","progress":{"stage":"当前阶段","blockers":"阻塞","openQuestions":"待确认事项","deliveryNotes":"交付要求"}}`。只传本轮需要更新的字段，冲突后重新读取合并。

`version` body：`{"expectedRevision":12,"assetId":"ASSET","disposition":"selected","reason":"用户已确认的理由"}`。disposition 可为 candidate、selected、rejected、delivered。多项素材可同时选定，不自动取消其他素材。标记 delivered 只记录状态，不搬动文件。

`checkpoint` body：`{"requestId":"唯一编号","expectedRevision":12,"title":"阶段交接"}`。返回固定 ID；通过 project-handoff --checkpoint ID 按章节读取。完整快照保存在项目 SQLite，backup 包含快照。

网页 GET：`/api/projects`、`/api/binding?conversation=CID`；其余项目接口必须带 `?project=PID`，媒体 URL 同样带 project。
网页 POST 都要求 `Content-Type: application/json` 和 `X-Canvas-Client: web`，项目级 body 必须有 projectId。对话写入还携带 conversationId、bindingVersion。
HTTP：`/api/projects/new`、`/api/bind`、`/api/ingest`、`/api/tasks`、`/api/claim`、`/api/result`、`/api/project`、`/api/versions`、`/api/checkpoints`。

对话绑定是画布本地索引中的持久关联，不会自动修改 Codex 桌面项目归属或系统提示。不同聊天可绑定同一项目；这是本机协作功能，尚无多人的审核/合并系统。

## 轻量入口

--conversation CID launch 返回当前对话的 URL；未绑定只返回空白入口，不创建或列举项目。
--conversation CID --project PID summary 返回精简摘要；--since PID:REVISION 在相同修订下只返回 unchanged。明确接续仍用 project-handoff，普通启动不读取它。
WebMCP 默认 get_canvas_context 为 summary；scope=selection 读取本页选区，task=T001 读取固定任务，默认分页3项。
get_canvas_detail(kind=project, section=tasks, checkpoint=ID) 读取完整项目对应章节；kind=handoff 获取接续指令。旧 get_canvas_project_handoff / get_canvas_handoff 网页工具已并入 detail，HTTP/CLI 完整交接接口不变。
写入前调用 enable_canvas_actions 一次；再发现新增工具。工具动作与旧版相同，新增 create_canvas_project 支持 requestId/name/goal/conversationId，显式创建后绑定并打开。
### 排布（只改节点坐标）

`layout --body-file JSON` 或 `POST /api/layout`，JSON 为 `{"expectedRevision":当前修订,"action":"arrange"}`；撤销时 action=undo。HTTP 带 projectId；聊天 CLI 仍需 project/conversation/binding-version 防护。读当前修订后提交，冲突时重读。手动移动或节点数量改变后，撤销会拒绝，避免覆盖新的工作。空项目安全无操作。

## 0.4.0 镜头版本与连续性

CLI 全局 project/conversation/binding-version 参数与原接口一致。只在相关分镜工作时读取，不扩大默认启动上下文。

```text
canvas_cli.py [global scope] storyboard --kind shots --limit 3
canvas_cli.py [global scope] storyboard --kind entities --limit 3
canvas_cli.py [global scope] storyboard-impact --entity wardrobe-main
canvas_cli.py [global scope] shot-packet --shot S03
canvas_cli.py [global scope] storyboard-edit --body-file edit.json
canvas_cli.py [global scope] storyboard-export
canvas_cli.py [global scope] storyboard-export --final
```

所有修改 body 包含 `requestId`、`expectedRevision`、`action`、`id`。响应不明时原样重试；修订冲突后重读。

- `action: entity`，新建时提供 `kind: character/wardrobe/scene/prop/product/style`，`fields` 包含 `description`、`locks` 字符串数组、可选 `assetId`。
- `action: shot`，`fields` 支持 `title/script/duration/camera/locks/entityRefs/outputAssetId`。`entityRefs` 如 `{"wardrobe-main":1}`，明确引用版本，缺省字段沿用本镜头当前版本。输出需为本项目已登记素材。改画面/机位/引用/锁定项时不传旧 outputAssetId；服务会清除旧输出关联。
- `action: select`，提供 `kind: shot/entity` 和 `version`，恢复该对象的完整历史版本。
- `action: review`，提供 `shotVersion`、`status: pass/fail` 和 `evidence`。只有看过实际输出后才能写 pass。依赖过期或缺图不可通过。

实体变更不会重写镜头或启动生成。`storyboard-impact` 返回精确受影响镜头；`shot-packet` 合并固定版本的资产锁定项及本镜头锁定项，可保存为 JSON 交给 Banana `--lock-file`。它不会自动传递参考图片，须按 packet 的 assetId 读取本项目素材后指定参考图。

HTTP GET：`/api/storyboard?kind=shots`、`/api/storyboard-impact?entity=ID`、`/api/shot-packet?shot=ID`、`/api/storyboard-export?final=1`，均需 project 参数。POST `/api/storyboard` 共用上述修改 body。完整交接支持 `section=shots/entities`。导出清单不含本机路径；final 只检查记录完整性和已有验收依据，不代表软件自动完成视觉判断。
