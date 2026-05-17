import customtkinter as ctk
from datetime import datetime
import os  # <-- NUEVO: Para poder manejar la creación de carpetas

# 1. MAIN CLASS
class MagicTaxiMeter(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        # --- DATA ATTRIBUTES (The "Boxes") ---
        self.secret_pin = "1234"
        self.trip_id = 1
        self.is_active = False    # Has the trip record started?
        self.is_running = False   # Is the clock ticking right now?
        self.is_moving = False    # Is the taxi driving?
        
        self.total_fare = 0.0
        self.fare_stopped = 0.0
        self.fare_moving = 0.0

        # --- WINDOW CONFIGURATION ---
        self.title("✨ Magic Taxi ✨")
        self.geometry("400x580") 
        self.configure(fg_color="#FFF0F5") # Lavender Blush

        self.show_login_ui()

    def show_login_ui(self):
        """Security and Welcome Screen"""
        self.login_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=25)
        self.login_frame.pack(pady=40, padx=30, fill="both", expand=True)

        # Título de Bienvenida
        ctk.CTkLabel(self.login_frame, text="🌸\n¡BIENVENIDO A MAGIC TAXI!", 
                     font=("Verdana", 16, "bold"), text_color="#FF69B4", justify="center").pack(pady=(25, 15))
        
        # Cuadro de instrucciones / tarifas
        info_text = (
            "✨ Guía de Uso del Taxímetro ✨\n\n"
            "• START / RESUME: Inicia o reanuda el viaje.\n"
            "• CHANGE GEAR: Cambia el estado del coche.\n"
            "• RESET TRIP: Borra el viaje actual si hubo un error.\n"
            "• FINISH: Finaliza el viaje y genera la factura.\n\n"
            " Tarifa en Movimiento: € 0.05 / seg\n"
            " Tarifa Parado: € 0.02 / seg"
        )
        
        self.info_label = ctk.CTkLabel(self.login_frame, text=info_text, 
                                       font=("Arial", 12), text_color="#555555",
                                       fg_color="#FFF0F5", corner_radius=15, 
                                       padx=15, pady=15, justify="left")
        self.info_label.pack(pady=10, padx=20, fill="x")
        
        # Etiqueta de acceso
        ctk.CTkLabel(self.login_frame, text="Introduce tu PIN para acceder:", 
                     font=("Arial", 12, "bold"), text_color="#8E244E").pack(pady=(20, 5))

        # Input de contraseña modificado con la indicación ENTER
        self.pin_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="PIN + ENTER",
                                      fg_color="#FFF0F5", border_color="#FFB6C1", justify="center",
                                      font=("Arial", 14))
        self.pin_entry.pack(pady=5, padx=40, fill="x")
        
        # Enlazar la tecla Enter (Return) a la verificación del PIN
        self.pin_entry.bind("<Return>", lambda event: self.verify_pin())
        self.pin_entry.focus() # Auto-selecciona el campo para escribir directamente

    def verify_pin(self):
        """PIN Verification logic"""
        if self.pin_entry.get() == self.secret_pin:
            self.login_frame.destroy()
            self.setup_main_app()
            self.run_clock_loop()
        else:
            self.pin_entry.configure(border_color="red")
            self.pin_entry.delete(0, 'end') # Limpia el PIN incorrecto
           
    def setup_main_app(self):
        """Main Aesthetic Interface"""
        ctk.CTkLabel(self, text="🌸 MAGIC TAXI 🌸", font=("Verdana", 20, "bold"), 
                     text_color="#FF69B4").pack(pady=(20, 5))

        # Main Fare Display
        self.display_frame = ctk.CTkFrame(self, corner_radius=25, fg_color="white", 
                                          border_width=2, border_color="#FFB6C1")
        self.display_frame.pack(pady=10, padx=30, fill="both")

        self.fare_display = ctk.CTkLabel(self.display_frame, text="€ 0.00", 
                                         font=("Courier New", 45, "bold"), text_color="#555555")
        self.fare_display.pack(pady=25)

        self.details_label = ctk.CTkLabel(self, text="Stop: €0.00 | Move: €0.00", 
                                          font=("Arial", 16), text_color="#FF69B4")
        self.details_label.pack(pady=2)

        # Status Badge
        self.status_label = ctk.CTkLabel(self, text="SYSTEM READY", font=("Arial", 11, "bold"), 
                                         text_color="white", fg_color="#ADD8E6", corner_radius=8)
        self.status_label.pack(pady=10)

        # --- CONTROL BUTTONS ---
        
        # START: Green tones
        self.btn_start = ctk.CTkButton(self, text="START / RESUME", corner_radius=15, 
                                       fg_color="#B2F2BB", text_color="#1E5631", hover_color="#74B886", 
                                       command=self.start_trip)
        self.btn_start.pack(pady=6, padx=50, fill="x")

        # DRIVE/STOP: Pink/Red tones
        self.btn_toggle = ctk.CTkButton(self, text="CHANGE GEAR", corner_radius=15, 
                                        fg_color="#FFD1DC", text_color="#8E244E", hover_color="#F0A1B5", 
                                        command=self.toggle_move)
        self.btn_toggle.pack(pady=6, padx=50, fill="x")

        # RESET: Tonos Amarillos/Naranjas (Alerta/Reinicio)
        self.btn_reset = ctk.CTkButton(self, text="RESET TRIP (ACCIDENT)", corner_radius=15, 
                                       fg_color="#FFE3A8", text_color="#7C5200", hover_color="#FFD075", 
                                       command=self.reset_trip)
        self.btn_reset.pack(pady=6, padx=50, fill="x")

        # FINISH TRIP: Blue tones
        self.btn_stop_trip = ctk.CTkButton(self, text="FINISH (GENERATE BILL)", corner_radius=15, 
                                           fg_color="#D0EBFF", text_color="#0D47A1", hover_color="#90CAF9", 
                                           command=self.finish_trip_final)
        self.btn_stop_trip.pack(pady=6, padx=50, fill="x")
        
        # --- BOTÓN QUIT (Abajo a la derecha) ---
        self.btn_quit = ctk.CTkButton(self, text="QUIT ×", width=85, height=30, corner_radius=10,
                                      fg_color="#FFC3C3", text_color="#7A1E1E", hover_color="#FFA6A6",
                                      font=("Arial", 12, "bold"), command=self.destroy)
        self.btn_quit.pack(side="bottom", anchor="e", pady=15, padx=20)
        
    def start_trip(self):
        if not self.is_active:
            self.is_active = True
            self.total_fare = 0.0
            self.fare_stopped = 0.0
            self.fare_moving = 0.0
            
        self.is_running = True 
        self.is_moving = True 
        
        self.status_label.configure(text="MOVING", fg_color="#51CF66")
        self.btn_start.configure(state="disabled", fg_color="#E0E0E0", text_color="#A0A0A0")

    def toggle_move(self):
        if self.is_running:
            self.is_moving = not self.is_moving
            status = "MOVING" if self.is_moving else "CAR STOPPED"
            color = "#51CF66" if self.is_moving else "#FAB005"
            self.status_label.configure(text=status, fg_color=color)

    def reset_trip(self):
        """Resets all metrics without changing the trip ID or creating a file"""
        self.is_active = False
        self.is_running = False
        self.is_moving = False
        
        # Reiniciar variables de dinero
        self.total_fare = 0.0
        self.fare_stopped = 0.0
        self.fare_moving = 0.0
        
        # Actualizar la interfaz visual de forma inmediata
        self.fare_display.configure(text="€ 0.00")
        self.details_label.configure(text="Stop: €0.00 | Move: €0.00")
        self.status_label.configure(text="SYSTEM READY", fg_color="#ADD8E6")
        self.btn_start.configure(state="normal", fg_color="#B2F2BB", text_color="#1E5631")
        print(f"Trip #{self.trip_id} was reset due to accidental activation.")

    def finish_trip_final(self):
        if self.is_active:
            self.is_active = False
            self.is_running = False
            self.status_label.configure(text="TRIP FINISHED", fg_color="#CED4DA")
            self.generate_invoice()
            self.trip_id += 1
            self.btn_start.configure(state="normal", fg_color="#B2F2BB", text_color="#1E5631")

    def generate_invoice(self):
        folder_name = "invoices"
        
        # Creamos la carpeta si no existe (exist_ok=True evita que lance error si ya existe)
        os.makedirs(folder_name, exist_ok=True)
        
        # Unimos la ruta de la carpeta con el nombre del archivo
        filename = os.path.join(folder_name, f"invoice_{self.trip_id:03d}.txt")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- MAGIC TAXI INVOICE #{self.trip_id:03d} ---\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total: €{self.total_fare:.2f}\n")
            f.write(f"Stopped Fare: €{self.fare_stopped:.2f}\n")
            f.write(f"Moving Fare: €{self.fare_moving:.2f}\n")
            f.write("--- Thank you! ---\n")
        print(f"Invoice {filename} generated inside '{folder_name}' folder.")

    def run_clock_loop(self):
        """Clock Logic"""
        if self.is_active and self.is_running:
            if self.is_moving:
                self.fare_moving += 0.05
            else:
                self.fare_stopped += 0.02
            
            self.total_fare = self.fare_moving + self.fare_stopped
            self.fare_display.configure(text=f"€ {self.total_fare:.2f}")
            self.details_label.configure(text=f"Stop: €{self.fare_stopped:.2f} | Move: €{self.fare_moving:.2f}")
        
        self.after(1000, self.run_clock_loop)

if __name__ == "__main__":
    app = MagicTaxiMeter()
    app.mainloop()