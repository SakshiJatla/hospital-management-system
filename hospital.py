import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta

# =========DATA STORAGE ===========
patients = []
doctors = []
appointments = []
medicines = []
orders = []
prescriptions = []
cart = []
beds = {"total": 100, "occupied": 0}
admin_cred = {"username": "admin", "password": "admin123"}
pharmacy_cred = {"username": "pharmacy", "password": "pharma123"}
current_user = None
time_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "02:00 PM", "03:00 PM", "04:00 PM"]

# ===================== HELPER FUNCTIONS =====================
def get_dates(days=30):
    return [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_footer(parent):
    footer = tk.Frame(parent, bg="#2c3e50", height=60)
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    tk.Label(footer, text="About Us | Contact: info@aura-medixora.com | © 2026 AURA MEDIXORA CARE CENTER", 
             bg="#2c3e50", fg="white", font=("Arial", 9)).pack(pady=15)

def create_header(parent, title):
    header = tk.Frame(parent, bg="#3498db", height=80)
    header.pack(side=tk.TOP, fill=tk.X)
    tk.Label(header, text=title, bg="#3498db", fg="white", 
             font=("Arial", 24, "bold")).pack(pady=20)

# ============ MAIN APPLICATION CLASS ==============
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AURA MEDIXORA CARE CENTER")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ecf0f1")
        self.main_frame = tk.Frame(root, bg="#ecf0f1")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_home()

    def show_home(self):
        global current_user
        current_user = None
        clear_frame(self.main_frame)
        create_header(self.main_frame, "AURA MEDIXORA CARE CENTER")
        
        center = tk.Frame(self.main_frame, bg="#ecf0f1")
        center.pack(expand=True)
        
        tk.Label(center, text="WELCOME TO AURA MEDIXORA CARE CENTER", bg="#ecf0f1", 
                fg="#2c3e50", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=20)
        
        buttons = [
            ("👤 Patient Portal", self.show_patient_options, "#3498db"),
            ("👨‍⚕️ Doctor Portal", self.show_doctor_login, "#9b59b6"),
            ("⚙️ Admin Portal", self.show_admin_login, "#27ae60"),
            ("💊 MediMart", self.show_pharmacy_login, "#e74c3c")
        ]
        
        for i, (text, cmd, color) in enumerate(buttons):
            btn = tk.Button(center, text=text, command=cmd, bg=color, fg="white",
                          font=("Arial", 14, "bold"), width=20, height=3, cursor="hand2")
            btn.grid(row=1+i//2, column=i%2, padx=15, pady=15)
        
        create_footer(self.main_frame)

    # ========= PATIENT PORTAL =========
    def show_patient_options(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Patient Portal")
        
        center = tk.Frame(self.main_frame, bg="#ecf0f1")
        center.pack(expand=True)
        
        tk.Button(center, text="Register New Account", command=self.show_patient_register,
                 bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25, height=2).pack(pady=10)
        tk.Button(center, text="Already have an account? Login", command=self.show_patient_login,
                 bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), width=25, height=2).pack(pady=10)
        tk.Button(center, text="← Back to Home", command=self.show_home,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_patient_register(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Patient Registration")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        fields = ["Name", "Age", "Email", "Mobile", "Password"]
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(center, text=field, bg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="w", pady=8)
            entry = tk.Entry(center, font=("Arial", 11), width=30, show="*" if field=="Password" else "")
            entry.grid(row=i, column=1, pady=8, padx=10)
            entries[field.lower()] = entry
        
        tk.Label(center, text="Gender", bg="white", font=("Arial", 11)).grid(row=len(fields), column=0, sticky="w", pady=8)
        gender_var = tk.StringVar(value="Male")
        ttk.Combobox(center, textvariable=gender_var, values=["Male", "Female", "Other"], 
                    font=("Arial", 11), width=28, state="readonly").grid(row=len(fields), column=1, pady=8)
        
        def register():
            import re
            data = {k: v.get() for k, v in entries.items()}
            data["gender"] = gender_var.get()
            
            # Validation
            if not all(data.values()):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            # Name validation (only letters and spaces)
            if not re.match(r"^[A-Za-z\s]+$", data["name"]):
                messagebox.showerror("Error", "Name should contain only letters")
                return
            
            # Email validation
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", data["email"]):
                messagebox.showerror("Error", "Invalid email format (e.g., user@example.com)")
                return
            
            # Mobile validation (10 digits)
            if not re.match(r"^[6-9]\d{9}$", data["mobile"]):
                messagebox.showerror("Error", "Invalid mobile number (must be 10 digits starting with 6-9)")
                return
            
            # Password validation (min 6 characters)
            if len(data["password"]) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long")
                return
            
            # Age validation
            try:
                age = int(data["age"])
                if age < 1 or age > 120:
                    messagebox.showerror("Error", "Age must be between 1 and 120")
                    return
            except:
                messagebox.showerror("Error", "Age must be a valid number")
                return
            
            # Check if email already exists
            if any(p["email"] == data["email"] for p in patients):
                messagebox.showerror("Error", "Email already registered")
                return
            
            data["id"] = f"P{len(patients)+1:03d}"
            patients.append(data)
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_patient_login()
        
        tk.Button(center, text="Register", command=register, bg="#3498db", fg="white",
                 font=("Arial", 12, "bold"), width=20, height=2).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_patient_options,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=len(fields)+2, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_patient_login(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Patient Login")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        tk.Label(center, text="Email", bg="white", font=("Arial", 11)).grid(row=0, column=0, pady=10)
        email_entry = tk.Entry(center, font=("Arial", 11), width=30)
        email_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(center, text="Password", bg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10)
        pass_entry = tk.Entry(center, font=("Arial", 11), width=30, show="*")
        pass_entry.grid(row=1, column=1, pady=10)
        
        def login():
            global current_user
            patient = next((p for p in patients if p["email"]==email_entry.get() and p["password"]==pass_entry.get()), None)
            if patient:
                current_user = patient
                self.show_patient_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        
        tk.Button(center, text="Login", command=login, bg="#3498db", fg="white",
                 font=("Arial", 12, "bold"), width=20, height=2).grid(row=2, column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_patient_options,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=3, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_patient_dashboard(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, f"Patient Dashboard - {current_user['name']}")
        
        center = tk.Frame(self.main_frame, bg="#ecf0f1")
        center.pack(expand=True, pady=30)
        
        buttons = [
            ("📋 My Profile", self.show_patient_profile),
            ("📅 Book Appointment", self.show_book_appointment),
            ("📝 View Appointments", self.show_view_appointments),
            ("💊 Medical Store", self.show_medical_store),
            ("🚪 Logout", self.show_home)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(center, text=text, command=cmd, bg="#3498db", fg="white",
                     font=("Arial", 12, "bold"), width=20, height=2).grid(row=i//2, column=i%2, padx=15, pady=15)
        
        create_footer(self.main_frame)

    def show_patient_profile(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "My Profile")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        info = f"""
        Patient ID: {current_user['id']}
        Name: {current_user['name']}
        Age: {current_user['age']}
        Gender: {current_user['gender']}
        Email: {current_user['email']}
        Mobile: {current_user['mobile']}
        """
        
        tk.Label(center, text=info, bg="white", font=("Arial", 12), justify="left").pack()
        tk.Button(center, text="← Back", command=self.show_patient_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=20)
        
        create_footer(self.main_frame)

    def show_book_appointment(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Book Appointment")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        if not doctors:
            tk.Label(center, text="No doctors available. Please contact admin.", bg="white", 
                    font=("Arial", 12), fg="red").pack(pady=20)
            tk.Button(center, text="← Back", command=self.show_patient_dashboard,
                     bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
            create_footer(self.main_frame)
            return
        
        tk.Label(center, text="Select Doctor", bg="white", font=("Arial", 11)).grid(row=0, column=0, pady=10, sticky="w")
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(center, textvariable=doctor_var, font=("Arial", 11), width=28, state="readonly")
        doctor_combo["values"] = [f"{d['name']} - {d['specialty']}" for d in doctors if d["available"]]
        doctor_combo.grid(row=0, column=1, pady=10)
        
        tk.Label(center, text="Select Date", bg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10, sticky="w")
        date_var = tk.StringVar()
        ttk.Combobox(center, textvariable=date_var, values=get_dates(), font=("Arial", 11), width=28, state="readonly").grid(row=1, column=1, pady=10)
        
        tk.Label(center, text="Select Time", bg="white", font=("Arial", 11)).grid(row=2, column=0, pady=10, sticky="w")
        time_var = tk.StringVar()
        ttk.Combobox(center, textvariable=time_var, values=time_slots, font=("Arial", 11), width=28, state="readonly").grid(row=2, column=1, pady=10)
        
        def confirm():
            if doctor_var.get() and date_var.get() and time_var.get():
                doc_name = doctor_var.get().split(" - ")[0]
                doc = next(d for d in doctors if d["name"]==doc_name)
                apt = {
                    "id": f"A{len(appointments)+1:03d}",
                    "patient_id": current_user["id"],
                    "patient_name": current_user["name"],
                    "doctor_id": doc["id"],
                    "doctor_name": doc["name"],
                    "specialty": doc["specialty"],
                    "date": date_var.get(),
                    "time": time_var.get(),
                    "status": "Pending"
                }
                appointments.append(apt)
                messagebox.showinfo("Success", "Appointment booked successfully!")
                self.show_patient_dashboard()
            else:
                messagebox.showerror("Error", "Please fill all fields")
        
        tk.Button(center, text="Confirm Appointment", command=confirm, bg="#27ae60", fg="white",
                 font=("Arial", 12, "bold"), width=20, height=2).grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_patient_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=4, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_view_appointments(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "My Appointments")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        my_apts = [a for a in appointments if a["patient_id"]==current_user["id"]]
        
        if not my_apts:
            tk.Label(scrollable, text="No appointments found", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for apt in my_apts:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            info = f"Dr. {apt['doctor_name']} ({apt['specialty']})\n{apt['date']} at {apt['time']}\nStatus: {apt['status']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 11), justify="left").pack(side=tk.LEFT, padx=15, pady=10)
            
            color = "#27ae60" if apt["status"]=="Confirmed" else "#e74c3c" if apt["status"]=="Rejected" else "#f39c12"
            tk.Label(frame, text=apt["status"], bg=color, fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(side=tk.RIGHT, padx=15)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_patient_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_medical_store(self):
        global cart
        clear_frame(self.main_frame)
        create_header(self.main_frame, "💊 Medical Store")
        
        if not medicines:
            center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
            center.pack(expand=True)
            tk.Label(center, text="No medicines available. Please contact pharmacy.", bg="white", 
                    font=("Arial", 12), fg="red").pack(pady=20)
            tk.Button(center, text="← Back", command=self.show_patient_dashboard,
                     bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
            create_footer(self.main_frame)
            return
        
        # Cart display
        cart_frame = tk.Frame(self.main_frame, bg="#d5f4e6", padx=10, pady=10)
        cart_frame.pack(fill=tk.X)
        
        cart_label = tk.Label(cart_frame, text=f"🛒 Cart: {len(cart)} items", bg="#d5f4e6", font=("Arial", 11, "bold"))
        cart_label.pack(side=tk.LEFT)
        
        def checkout():
            if cart:
                total = sum(item["price"]*item["qty"] for item in cart)
                order = {"id": f"O{len(orders)+1:03d}", "patient_id": current_user["id"], 
                        "items": cart.copy(), "total": total, "date": datetime.now().strftime("%Y-%m-%d"), "status": "Pending"}
                orders.append(order)
                cart.clear()
                messagebox.showinfo("Success", f"Order placed! Total: ₹{total}")
                self.show_patient_dashboard()
            else:
                messagebox.showwarning("Empty Cart", "Your cart is empty")
        
        tk.Button(cart_frame, text="Checkout", command=checkout, bg="#27ae60", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
        
        # Medicine list
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for med in medicines:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(frame, text=med["name"], bg="white", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=2)
            tk.Label(frame, text=f"Use: {med['use']} | Price: ₹{med['price']} | Stock: {med['stock']}", 
                    bg="white", font=("Arial", 9)).pack(anchor="w", padx=10, pady=2)
            
            def add_to_cart(m=med):
                if m["stock"] > 0:
                    existing = next((item for item in cart if item["id"]==m["id"]), None)
                    if existing:
                        existing["qty"] += 1
                    else:
                        cart.append({**m, "qty": 1})
                    messagebox.showinfo("Added", f"{m['name']} added to cart")
                    self.show_medical_store()
                else:
                    messagebox.showerror("Out of Stock", f"{m['name']} is out of stock")
            
            tk.Button(frame, text="+ Add to Cart", command=add_to_cart, bg="#3498db", fg="white",
                     font=("Arial", 9)).pack(side=tk.RIGHT, padx=10, pady=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_patient_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    # ========== DOCTOR PORTAL ==========
    def show_doctor_login(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Doctor Login")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        tk.Label(center, text="Doctor ID", bg="white", font=("Arial", 11)).grid(row=0, column=0, pady=10)
        id_entry = tk.Entry(center, font=("Arial", 11), width=30)
        id_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(center, text="Password", bg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10)
        pass_entry = tk.Entry(center, font=("Arial", 11), width=30, show="*")
        pass_entry.grid(row=1, column=1, pady=10)
        
        def login():
            global current_user
            doc = next((d for d in doctors if d["id"]==id_entry.get() and d["password"]==pass_entry.get()), None)
            if doc:
                current_user = doc
                self.show_doctor_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        
        tk.Button(center, text="Login", command=login, bg="#9b59b6", fg="white",
                 font=("Arial", 12, "bold"), width=20, height=2).grid(row=2, column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_home,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=3, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_doctor_dashboard(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, f"Dr. Dashboard - {current_user['name']}")
        
        center = tk.Frame(self.main_frame, bg="#ecf0f1")
        center.pack(expand=True, pady=30)
        
        buttons = [
            ("📅 View Appointments", self.show_doctor_appointments),
            ("📝 Write Prescription", self.show_write_prescription),
            ("📊 Appointment History", self.show_appointment_history),
            ("🚪 Logout", self.show_home)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(center, text=text, command=cmd, bg="#9b59b6", fg="white",
                     font=("Arial", 12, "bold"), width=22, height=2).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_doctor_appointments(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Appointments")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        my_apts = [a for a in appointments if a["doctor_id"]==current_user["id"]]
        
        if not my_apts:
            tk.Label(scrollable, text="No appointments found", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for apt in my_apts:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            info = f"Patient: {apt['patient_name']} (ID: {apt['patient_id']})\n{apt['date']} at {apt['time']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 11), justify="left").pack(side=tk.LEFT, padx=15, pady=10)
            
            def confirm(a=apt):
                a["status"] = "Confirmed"
                messagebox.showinfo("Done", "Appointment confirmed")
                self.show_doctor_appointments()
            
            def reject(a=apt):
                a["status"] = "Rejected"
                messagebox.showinfo("Done", "Appointment rejected")
                self.show_doctor_appointments()
            
            if apt["status"] == "Pending":
                tk.Button(frame, text="✓ Confirm", command=confirm, bg="#27ae60", fg="white",
                         font=("Arial", 9)).pack(side=tk.RIGHT, padx=5, pady=5)
                tk.Button(frame, text="✗ Reject", command=reject, bg="#e74c3c", fg="white",
                         font=("Arial", 9)).pack(side=tk.RIGHT, padx=5, pady=5)
            else:
                tk.Label(frame, text=apt["status"], bg="white", fg="#7f8c8d", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=15)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_doctor_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_write_prescription(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Write Prescription")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True, fill=tk.BOTH)
        
        my_apts = [a for a in appointments if a["doctor_id"]==current_user["id"] and a["status"]=="Confirmed"]
        
        if not my_apts:
            tk.Label(center, text="No confirmed appointments to write prescriptions.", bg="white", 
                    font=("Arial", 12), fg="red").pack(pady=20)
            tk.Button(center, text="← Back", command=self.show_doctor_dashboard,
                     bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
            create_footer(self.main_frame)
            return
        
        if not medicines:
            tk.Label(center, text="No medicines available in database.", bg="white", 
                    font=("Arial", 12), fg="red").pack(pady=20)
            tk.Button(center, text="← Back", command=self.show_doctor_dashboard,
                     bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
            create_footer(self.main_frame)
            return
        
        tk.Label(center, text="Select Appointment", bg="white", font=("Arial", 11)).pack(pady=10)
        apt_var = tk.StringVar()
        apt_combo = ttk.Combobox(center, textvariable=apt_var, font=("Arial", 10), width=50, state="readonly")
        apt_combo["values"] = [f"{a['patient_name']} - {a['date']} {a['time']}" for a in my_apts]
        apt_combo.pack(pady=10)
        
        tk.Label(center, text="Select Medicines (Ctrl+Click for multiple)", bg="white", font=("Arial", 11)).pack(pady=10)
        med_listbox = tk.Listbox(center, selectmode=tk.MULTIPLE, font=("Arial", 10), height=8, width=60)
        for med in medicines:
            med_listbox.insert(tk.END, f"{med['name']} - {med['use']}")
        med_listbox.pack(pady=10)
        
        def save():
            if apt_var.get() and med_listbox.curselection():
                apt_idx = apt_combo.current()
                selected_apt = my_apts[apt_idx]
                selected_meds = [medicines[i]["name"] for i in med_listbox.curselection()]
                
                prescription = {
                    "id": f"PR{len(prescriptions)+1:03d}",
                    "appointment_id": selected_apt["id"],
                    "patient_id": selected_apt["patient_id"],
                    "doctor_id": current_user["id"],
                    "medicines": selected_meds,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
                prescriptions.append(prescription)
                messagebox.showinfo("Success", "Prescription saved!")
                self.show_doctor_dashboard()
            else:
                messagebox.showerror("Error", "Please select appointment and medicines")
        
        tk.Button(center, text="Save Prescription", command=save, bg="#27ae60", fg="white",
                 font=("Arial", 11, "bold"), width=20).pack(pady=20)
        tk.Button(center, text="← Back", command=self.show_doctor_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack()
        
        create_footer(self.main_frame)

    def show_appointment_history(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Appointment History")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        my_apts = [a for a in appointments if a["doctor_id"]==current_user["id"]]
        
        if not my_apts:
            tk.Label(scrollable, text="No appointment history", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for apt in my_apts:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            info = f"Patient: {apt['patient_name']} | {apt['date']} at {apt['time']} | Status: {apt['status']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 11)).pack(padx=15, pady=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_doctor_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    # ============ ADMIN PORTAL =============
    def show_admin_login(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Admin Login")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        tk.Label(center, text="Username", bg="white", font=("Arial", 11)).grid(row=0, column=0, pady=10)
        user_entry = tk.Entry(center, font=("Arial", 11), width=30)
        user_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(center, text="Password", bg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10)
        pass_entry = tk.Entry(center, font=("Arial", 11), width=30, show="*")
        pass_entry.grid(row=1, column=1, pady=10)
        
        def login():
            if user_entry.get()==admin_cred["username"] and pass_entry.get()==admin_cred["password"]:
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        
        tk.Button(center, text="Login", command=login, bg="#27ae60", fg="white",
                 font=("Arial", 12, "bold"), width=20, height=2).grid(row=2, column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_home,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=3, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_admin_dashboard(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Admin Dashboard")
        
        center = tk.Frame(self.main_frame, bg="#ecf0f1")
        center.pack(expand=True, pady=20)
        
        buttons = [
            ("👨‍⚕️ Manage Doctors", self.show_manage_doctors),
            ("👥 View All Patients", self.show_all_patients),
            ("📅 Manage Appointments", self.show_manage_appointments),
            ("🛏️ Bed Management", self.show_bed_management),
            ("💊 Stock Overview", self.show_stock_overview),
            ("🚪 Logout", self.show_home)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(center, text=text, command=cmd, bg="#27ae60", fg="white",
                     font=("Arial", 12, "bold"), width=22, height=2).grid(row=i//2, column=i%2, padx=15, pady=10)
        
        create_footer(self.main_frame)

    def show_manage_doctors(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Manage Doctors")
        
        # Add Doctor Section
        add_frame = tk.Frame(self.main_frame, bg="white", padx=20, pady=20)
        add_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(add_frame, text="Add New Doctor", bg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        
        tk.Label(add_frame, text="Name:", bg="white", font=("Arial", 10)).grid(row=1, column=0, padx=5)
        name_entry = tk.Entry(add_frame, font=("Arial", 10), width=20)
        name_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(add_frame, text="Specialty:", bg="white", font=("Arial", 10)).grid(row=1, column=2, padx=5)
        spec_entry = tk.Entry(add_frame, font=("Arial", 10), width=20)
        spec_entry.grid(row=1, column=3, padx=5)
        
        def add_doctor():
            if name_entry.get() and spec_entry.get():
                new_doc = {
                    "id": f"D{len(doctors)+1:03d}",
                    "name": name_entry.get(),
                    "specialty": spec_entry.get(),
                    "password": "doc123",
                    "available": True
                }
                doctors.append(new_doc)
                messagebox.showinfo("Success", f"Doctor added! ID: {new_doc['id']}, Password: doc123")
                self.show_manage_doctors()
            else:
                messagebox.showerror("Error", "Please fill all fields")
        
        tk.Button(add_frame, text="Add Doctor", command=add_doctor, bg="#27ae60", fg="white",
                 font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Doctor List
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(scrollable, text="Existing Doctors", bg="#ecf0f1", font=("Arial", 12, "bold")).pack(pady=10)
        
        if not doctors:
            tk.Label(scrollable, text="No doctors in system", bg="#ecf0f1", 
                    font=("Arial", 11), fg="gray").pack(pady=10)
        
        for doc in doctors:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=8)
            
            info = f"{doc['name']} ({doc['id']}) - {doc['specialty']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=15, pady=8)
            
            status_text = "Available" if doc["available"] else "Busy"
            status_color = "#27ae60" if doc["available"] else "#e74c3c"
            tk.Label(frame, text=status_text, bg=status_color, fg="white", font=("Arial", 9, "bold"), 
                    padx=8, pady=3).pack(side=tk.RIGHT, padx=5)
            
            def toggle(d=doc):
                d["available"] = not d["available"]
                self.show_manage_doctors()
            
            tk.Button(frame, text="Toggle", command=toggle, bg="#3498db", fg="white",
                     font=("Arial", 8)).pack(side=tk.RIGHT, padx=5)
            
            def remove(d=doc):
                if messagebox.askyesno("Confirm", f"Remove {d['name']}?"):
                    doctors.remove(d)
                    self.show_manage_doctors()
            
            tk.Button(frame, text="Remove", command=remove, bg="#e74c3c", fg="white",
                     font=("Arial", 8)).pack(side=tk.RIGHT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_admin_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_all_patients(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "All Patients")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not patients:
            tk.Label(scrollable, text="No patients registered", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for patient in patients:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            info = f"ID: {patient['id']} | Name: {patient['name']} | Age: {patient['age']} | Gender: {patient['gender']}\nEmail: {patient['email']} | Mobile: {patient['mobile']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10), justify="left").pack(side=tk.LEFT, padx=15, pady=10)
            
            def edit(p=patient):
                self.show_edit_patient(p)
            
            tk.Button(frame, text="Edit", command=edit, bg="#3498db", fg="white",
                     font=("Arial", 9)).pack(side=tk.RIGHT, padx=10, pady=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_admin_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_edit_patient(self, patient):
        clear_frame(self.main_frame)
        create_header(self.main_frame, f"Edit Patient - {patient['name']}")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        fields = ["email", "mobile", "password"]
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(center, text=field.capitalize(), bg="white", font=("Arial", 11)).grid(row=i, column=0, pady=10, sticky="w")
            entry = tk.Entry(center, font=("Arial", 11), width=30)
            entry.insert(0, patient[field])
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[field] = entry
        
        def save():
            for field, entry in entries.items():
                patient[field] = entry.get()
            messagebox.showinfo("Success", "Patient details updated!")
            self.show_all_patients()
        
        tk.Button(center, text="Save Changes", command=save, bg="#27ae60", fg="white",
                 font=("Arial", 11, "bold"), width=20).grid(row=len(fields), column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_all_patients,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=len(fields)+1, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_manage_appointments(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Manage Appointments")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not appointments:
            tk.Label(scrollable, text="No appointments in system", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for apt in appointments:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            info = f"ID: {apt['id']} | Patient: {apt['patient_name']} | Doctor: {apt['doctor_name']}\n{apt['date']} at {apt['time']} | Status: {apt['status']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10), justify="left").pack(side=tk.LEFT, padx=15, pady=10)
            
            def confirm(a=apt):
                a["status"] = "Confirmed"
                messagebox.showinfo("Done", "Appointment confirmed")
                self.show_manage_appointments()
            
            def reject(a=apt):
                a["status"] = "Rejected"
                messagebox.showinfo("Done", "Appointment rejected")
                self.show_manage_appointments()
            
            if apt["status"] == "Pending":
                tk.Button(frame, text="Confirm", command=confirm, bg="#27ae60", fg="white",
                         font=("Arial", 9)).pack(side=tk.RIGHT, padx=5, pady=5)
                tk.Button(frame, text="Reject", command=reject, bg="#e74c3c", fg="white",
                         font=("Arial", 9)).pack(side=tk.RIGHT, padx=5, pady=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_admin_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_bed_management(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Bed Management")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=40)
        center.pack(expand=True)
        
        tk.Label(center, text=f"🛏️ Total Beds: {beds['total']}", bg="white", 
                font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(center, text=f"❌ Occupied: {beds['occupied']}", bg="white", 
                font=("Arial", 12), fg="#e74c3c").pack(pady=10)
        tk.Label(center, text=f"✅ Available: {beds['total']-beds['occupied']}", bg="white", 
                font=("Arial", 12), fg="#27ae60").pack(pady=10)
        
        tk.Label(center, text="Update Occupied Beds:", bg="white", font=("Arial", 11)).pack(pady=20)
        bed_entry = tk.Entry(center, font=("Arial", 11), width=15)
        bed_entry.insert(0, str(beds["occupied"]))
        bed_entry.pack(pady=10)
        
        def update_beds():
            try:
                occupied = int(bed_entry.get())
                if 0 <= occupied <= beds["total"]:
                    beds["occupied"] = occupied
                    messagebox.showinfo("Success", "Bed count updated!")
                    self.show_bed_management()
                else:
                    messagebox.showerror("Error", f"Number must be between 0 and {beds['total']}")
            except:
                messagebox.showerror("Error", "Enter valid number")
        
        tk.Button(center, text="Update", command=update_beds, bg="#27ae60", fg="white",
                 font=("Arial", 11, "bold"), width=15).pack(pady=10)
        tk.Button(center, text="← Back", command=self.show_admin_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=20)
        
        create_footer(self.main_frame)

    def show_stock_overview(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Medicine Stock Overview")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not medicines:
            tk.Label(scrollable, text="No medicines in stock", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for med in medicines:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=8)
            
            info = f"{med['name']} | Use: {med['use']} | Price: ₹{med['price']} | Stock: {med['stock']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=15, pady=8)
            
            stock_color = "#27ae60" if med["stock"] > 100 else "#f39c12" if med["stock"] > 50 else "#e74c3c"
            tk.Label(frame, text=f"Stock: {med['stock']}", bg=stock_color, fg="white", 
                    font=("Arial", 9, "bold"), padx=8, pady=3).pack(side=tk.RIGHT, padx=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_admin_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    # ============= PHARMACY PORTAL ==============
    def show_pharmacy_login(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "💊 MediMart Login")
        
        center = tk.Frame(self.main_frame, bg="white", padx=40, pady=30)
        center.pack(expand=True)
        
        tk.Label(center, text="Username", bg="white", font=("Arial", 11)).grid(row=0, column=0, pady=10)
        user_entry = tk.Entry(center, font=("Arial", 11), width=30)
        user_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(center, text="Password", bg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10)
        pass_entry = tk.Entry(center, font=("Arial", 11), width=30, show="*")
        pass_entry.grid(row=1, column=1, pady=10)
        
        def login():
            if user_entry.get()==pharmacy_cred["username"] and pass_entry.get()==pharmacy_cred["password"]:
                self.show_pharmacy_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        
        tk.Button(center, text="Login", command=login, bg="#e74c3c", fg="white",
                 font=("Arial", 12, "bold"), width=20, height=2).grid(row=2, column=0, columnspan=2, pady=20)
        tk.Button(center, text="← Back", command=self.show_home,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).grid(row=3, column=0, columnspan=2)
        
        create_footer(self.main_frame)

    def show_pharmacy_dashboard(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "💊 MediMart Dashboard")
        
        center = tk.Frame(self.main_frame, bg="#ecf0f1")
        center.pack(expand=True, pady=30)
        
        buttons = [
            ("📦 View Orders", self.show_pharmacy_orders),
            ("💊 Manage Medicines", self.show_manage_medicines),
            ("📊 Stock Management", self.show_pharmacy_stock),
            ("🚪 Logout", self.show_home)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(center, text=text, command=cmd, bg="#e74c3c", fg="white",
                     font=("Arial", 12, "bold"), width=22, height=2).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_pharmacy_orders(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Patient Orders")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not orders:
            tk.Label(scrollable, text="No orders received yet", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for order in orders:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            items_str = ", ".join([f"{item['name']} x{item['qty']}" for item in order['items']])
            info = f"Order ID: {order['id']} | Patient: {order['patient_id']}\nDate: {order['date']} | Total: ₹{order['total']}\nItems: {items_str}\nStatus: {order['status']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10), justify="left").pack(padx=15, pady=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_pharmacy_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_manage_medicines(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Manage Medicines")
        
        # Add Medicine Section
        add_frame = tk.Frame(self.main_frame, bg="white", padx=20, pady=15)
        add_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(add_frame, text="Add New Medicine", bg="white", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=6, pady=8)
        
        tk.Label(add_frame, text="Name:", bg="white", font=("Arial", 9)).grid(row=1, column=0)
        name_entry = tk.Entry(add_frame, font=("Arial", 9), width=15)
        name_entry.grid(row=1, column=1, padx=3)
        
        tk.Label(add_frame, text="Use:", bg="white", font=("Arial", 9)).grid(row=1, column=2)
        use_entry = tk.Entry(add_frame, font=("Arial", 9), width=15)
        use_entry.grid(row=1, column=3, padx=3)
        
        tk.Label(add_frame, text="Price:", bg="white", font=("Arial", 9)).grid(row=1, column=4)
        price_entry = tk.Entry(add_frame, font=("Arial", 9), width=10)
        price_entry.grid(row=1, column=5, padx=3)
        
        def add_medicine():
            if name_entry.get() and use_entry.get() and price_entry.get():
                try:
                    new_med = {
                        "id": f"M{len(medicines)+1:03d}",
                        "name": name_entry.get(),
                        "use": use_entry.get(),
                        "price": int(price_entry.get()),
                        "stock": 0
                    }
                    medicines.append(new_med)
                    messagebox.showinfo("Success", "Medicine added!")
                    self.show_manage_medicines()
                except:
                    messagebox.showerror("Error", "Invalid price")
            else:
                messagebox.showerror("Error", "Fill all fields")
        
        tk.Button(add_frame, text="Add Medicine", command=add_medicine, bg="#27ae60", fg="white",
                 font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=6, pady=8)
        
        # Medicine List
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not medicines:
            tk.Label(scrollable, text="No medicines in database", bg="#ecf0f1", 
                    font=("Arial", 11), fg="gray").pack(pady=10)
        
        for med in medicines:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=8)
            
            info = f"{med['name']} | {med['use']} | ₹{med['price']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=15, pady=8)
            
            def remove(m=med):
                if messagebox.askyesno("Confirm", f"Remove {m['name']}?"):
                    medicines.remove(m)
                    self.show_manage_medicines()
            
            tk.Button(frame, text="Remove", command=remove, bg="#e74c3c", fg="white",
                     font=("Arial", 8)).pack(side=tk.RIGHT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_pharmacy_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)

    def show_pharmacy_stock(self):
        clear_frame(self.main_frame)
        create_header(self.main_frame, "Stock Management")
        
        canvas = tk.Canvas(self.main_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not medicines:
            tk.Label(scrollable, text="No medicines in database", bg="#ecf0f1", 
                    font=("Arial", 12)).pack(pady=20)
        
        for med in medicines:
            frame = tk.Frame(scrollable, bg="white", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, padx=20, pady=8)
            
            info = f"{med['name']} | Current Stock: {med['stock']}"
            tk.Label(frame, text=info, bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=15, pady=8)
            
            def update_stock(m=med):
                new_stock = simpledialog.askinteger("Update Stock", f"Enter new stock for {m['name']}:", 
                                                   initialvalue=m['stock'], minvalue=0)
                if new_stock is not None:
                    m['stock'] = new_stock
                    messagebox.showinfo("Success", "Stock updated!")
                    self.show_pharmacy_stock()
            
            tk.Button(frame, text="Update Stock", command=update_stock, bg="#3498db", fg="white",
                     font=("Arial", 9)).pack(side=tk.RIGHT, padx=10, pady=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.main_frame, text="← Back", command=self.show_pharmacy_dashboard,
                 bg="#95a5a6", fg="white", font=("Arial", 10)).pack(pady=10)
        
        create_footer(self.main_frame)


# =============== RUN APPLICATION ===============
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
