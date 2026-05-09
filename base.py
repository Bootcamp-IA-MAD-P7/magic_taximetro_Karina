import customtkinter as ctk
from datetime import datetime

# 1. THE CLASS (The "Container" of your app)
class MagicTaxiMeter(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        # --- DATA BOXES (Variables / Attributes) ---
        self.secret_pin = "1234"
        self.trip_id = 1
        self.is_active = False
        self.is_moving = False
        self.total_fare = 0.0
        self.fare_stopped = 0.0
        self.fare_moving = 0.0

        # --- WINDOW DESIGN ---
        self.title("✨ Magic Taxi Meter ✨")
        self.geometry("400x680")
        self.configure(fg_color="#FFF0F5") # Soft pink background

        # Start with Login
        self.show_login_ui()

    def show_login_ui(self):
        """Creates the security entrance"""
        self.login_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=30)
        self.login_frame.pack(pady=100, padx=50, fill="both", expand=True)

        ctk.CTkLabel(self.login_frame, text="🌸\nSECURE LOGIN", 
                     font=("Verdana", 20, "bold"), text_color="#FF69B4").pack(pady=(40, 20))
        
        self.pin_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="Enter PIN",
                                      fg_color="#FFF0F5", border_color="#FFB6C1")
        self.pin_entry.pack(pady=10, padx=30)

        self.unlock_btn = ctk.CTkButton(self.login_frame, text="UNLOCK MAGIC", 
                                        fg_color="#FFB6C1", text_color="white",
                                        hover_color="#FF69B4", command=self.verify_pin)
        self.unlock_btn.pack(pady=20, padx=30)

    def verify_pin(self):
        """Logic to check the password"""
        if self.pin_entry.get() == self.secret_pin:
            self.login_frame.destroy() # Remove login
            self.setup_main_app()      # Build the meter
            self.run_clock_loop()      # Start the engine
        else:
            self.pin_entry.configure(border_color="red")

    def setup_main_app(self):
        """The Aesthetic Meter Interface"""
        # Header
        ctk.CTkLabel(self, text="🌸 MAGIC TAXI 🌸", font=("Verdana", 24, "bold"), 
                     text_color="#FF69B4").pack(pady=(30, 10))

        # Main Display Frame
        self.display_frame = ctk.CTkFrame(self, corner_radius=30, fg_color="white", 
                                          border_width=2, border_color="#FFB6C1")
        self.display_frame.pack(pady=10, padx=40, fill="both")

        self.fare_display = ctk.CTkLabel(self.display_frame, text="€ 0.00", 
                                         font=("Courier New", 55, "bold"), text_color="#555555")
        self.fare_display.pack(pady=40)

        # Detailed Breakdown Labels (Small text)
        self.details_label = ctk.CTkLabel(self, text="Stop: €0.00 | Move: €0.00", 
                                          font=("Arial", 12), text_color="#FF69B4")
        self.details_label.pack(pady=5)

        # Status Badge
        self.status_label = ctk.CTkLabel(self, text="READY", font=("Arial", 12, "bold"), 
                                         text_color="white", fg_color="#ADD8E6", corner_radius=10)
        self.status_label.pack(pady=10)

        # Control Buttons
        self.btn_start = ctk.CTkButton(self, text="START TRIP", corner_radius=20, 
                                       fg_color="#B2F2BB", text_color="#2B8A3E", command=self.start)
        self.btn_start.pack(pady=10, padx=60, fill="x")

        self.btn_toggle = ctk.CTkButton(self, text="DRIVE / STOP", corner_radius=20, 
                                        fg_color="#FFD1DC", text_color="#D6336C", command=self.toggle)
        self.btn_toggle.pack(pady=10, padx=60, fill="x")

        self.btn_bill = ctk.CTkButton(self, text="GENERATE INVOICE", corner_radius=20, 
                                      fg_color="#D0EBFF", text_color="#1971C2", command=self.bill)
        self.btn_bill.pack(pady=10, padx=60, fill="x")

    def start(self):
        """Starts a new journey"""
        self.total_fare = 0.0
        self.fare_stopped = 0.0
        self.fare_moving = 0.0
        self.is_active = True
        self.is_moving = False
        self.status_label.configure(text="ACTIVE - STOPPED", fg_color="#FAB005")

    def toggle(self):
        """Switches between driving and standing still"""
        if self.is_active:
            self.is_moving = not self.is_moving
            if self.is_moving:
                self.status_label.configure(text="MOVING", fg_color="#51CF66")
            else:
                self.status_label.configure(text="STOPPED", fg_color="#FAB005")

    def bill(self):
        """Ends the trip and creates the file"""
        if self.is_active:
            self.is_active = False
            self.status_label.configure(text="FINISHED", fg_color="#CED4DA")
            self.create_invoice_file()
            self.trip_id += 1

    def create_invoice_file(self):
        """Saves a professional record"""
        filename = f"invoice_{self.trip_id:03d}.txt"
        with open(filename, "w") as f:
            f.write(f"--- MAGIC TAXI INVOICE #{self.trip_id:03d} ---\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"-----------------------------------\n")
            f.write(f"Stopped Fare:  € {self.fare_stopped:.2f}\n")
            f.write(f"Moving Fare:   € {self.fare_moving:.2f}\n")
            f.write(f"-----------------------------------\n")
            f.write(f"TOTAL PAID:    € {self.total_fare:.2f}\n")
            f.write(f"-----------------------------------\n")
        print(f"LOG: Invoice {filename} saved!")

    def run_clock_loop(self):
        """The automatic engine (Run every 1 second)"""
        if self.is_active:
            if self.is_moving:
                self.fare_moving += 0.05
            else:
                self.fare_stopped += 0.02
            
            self.total_fare = self.fare_moving + self.fare_stopped
            
            # Update the screen
            self.fare_display.configure(text=f"€ {self.total_fare:.2f}")
            self.details_label.configure(text=f"Stop: €{self.fare_stopped:.2f} | Move: €{self.fare_moving:.2f}")
        
        self.after(1000, self.run_clock_loop)

# 2. LAUNCH THE APP
if __name__ == "__main__":
    app = MagicTaxiMeter()
    app.mainloop()