import os

class PDDLPlan:
    """
    Legge il file sas_plan o log di Fast Downward nella cartella 'benchmarks'
    e salva solo le azioni reali in un file separato.
    """

    def __init__(self):
        self.plan = []

    # -------------------------------
    def load_plan(self, input_file="sas_plan"):
        """
        Legge il piano dal file e filtra solo le azioni reali.
        """
        # Percorso nella cartella benchmarks locale
        benchmarks_dir = os.path.join(os.getcwd(), "benchmarks")
        path = os.path.join(benchmarks_dir, input_file)

        if not os.path.exists(path):
            print(f"{input_file} non trovato in benchmarks/")
            return

        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Ignora righe informative, commenti o parentesi
                if line.startswith("[") or line.startswith("INFO") or line.startswith("(") or line.startswith(";"):
                    continue

                tokens = line.split()
                if not tokens:
                    continue

                # Considera solo azioni Sokoban reali (es: push-down, move, pull)
                action_name = tokens[0]
                if action_name not in {"push-down", "move", "pull"}:
                    continue

                # player, box e posizioni
                player = tokens[1] if len(tokens) > 1 else None
                box = tokens[2] if len(tokens) > 2 else None
                positions = tokens[3:] if len(tokens) > 3 else []

                # rimuove eventuali (1) finali o simili
                positions = [p for p in positions if not (p.startswith("(") and p.endswith(")"))]

                self.plan.append({
                    "action": action_name,
                    "player": player,
                    "box": box,
                    "positions": positions
                })

    # -------------------------------
    def save_actions(self, output_file="plan_actions.txt"):
        """
        Scrive il piano filtrato in un file testuale in formato PDDL-style.
        """
        if not self.plan:
            print("Nessuna azione da salvare")
            return

        with open(output_file, "w") as f:
            for step in self.plan:
                parts = [step["action"]]
                if step["player"]:
                    parts.append(step["player"])
                if step["box"]:
                    parts.append(step["box"])
                if step["positions"]:
                    parts.extend(step["positions"])

                # Scrive in formato PDDL: tutto tra parentesi
                line = "(" + " ".join(parts) + ")"
                f.write(line + "\n")

        print(f"Piano salvato in {output_file}")

