# Configuration

The CLI loads configuration from the JSON file pointed to by `ORGPLAN_CONFIG`
or the `--config` flag.

## Keys
- `data_root` (required): Directory that contains `YYYY/MM-notes.md` files.
- `plugins` (optional): List of plugin directories. Each must include
  `orgplan_plugin.py`.
- `plugin_opts` (optional): Plugin-specific configuration keyed by plugin name.

## Example

```json
{
  "data_root": "C:\\Users\\you\\orgplan-data",
  "plugins": [
    "C:\\Users\\you\\repos\\orgplan\\examples\\reference_plugin"
  ],
  "plugin_opts": {}
}
```
