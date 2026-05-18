# test_magic_taximetro.py
import unittest
from base import MagicTaxiMeter  # Imports your class from base.py

class TestMagicTaxiMeterLogic(unittest.TestCase):

    def setUp(self):
        """Initializes the app before each test"""
        self.app = MagicTaxiMeter()
        if hasattr(self.app, 'login_frame'):
            self.app.login_frame.destroy()  # Virtually destroys the login screen
        self.app.setup_main_app()       # Loads the main interface directly

    def tearDown(self):
        """Cleans up memory after each test"""
        self.app.destroy()

    def test_01_initial_state(self):
        """Verifies that the initial state values are set to zero"""
        self.assertEqual(self.app.total_fare, 0.0)
        self.assertEqual(self.app.fare_moving, 0.0)
        self.assertEqual(self.app.fare_stopped, 0.0)
        self.assertEqual(self.app.status_label.cget("text"), "SYSTEM READY")

    def test_02_start_trip_activation(self):
        """Tests that the START button correctly activates the execution flags"""
        self.app.start_trip()
        self.assertTrue(self.app.is_active)
        self.assertTrue(self.app.is_running)
        self.assertTrue(self.app.is_moving)
        self.assertEqual(self.app.status_label.cget("text"), "MOVING")

    def test_03_fare_calculation_moving(self):
        """Simulates a trip in motion. Expected: €0.15"""
        self.app.start_trip()
        for _ in range(3):
            if self.app.is_active and self.app.is_running:
                self.app.fare_moving += 0.05
                self.app.total_fare = self.app.fare_moving + self.app.fare_stopped

        self.assertAlmostEqual(self.app.total_fare, 0.15, places=2)

    def test_04_fare_calculation_stopped(self):
        """Simulates a stopped car. Expected: €0.08"""
        self.app.start_trip()
        self.app.toggle_move()
        
        for _ in range(4):
            if self.app.is_active and self.app.is_running:
                self.app.fare_stopped += 0.02
                self.app.total_fare = self.app.fare_moving + self.app.fare_stopped

        self.assertAlmostEqual(self.app.total_fare, 0.08, places=2)

    def test_05_reset_trip(self):
        """Verifies that the RESET function clears all counters"""
        self.app.start_trip()
        self.app.fare_moving = 1.50
        self.app.total_fare = 1.50
        
        self.app.reset_trip()
        
        self.assertEqual(self.app.total_fare, 0.0)
        self.assertFalse(self.app.is_active)

if __name__ == "__main__":
    unittest.main()