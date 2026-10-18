import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "check_webhooks", pathlib.Path(__file__).with_name("check-discord-webhooks.py")
)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class WebhookScanTests(unittest.TestCase):
    def test_detects_endpoint_variants(self):
        for host in ("discord.com", "discordapp.com", "canary.discord.com", "ptb.discord.com"):
            for api in ("api", "api/v10"):
                endpoint = f"https://{host}/{api}/webhooks/123456/{'x' * 40}"
                with self.subTest(host=host, api=api):
                    self.assertTrue(scanner.has_webhook(endpoint))
                    self.assertTrue(scanner.has_webhook(endpoint.replace("/", r"\/")))

    def test_allows_documentation_and_environment_expressions(self):
        self.assertFalse(scanner.has_webhook("={{ $env.DISCORD_WEBHOOK_URL }}"))
        self.assertFalse(scanner.has_webhook("https://discord.com/api/webhooks/ID/TOKEN"))
        self.assertFalse(scanner.has_webhook("https://discord.com/developers/docs"))


if __name__ == "__main__":
    unittest.main()
