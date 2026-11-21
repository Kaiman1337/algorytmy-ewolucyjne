
import tkinter as tk
import math

from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from truck_route_optimizer.genetic_algorithm import optimize_route
from truck_route_optimizer.vehicle import create_vehicle, get_available_profiles
from truck_route_optimizer.visualization import draw_road_network
from truck_route_optimizer.road_network import create_road_network


class TruckRouteOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Truck Route Optimizer")
        self.root.geometry("1250x850")
        self.root.minsize(950, 650)

        self.graph = create_road_network()
        self.cities = list(self.graph.nodes)

        self.road_editor = None
        self.road_lookup = {}
        self.road_vars = {}

        self._configure_style()
        self._build_interface()


    def _configure_style(self):
        self.bg = "#0d1117"
        self.panel = "#161b22"
        self.input_bg = "#21262d"
        self.fg = "#e6edf3"
        self.muted = "#8b949e"
        self.accent = "#238636"
        self.border = "#30363d"

        self.root.configure(bg=self.bg)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            ".",
            background=self.bg,
            foreground=self.fg,
            font=("Segoe UI", 10)
        )

        style.configure(
            "TFrame",
            background=self.bg
        )

        style.configure(
            "TLabel",
            background=self.bg,
            foreground=self.fg
        )

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 19, "bold"),
            foreground="#ffffff"
        )

        style.configure(
            "TLabelFrame",
            background=self.bg,
            foreground=self.fg,
            bordercolor=self.border
        )

        style.configure(
            "TLabelFrame.Label",
            background=self.bg,
            foreground=self.fg,
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "TButton",
            background=self.input_bg,
            foreground=self.fg,
            bordercolor=self.border,
            padding=(10, 7)
        )

        style.map(
            "TButton",
            background=[
                ("active", "#30363d"),
                ("disabled", "#161b22")
            ],
            foreground=[
                ("disabled", "#6e7681")
            ]
        )

        style.configure(
            "Accent.TButton",
            background=self.accent,
            foreground="#ffffff",
            bordercolor=self.accent,
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8)
        )

        style.map(
            "Accent.TButton",
            background=[
                ("active", "#2ea043"),
                ("disabled", "#21262d")
            ],
            foreground=[
                ("disabled", "#8b949e")
            ]
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.input_bg,
            background=self.input_bg,
            foreground=self.fg,
            arrowcolor=self.fg,
            bordercolor=self.border,
            padding=6
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.input_bg)],
            foreground=[("readonly", self.fg)],
            selectbackground=[("readonly", self.input_bg)],
            selectforeground=[("readonly", self.fg)]
        )

        style.configure(
            "TEntry",
            fieldbackground=self.input_bg,
            foreground=self.fg,
            insertcolor=self.fg,
            bordercolor=self.border,
            padding=6
        )

        style.configure(
            "TCheckbutton",
            background=self.bg,
            foreground=self.fg
        )

        style.map(
            "TCheckbutton",
            background=[("active", self.bg)],
            foreground=[("active", "#ffffff")]
        )

    def _build_interface(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Nagłówek
        ttk.Label(
            main_frame,
            text="Truck Route Optimizer",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        # Parametry trasy
        settings_frame = ttk.LabelFrame(
            main_frame,
            text="Parametry trasy",
            padding=10
        )
        settings_frame.pack(fill="x", pady=(0, 10))

        settings_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(3, weight=1)
        settings_frame.columnconfigure(5, weight=1)

        ttk.Label(
            settings_frame,
            text="Początek:"
        ).grid(row=0, column=0, padx=(5, 8), pady=5)

        self.start_var = tk.StringVar(value=self.cities[0])

        ttk.Combobox(
            settings_frame,
            textvariable=self.start_var,
            values=self.cities,
            state="readonly",
            width=18
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(
            settings_frame,
            text="Cel:"
        ).grid(row=0, column=2, padx=(12, 8), pady=5)

        self.end_var = tk.StringVar(value=self.cities[-1])

        ttk.Combobox(
            settings_frame,
            textvariable=self.end_var,
            values=self.cities,
            state="readonly",
            width=18
        ).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(
            settings_frame,
            text="Pojazd:"
        ).grid(row=0, column=4, padx=(12, 8), pady=5)

        self.vehicle_var = tk.StringVar()

        self.vehicle_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.vehicle_var,
            values=get_available_profiles(),
            state="readonly",
            width=22
        )
        self.vehicle_combo.grid(
            row=0, column=5,
            sticky="ew", padx=5, pady=5
        )
        self.vehicle_combo.current(0)

        self.optimize_button = ttk.Button(
            settings_frame,
            text="Optymalizuj",
            style="Accent.TButton",
            command=self.optimize_route
        )
        self.optimize_button.grid(
            row=0, column=6,
            padx=(12, 5), pady=5
        )

        ttk.Button(
            settings_frame,
            text="Warunki drogowe",
            command=self._open_road_editor
        ).grid(
            row=0, column=7,
            padx=5, pady=5
        )

        # Mapa
        map_frame = ttk.LabelFrame(
            main_frame,
            text="Mapa sieci drogowej",
            padding=5
        )
        map_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.figure = Figure(
            figsize=(10, 6),
            dpi=100,
            facecolor=self.bg
        )

        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.panel)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=map_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        draw_road_network(self.graph, ax=self.ax)
        self.canvas.draw()

        # Wyniki pod mapą
        result_frame = ttk.LabelFrame(
            main_frame,
            text="Wyniki optymalizacji",
            padding=10
        )
        result_frame.pack(fill="x")

        self.result_label = ttk.Label(
            result_frame,
            text="Wybierz parametry trasy i uruchom optymalizację.",
            justify="left",
            wraplength=1100
        )
        self.result_label.pack(anchor="w")

    def _open_road_editor(self):
        if self.road_editor is not None and self.road_editor.winfo_exists():
            self.road_editor.lift()
            self.road_editor.focus_force()
            return

        self.road_editor = tk.Toplevel(self.root)
        self.road_editor.title("Edycja warunków drogowych")
        self.road_editor.geometry("720x400")
        self.road_editor.resizable(False, False)
        self.road_editor.configure(bg=self.bg)
        self.road_editor.transient(self.root)

        frame = ttk.Frame(self.road_editor, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Warunki drogowe",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        road_frame = ttk.LabelFrame(
            frame,
            text="Wybrany odcinek",
            padding=10
        )
        road_frame.pack(fill="x")

        self.road_lookup = {}
        road_options = []

        for start, end in self.graph.edges:
            if start < end:
                label = f"{start} ↔ {end}"
                road_options.append(label)
                self.road_lookup[label] = (start, end)

        road_options.sort()

        self.road_var = tk.StringVar()

        ttk.Label(
            road_frame,
            text="Odcinek:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=6)

        self.road_combo = ttk.Combobox(
            road_frame,
            textvariable=self.road_var,
            values=road_options,
            state="readonly",
            width=35
        )
        self.road_combo.grid(
            row=0, column=1, columnspan=3,
            sticky="ew", padx=5, pady=6
        )
        self.road_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self._load_selected_road()
        )

        self.road_closed_var = tk.BooleanVar()

        ttk.Checkbutton(
            road_frame,
            text="Droga zamknięta",
            variable=self.road_closed_var
        ).grid(
            row=0, column=4,
            padx=10, pady=6
        )
 
        self.road_vars = {}

        road_fields = [
            ("traffic_factor", "Natężenie ruchu"),
            ("max_weight_t", "Maksymalna masa (t)"),
            ("max_height_m", "Maksymalna wysokość (m)"),
            ("max_width_m", "Maksymalna szerokość (m)"),
            ("max_length_m", "Maksymalna długość (m)")
        ]

        for index, (key, label) in enumerate(road_fields):
            row = 1 + index // 2
            column = (index % 2) * 2

            ttk.Label(
                road_frame,
                text=label
            ).grid(
                row=row, column=column,
                sticky="w", padx=5, pady=7
            )

            variable = tk.StringVar()
            self.road_vars[key] = variable

            ttk.Entry(
                road_frame,
                textvariable=variable,
                width=14
            ).grid(
                row=row, column=column + 1,
                sticky="ew", padx=5, pady=7
            )

        # Poziom robót drogowych
        ttk.Label(
            road_frame,
            text="Poziom robót drogowych (0–5):"
        ).grid(
            row=4, column=0,
            sticky="w", padx=5, pady=7
        )

        self.roadworks_var = tk.StringVar(value="0")

        self.roadworks_combo = ttk.Combobox(
            road_frame,
            textvariable=self.roadworks_var,
            values=["0", "1", "2", "3", "4", "5"],
            state="readonly",
            width=12
        )
        self.roadworks_combo.grid(
            row=4, column=1,
            sticky="ew", padx=5, pady=7
        )

        self.roadworks_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self._update_roadworks_description()
        )

        self.roadworks_description = ttk.Label(
            frame,
            text="",
            foreground=self.muted,
            wraplength=660,
            justify="left"
        )
        self.roadworks_description.pack(
            anchor="w",
            pady=(8, 5)
        )

        self.road_status = ttk.Label(
            frame,
            text="",
            foreground="#3fb950",
            wraplength=660
        )
        self.road_status.pack(
            anchor="w",
            pady=5
        )

        for column in range(5):
            road_frame.columnconfigure(column, weight=1)

        self._update_roadworks_description()

        self.save_road_button = tk.Button(
            self.road_editor,
            text="ZAPISZ ZMIANY",
            command=self.apply_road_conditions,
            bg="#238636",
            fg="#ffffff",
            activebackground="#2ea043",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=9
        )

        self.save_road_button.place(
            relx=0.97,
            rely=0.96,
            anchor="se"
        )


    def _update_roadworks_description(self):
        descriptions = {
            0: "Brak robót drogowych. Normalna prędkość przejazdu.",
            1: "Bardzo niewielkie utrudnienia. Czas na tym odcinku rośnie o około 10%.",
            2: "Małe roboty drogowe. Czas na tym odcinku rośnie o około 20%.",
            3: "Umiarkowane roboty. Czas na tym odcinku rośnie o około 40%.",
            4: "Duże roboty drogowe. Czas na tym odcinku rośnie o około 70%.",
            5: "Bardzo poważne roboty. Czas na tym odcinku rośnie o około 100%."
        }

        try:
            level = int(self.roadworks_var.get())
            description = descriptions[level]
        except (ValueError, KeyError):
            description = "Wybierz poziom od 0 do 5."

        self.roadworks_description.config(
            text=description
        )


    def _load_selected_road(self):
        label = self.road_var.get()
        self.road_status.config(text="")

        if label not in self.road_lookup:
            return

        start, end = self.road_lookup[label]
        road = self.graph[start][end]

        self.road_closed_var.set(road["closed"])

        self.roadworks_var.set(
            str(road.get("roadworks_level", 0))
        )

        self._update_roadworks_description()

        for key, variable in self.road_vars.items():
            variable.set(str(road[key]))


    def apply_road_conditions(self):
        label = self.road_var.get()

        if label not in self.road_lookup:
            messagebox.showwarning(
                "Brak odcinka",
                "Najpierw wybierz odcinek drogi.",
                parent=self.road_editor
            )
            return

        start, end = self.road_lookup[label]

        try:
            values = {}

            roadworks_level = int(self.roadworks_var.get())

            if roadworks_level not in range(6):
                raise ValueError(
                    "Poziom robót musi wynosić od 0 do 5."
                )

            for key, variable in self.road_vars.items():
                value = float(variable.get().replace(",", "."))

                if not math.isfinite(value) or value <= 0:
                    raise ValueError(
                        "Wszystkie wartości liczbowe muszą być dodatnie."
                    )

                if key == "traffic_factor" and value < 1:
                    raise ValueError(
                        "Współczynnik natężenia ruchu "
                        "nie może być mniejszy niż 1."
                    )

                values[key] = value

            values["roadworks_level"] = roadworks_level

            # Aktualizacja obu kierunków drogi
            for source, destination in ((start, end), (end, start)):
                road = self.graph[source][destination]
                road.update(values)
                road["closed"] = self.road_closed_var.get()

            # Odświeżenie mapy
            self._redraw_map()

            self.result_label.config(
                text=(
                    f"Zmieniono warunki odcinka {start} ↔ {end}. "
                    "Uruchom ponownie optymalizację, "
                    "aby uwzględnić nowe warunki."
                )
            )

            self.road_status.config(
                text=f"✓ Zapisano warunki odcinka {start} ↔ {end}."
            )

        except ValueError as error:
            messagebox.showerror(
                "Nieprawidłowe dane",
                str(error),
                parent=self.road_editor
            )

    def _redraw_map(self, route=None):
        draw_road_network(
            self.graph,
            route=route,
            ax=self.ax
        )

        self.figure.set_facecolor(self.bg)
        self.ax.set_facecolor(self.panel)
        self.canvas.draw()

    def optimize_route(self):
        start = self.start_var.get()
        end = self.end_var.get()
        profile = self.vehicle_var.get()

        if start == end:
            messagebox.showwarning(
                "Nieprawidłowa trasa",
                "Miasto początkowe i docelowe muszą być różne."
            )
            return

        self.optimize_button.config(
            state="disabled",
            text="Optymalizacja..."
        )
        self.root.update_idletasks()

        try:
            vehicle = create_vehicle(profile)

            result = optimize_route(
                graph=self.graph,
                vehicle=vehicle,
                start_city=start,
                end_city=end,
                population_size=50,
                generations=100,
                random_seed=42
            )

            route_text = " → ".join(result.best_route)

            # Lista przejechanych odcinków
            segments = []

            for start_city, end_city in zip(
                result.best_route,
                result.best_route[1:]
            ):
                distance = self.graph[start_city][end_city]["distance_km"]

                segments.append(
                    f"  • {start_city} → {end_city}: {distance} km"
                )

            segments_text = "\n".join(segments)

            self.result_label.config(
                text=(
                    f"Pojazd: {vehicle.name}\n"
                    f"Trasa: {route_text}\n"
                    f"Czas przejazdu: {result.best_time_hours:.2f} h    |    "
                    f"Dystans: {result.best_distance_km:.2f} km    |    "
                    f"Zużycie paliwa: {result.best_fuel_liters:.2f} l\n\n"
                    f"Przejechane odcinki:\n{segments_text}"
                )
            )


            self._redraw_map(route=result.best_route)

        except (ValueError, RuntimeError) as error:
            messagebox.showerror(
                "Błąd optymalizacji",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Nieoczekiwany błąd",
                str(error)
            )

        finally:
            self.optimize_button.config(
                state="normal",
                text="Optymalizuj"
            )


def run_gui():
    root = tk.Tk()
    TruckRouteOptimizerGUI(root)
    root.mainloop()
