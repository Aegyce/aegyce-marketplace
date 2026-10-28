# 能力包发布

Agent 仓库维护能力源文件；本仓库保存可直接展示和安装的发布副本。使用者添加市场后，无需先安装插件即可读取名称、介绍、网站和图标。不要直接编辑 `plugins/`、`.agents/plugins/marketplace.json` 或 `sources.lock.json`，这些文件由同步脚本生成。

## 来源与版本

在 `sources.json` 登记插件名称、公开 GitHub 仓库、跟踪分支、源目录及市场内的发布目录。每个源目录须包含 `plugin.json`、完整许可证、商业授权说明和所有引用的资源。插件版本采用 `major.minor.patch`；任何包内内容变更都须提高版本号。

`sources.lock.json` 记录每个发布包的源提交、Git 树、版本和内容摘要。与能力包无关的 Agent 提交不会改变发布副本或锁定记录。同版本内容变化、版本倒退、缺失资源及越界路径会使同步失败，已发布内容保持不变。

## 跨仓库触发配置

1. 创建一个 fine-grained personal access token，仅允许访问 `Aegyce/aegyce-marketplace`，赋予 **Contents: Read and write** 权限。创建入口：[GitHub 令牌设置](https://github.com/settings/personal-access-tokens/new)。
2. 在来源 Agent 仓库的 **Settings → Secrets and variables → Actions** 中新增 Repository secret，名称为 `AEGYCE_MARKETPLACE_TOKEN`，值为该令牌。Aesy 的入口为 [Actions secrets](https://github.com/Aegyce/agent-aesy/settings/secrets/actions)。不要把令牌提交到仓库或粘贴到聊天中。
3. 在两个仓库启用 GitHub Actions。若仓库规则禁止工作流直接写入 `main`，需按组织规则允许发布工作流写入，或另行采用 PR 合并流程；同步脚本不会绕过分支规则。
4. 修改并 push Agent 主分支，或手动运行 Agent 仓库的 **Publish capability updates**。该工作流向市场发送 `agent-updated` 事件；市场的 **Sync plugins** 执行同步与提交。

Agent 默认的 `GITHUB_TOKEN` 仅限本仓库，因此跨仓库事件使用上述 Secret；市场提交自身内容使用其默认 `GITHUB_TOKEN`，不另需写入令牌。令牌过期后更新同名 Secret。

通知中的 `agent` 字段取来源仓库名。市场运行标题显示为 `<agent-repository> updated`，例如 `agent-aesy updated`；`agent-updated` 保留为内部事件类型。其他 Agent 接入时沿用同一规则，无需为每个 Agent 增加市场工作流。

## 同步流程

```text
Agent main push
    → Publish capability updates
    → repository_dispatch: agent-updated
    → 市场 Sync plugins
    → 校验来源、版本、描述、图标和许可证
    → 生成发布副本、市场索引与来源锁定记录
    → 有变化时提交到市场 main
```

不配置定时检查。收到通知后只检查对应 Agent：先用 `git ls-remote` 比较提交 SHA；相同则跳过下载。提交变化时浅取该提交，再比较能力目录的 Git tree SHA；目录未变则不导出、不复制。同一 Agent 的多个包共享一次仓库获取。仅对变化的包执行版本递增检查并重新生成副本；已有副本的本地一致性检查不访问网络。来源事件仅用于唤起同步；同步开始时读取登记分支的当前提交，避免事件乱序导致旧版本覆盖新版本。多个通知合并到后一次执行时，以当前分支内容为准。同步只复制已登记包，不执行 Agent 包中的脚本或安装其依赖。

修改市场的 `sources.json`、同步脚本、测试或工作流，也会触发同步。需要补发时，可以在市场的 [Actions 页面](https://github.com/Aegyce/aegyce-marketplace/actions/workflows/sync-plugins.yml) 手动运行 **Sync plugins**。

本地检查与同步：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/sync_plugins.py
python3 scripts/sync_plugins.py --check
```

事件发送成功不等于发布完成，应核对市场工作流的结果和 `sources.lock.json`。自动提交与人工修改冲突时推送会被拒绝；处理冲突后重新运行，不强制覆盖远程提交。

机制依据：[repository_dispatch](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch)、[GITHUB_TOKEN 权限范围](https://docs.github.com/en/actions/concepts/security/github_token)。
