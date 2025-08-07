# tests/test_core_engine.py

import unittest
from src.core_engine import CognitiveCore

class TestCognitiveCore(unittest.TestCase):
    def setUp(self):
        self.core = CognitiveCore()

    def test_signal_processing_format(self):
        input_signal = {"ticker": "SOXL", "confidence": 0.85}
        output = self.core.process_input(input_signal)
        self.assertIsInstance(output, dict)
        self.assertIn("signal", output)

    def test_state_reset_functionality(self):
        self.core.state["temp"] = "active"
        self.core.reset()
        self.assertEqual(self.core.state, {})

if __name__ == "__main__":
    unittest.main()
