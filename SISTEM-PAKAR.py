import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from PIL import Image, ImageTk

class DiagnosisExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Diagnosis")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")
        
        self.system_name = "Sistem Pakar Diagnosis Penyakit Menular Pada Anak Balita"
        
        os.makedirs("assets", exist_ok=True)
        
        self.rules = self.get_default_rules()
        self.gejala_list = self.get_default_gejala()
        self.gejala_categories = self.get_default_categories()
        
        self.load_data()
        
        self.setup_styles()
        
        self.main_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.frames = {}
        self.create_frames()
        
        self.show_frame("main_menu")
    
    def load_data(self):
        try:
            if os.path.exists("expert_system_data.json"):
                with open("expert_system_data.json", "r") as file:
                    data = json.load(file)
                    self.rules = data.get("rules", self.rules)
                    self.gejala_list = data.get("gejala_list", self.gejala_list)
                    self.gejala_categories = data.get("gejala_categories", self.gejala_categories)
                    self.system_name = data.get("system_name", self.system_name)
                    print(f"Loaded {len(self.rules)} rules from file")
        except Exception as e:
            print(f"Error loading data: {e}")
            pass
    
    def save_data(self):
        try:
            data = {
                "rules": self.rules,
                "gejala_list": self.gejala_list,
                "gejala_categories": self.gejala_categories,
                "system_name": self.system_name
            }
            with open("expert_system_data.json", "w") as file:
                json.dump(data, file, indent=4)
            print(f"Saved {len(self.rules)} rules to file")
        except Exception as e:
            print(f"Error saving data: {e}")
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}", parent=self.root)
    
    def get_default_rules(self):
        return [
            {
                "penyakit": "Campak / Morbili (P01)",
                "gejala": ["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G08"],
                "solusi": (
                    "Pastikan anak mendapatkan cukup cairan, beri obat penurun demam, "
                    "dan segera konsultasikan dengan dokter untuk perawatan lebih lanjut."
                ),
            },
            {
                "penyakit": "Rubella (Campak Jerman) (P02)",
                "gejala": ["G02", "G03", "G06", "G09", "G10", "G11", "G12", "G13", "G14"],
                "solusi": (
                    "Istirahat yang cukup, perbanyak asupan nutrisi, hindari kontak dengan ibu hamil, "
                    "dan konsultasi dengan dokter segera."
                ),
            },
            {
                "penyakit": "Cacar Air / Varisela (P03)",
                "gejala": ["G09", "G10", "G15", "G16", "G17", "G18"],
                "solusi": (
                    "Hindari menggaruk ruam, gunakan salep pereda gatal, berikan obat penurun demam jika diperlukan, "
                    "dan konsultasikan dengan dokter."
                ),
            },
            {
                "penyakit": "Sindrom Pipi Merah (Eritema infeksiosa) (P04)",
                "gejala": ["G03", "G04", "G09", "G19", "G20", "G21", "G22"],
                "solusi": (
                    "Istirahat cukup, beri obat sesuai anjuran dokter jika diperlukan, "
                    "dan cegah penyebaran dengan menjaga kebersihan lingkungan."
                ),
            },
            {
                "penyakit": "Roseola infantum (P05)",
                "gejala": ["G01", "G03", "G04", "G06", "G23", "G24", "G25", "G26", "G27", "G28"],
                "solusi": (
                    "Perbanyak cairan untuk anak, hindari makanan berat, dan segera hubungi dokter "
                    "jika gejala bertambah parah."
                ),
            },
            {
                "penyakit": "Impetigo (P06)",
                "gejala": ["G29", "G30", "G31", "G32"],
                "solusi": (
                    "Cuci area terinfeksi dengan sabun antiseptik, gunakan salep antibiotik, "
                    "dan segera konsultasikan dengan dokter untuk pengobatan lebih lanjut."
                ),
            },
            {
                "penyakit": "Demam Berdarah (P07)",
                "gejala": ["G01", "G03", "G15", "G33", "G34", "G35", "G36", "G37", "G38", "G39", "G40", "G41"],
                "solusi": (
                    "Segera bawa anak ke fasilitas kesehatan terdekat untuk perawatan medis intensif."
                ),
            },
        ]
    
    def get_default_gejala(self):
        return [
            ("Suhu badan di atas 38 derajat Celcius", "G01"),
            ("Mata berair dan merah pada bagian konjungtiva", "G02"),
            ("Batuk", "G03"),
            ("Pilek", "G04"),
            ("Bercak putih di dalam rongga mulut", "G05"),
            ("Muncul kelainan kemerahan pada kulit", "G06"),
            ("Ruam berwarna coklat kemerahan memenuhi tubuh dalam waktu 3 hari", "G07"),
            ("Ruam memudar pada hari ke-5 atau ke-6", "G08"),
            ("Suhu badan di bawah 38 derajat Celcius", "G09"),
            ("Sakit kepala", "G10"),
            ("Pembesaran kelenjar getah bening di leher", "G11"),
            ("Ruam merah muda muncul dalam waktu 24-48 jam", "G12"),
            ("Ruam berupa bintik-bintik kecil merah", "G13"),
            ("Ruam memudar pada hari ke-3", "G14"),
            ("Mengalami mual", "G15"),
            ("Timbul ruam pada kulit", "G16"),
            ("Bekas cacar air berbentuk cekungan merah muda", "G17"),
            ("Ruam terasa gatal", "G18"),
            ("Gangguan pernafasan", "G19"),
            ("Pipi anak berwarna merah", "G20"),
            ("Sakit tenggorokan", "G21"),
            ("Ruam menyebar ke tubuh, tangan, dan kaki", "G22"),
            ("Penurunan demam secara drastis", "G23"),
            ("Ruam berwarna merah tua", "G24"),
            ("Tidak nafsu makan", "G26"),
            ("Diare ringan", "G27"),
            ("Kejang", "G28"),
            ("Infeksi di sekitar mulut", "G29"),
            ("Bintik kuning seperti madu", "G30"),
            ("Bintik pecah menyebabkan kemerahan", "G31"),
            ("Bintik melepuh berisi nanah", "G32"),
            ("Demam tinggi 2-7 hari", "G33"),
            ("Pendarahan kulit", "G34"),
        ]
    
    def get_default_categories(self):
        return {
            "Demam & Suhu Tubuh": ["G01", "G09", "G33"],
            "Gejala Pernapasan": ["G03", "G04", "G19", "G21"],
            "Gejala Kulit & Ruam": ["G06", "G07", "G08", "G12", "G13", "G14", "G16", "G17", "G18", "G20", "G22", "G24", "G34"],
            "Gejala Mulut & Mata": ["G02", "G05", "G29", "G30", "G31", "G32"],
            "Gejala Umum Lainnya": ["G10", "G11", "G15", "G23", "G26", "G27", "G28"]
        }
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TLabel", font=("Poppins", 11), background="#f5f5f5")
        style.configure("TButton", font=("Poppins", 11), padding=5)
        style.configure("TCheckbutton", font=("Poppins", 11), background="#ffffff")
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TNotebook", background="#f5f5f5", tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", font=("Poppins", 11), padding=[10, 5], background="#e0e0e0", foreground="#2c3e50")
        style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "#ffffff")])
    
        os.makedirs("assets", exist_ok=True)
        icon_path = "assets/icon.png"
        if os.path.exists(icon_path):
            try:
                self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
            except Exception as e:
                print(f"Error loading icon: {e}")
        else:
            print(f"Icon file not found: {icon_path}")
            
    def create_frames(self):
        self.frames["main_menu"] = MainMenuFrame(self.main_frame, self)
        self.frames["diagnosis"] = DiagnosisFrame(self.main_frame, self)
        self.frames["edit"] = EditFrame(self.main_frame, self)
        self.frames["result"] = ResultFrame(self.main_frame, self)
        
        for frame in self.frames.values():
            frame.pack(fill=tk.BOTH, expand=True)
            frame.pack_forget()
    
    def show_frame(self, frame_name):
        for name, frame in self.frames.items():
            frame.pack_forget()
        
        if frame_name == "diagnosis":
            self.frames[frame_name].setup_diagnosis_page()
        elif frame_name == "edit":
            self.frames[frame_name].refresh_data()
        
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)
    
    def update_system_name(self, new_name):
        self.system_name = new_name
        self.save_data()
        for frame in self.frames.values():
            if hasattr(frame, "update_title"):
                frame.update_title()
    
    def diagnose(self, selected_gejala):
        if not selected_gejala:
            messagebox.showwarning("Peringatan", "Pilih minimal satu gejala!", parent=self.root)
            return None
        
        results = []
        for rule in self.rules:
            matched = sum(1 for gejala in rule["gejala"] if gejala in selected_gejala)
            total = len(rule["gejala"])
            percentage = (matched / total) * 100
            
            results.append({
                "penyakit": rule["penyakit"],
                "solusi": rule["solusi"],
                "persentase": percentage,
                "matched_count": matched,
                "total_count": total
            })
        
        results.sort(key=lambda x: x["persentase"], reverse=True)
        
        return results


