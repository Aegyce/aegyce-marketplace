# Aegyce Marketplace

Aegyce 各 Agent 可复用组件的插件市场，按 Agent 组织。组件可包括 Skill、MCP 集成、工具及使用方 AI 工具支持的其他能力。<br>
<sub>The marketplace for reusable components from Aegyce agents, organized by agent. Components may include skills, MCP integrations, tools, and other capabilities supported by the receiving AI tool.</sub>

## 当前插件<br><sub>Available plugins</sub>

### Aesy

- [Aesy:computer-technical-language](https://github.com/Aegyce/agent-aesy/tree/main/plugins/computer-technical-language)：提供计算机技术用语 Skill，用于编写、润色和审查技术表达。<br>
  <sub>Provides the computer technical language skill for writing, revising, and reviewing technical language.</sub>

## 使用方式<br><sub>Usage</sub>

1. 在 AI 工具的插件市场管理页面选择“添加市场”，来源填写 `https://github.com/Aegyce/aegyce-marketplace.git`。<br>
   <sub>Open the plugin marketplace settings in your AI tool, choose Add marketplace, and enter `https://github.com/Aegyce/aegyce-marketplace.git` as the source.</sub>
2. 如需填写 Git 引用，使用 `main`；稀疏路径留空。<br>
   <sub>If a Git reference is required, use `main` and leave the sparse path empty.</sub>
3. 打开 Aegyce Marketplace，选择所需能力包并安装；例如 `Aesy:computer-technical-language`。<br>
   <sub>Open Aegyce Marketplace and install the capability package you need, such as `Aesy:computer-technical-language`.</sub>
4. 市场内容更新后，在使用方工具中刷新市场，再检查已安装插件是否有更新。<br>
   <sub>When the catalog changes, refresh the marketplace in your tool, then check installed plugins for updates.</sub>

上述步骤适用于支持此市场格式的 AI 工具，具体入口名称以使用方为准。每次安装包含所选插件内的全部组件；不同能力包可独立选择。<br>
<sub>These steps apply to AI tools that support this marketplace format; interface labels may vary. Each installation includes all components of the selected plugin, while separate capability packages can be selected independently.</sub>

## 发布维护<br><sub>Publishing</sub>

能力在各 Agent 仓库维护，市场中的发布副本、描述和图标由 GitHub Actions 同步生成。跨仓库触发的配置与版本要求见[发布说明](docs/publishing.md)。<br>
<sub>Capabilities are maintained in their Agent repositories. GitHub Actions generates the marketplace publication copies, descriptions, and icons. See the [publishing guide](docs/publishing.md) for cross-repository trigger setup and version requirements.</sub>

## 许可<br><sub>License</sub>

原创内容采用 [CC BY-NC 4.0](LICENSE) 许可，商业用途须取得[单独书面授权](COMMERCIAL-LICENSE.md)。<br>
<sub>Original materials are licensed under [CC BY-NC 4.0](LICENSE). Commercial use requires [separate written permission](COMMERCIAL-LICENSE.md).</sub>
