
import tkinter as tk
import math
import queue
import re
import threading

from tkinter import ttk, messagebox

from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from truck_route_optimizer.experiments import run_experiments
from truck_route_optimizer.experiment_visualization import (
    save_experiment_results,
)
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
        
        self.experiment_queue = queue.Queue()
        self.experiment_running = False

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

        
        # Własny układ Combobox z dokładnie jednym przyciskiem strzałki.
        style.layout(
            "Single.TCombobox",
            [
                (
                    "Combobox.field",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "Combobox.downarrow",
                                {
                                    "side": "right",
                                    "sticky": "ns"
                                }
                            ),
                            (
                                "Combobox.padding",
                                {
                                    "sticky": "nswe",
                                    "children": [
                                        (
                                            "Combobox.textarea",
                                            {"sticky": "nswe"}
                                        )
                                    ]
                                }
                            )
                        ]
                    }
                )
            ]
        )

        style.configure(
            "Single.TCombobox",
            fieldbackground=self.input_bg,
            background=self.input_bg,
            foreground=self.fg,
            arrowcolor=self.fg,
            bordercolor=self.border,
            padding=6
        )

        style.map(
            "Single.TCombobox",
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


    def _update_vehicle_information(self, event=None):
        """Aktualizuje informacje o wybranym pojeździe."""
        profile = self.vehicle_var.get()

        if not profile:
            return

        vehicle = create_vehicle(profile)

        information = (
            f"Masa własna: {vehicle.curb_weight_kg / 1000:.2f} t"
            f"    |    Ładunek: {vehicle.payload_kg / 1000:.2f} t"
            f"    |    Masa całkowita: {vehicle.gross_weight_kg / 1000:.2f} t"
            f"    |    DMC: {vehicle.max_gross_weight_kg / 1000:.2f} t\n"
            f"Wysokość: {vehicle.height_m:.2f} m"
            f"    |    Szerokość: {vehicle.width_m:.2f} m"
            f"    |    Długość: {vehicle.length_m:.2f} m"
            f"    |    Spalanie: {vehicle.fuel_consumption_l_100km:.1f} l/100 km"
        )

        self.vehicle_information_label.config(text=information)


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
            style="Single.TCombobox",
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
            style="Single.TCombobox",
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
            style="Single.TCombobox",
            width=22
        )
        self.vehicle_combo.grid(
            row=0, column=5,
            sticky="ew", padx=5, pady=5
        )
        self.vehicle_combo.current(0)


        self.vehicle_combo.bind(
            "<<ComboboxSelected>>",
            self._update_vehicle_information
        )

        self.vehicle_information_label = ttk.Label(
            settings_frame,
            text="",
            justify="left",
            foreground=self.muted,
            wraplength=1100
        )
        self.vehicle_information_label.grid(
            row=1,
            column=0,
            columnspan=8,
            sticky="w",
            padx=5,
            pady=(8, 4)
        )

        self._update_vehicle_information()

        self.optimize_button = ttk.Button(
            settings_frame,
            text="Optymalizuj",
            style="Accent.TButton",
            command=self.optimize_route,
            width=18
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

        # Wyniki pod mapą - przewijany panel
        result_frame = ttk.LabelFrame(
            main_frame,
            text="Wyniki optymalizacji",
            padding=8
        )
        result_frame.pack(fill="x")

        result_container = tk.Frame(
            result_frame,
            bg=self.bg
        )
        result_container.pack(fill="both", expand=True)

        # Canvas umożliwiający przewijanie zawartości
        self.result_canvas = tk.Canvas(
            result_container,
            bg=self.bg,
            highlightthickness=0,
            height=135
        )
        self.result_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Pionowy pasek przewijania
        self.result_scrollbar = ttk.Scrollbar(
            result_container,
            orient="vertical",
            command=self.result_canvas.yview
        )
        self.result_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_canvas.configure(
            yscrollcommand=self.result_scrollbar.set
        )

        # Wewnętrzny kontener na tekst wyników
        self.result_content = tk.Frame(
            self.result_canvas,
            bg=self.bg
        )

        self.result_window = self.result_canvas.create_window(
            (0, 0),
            window=self.result_content,
            anchor="nw"
        )

        self.result_label = ttk.Label(
            self.result_content,
            text="Wybierz parametry trasy i uruchom optymalizację.",
            justify="left",
            wraplength=1100
        )
        self.result_label.pack(
            anchor="w",
            fill="x",
            padx=5,
            pady=5
        )

        # Aktualizacja obszaru przewijania po zmianie zawartości
        self.result_content.bind(
            "<Configure>",
            self._update_result_scroll_region
        )

        # Dopasowanie szerokości tekstu do panelu
        self.result_canvas.bind(
            "<Configure>",
            self._resize_result_content
        )

        # Obsługa kółka myszy
        self.result_canvas.bind(
            "<Enter>",
            self._bind_result_mousewheel
        )
        self.result_canvas.bind(
            "<Leave>",
            self._unbind_result_mousewheel
        )

    def _update_result_scroll_region(self, event=None):
        """Aktualizuje obszar przewijania wyników."""

        self.result_canvas.configure(
            scrollregion=self.result_canvas.bbox("all")
        )

    def _resize_result_content(self, event):
        """Dopasowuje szerokość zawartości do panelu."""

        self.result_canvas.itemconfigure(
            self.result_window,
            width=event.width
        )

        self.result_label.configure(
            wraplength=max(100, event.width - 15)
        )


    def _bind_result_mousewheel(self, event=None):
        """Włącza przewijanie tylko dla panelu wyników."""
        widgets = (
            self.result_canvas,
            self.result_content,
            self.result_label
        )

        for widget in widgets:
            widget.bind("<MouseWheel>", self._on_result_mousewheel)
            widget.bind("<Button-4>", self._on_result_mousewheel)
            widget.bind("<Button-5>", self._on_result_mousewheel)

    def _unbind_result_mousewheel(self, event=None):
        """Usuwa lokalne powiązania przewijania."""
        widgets = (
            self.result_canvas,
            self.result_content,
            self.result_label
        )

        for widget in widgets:
            widget.unbind("<MouseWheel>")
            widget.unbind("<Button-4>")
            widget.unbind("<Button-5>")

    def _on_result_mousewheel(self, event):
        """Przewija panel wyników."""
        if event.num == 4:
            self.result_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.result_canvas.yview_scroll(1, "units")
        else:
            self.result_canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )

        return "break"
    
    def _set_result_text(self, text):
        """Aktualizuje wyniki i przewija panel na początek."""
        self.result_label.config(text=text)

        self.result_content.update_idletasks()

        self.result_canvas.configure(
            scrollregion=self.result_canvas.bbox("all")
        )

        self.result_canvas.yview_moveto(0)

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
            style="Single.TCombobox",
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
            style="Single.TCombobox",
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

            self._set_result_text(
                (
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


    def _create_experiment_directory(self, start, end):
        """Tworzy unikalny katalog dla kolejnego eksperymentu."""

        results_root = (
            Path(__file__).resolve().parents[2]
            / "experiment_results"
        )

        results_root.mkdir(parents=True, exist_ok=True)

        # Usunięcie znaków niedozwolonych w nazwach Windows.
        route_name = f"{start} - {end}"
        route_name = re.sub(
            r'[<>:"/\\|?*]',
            "-",
            route_name,
        ).strip(" .")

        experiment_number = 1

        while True:
            directory = (
                results_root
                / f"{route_name} #{experiment_number:03d}"
            )

            if not directory.exists():
                return directory

            experiment_number += 1


    def _build_experiment_parameters(self, graph, vehicle, start, end):
        """Tworzy kompletny zapis konfiguracji eksperymentu."""

        parameters = {
            "runs": 10,
            "base_seed": 42,
            "population_size": 50,
            "generations": 100,
            "crossover_probability": 0.8,
            "mutation_probability": 0.2,
            "elite_size": 2,
            "tournament_size": 3,

            "start_city": start,
            "end_city": end,
            "vehicle": vars(vehicle).copy(),

            # Pełna topologia grafu wraz z atrybutami miast.
            "nodes": [
                {
                    "name": node,
                    "attributes": dict(attributes),
                }
                for node, attributes in graph.nodes(data=True)
            ],

            # Wszystkie skierowane krawędzie.
            # Drogi dwukierunkowe są zapisane w obu kierunkach.
            "edges": [
                {
                    "start": source,
                    "end": destination,
                    "attributes": dict(attributes),
                }
                for source, destination, attributes
                in graph.edges(data=True)
            ],
        }

        return parameters


    def _finish_experiment(self, result, parameters, output_dir):
        """Zapisuje wyniki i aktualizuje GUI."""

        try:
            save_experiment_results(
                result=result,
                output_dir=output_dir,
                base_seed=parameters["base_seed"],
                parameters=parameters,
            )

            best = result.best_result
            vehicle = create_vehicle(parameters["vehicle"]["name"])

            route_text = " → ".join(best.best_route)

            segments = []

            for start_city, end_city in zip(
                best.best_route,
                best.best_route[1:],
            ):
                distance = self.graph[start_city][end_city]["distance_km"]

                segments.append(
                    f"  • {start_city} → {end_city}: {distance:.2f} km"
                )

            segments_text = "\n".join(segments)

            run_number = next(
                (
                    index + 1
                    for index, run in enumerate(result.runs)
                    if run is best
                ),
                None,
            )

            self._set_result_text(
                (
                    f"EKSPERYMENT ZAKOŃCZONY\n\n"
                    f"Pojazd: {vehicle.name}\n"
                    f"Trasa: {route_text}\n"
                    f"Czas przejazdu: {best.best_time_hours:.2f} h    |    "
                    f"Dystans: {best.best_distance_km:.2f} km    |    "
                    f"Zużycie paliwa: {best.best_fuel_liters:.2f} l\n"
                    f"Najlepszy przebieg: {run_number} / {len(result.runs)}\n"
                    f"Ziarna losowości: "
                    f"{parameters['base_seed']}–"
                    f"{parameters['base_seed'] + len(result.runs) - 1}\n\n"
                    f"Przejechane odcinki:\n{segments_text}\n\n"
                    f"Wyniki zapisano w:\n{output_dir}"
                )
            )

            self._redraw_map(route=best.best_route)

            messagebox.showinfo(
                "Eksperyment zakończony",
                (
                    f"Przeprowadzono {len(result.runs)} przebiegów.\n\n"
                    f"Najlepszy czas: {best.best_time_hours:.2f} h\n"
                    f"Najlepsze zużycie paliwa: "
                    f"{best.best_fuel_liters:.2f} l\n\n"
                    f"Wyniki zapisano w:\n{output_dir}"
                ),
            )

        except Exception as error:
            messagebox.showerror(
                "Błąd zapisywania wyników",
                str(error),
            )


    def _poll_experiment_queue(self):
        """Odbiera wynik pracy wątku bez blokowania GUI."""

        try:
            status, payload = self.experiment_queue.get_nowait()

        except queue.Empty:
            if self.experiment_running:
                self.root.after(100, self._poll_experiment_queue)

            return

        self.experiment_running = False

        self.optimize_button.config(
            state="normal",
            text="Optymalizuj",
        )

        if status == "error":
            messagebox.showerror(
                "Błąd eksperymentu",
                str(payload),
            )
            return

        result, parameters, output_dir = payload

        self._finish_experiment(
            result,
            parameters,
            output_dir,
        )


    def optimize_route(self):
        """Uruchamia serię 10 niezależnych eksperymentów."""

        if self.experiment_running:
            return

        start = self.start_var.get()
        end = self.end_var.get()
        profile = self.vehicle_var.get()

        if start == end:
            messagebox.showwarning(
                "Nieprawidłowa trasa",
                "Miasto początkowe i docelowe muszą być różne.",
            )
            return

        try:
            vehicle = create_vehicle(profile)

            # Kopia grafu zabezpiecza eksperyment przed zmianami
            # warunków drogowych dokonywanymi później w GUI.
            experiment_graph = self.graph.copy()

            parameters = self._build_experiment_parameters(
                experiment_graph,
                vehicle,
                start,
                end,
            )

            output_dir = self._create_experiment_directory(
                start,
                end,
            )

        except Exception as error:
            messagebox.showerror(
                "Błąd przygotowania eksperymentu",
                str(error),
            )
            return

        self.experiment_running = True

        self.optimize_button.config(
            state="disabled",
            text="Eksperyment trwa...",
        )

        self._set_result_text(
            (
                f"Trwa eksperyment: {start} → {end}\n\n"
                f"Pojazd: {vehicle.name}\n"
                f"Liczba przebiegów: {parameters['runs']}\n"
                f"Populacja: {parameters['population_size']}\n"
                f"Liczba pokoleń: {parameters['generations']}\n"
                f"Ziarna losowości: "
                f"{parameters['base_seed']}–"
                f"{parameters['base_seed'] + parameters['runs'] - 1}\n\n"
                "Proszę czekać. Wyniki zostaną zapisane automatycznie."
            )
        )

        def worker():
            try:
                result = run_experiments(
                    graph=experiment_graph,
                    vehicle=vehicle,
                    start_city=start,
                    end_city=end,
                    runs=parameters["runs"],
                    base_seed=parameters["base_seed"],
                    population_size=parameters["population_size"],
                    generations=parameters["generations"],
                    crossover_probability=parameters["crossover_probability"],
                    mutation_probability=parameters["mutation_probability"],
                    elite_size=parameters["elite_size"],
                    tournament_size=parameters["tournament_size"],
                )

                self.experiment_queue.put(
                    (
                        "success",
                        (result, parameters, output_dir),
                    )
                )

            except Exception as error:
                self.experiment_queue.put(
                    ("error", error)
                )

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

        self.root.after(
            100,
            self._poll_experiment_queue,
        )

def run_gui():
    root = tk.Tk()
    TruckRouteOptimizerGUI(root)
    root.mainloop()