class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f5f5f5")
        self.controller = controller
        
        self.create_widgets()
    
    def create_widgets(self):
        self.header_frame = tk.Frame(self, height=80, bg="#3498db")
        self.header_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            self.header_frame,
            text="Kembali",
            font=("Poppins", 10),
            bg="#2c3e50",
            fg="white",
            padx=10,
            pady=5,
            relief="flat",
            command=lambda: self.controller.show_frame("main_menu")
        )
        back_button.pack(side="left", padx=10)
        back_button.pack_forget()  
        
        self.title_label = tk.Label(
            self.header_frame,
            text=self.controller.system_name,
            font=("Poppins", 16, "bold"),
            bg="#3498db",
            fg="white"
        )
        self.title_label.pack(pady=15)
        
        content_frame = tk.Frame(self, bg="#f5f5f5", padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_label = tk.Label(
            content_frame,
            text="Selamat Datang di Sistem Pakar",
            font=("Poppins", 20, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        welcome_label.pack(pady=(20, 30))
        
        info_frame = tk.Frame(content_frame, bg="white", padx=25, pady=25, relief="ridge", bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = (
            "Sistem pakar adalah program komputer yang dirancang untuk meniru kemampuan "
            "pemecahan masalah dari seorang pakar manusia. Sistem ini menggunakan pengetahuan "
            "dan aturan yang telah dikodifikasi untuk memberikan solusi atau diagnosis "
            "berdasarkan gejala atau kondisi yang dimasukkan oleh pengguna.\n\n"
            "Cara menggunakan sistem ini:\n"
            "1. Pilih gejala-gejala yang relevan pada halaman diagnosis\n"
            "2. Sistem akan menganalisis gejala dan memberikan diagnosis beserta solusi\n"
            "3. Anda juga dapat mengedit data sistem melalui halaman edit"
        )
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Poppins", 12),
            bg="white",
            fg="#34495e",
            justify="left",
            wraplength=700
        )
        info_label.pack(anchor="w")
        
        button_frame = tk.Frame(content_frame, bg="#f5f5f5", pady=30)
        button_frame.pack()
        
        diagnosis_button = tk.Button(
            button_frame,
            text="Mulai Diagnosis",
            font=("Poppins", 14, "bold"),
            bg="#3498db",
            fg="white",
            padx=30,
            pady=15,
            relief="flat",
            command=lambda: self.controller.show_frame("diagnosis")
        )
        diagnosis_button.grid(row=0, column=0, padx=20)
        
        edit_button = tk.Button(
            button_frame,
            text="Edit Data Sistem",
            font=("Poppins", 14, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=15,
            relief="flat",
            command=lambda: self.controller.show_frame("edit")
        )
        edit_button.grid(row=0, column=1, padx=20)
        
        for button in [diagnosis_button, edit_button]:
            self.setup_button_hover(button)
        
        footer_frame = tk.Frame(self, bg="#34495e", height=30)
        footer_frame.pack(fill=tk.X, side="bottom")
        
        tk.Label(
            footer_frame,
            text="© 2023 Sistem Pakar",
            font=("Poppins", 9),
            bg="#34495e",
            fg="#ecf0f1",
            pady=5
        ).pack()
    
    def setup_button_hover(self, button):
        original_color = button["bg"]
        hover_colors = {
            "#3498db": "#2980b9",
            "#2ecc71": "#27ae60",
            "#e74c3c": "#c0392b",
            "#2c3e50": "#1a252f"
        }
        
        button.bind("<Enter>", lambda e, b=button, c=hover_colors[original_color]: self.on_enter(e, b, c))
        button.bind("<Leave>", lambda e, b=button, c=original_color: self.on_leave(e, b, c))
    
    def on_enter(self, e, button, color):
        button['bg'] = color
    
    def on_leave(self, e, button, color):
        button['bg'] = color
    
    def update_title(self):
        self.title_label.config(text=self.controller.system_name)


class DiagnosisFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f5f5f5")
        self.controller = controller
        self.gejala_vars = []
        
        self.create_widgets()
    
    def create_widgets(self):
        self.header_frame = tk.Frame(self, height=80, bg="#3498db")
        self.header_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.header_frame,
            text=self.controller.system_name,
            font=("Poppins", 16, "bold"),
            bg="#3498db",
            fg="white"
        )
        self.title_label.pack(pady=15)
        
        self.content_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=15)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        desc_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        desc_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            desc_frame,
            text="Pilih gejala yang dialami untuk mendapatkan diagnosis:",
            font=("Poppins", 12),
            bg="#f5f5f5",
            fg="#2c3e50"
        ).pack(anchor="w")
        
        self.gejala_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        self.gejala_frame.pack(fill=tk.BOTH, expand=True)
        
        button_frame = tk.Frame(self, bg="#f5f5f5", pady=15)
        button_frame.pack(fill=tk.X)
        
        diagnose_button = tk.Button(
            button_frame,
            text="Diagnosa",
            font=("Poppins", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.diagnose
        )
        diagnose_button.pack(side="left", padx=20)
        
        reset_button = tk.Button(
            button_frame,
            text="Reset",
            font=("Poppins", 12),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.reset_checkboxes
        )
        reset_button.pack(side="left", padx=5)
        
        back_button = tk.Button(
            button_frame,
            text="Kembali ke Menu",
            font=("Poppins", 12),
            bg="#2c3e50",
            fg="white",
            padx=15,
            pady=10,
            relief="flat",
            command=lambda: self.controller.show_frame("main_menu")
        )
        back_button.pack(side="right", padx=20)
        
        for button, color, hover_color in [
            (diagnose_button, "#3498db", "#2980b9"),
            (reset_button, "#e74c3c", "#c0392b"),
            (back_button, "#2c3e50", "#1a252f")
        ]:
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(e, b, c))
        
        footer_frame = tk.Frame(self, bg="#34495e", height=30)
        footer_frame.pack(fill=tk.X, side="bottom")
        
        tk.Label(
            footer_frame,
            text="© 2023 Sistem Pakar",
            font=("Poppins", 9),
            bg="#34495e",
            fg="#ecf0f1",
            pady=5
        ).pack()
    
    def setup_diagnosis_page(self):
        # Clear previous widgets
        for widget in self.gejala_frame.winfo_children():
            widget.destroy()
        
        self.gejala_vars = []
        
        # Create a canvas with scrollbar for all symptoms
        canvas = tk.Canvas(self.gejala_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.gejala_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#ffffff", padx=10, pady=10)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        for i, (desc, code) in enumerate(self.controller.gejala_list):
            var = tk.StringVar()
            frame = tk.Frame(scrollable_frame, bg="#ffffff" if i % 2 == 0 else "#f9f9f9", pady=5)
            frame.pack(fill=tk.X)
            
            cb = ttk.Checkbutton(
                frame, 
                text=f"{code} - {desc}", 
                variable=var, 
                onvalue=code, 
                offvalue=""
            )
            cb.pack(side="left", anchor="w", padx=5)
            self.gejala_vars.append(var)
    
    def diagnose(self):
        selected_gejala = [var.get() for var in self.gejala_vars if var.get()]
        results = self.controller.diagnose(selected_gejala)
        
        if results:
            self.controller.frames["result"].display_results(results)
            self.controller.show_frame("result")
    
    def reset_checkboxes(self):
        for var in self.gejala_vars:
            var.set("")
    
    def on_enter(self, e, button, color):
        button['bg'] = color
    
    def on_leave(self, e, button, color):
        button['bg'] = color
    
    def update_title(self):
        self.title_label.config(text=self.controller.system_name)


class ResultFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f5f5f5")
        self.controller = controller
        
        self.create_widgets()
    
    def create_widgets(self):
        self.header_frame = tk.Frame(self, bg="#3498db", pady=15)
        self.header_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="Hasil Diagnosis",
            font=("Poppins", 18, "bold"),
            bg="#3498db",
            fg="white"
        )
        self.title_label.pack()
        
        self.content_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.content_frame, bg="#f5f5f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f5f5")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        footer_frame = tk.Frame(self, bg="#f5f5f5", pady=15)
        footer_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            footer_frame,
            text="Kembali ke Diagnosis",
            font=("Poppins", 11),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            relief="flat",
            command=lambda: self.controller.show_frame("diagnosis")
        )
        back_button.pack(side="left", padx=20)
        
        menu_button = tk.Button(
            footer_frame,
            text="Menu Utama",
            font=("Poppins", 11),
            bg="#2c3e50",
            fg="white",
            padx=20,
            pady=8,
            relief="flat",
            command=lambda: self.controller.show_frame("main_menu")
        )
        menu_button.pack(side="right", padx=20)
        
        for button, color, hover_color in [
            (back_button, "#3498db", "#2980b9"),
            (menu_button, "#2c3e50", "#1a252f")
        ]:
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(e, b, c))
    
    def display_results(self, results):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter out results with 0% match
        filtered_results = [result for result in results if result["persentase"] > 0]
        
        if not filtered_results:
            no_match_frame = tk.Frame(self.scrollable_frame, bg="white", padx=15, pady=15, relief="ridge", bd=1)
            no_match_frame.pack(fill=tk.X, pady=10, padx=5)
            
            tk.Label(
                no_match_frame,
                text="Tidak Ada Hasil yang Cocok",
                font=("Poppins", 14, "bold"),
                bg="white",
                fg="#2c3e50",
                justify="center"
            ).pack(pady=10)
            
            tk.Label(
                no_match_frame,
                text="Gejala yang dipilih tidak cocok dengan penyakit yang ada dalam sistem. Silakan pilih gejala lain atau konsultasikan dengan dokter.",
                font=("Poppins", 11),
                bg="white",
                fg="#34495e",
                justify="center",
                wraplength=500
            ).pack(pady=5)
            return
        
        for i, result in enumerate(filtered_results):
            result_card = tk.Frame(self.scrollable_frame, bg="white", padx=15, pady=15, relief="ridge", bd=1)
            result_card.pack(fill=tk.X, pady=10, padx=5)
            
            title_frame = tk.Frame(result_card, bg="white")
            title_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(
                title_frame,
                text=result["penyakit"],
                font=("Poppins", 14, "bold"),
                bg="white",
                fg="#2c3e50",
                justify="left"
            ).pack(side="left")
            
            percentage_label = tk.Label(
                title_frame,
                text=f"{result['persentase']:.1f}%",
                font=("Poppins", 12),
                bg="#e74c3c" if result["persentase"] < 50 else "#f39c12" if result["persentase"] < 70 else "#2ecc71",
                fg="white",
                padx=8,
                pady=2
            )
            percentage_label.pack(side="right")
            percentage_label.configure(relief="ridge", bd=0)
            
            match_info = tk.Label(
                title_frame,
                text=f"({result['matched_count']}/{result['total_count']} gejala)",
                font=("Poppins", 10),
                bg="white",
                fg="#7f8c8d",
                padx=5
            )
            match_info.pack(side="right")
            
            separator = tk.Frame(result_card, height=1, bg="#e0e0e0")
            separator.pack(fill=tk.X, pady=5)
            
            solution_frame = tk.Frame(result_card, bg="white")
            solution_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                solution_frame,
                text="Solusi:",
                font=("Poppins", 12, "bold"),
                bg="white",
                fg="#2c3e50",
                anchor="w"
            ).pack(fill=tk.X)
            
            tk.Label(
                solution_frame,
                text=result["solusi"],
                font=("Poppins", 11),
                bg="white",
                fg="#34495e",
                justify="left",
                wraplength=500,
                anchor="w"
            ).pack(fill=tk.X, pady=(5, 0))
    
    def on_enter(self, e, button, color):
        button['bg'] = color
    
    def on_leave(self, e, button, color):
        button['bg'] = color
    
    def update_title(self):
        self.title_label.config(text="Hasil Diagnosis")


class EditFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f5f5f5")
        self.controller = controller
        self.root = controller.root
        
        # Initialize attributes to avoid AttributeError
        self.gejala_select_frame = None
        self.gejala_checkboxes = []
        self.gejala_vars = []
        self.gejala_tree = None
        self.penyakit_tree = None
        
        self.create_widgets()
    
    def create_widgets(self):
        self.header_frame = tk.Frame(self, height=80, bg="#3498db")
        self.header_frame.pack(fill=tk.X)
        
        # Add back button
        back_button = tk.Button(
            self.header_frame,
            text="« Kembali ke Menu",
            font=("Poppins", 10),
            bg="#2980b9",
            fg="white",
            padx=10,
            pady=5,
            relief="flat",
            command=lambda: self.controller.show_frame("main_menu")
        )
        back_button.pack(side="left", padx=10, pady=10)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="Edit Data Sistem Pakar",
            font=("Poppins", 16, "bold"),
            bg="#3498db",
            fg="white"
        )
        self.title_label.pack(pady=15)
        
        self.content_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=15)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.system_tab = ttk.Frame(notebook)
        self.gejala_tab = ttk.Frame(notebook)
        self.penyakit_tab = ttk.Frame(notebook)
        
        notebook.add(self.system_tab, text="Pengaturan Sistem")
        notebook.add(self.gejala_tab, text="Kelola Gejala")
        notebook.add(self.penyakit_tab, text="Kelola Penyakit")
        
        self.setup_system_tab()
        self.setup_gejala_tab()
        self.setup_penyakit_tab()
        
        button_frame = tk.Frame(self, bg="#f5f5f5", pady=15)
        button_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            button_frame,
            text="Kembali ke Menu",
            font=("Poppins", 12),
            bg="#2c3e50",
            fg="white",
            padx=15,
            pady=10,
            relief="flat",
            command=lambda: self.controller.show_frame("main_menu")
        )
        back_button.pack(side="right", padx=20)
        
        back_button.bind("<Enter>", lambda e: self.on_enter(e, back_button, "#1a252f"))
        back_button.bind("<Leave>", lambda e: self.on_leave(e, back_button, "#2c3e50"))
        
        footer_frame = tk.Frame(self, bg="#34495e", height=30)
        footer_frame.pack(fill=tk.X, side="bottom")
        
        tk.Label(
            footer_frame,
            text="© 2023 Sistem Pakar",
            font=("Poppins", 9),
            bg="#34495e",
            fg="#ecf0f1",
            pady=5
        ).pack()
    
    def setup_system_tab(self):
        frame = tk.Frame(self.system_tab, bg="#f5f5f5", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        system_name_frame = tk.Frame(frame, bg="white", padx=20, pady=20, relief="ridge", bd=1)
        system_name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            system_name_frame,
            text="Nama Sistem Pakar:",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        self.system_name_var = tk.StringVar(value=self.controller.system_name)
        system_name_entry = tk.Entry(
            system_name_frame,
            textvariable=self.system_name_var,
            font=("Poppins", 12),
            width=50
        )
        system_name_entry.pack(fill=tk.X, pady=5)
        
        button_frame = tk.Frame(system_name_frame, bg="white", pady=10)
        button_frame.pack(fill=tk.X)
        
        save_name_button = tk.Button(
            button_frame,
            text="Simpan Nama Sistem",
            font=("Poppins", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=self.save_system_name
        )
        save_name_button.pack(side="left")
        
        save_name_button.bind("<Enter>", lambda e: self.on_enter(e, save_name_button, "#27ae60"))
        save_name_button.bind("<Leave>", lambda e: self.on_leave(e, save_name_button, "#2ecc71"))
        
        reset_data_frame = tk.Frame(frame, bg="white", padx=20, pady=20, relief="ridge", bd=1)
        reset_data_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            reset_data_frame,
            text="Reset Data Sistem:",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        tk.Label(
            reset_data_frame,
            text="Mengembalikan semua data ke pengaturan awal. Tindakan ini tidak dapat dibatalkan.",
            font=("Poppins", 11),
            bg="white",
            fg="#34495e",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=5)
        
        reset_button = tk.Button(
            reset_data_frame,
            text="Reset Semua Data",
            font=("Poppins", 11),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=self.reset_all_data
        )
        reset_button.pack(anchor="w", pady=10)
        
        reset_button.bind("<Enter>", lambda e: self.on_enter(e, reset_button, "#c0392b"))
        reset_button.bind("<Leave>", lambda e: self.on_leave(e, reset_button, "#e74c3c"))
    
    def setup_gejala_tab(self):
        frame = tk.Frame(self.gejala_tab, bg="#f5f5f5", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a horizontal split with two frames
        main_frame = tk.Frame(frame, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for adding symptoms
        add_frame = tk.Frame(main_frame, bg="white", padx=20, pady=20, relief="ridge", bd=1)
        add_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            add_frame,
            text="Tambah Gejala Baru:",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        input_frame = tk.Frame(add_frame, bg="white")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            input_frame,
            text="Kode Gejala:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.new_gejala_code = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.new_gejala_code,
            font=("Poppins", 11),
            width=10
        ).grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(
            input_frame,
            text="Deskripsi:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.new_gejala_desc = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.new_gejala_desc,
            font=("Poppins", 11),
            width=50
        ).grid(row=1, column=1, sticky="w", pady=5)
        
        add_button = tk.Button(
            add_frame,
            text="Tambah Gejala",
            font=("Poppins", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=self.add_gejala
        )
        add_button.pack(anchor="w", pady=10)
        
        add_button.bind("<Enter>", lambda e: self.on_enter(e, add_button, "#27ae60"))
        add_button.bind("<Leave>", lambda e: self.on_leave(e, add_button, "#2ecc71"))
        
        # Right frame for symptom list
        list_frame = tk.Frame(main_frame, bg="white", padx=20, pady=20, relief="ridge", bd=1)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(
            list_frame,
            text="Daftar Gejala:",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        # Add action buttons above the tree
        action_frame = tk.Frame(list_frame, bg="white", pady=10)
        action_frame.pack(fill=tk.X, side="top", pady=(0, 10))

        edit_btn = tk.Button(
            action_frame, 
            text="Edit Gejala", 
            bg="#2ecc71", 
            fg="white",
            padx=10,
            pady=5,
            command=self.edit_selected_gejala
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(
            action_frame, 
            text="Hapus Gejala", 
            bg="#e74c3c", 
            fg="white",
            padx=10,
            pady=5,
            command=self.delete_selected_gejala
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        for button, color, hover_color in [
            (edit_btn, "#2ecc71", "#27ae60"),
            (delete_btn, "#e74c3c", "#c0392b")
        ]:
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(e, b, c))
        
        # Create a frame that will contain the treeview and scrollbar
        self.gejala_listbox_frame = tk.Frame(list_frame, bg="white")
        self.gejala_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_gejala_list()
    
    def setup_penyakit_tab(self):
        frame = tk.Frame(self.penyakit_tab, bg="#f5f5f5", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a horizontal split with two frames
        top_frame = tk.Frame(frame, bg="#f5f5f5")
        top_frame.pack(fill=tk.X, pady=10)
        
        # Left frame for adding disease
        add_frame = tk.Frame(top_frame, bg="white", padx=20, pady=20, relief="ridge", bd=1)
        add_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            add_frame,
            text="Tambah Penyakit Baru:",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        input_frame = tk.Frame(add_frame, bg="white")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            input_frame,
            text="Nama Penyakit:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.new_penyakit_name = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.new_penyakit_name,
            font=("Poppins", 11),
            width=50
        ).grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(
            input_frame,
            text="Solusi:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=1, column=0, sticky="nw", pady=5)
        
        self.new_penyakit_solusi = tk.Text(
            input_frame,
            font=("Poppins", 11),
            width=50,
            height=4
        )
        self.new_penyakit_solusi.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(
            input_frame,
            text="Gejala:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=2, column=0, sticky="nw", pady=5)
        
        # Store as class attribute
        self.gejala_select_frame = tk.Frame(input_frame, bg="white")
        self.gejala_select_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        self.refresh_gejala_checkboxes()
        
        add_button = tk.Button(
            add_frame,
            text="Tambah Penyakit",
            font=("Poppins", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=self.add_penyakit
        )
        add_button.pack(anchor="w", pady=10)
        
        add_button.bind("<Enter>", lambda e: self.on_enter(e, add_button, "#27ae60"))
        add_button.bind("<Leave>", lambda e: self.on_leave(e, add_button, "#2ecc71"))
        
        # Right frame for disease list
        list_frame_right = tk.Frame(top_frame, bg="white", padx=20, pady=20, relief="ridge", bd=1)
        list_frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(
            list_frame_right,
            text="Daftar Penyakit:",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        # Add action buttons above the tree
        action_frame_right = tk.Frame(list_frame_right, bg="white", pady=10)
        action_frame_right.pack(fill=tk.X, side="top", pady=(0, 10))

        edit_btn_right = tk.Button(
            action_frame_right, 
            text="Edit Penyakit", 
            bg="#2ecc71", 
            fg="white",
            padx=10,
            pady=5,
            command=self.edit_selected_penyakit
        )
        edit_btn_right.pack(side=tk.LEFT, padx=5)

        delete_btn_right = tk.Button(
            action_frame_right, 
            text="Hapus Penyakit", 
            bg="#e74c3c", 
            fg="white",
            padx=10,
            pady=5,
            command=self.delete_selected_penyakit
        )
        delete_btn_right.pack(side=tk.LEFT, padx=5)

        for button, color, hover_color in [
            (edit_btn_right, "#2ecc71", "#27ae60"),
            (delete_btn_right, "#e74c3c", "#c0392b")
        ]:
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(e, b, c))
        
        # Create a frame that will contain the treeview and scrollbar
        penyakit_tree_frame = tk.Frame(list_frame_right, bg="white")
        penyakit_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("penyakit", "gejala", "solusi")
        self.penyakit_tree_right = ttk.Treeview(penyakit_tree_frame, columns=columns, show="headings", height=10)
        
        self.penyakit_tree_right.heading("penyakit", text="Penyakit")
        self.penyakit_tree_right.heading("gejala", text="Jumlah Gejala")
        self.penyakit_tree_right.heading("solusi", text="Solusi")
        
        # Adjust column widths to fit content better
        self.penyakit_tree_right.column("penyakit", width=200)
        self.penyakit_tree_right.column("gejala", width=80)
        self.penyakit_tree_right.column("solusi", width=200)
        
        self.refresh_penyakit_tree()
        
        scrollbar_right = ttk.Scrollbar(penyakit_tree_frame, orient="vertical", command=self.penyakit_tree_right.yview)
        self.penyakit_tree_right.configure(yscrollcommand=scrollbar_right.set)
        
        self.penyakit_tree_right.pack(fill="both", expand=True, side="left")
        scrollbar_right.pack(side="right", fill="y")
    
    def refresh_penyakit_tree(self):
        # Clear existing items
        for item in self.penyakit_tree_right.get_children():
            self.penyakit_tree_right.delete(item)
        
        # Add current rules
        for rule in self.controller.rules:
            self.penyakit_tree_right.insert("", "end", values=(
                rule["penyakit"],
                len(rule["gejala"]),
                rule["solusi"][:50] + "..." if len(rule["solusi"]) > 50 else rule["solusi"]
            ))
    
    def refresh_gejala_checkboxes(self):
        # Clear existing checkboxes
        for widget in self.gejala_select_frame.winfo_children():
            widget.destroy()
        
        self.gejala_checkboxes = []
        self.gejala_vars = []
        
        canvas = tk.Canvas(self.gejala_select_frame, bg="white", highlightthickness=0, width=400, height=200)
        scrollbar = ttk.Scrollbar(self.gejala_select_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Add all symptoms to the checkboxes
        for i, (desc, code) in enumerate(self.controller.gejala_list):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                scrollable_frame,
                text=f"{code} - {desc}",
                variable=var
            )
            cb.grid(row=i, column=0, sticky="w", pady=2)
            self.gejala_checkboxes.append(cb)
            self.gejala_vars.append((var, code))

    def refresh_gejala_list(self):
        for widget in self.gejala_listbox_frame.winfo_children():
            widget.destroy()
      
        # Create a frame that will contain the treeview and scrollbar
        tree_container = tk.Frame(self.gejala_listbox_frame, bg="white")
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ("kode", "deskripsi")
        self.gejala_tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=15)
      
        self.gejala_tree.heading("kode", text="Kode")
        self.gejala_tree.heading("deskripsi", text="Deskripsi")
      
        self.gejala_tree.column("kode", width=80)
        self.gejala_tree.column("deskripsi", width=500)
      
        for desc, code in self.controller.gejala_list:
            self.gejala_tree.insert("", "end", values=(code, desc))
      
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.gejala_tree.yview)
        self.gejala_tree.configure(yscrollcommand=scrollbar.set)
      
        self.gejala_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def edit_selected_gejala(self):
        selected_items = self.gejala_tree.selection()
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih gejala yang akan diedit!", parent=self.root)
            return
      
        item = selected_items[0]
        values = self.gejala_tree.item(item, "values")
        code = values[0]
        self.edit_gejala_by_code(code)
  
    def delete_selected_gejala(self):
        selected_items = self.gejala_tree.selection()
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih gejala yang akan dihapus!", parent=self.root)
            return
      
        item = selected_items[0]
        values = self.gejala_tree.item(item, "values")
        code = values[0]
        self.delete_gejala_by_code(code)
  
    def edit_selected_penyakit(self):
        # Try to get selection from both
        selected_items = None
        tree_used = None
        
        # First check the main penyakit tree
        if hasattr(self, 'penyakit_tree') and self.penyakit_tree:
            selected_items = self.penyakit_tree.selection()
            if selected_items:
                tree_used = self.penyakit_tree
        
        # If nothing selected, try the right side tree
        if not selected_items and hasattr(self, 'penyakit_tree_right') and self.penyakit_tree_right:
            selected_items = self.penyakit_tree_right.selection()
            if selected_items:
                tree_used = self.penyakit_tree_right
        
        if not selected_items or not tree_used:
            messagebox.showwarning("Peringatan", "Pilih penyakit yang akan diedit!", parent=self.root)
            return
      
        item = selected_items[0]
        values = tree_used.item(item, "values")
        penyakit_name = values[0]
        self.edit_penyakit_by_name(penyakit_name)
  
    def delete_selected_penyakit(self):
        # Try to get selection from both
        selected_items = None
        tree_used = None
        
        # First check the main penyakit tree
        if hasattr(self, 'penyakit_tree') and self.penyakit_tree:
            selected_items = self.penyakit_tree.selection()
            if selected_items:
                tree_used = self.penyakit_tree
        
        # If nothing selected, try the right side tree
        if not selected_items and hasattr(self, 'penyakit_tree_right') and self.penyakit_tree_right:
            selected_items = self.penyakit_tree_right.selection()
            if selected_items:
                tree_used = self.penyakit_tree_right
        
        if not selected_items or not tree_used:
            messagebox.showwarning("Peringatan", "Pilih penyakit yang akan dihapus!", parent=self.root)
            return
      
        item = selected_items[0]
        values = tree_used.item(item, "values")
        penyakit_name = values[0]
        self.delete_penyakit_by_name(penyakit_name)

    def edit_gejala_by_code(self, code):
        # Find the gejala
        gejala_desc = ""
        for desc, c in self.controller.gejala_list:
            if c == code:
                gejala_desc = desc
                break
      
        if not gejala_desc:
            messagebox.showerror("Error", f"Gejala dengan kode {code} tidak ditemukan!", parent=self.root)
            return
      
        # Find the category
        current_category = "Gejala Umum"
        for cat, codes in self.controller.gejala_categories.items():
            if code in codes:
                current_category = cat
                break
      
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Gejala {code}")
        edit_window.geometry("500x250")
        edit_window.configure(bg="#f5f5f5")
        edit_window.transient(self.root)
        edit_window.grab_set()
      
        frame = tk.Frame(edit_window, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
      
        tk.Label(
            frame,
            text=f"Edit Gejala {code}",
            font=("Poppins", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 20))
      
        input_frame = tk.Frame(frame, bg="white")
        input_frame.pack(fill=tk.X, pady=5)
      
        tk.Label(
            input_frame,
            text="Kode Gejala:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=5)
      
        new_code_var = tk.StringVar(value=code)
        tk.Entry(
            input_frame,
            textvariable=new_code_var,
            font=("Poppins", 11),
            width=10
        ).grid(row=0, column=1, sticky="w", pady=5)
      
        tk.Label(
            input_frame,
            text="Deskripsi:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=5)
      
        new_desc_var = tk.StringVar(value=gejala_desc)
        tk.Entry(
            input_frame,
            textvariable=new_desc_var,
            font=("Poppins", 11),
            width=40
        ).grid(row=1, column=1, sticky="w", pady=5)
      
        button_frame = tk.Frame(frame, bg="white", pady=20)
        button_frame.pack(fill=tk.X)
      
        save_button = tk.Button(
            button_frame,
            text="Simpan",
            font=("Poppins", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=lambda: self.save_edited_gejala(
              code, 
              new_code_var.get().strip(), 
              new_desc_var.get().strip(),
              current_category,
              current_category,  # No category dropdown, use same category
              edit_window
          )
        )
        save_button.pack(side="left", padx=5)
      
        cancel_button = tk.Button(
            button_frame,
            text="Batal",
            font=("Poppins", 11),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=edit_window.destroy
        )
        cancel_button.pack(side="left", padx=5)
      
        for button, color, hover_color in [
            (save_button, "#2ecc71", "#27ae60"),
            (cancel_button, "#e74c3c", "#c0392b")
        ]:
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(e, b, c))
  
    def delete_gejala_by_code(self, code):
        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus gejala dengan kode {code}?",
            parent=self.root
        )
      
        if not confirm:
            return
      
        # Remove from gejala_list
        self.controller.gejala_list = [(desc, c) for desc, c in self.controller.gejala_list if c != code]
      
        # Remove from categories
        for category, codes in self.controller.gejala_categories.items():
            if code in codes:
                self.controller.gejala_categories[category].remove(code)
      
        # Remove from rules
        for rule in self.controller.rules:
            if code in rule["gejala"]:
                rule["gejala"].remove(code)
      
        self.controller.save_data()
        self.refresh_gejala_list()
        self.refresh_gejala_checkboxes()  # Refresh checkboxes to reflect the changes
        messagebox.showinfo("Sukses", f"Gejala dengan kode {code} berhasil dihapus!", parent=self.root)
  
    def edit_penyakit_by_name(self, penyakit_name):
        # Find the penyakit
        found_rule = None
        for rule in self.controller.rules:
            if rule["penyakit"] == penyakit_name:
                found_rule = rule
                break
      
        if not found_rule:
            messagebox.showerror("Error", f"Penyakit {penyakit_name} tidak ditemukan!", parent=self.root)
            return
      
        # Extract code from penyakit name (format: "Name (Code)")
        code = penyakit_name.split("(")[-1].split(")")[0]
        name = penyakit_name.split(" (")[0]
      
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Penyakit {code}")
        edit_window.geometry("600x550")
        edit_window.configure(bg="#f5f5f5")
        edit_window.transient(self.root)
        edit_window.grab_set()
      
        frame = tk.Frame(edit_window, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
      
        tk.Label(
            frame,
            text=f"Edit Penyakit {code}",
            font=("Poppins", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 20))
      
        input_frame = tk.Frame(frame, bg="white")
        input_frame.pack(fill=tk.X, pady=5)
      
        tk.Label(
            input_frame,
            text="Nama Penyakit:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=5)
      
        new_name_var = tk.StringVar(value=name)
        tk.Entry(
            input_frame,
            textvariable=new_name_var,
            font=("Poppins", 11),
            width=40
        ).grid(row=0, column=1, sticky="w", pady=5)
      
        tk.Label(
            input_frame,
            text="Solusi:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=1, column=0, sticky="nw", pady=5)
      
        new_solusi_text = tk.Text(
            input_frame,
            font=("Poppins", 11),
            width=40,
            height=4
        )
        new_solusi_text.grid(row=1, column=1, sticky="w", pady=5)
        new_solusi_text.insert("1.0", found_rule["solusi"])
      
        tk.Label(
            input_frame,
            text="Gejala:",
            font=("Poppins", 11),
            bg="white",
            fg="#2c3e50",
            width=15,
            anchor="w"
        ).grid(row=2, column=0, sticky="nw", pady=5)
      
        gejala_select_frame = tk.Frame(input_frame, bg="white")
        gejala_select_frame.grid(row=2, column=1, sticky="w", pady=5)
      
        canvas = tk.Canvas(gejala_select_frame, bg="white", highlightthickness=0, width=400, height=200)
        scrollbar = ttk.Scrollbar(gejala_select_frame, orient="vertical", command=canvas.yview)
      
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
      
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
      
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
      
        gejala_vars = []
        for i, (desc, code) in enumerate(self.controller.gejala_list):
            var = tk.BooleanVar(value=code in found_rule["gejala"])
            cb = ttk.Checkbutton(
                scrollable_frame,
                text=f"{code} - {desc}",
                variable=var
            )
            cb.grid(row=i, column=0, sticky="w", pady=2)
            gejala_vars.append((var, code))
      
        button_frame = tk.Frame(frame, bg="white", pady=20)
        button_frame.pack(fill=tk.X)
      
        save_button = tk.Button(
            button_frame,
            text="Simpan",
            font=("Poppins", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=lambda: self.save_edited_penyakit(
              penyakit_name,
              code,
              new_name_var.get().strip(),
              new_solusi_text.get("1.0", tk.END).strip(),
              gejala_vars,
              edit_window
          )
        )
        save_button.pack(side="left", padx=5)
      
        cancel_button = tk.Button(
            button_frame,
            text="Batal",
            font=("Poppins", 11),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            command=edit_window.destroy
        )
        cancel_button.pack(side="left", padx=5)
      
        for button, color, hover_color in [
            (save_button, "#2ecc71", "#27ae60"),
            (cancel_button, "#e74c3c", "#c0392b")
        ]:
            button.bind("<Enter>", lambda e, b=button, c=hover_color: self.on_enter(e, b, c))
            button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(e, b, c))
  
    def delete_penyakit_by_name(self, penyakit_name):
        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus penyakit {penyakit_name}?",
            parent=self.root
        )
      
        if not confirm:
            return
      
        # Remove from rules
        self.controller.rules = [rule for rule in self.controller.rules if rule["penyakit"] != penyakit_name]
      
        self.controller.save_data()
        # Update the penyakit tree
        self.refresh_penyakit_tree()
        messagebox.showinfo("Sukses", f"Penyakit {penyakit_name} berhasil dihapus!", parent=self.root)
    
    def save_system_name(self):
        new_name = self.system_name_var.get().strip()
        if new_name:
            self.controller.update_system_name(new_name)
            messagebox.showinfo("Sukses", "Nama sistem berhasil diubah!", parent=self.root)
        else:
            messagebox.showwarning("Peringatan", "Nama sistem tidak boleh kosong!", parent=self.root)
    
    def reset_all_data(self):
        confirm = messagebox.askyesno(
            "Konfirmasi Reset",
            "Apakah Anda yakin ingin mengembalikan semua data ke pengaturan awal? Tindakan ini tidak dapat dibatalkan.",
            parent=self.root
        )
        
        if confirm:
            self.controller.rules = self.controller.get_default_rules()
            self.controller.gejala_list = self.controller.get_default_gejala()
            self.controller.gejala_categories = self.controller.get_default_categories()
            self.controller.system_name = "Sistem Pakar Diagnosis Penyakit Menular Pada Anak Balita"
            self.controller.save_data()
            
            self.refresh_data()
            self.controller.frames["main_menu"].update_title()
            self.controller.frames["diagnosis"].update_title()
            self.update_title()
            
            messagebox.showinfo("Sukses", "Data berhasil direset ke pengaturan awal!", parent=self.root)
    
    def add_gejala(self):
        code = self.new_gejala_code.get().strip()
        desc = self.new_gejala_desc.get().strip()
        
        if not code or not desc:
            messagebox.showwarning("Peringatan", "Kode dan deskripsi gejala harus diisi!", parent=self.root)
            return
        
        if any(c == code for _, c in self.controller.gejala_list):
            messagebox.showwarning("Peringatan", f"Kode gejala {code} sudah ada!", parent=self.root)
            return
        
        self.controller.gejala_list.append((desc, code))
        
        # Add to default category
        default_category = list(self.controller.gejala_categories.keys())[0]
        self.controller.gejala_categories[default_category].append(code)
        
        self.controller.save_data()
        
        self.new_gejala_code.set("")
        self.new_gejala_desc.set("")
        
        self.refresh_gejala_list()
        self.refresh_gejala_checkboxes()  # Refresh checkboxes to include the new symptom
        messagebox.showinfo("Sukses", f"Gejala {code} berhasil ditambahkan!", parent=self.root)
    
    def add_penyakit(self):
        name = self.new_penyakit_name.get().strip()
        solusi = self.new_penyakit_solusi.get("1.0", tk.END).strip()
        
        if not name or not solusi:
            messagebox.showwarning("Peringatan", "Nama dan solusi penyakit harus diisi!", parent=self.root)
            return
        
        selected_gejala = [code for var, code in self.gejala_vars if var.get()]
        
        if not selected_gejala:
            messagebox.showwarning("Peringatan", "Pilih minimal satu gejala!", parent=self.root)
            return
        
        # Generate a new code for the disease (P01, P02, etc.)
        existing_codes = [rule["penyakit"].split("(")[-1].split(")")[0] for rule in self.controller.rules]
        new_code = "P01"
        i = 1
        while new_code in existing_codes:
            i += 1
            new_code = f"P{i:02d}"
        
        full_name = f"{name} ({new_code})"
        
        new_rule = {
            "penyakit": full_name,
            "gejala": selected_gejala,
            "solusi": solusi
        }
        
        self.controller.rules.append(new_rule)
        self.controller.save_data()
        
        self.new_penyakit_name.set("")
        self.new_penyakit_solusi.delete("1.0", tk.END)
        for var, _ in self.gejala_vars:
            var.set(False)
        
        # Update the penyakit tree
        self.refresh_penyakit_tree()
        messagebox.showinfo("Sukses", f"Penyakit {full_name} berhasil ditambahkan!", parent=self.root)
    
    def save_edited_gejala(self, old_code, new_code, new_desc, old_category, new_category, window):
        if not new_code or not new_desc:
            messagebox.showwarning("Peringatan", "Kode dan deskripsi gejala harus diisi!", parent=window)
            return
        
        if new_code != old_code and any(c == new_code for _, c in self.controller.gejala_list):
            messagebox.showwarning("Peringatan", f"Kode gejala {new_code} sudah ada!", parent=window)
            return
        
        # Update gejala list
        for i, (desc, code) in enumerate(self.controller.gejala_list):
            if code == old_code:
                self.controller.gejala_list[i] = (new_desc, new_code)
                break
        
        # Update code in rules if code changed
        if old_code != new_code:
            for rule in self.controller.rules:
                if old_code in rule["gejala"]:
                    rule["gejala"].remove(old_code)
                    rule["gejala"].append(new_code)
            
            # Update in categories
            for category, codes in self.controller.gejala_categories.items():
                if old_code in codes:
                    codes.remove(old_code)
                    codes.append(new_code)
        
        self.controller.save_data()
        self.refresh_gejala_list()
        self.refresh_gejala_checkboxes()  # Refresh checkboxes to reflect the changes
        window.destroy()
        messagebox.showinfo("Sukses", f"Gejala berhasil diperbarui!", parent=self.root)
    
    def save_edited_penyakit(self, old_name, code, new_name, new_solusi, gejala_vars, window):
        if not new_name or not new_solusi:
            messagebox.showwarning("Peringatan", "Nama dan solusi penyakit harus diisi!", parent=window)
            return
        
        selected_gejala = [code for var, code in gejala_vars if var.get()]
        
        if not selected_gejala:
            messagebox.showwarning("Peringatan", "Pilih minimal satu gejala!", parent=window)
            return
        
        new_full_name = f"{new_name} ({code})"
        
        # Update rule
        found = False
        for i, rule in enumerate(self.controller.rules):
            if rule["penyakit"] == old_name:
                self.controller.rules[i] = {
                    "penyakit": new_full_name,
                    "solusi": new_solusi,
                    "gejala": selected_gejala
                }
                found = True
                break
        
        if not found:
            messagebox.showerror("Error", f"Penyakit {old_name} tidak ditemukan!", parent=window)
            return
        
        self.controller.save_data()
        # Update the penyakit tree
        self.refresh_penyakit_tree()
        window.destroy()
        messagebox.showinfo("Sukses", f"Penyakit berhasil diperbarui!", parent=self.root)
    
    def on_enter(self, e, button, color):
        button['bg'] = color
    
    def on_leave(self, e, button, color):
        button['bg'] = color
    
    def update_title(self):
        self.title_label.config(text="Edit Data Sistem Pakar")

    def refresh_data(self):
        self.system_name_var.set(self.controller.system_name)
        self.refresh_gejala_list()
        self.refresh_gejala_checkboxes()
        self.refresh_penyakit_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosisExpertSystem(root)
    root.mainloop()