# Agent

`dev.Agent` loads one checkpoint and answers typed questions about a state. `dev.load` is
a shortcut for `Agent(...)`, and `dev.RLAgent` is an alias of `Agent`. `ONNXAgent` runs an
exported ONNX model on CPU; import it from `dev.onnx_agent`.

::: dev.agent.Agent

::: dev.agent.load

::: dev.onnx_agent.ONNXAgent
