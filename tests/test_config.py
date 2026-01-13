import json
import os
import tempfile
import unittest

from orgplan.config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_config_from_env(self):
        with tempfile.TemporaryDirectory() as data_root:
            payload = {
                "data_root": data_root,
                "plugins": ["/tmp/plugin"],
                "plugin_opts": {"demo": {"enabled": True}},
            }
            with tempfile.NamedTemporaryFile("w", delete=False) as handle:
                json.dump(payload, handle)
                path = handle.name

            try:
                os.environ["ORGPLAN_CONFIG"] = path
                config = load_config()
                self.assertEqual(config.data_root, os.path.abspath(data_root))
                self.assertEqual(config.plugins[-1].endswith("plugin"), True)
                self.assertIn("demo", config.plugin_opts)
            finally:
                os.environ.pop("ORGPLAN_CONFIG", None)
                os.unlink(path)

    def test_plugins_must_be_list(self):
        with tempfile.TemporaryDirectory() as data_root:
            payload = {"data_root": data_root, "plugins": "not-a-list"}
            with tempfile.NamedTemporaryFile("w", delete=False) as handle:
                json.dump(payload, handle)
                path = handle.name

            try:
                with self.assertRaises(ValueError):
                    load_config(path)
            finally:
                os.unlink(path)

    def test_missing_data_root(self):
        payload = {"plugins": []}
        with tempfile.NamedTemporaryFile("w", delete=False) as handle:
            json.dump(payload, handle)
            path = handle.name

        try:
            with self.assertRaises(ValueError):
                load_config(path)
        finally:
            os.unlink(path)

    def test_nonexistent_data_root(self):
        payload = {"data_root": "/no/such/path", "plugins": []}
        with tempfile.NamedTemporaryFile("w", delete=False) as handle:
            json.dump(payload, handle)
            path = handle.name

        try:
            with self.assertRaises(ValueError):
                load_config(path)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
