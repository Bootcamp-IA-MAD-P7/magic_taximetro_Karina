import customtkinter as ctk
from datetime import datetime

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
        self.geometry("360x600") 
        self.configure(fg_color="#FFF0F5") # Lavender Blush

        self.show_login_ui()

    def show_login_ui(self):
        """Security Screen"""
        self.login_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=25)
        self.login_frame.pack(pady=60, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.login_frame, text="🌸\nLOGIN", 
                     font=("Verdana", 18, "bold"), text_color="#FF69B4").pack(pady=(30, 15))
        
        self.pin_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="PIN",
                                      fg_color="#FFF0F5", border_color="#FFB6C1", justify="center")
        self.pin_entry.pack(pady=10, padx=30)

        self.unlock_btn = ctk.CTkButton(self.login_frame, text="UNLOCK", 
                                        fg_color="#FFB6C1", text_color="white",
                                        hover_color="#FF69B4", command=self.verify_pin)
        self.unlock_btn.pack(pady=20, padx=30)

    def verify_pin(self):
        """PIN Verification logic"""
        if self.pin_entry.get() == self.secret_pin:
            self.login_frame.destroy()
            self.setup_main_app()
            self.run_clock_loop()
        else:
            self.pin_entry.configure(border_color="red")
           
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

        self.details_label = ctk.CTkLabel(self, text="Stopped: €0.00 | Moving: €0.00", 
                                          font=("Arial", 20), text_color="#FF69B4")
        self.details_label.pack(pady=2)

        # Status Badge
        self.status_label = ctk.CTkLabel(self, text="SYSTEM READY", font=("Arial", 11, "bold"), 
                                         text_color="white", fg_color="#ADD8E6", corner_radius=8)
        self.status_label.pack(pady=10)

# --- CONTROL BUTTONS (High Contrast Edition) ---
        
        # START: Green tones
        # Normal: Light Green background, Dark Green text
        # Hover: Dark Green background (the text will still be visible)
        self.btn_start = ctk.CTkButton(self, text="START / RESUME", corner_radius=15, 
                                       fg_color="#B2F2BB", 
                                       text_color="#1E5631", # Darker green for better contrast
                                       hover_color="#74B886", # Medium green so dark text is still visible
                                       command=self.start_trip)
        self.btn_start.pack(pady=8, padx=50, fill="x")

        # DRIVE/STOP: Pink/Red tones
        self.btn_toggle = ctk.CTkButton(self, text="CHANGE GEAR", corner_radius=15, 
                                        fg_color="#FFD1DC", 
                                        text_color="#8E244E", # Deep wine color
                                        hover_color="#F0A1B5", # Medium pink
                                        command=self.toggle_move)
        self.btn_toggle.pack(pady=8, padx=50, fill="x")

        # FINISH TRIP: Blue tones
        self.btn_stop_trip = ctk.CTkButton(self, text="FINISH (GENERATE BILL)", corner_radius=15, 
                                           fg_color="#D0EBFF", 
                                           text_color="#0D47A1", # Deep Navy blue
                                           hover_color="#90CAF9", # Sky blue
                                           command=self.finish_trip_final)
        self.btn_stop_trip.pack(pady=8, padx=50, fill="x")
        
    def start_trip(self):
        if not self.is_active:
            self.is_active = True
            self.total_fare = 0.0
            self.fare_stopped = 0.0
            self.fare_moving = 0.0
            
        self.is_running = True 
        self.status_label.configure(text="TRIP IN PROGRESS", fg_color="#51CF66")

    def toggle_move(self):
        if self.is_running:
            self.is_moving = not self.is_moving
            status = "MOVING" if self.is_moving else "CAR STOPPED"
            color = "#51CF66" if self.is_moving else "#FAB005"
            self.status_label.configure(text=status, fg_color=color)

    def finish_trip_final(self):
        if self.is_active:
            self.is_active = False
            self.is_running = False
            self.status_label.configure(text="TRIP FINISHED", fg_color="#CED4DA")
            self.generate_invoice()
            self.trip_id += 1

    def generate_invoice(self):
        filename = f"invoice_{self.trip_id:03d}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- MAGIC TAXI INVOICE #{self.trip_id:03d} ---\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total: €{self.total_fare:.2f}\n")
            f.write(f"Stopped Fare: €{self.fare_stopped:.2f}\n")
            f.write(f"Moving Fare: €{self.fare_moving:.2f}\n")
            f.write("--- Thank you! ---\n")
        print(f"Invoice {filename} generated.")

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