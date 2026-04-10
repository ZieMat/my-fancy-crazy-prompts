# HexStrike MCP Setup

## Quick Start

1. **Install dependencies**
   ```bash
   pip install requests
   ```

2. **Update `mcp.json`**
   ```json
   {
     "command": "python3",
     "args": ["/path/to/hexstrike_mcp.py", "--server", "http://IP:8888"]
   }
   ```

3. **Run HexStrike server**
   ```bash
   hexstrike-server --port 8888
   ```

4. **Test connection**
   ```bash
   python3 hexstrike_mcp.py --server http://localhost:8888 --test
   ```

## Configuration

Replace in `mcp.json`:
- `/path/to/hexstrike_mcp.py` → actual file path
- `IP` → server IP address
- `8888` → server port

## Security

⚠️ **`alwaysAllow` is empty by default!**

For autonomous execution, add: `"alwaysAllow": ["*"]`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Import error | `pip install requests` |
| Connection refused | Check HexStrike server is running |
| Timeout | Increase `timeout` in config |
