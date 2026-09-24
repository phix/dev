"""MCP (Model Context Protocol) stdio server for Dev (optional extra).

Install the extra to use it:

    pip install "dev[mcp]"

Then run the server:

    dev-mcp-server            # console script
    python -m dev.mcp.server  # equivalent module form

The submodules ``device`` and ``tools`` are importable without the ``mcp``
dependency; ``server`` requires the extra.
"""

__all__ = ["device", "server", "tools"]
