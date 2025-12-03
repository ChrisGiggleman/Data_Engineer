# gui_tk.py
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from schema import SchemaConfig
from nl_parser import parse_nl_to_intent
from sql_builder import build_sql


class SQLBuilderGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Natural Language → SQL Builder")
        self.geometry("900x600")

        self._init_schema()
        self._build_layout()

    def _init_schema(self):
        # Assume this file lives inside sql_builder/ and schema_config.json is next to it
        base_dir = Path(__file__).resolve().parent
        schema_path = base_dir / "schema_config.json"
        self.schema = SchemaConfig(schema_path)

    def _build_layout(self):
        # Main layout: top = input, middle = buttons + parsed intent, bottom = SQL
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # --- Input frame ---
        input_frame = ttk.LabelFrame(self, text="Natural Language Request")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        self.input_text = tk.Text(input_frame, height=5, wrap="word")
        self.input_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # --- Buttons + Parsed Intent frame ---
        middle_frame = ttk.Frame(self)
        middle_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        middle_frame.columnconfigure(0, weight=0)
        middle_frame.columnconfigure(1, weight=1)
        middle_frame.rowconfigure(0, weight=1)

        # Button column
        button_col = ttk.Frame(middle_frame)
        button_col.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        generate_btn = ttk.Button(button_col, text="Generate SQL", command=self.on_generate_sql)
        generate_btn.pack(fill="x", pady=(0, 5))

        clear_btn = ttk.Button(button_col, text="Clear", command=self.on_clear)
        clear_btn.pack(fill="x")

        # Parsed intent view
        intent_frame = ttk.LabelFrame(middle_frame, text="Parsed Intent")
        intent_frame.grid(row=0, column=1, sticky="nsew")
        intent_frame.columnconfigure(0, weight=1)
        intent_frame.rowconfigure(0, weight=1)

        self.intent_text = tk.Text(intent_frame, height=10, wrap="word", state="disabled")
        self.intent_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # --- SQL output frame ---
        sql_frame = ttk.LabelFrame(self, text="Generated SQL")
        sql_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        sql_frame.columnconfigure(0, weight=1)
        sql_frame.rowconfigure(0, weight=1)

        self.sql_text = tk.Text(sql_frame, height=10, wrap="none")
        self.sql_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Make SQL box a bit nicer with horizontal scroll
        x_scroll = tk.Scrollbar(sql_frame, orient="horizontal", command=self.sql_text.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        self.sql_text.configure(xscrollcommand=x_scroll.set)

    def on_clear(self):
        self.input_text.delete("1.0", tk.END)
        self._set_intent_text("")
        self.sql_text.delete("1.0", tk.END)

    def _set_intent_text(self, content: str):
        self.intent_text.config(state="normal")
        self.intent_text.delete("1.0", tk.END)
        self.intent_text.insert("1.0", content)
        self.intent_text.config(state="disabled")

    def on_generate_sql(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("No input", "Please enter a natural language request.")
            return

        try:
            intent = parse_nl_to_intent(prompt, self.schema)
            sql = build_sql(intent, self.schema)

            # Show intent in a human-friendly way
            intent_lines = [
                f"Entity:   {intent.entity}",
                f"Fields:   {intent.fields}",
                f"Distinct: {intent.distinct}",
            ]
            if intent.filters:
                intent_lines.append("Filters:")
                for f in intent.filters:
                    intent_lines.append(f"  - {f.field} {f.operator} {f.value}")
            if intent.sort:
                intent_lines.append("Sort:")
                for s in intent.sort:
                    intent_lines.append(f"  - {s.field} {s.direction}")
            if intent.limit is not None:
                intent_lines.append(f"Limit:   {intent.limit}")

            self._set_intent_text("\n".join(intent_lines))

            # Show SQL
            self.sql_text.delete("1.0", tk.END)
            self.sql_text.insert("1.0", sql)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate SQL:\n\n{e}")


def main():
    app = SQLBuilderGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
