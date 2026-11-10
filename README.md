# Aegyce Marketplace

Aegyce Marketplace 按 Agent 分类，分发各 Agent 中可复用的组件。组件可包括 Skill、MCP 集成、工具，以及 AI 工具支持的其他能力。<br><sub>Aegyce Marketplace distributes reusable components from Aegyce agents, with plugins grouped by agent. Components may include skills, MCP integrations, tools, and other capabilities supported by AI tools.</sub>

## 当前插件<br><sub>Available plugins</sub>

### Aesy

[Aesy](https://github.com/Aegyce/agent-aesy) 是 Aegyce 的通用 Agent。当 Requirement 未找到适合处理当前任务的领域 Agent 时，由 Aesy 执行其委派的计划。其可复用的 Skill、MCP 集成与工具等组件以独立能力包形式在本市场分发；具体能力与组件详情见其仓库说明。<br><sub>[Aesy](https://github.com/Aegyce/agent-aesy) is Aegyce's general-purpose agent. When Requirement cannot find a specialized agent suited to the current task, it delegates the plan to Aesy for execution. Its reusable skills, MCP integrations, and tools are distributed in this marketplace as standalone capability packages; see its repository for detailed capabilities and components.</sub>

## 使用方式<br><sub>Usage</sub>

1. 在 AI 工具的插件市场管理页面选择“添加市场”，来源填写 `https://github.com/Aegyce/aegyce-marketplace.git`。<br><sub>Open the plugin marketplace settings in your AI tool, choose Add marketplace, and enter `https://github.com/Aegyce/aegyce-marketplace.git` as the source.</sub>

2. 如需填写 Git 引用，使用 `main`；稀疏路径留空。<br><sub>If a Git reference is required, use `main` and leave the sparse path empty.</sub>

3. 打开 Aegyce Marketplace，选择所需能力包并安装；例如 `Aesy:computer-technical-language`。<br><sub>Open Aegyce Marketplace and install the capability package you need, such as `Aesy:computer-technical-language`.</sub>

4. 市场内容更新后，在所用的 AI 工具中刷新市场，再检查已安装插件是否有更新。<br><sub>When the catalog changes, refresh the marketplace in your AI tool, then check installed plugins for updates.</sub>

上述步骤适用于支持此市场格式的 AI 工具，具体入口名称以相应工具的界面为准。安装插件时会安装其中的全部组件；不同能力包可以分别选择和安装。<br><sub>These steps apply to AI tools that support this marketplace format; refer to your tool’s interface for the exact labels. Installing a plugin installs all of its components. You can choose and install each capability package separately.</sub>

## 许可<br><sub>License</sub>

原创内容采用 [CC BY-NC 4.0](LICENSE) 许可，商业用途须取得[单独书面授权](COMMERCIAL-LICENSE.md)。<br><sub>Original materials are licensed under [CC BY-NC 4.0](LICENSE). Commercial use requires [separate written permission](COMMERCIAL-LICENSE.md).</sub>
