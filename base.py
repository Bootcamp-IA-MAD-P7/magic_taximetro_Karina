import customtkinter as ctk
from datetime import datetime
import os
import logging  


class MagicTaxiMeter(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        # Start the logging system first to record everything from the beginning
        self.setup_logging()

        # Secret password and counter for the trips
        self.secret_pin = "1234"
        self.trip_id = 1
        
        # True/False variables to control what the taxi is doing right now
        self.is_active = False    # True if there is a passenger inside the taxi
        self.is_running = False   # True if the taxi meter clock is ticking
        self.is_moving = False    # True if the car is driving, False if it is stopped
        
        # Variables to store the money/fare calculations
        self.total_fare = 0.0
        self.fare_stopped = 0.0
        self.fare_moving = 0.0

        # Set up the window title, size, and background color
        self.title("✨ Magic Taxi ✨")
        self.geometry("400x580") 
        self.configure(fg_color="#FFF0F5") 

        # Show the login screen first for security
        self.show_login_ui()

    def setup_logging(self):
        # Create a folder for logs if it does not exist and set up the text file
        log_folder = "logs"
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(log_folder, "taxi_system.log")
        
        # Set how the log file will look (date, time, and the message)
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            encoding="utf-8"
        )
        logging.info("--- SISTEMA INICIADO ---")

    def show_login_ui(self):
        # Create the white box (frame) for the login screen
        self.login_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=25)
        self.login_frame.pack(pady=40, padx=30, fill="both", expand=True)

        ctk.CTkLabel(self.login_frame, text="🌸\n¡BIENVENIDO A MAGIC TAXI!", 
                     font=("Verdana", 16, "bold"), text_color="#FF69B4", justify="center").pack(pady=(25, 15))
        
        # Text guide to show the rules and prices to the driver
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
        
        ctk.CTkLabel(self.login_frame, text="Introduce tu PIN para acceder:", 
                     font=("Arial", 12, "bold"), text_color="#8E244E").pack(pady=(20, 5))

        self.pin_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="PIN + ENTER",
                                      fg_color="#FFF0F5", border_color="#FFB6C1", justify="center",
                                      font=("Arial", 14))
        self.pin_entry.pack(pady=5, padx=40, fill="x")
        
        # Connect the Enter key of the keyboard to check the PIN
        self.pin_entry.bind("<Return>", lambda event: self.verify_pin())
        self.pin_entry.focus()

    def verify_pin(self):
        # Get the text from the entry and check if it matches the secret PIN
        entered_pin = self.pin_entry.get()
        if entered_pin == self.secret_pin:
            logging.info("Inicio de sesión correcto.")
            self.login_frame.destroy()  # Delete the login screen to open the main app
            self.setup_main_app()       # Load the buttons and the main window
            self.run_clock_loop()       # Start the automatic clock timer
        else:
            # If the PIN is wrong, turn the border red, clear the text, and log a warning
            logging.warning(f"Intento de acceso fallido con el PIN: {entered_pin}")
            self.pin_entry.configure(border_color="red")
            self.pin_entry.delete(0, 'end') 
           
    def setup_main_app(self):
        # Design and place all the buttons and text labels for the taxi meter
        ctk.CTkLabel(self, text="🌸 MAGIC TAXI 🌸", font=("Verdana", 20, "bold"), 
                     text_color="#FF69B4").pack(pady=(20, 5))

        self.display_frame = ctk.CTkFrame(self, corner_radius=25, fg_color="white", 
                                          border_width=2, border_color="#FFB6C1")
        self.display_frame.pack(pady=10, padx=30, fill="both")

        self.fare_display = ctk.CTkLabel(self.display_frame, text="€ 0.00", 
                                         font=("Courier New", 45, "bold"), text_color="#555555")
        self.fare_display.pack(pady=25)

        self.details_label = ctk.CTkLabel(self, text="Stop: €0.00 | Move: €0.00", 
                                          font=("Arial", 16), text_color="#FF69B4")
        self.details_label.pack(pady=2)

        self.status_label = ctk.CTkLabel(self, text="SYSTEM READY", font=("Arial", 11, "bold"), 
                                         text_color="white", fg_color="#ADD8E6", corner_radius=8)
        self.status_label.pack(pady=10)

        self.btn_start = ctk.CTkButton(self, text="START / RESUME", corner_radius=15, 
                                       fg_color="#B2F2BB", text_color="#1E5631", hover_color="#74B886", 
                                       command=self.start_trip)
        self.btn_start.pack(pady=6, padx=50, fill="x")

        self.btn_toggle = ctk.CTkButton(self, text="CHANGE GEAR", corner_radius=15, 
                                        fg_color="#FFD1DC", text_color="#8E244E", hover_color="#F0A1B5", 
                                        command=self.toggle_move)
        self.btn_toggle.pack(pady=6, padx=50, fill="x")

        self.btn_reset = ctk.CTkButton(self, text="RESET TRIP (ACCIDENT)", corner_radius=15, 
                                       fg_color="#FFE3A8", text_color="#7C5200", hover_color="#FFD075", 
                                       command=self.reset_trip)
        self.btn_reset.pack(pady=6, padx=50, fill="x")

        self.btn_stop_trip = ctk.CTkButton(self, text="FINISH (GENERATE BILL)", corner_radius=15, 
                                           fg_color="#D0EBFF", text_color="#0D47A1", hover_color="#90CAF9", 
                                           command=self.finish_trip_final)
        self.btn_stop_trip.pack(pady=6, padx=50, fill="x")
        
        self.btn_quit = ctk.CTkButton(self, text="QUIT ×", width=85, height=30, corner_radius=10,
                                      fg_color="#FFC3C3", text_color="#7A1E1E", hover_color="#FFA6A6",
                                      font=("Arial", 12, "bold"), command=self.exit_application)
        self.btn_quit.pack(side="bottom", anchor="e", pady=15, padx=20)
        
    def start_trip(self):
        # If it is a brand new trip, reset money to 0. If not, just resume it
        if not self.is_active:
            self.is_active = True
            self.total_fare = 0.0
            self.fare_stopped = 0.0
            self.fare_moving = 0.0
            logging.info(f"Viaje #{self.trip_id} iniciado.")
        else:
            logging.info(f"Viaje #{self.trip_id} reanudado.")
            
        self.is_running = True 
        self.is_moving = True 
        
        # Change the status label to MOVING and disable the start button to prevent double clicks
        self.status_label.configure(text="MOVING", fg_color="#51CF66")
        self.btn_start.configure(state="disabled", fg_color="#E0E0E0", text_color="#A0A0A0")

    def toggle_move(self):
        # Switch between driving and stopped every time the driver clicks this button
        if self.is_running:
            self.is_moving = not self.is_moving
            status = "MOVING" if self.is_moving else "CAR STOPPED"
            color = "#51CF66" if self.is_moving else "#FAB005"
            self.status_label.configure(text=status, fg_color=color)
            logging.info(f"Cambio de estado en Viaje #{self.trip_id}: El coche ahora está en {status}.")

    def reset_trip(self):
        # Cancel the trip and clear all the numbers without changing the trip ID
        logging.warning(f"Viaje #{self.trip_id} cancelado/reiniciado por el usuario.")
        
        self.is_active = False
        self.is_running = False
        self.is_moving = False
        
        self.total_fare = 0.0
        self.fare_stopped = 0.0
        self.fare_moving = 0.0
        
        # Reset the interface back to how it looked at the very beginning
        self.fare_display.configure(text="€ 0.00")
        self.details_label.configure(text="Stop: €0.00 | Move: €0.00")
        self.status_label.configure(text="SYSTEM READY", fg_color="#ADD8E6")
        self.btn_start.configure(state="normal", fg_color="#B2F2BB", text_color="#1E5631")
        print(f"Trip #{self.trip_id} was reset due to accidental activation.")

    def finish_trip_final(self):
        # Stop the trip, save the invoice file, and prepare the counter for the next client
        if self.is_active:
            logging.info(f"Viaje #{self.trip_id} completado con éxito. Importe total: €{self.total_fare:.2f}")
            self.is_active = False
            self.is_running = False
            self.status_label.configure(text="TRIP FINISHED", fg_color="#CED4DA")
            self.generate_invoice()       # Save the text file with the bill details
            self.trip_id += 1             # Add +1 to the trip number for the next passenger
            self.btn_start.configure(state="normal", fg_color="#B2F2BB", text_color="#1E5631")

    def generate_invoice(self):
        # Open a new text file inside the 'invoices' folder and write the final bill
        folder_name = "invoices"
        os.makedirs(folder_name, exist_ok=True)
        filename = os.path.join(folder_name, f"invoice_{self.trip_id:03d}.txt")
        
        # Using 'with open' ensures the file is closed correctly after writing data
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- MAGIC TAXI INVOICE #{self.trip_id:03d} ---\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total: €{self.total_fare:.2f}\n")
            f.write(f"Stopped Fare: €{self.fare_stopped:.2f}\n")
            f.write(f"Moving Fare: €{self.fare_moving:.2f}\n")
            f.write("--- Thank you! ---\n")
        print(f"Invoice {filename} generated inside '{folder_name}' folder.")

    def run_clock_loop(self):
        # This function runs automatically every 1 second to update the money counters
        if self.is_active and self.is_running:
            if self.is_moving:
                self.fare_moving += 0.05  # Add 5 cents if the taxi is driving
            else:
                self.fare_stopped += 0.02 # Add 2 cents if the taxi is stopped in traffic
            
            # Sum up both fares and show the text on the screen with only 2 decimals
            self.total_fare = self.fare_moving + self.fare_stopped
            self.fare_display.configure(text=f"€ {self.total_fare:.2f}")
            self.details_label.configure(text=f"Stop: €{self.fare_stopped:.2f} | Move: €{self.fare_moving:.2f}")
        
        # Tell the window to call this exact same function again in 1000 milliseconds (1 second)
        self.after(1000, self.run_clock_loop)

    def exit_application(self):
        # Save a closing message in the log file and close the application window
        logging.info("--- SISTEMA CERRADO POR EL USUARIO (QUIT) ---\n")
        self.destroy()

if __name__ == "__main__":
    app = MagicTaxiMeter()
    app.mainloop()