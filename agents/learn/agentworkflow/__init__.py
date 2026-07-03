"""
## Automating workflows with Multi-Agent Workflows

Instead of manual workflow creation, we can use the AgentWorkflow class to create a multi-agent
workflow. The AgentWorkflow uses Workflow Agents to allow you to create a system of one or more
agents that can collaborate and hand off tasks to each other based on their specialized
capabilities. This enables building complex agent systems where different agents handle
different aspects of a task. Instead of importing classes from llama_index.core.agent,
we will import the agent classes from llama_index.core.agent.workflow.
One agent must be designated as the root agent in the AgentWorkflow constructor.
When a user message comes in, it is first routed to the root agent.

Each agent can then:

    - Handle the request directly using their tools
    - Handoff to another agent better suited for the task
    - Return a response to the user

    for more information: https://huggingface.co/learn/agents-course/unit2/llama-index/workflows#automating-workflows-with-multi-agent-workflows
"""
