# test_magic_taximetro.py
import unittest
from base import MagicTaxiMeter  # Importa tu clase desde base.py

class TestMagicTaxiMeterLogic(unittest.TestCase):

    def setUp(self):
        """Inicializa la app antes de cada test"""
        self.app = MagicTaxiMeter()
        if hasattr(self.app, 'login_frame'):
            self.app.login_frame.destroy()  # Destruye el login virtualmente
        self.app.setup_main_app()       # Carga la interfaz principal directamente

    def tearDown(self):
        """Limpia la memoria tras cada test"""
        self.app.destroy()

    def test_01_initial_state(self):
        """Verifica el estado inicial a cero"""
        self.assertEqual(self.app.total_fare, 0.0)
        self.assertEqual(self.app.fare_moving, 0.0)
        self.assertEqual(self.app.fare_stopped, 0.0)
        self.assertEqual(self.app.status_label.cget("text"), "SYSTEM READY")

    def test_02_start_trip_activation(self):
        """Prueba que el botón START activa los flags correctamente"""
        self.app.start_trip()
        self.assertTrue(self.app.is_active)
        self.assertTrue(self.app.is_running)
        self.assertTrue(self.app.is_moving)
        self.assertEqual(self.app.status_label.cget("text"), "MOVING")

    def test_03_fare_calculation_moving(self):
        """Simula viaje en movimiento. Esperado: €0.15"""
        self.app.start_trip()
        for _ in range(3):
            if self.app.is_active and self.app.is_running:
                self.app.fare_moving += 0.05
                self.app.total_fare = self.app.fare_moving + self.app.fare_stopped

        self.assertAlmostEqual(self.app.total_fare, 0.15, places=2)

    def test_04_fare_calculation_stopped(self):
        """Simula coche detenido. Esperado: €0.08"""
        self.app.start_trip()
        self.app.toggle_move()
        
        for _ in range(4):
            if self.app.is_active and self.app.is_running:
                self.app.fare_stopped += 0.02
                self.app.total_fare = self.app.fare_moving + self.app.fare_stopped

        self.assertAlmostEqual(self.app.total_fare, 0.08, places=2)

    def test_05_reset_trip(self):
        """Verifica que el RESET limpie los contadores"""
        self.app.start_trip()
        self.app.fare_moving = 1.50
        self.app.total_fare = 1.50
        
        self.app.reset_trip()
        
        self.assertEqual(self.app.total_fare, 0.0)
        self.assertFalse(self.app.is_active)

if __name__ == "__main__":
    unittest.main()