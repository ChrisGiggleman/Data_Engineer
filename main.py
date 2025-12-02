# main.py
from pathlib import Path

from schema import SchemaConfig
from nl_parser import parse_nl_to_intent
from sql_builder import build_sql


def main():
    base_dir = Path(__file__).resolve().parent
    schema_path = base_dir / "schema_config.json"
    schema = SchemaConfig(schema_path)

    print("Natural Language → SQL Builder")
    print("Type your data request (blank line to exit).")
    print("-" * 60)

    while True:
        print("\nEnter your request:")
        user_input_lines = []
        while True:
            try:
                line = input("> ")
            except EOFError:
                line = ""
            if not line.strip():
                break
            user_input_lines.append(line)

        prompt = "\n".join(user_input_lines).strip()
        if not prompt:
            print("Goodbye.")
            break

        try:
            intent = parse_nl_to_intent(prompt, schema)
            sql = build_sql(intent, schema)

            print("\n--- Parsed intent ---")
            print(f"Entity:   {intent.entity}")
            print(f"Fields:   {intent.fields}")
            print(f"Distinct: {intent.distinct}")
            if intent.filters:
                print("Filters:")
                for f in intent.filters:
                    print(f"  - {f.field} {f.operator} {f.value}")
            if intent.sort:
                print("Sort:")
                for s in intent.sort:
                    print(f"  - {s.field} {s.direction}")
            if intent.limit is not None:
                print(f"Limit:    {intent.limit}")

            print("\n--- Generated SQL ---")
            print(sql)
            print("---------------------")
            print("Copy this SQL into your system to run it.")

        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()
