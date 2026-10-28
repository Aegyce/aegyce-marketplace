# Aegyce Marketplace

Aegyce 各 Agent 可复用组件的插件市场，按 Agent 组织。组件可包括 Skill、MCP 集成、工具及使用方 AI 工具支持的其他能力。<br>
The marketplace for reusable components from Aegyce agents, organized by agent. Components may include skills, MCP integrations, tools, and other capabilities supported by the receiving AI tool.

## 当前插件<br>Available plugins

### Aesy

- [Aesy:computer-technical-language](https://github.com/Aegyce/agent-aesy/tree/main/plugins/computer-technical-language)：提供计算机技术用语 Skill，用于编写、润色和审查技术表达。<br>
  Provides the computer technical language skill for writing, revising, and reviewing technical language.

## 使用方式<br>Usage

1. 在 AI 工具的插件市场管理页面选择“添加市场”，来源填写 `https://github.com/Aegyce/aegyce-marketplace.git`。<br>
   Open the plugin marketplace settings in your AI tool, choose Add marketplace, and enter `https://github.com/Aegyce/aegyce-marketplace.git` as the source.
2. 如需填写 Git 引用，使用 `main`；稀疏路径留空。<br>
   If a Git reference is required, use `main` and leave the sparse path empty.
3. 打开 Aegyce Marketplace，选择所需能力包并安装；例如 `Aesy:computer-technical-language`。<br>
   Open Aegyce Marketplace and install the capability package you need, such as `Aesy:computer-technical-language`.
4. 市场内容更新后，在使用方工具中刷新市场，再检查已安装插件是否有更新。<br>
   When the catalog changes, refresh the marketplace in your tool, then check installed plugins for updates.

上述步骤适用于支持此市场格式的 AI 工具，具体入口名称以使用方为准。每次安装包含所选插件内的全部组件；不同能力包可独立选择。<br>
These steps apply to AI tools that support this marketplace format; interface labels may vary. Each installation includes all components of the selected plugin, while separate capability packages can be selected independently.

## 许可<br>License

原创内容采用 [CC BY-NC 4.0](LICENSE) 许可，商业用途须取得[单独书面授权](COMMERCIAL-LICENSE.md)。<br>
Original materials are licensed under [CC BY-NC 4.0](LICENSE). Commercial use requires [separate written permission](COMMERCIAL-LICENSE.md).
