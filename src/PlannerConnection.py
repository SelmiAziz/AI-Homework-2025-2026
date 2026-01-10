import subprocess
import os

class PlannerConnection:
    """
    Connessione al planner Fast Downward tramite Docker.
    Salva il piano in un file locale sas_plan dentro la cartella benchmarks/
    e lo legge come lista di azioni.
    """

    def __init__(self):
        # cartella benchmarks locale
        self.workdir = os.path.join(os.getcwd(), "benchmarks")
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def run(self, domain_file, problem_file):
        plan_file = os.path.join(self.workdir, "sas_plan")

        # comando Docker: monta la cartella benchmarks locale nel container
        cmd = [
            "sudo", "docker", "run", "--rm",
            "-v", f"{self.workdir}:/benchmarks",
            "aibasel/downward",
            "--alias", "lama-first",
            f"/benchmarks/{domain_file}",
            f"/benchmarks/{problem_file}"
        ]

        try:
            # eseguo il container e redirect stdout su sas_plan nella cartella benchmarks/
            with open(plan_file, "w") as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

            # controllo errori
            if result.returncode != 0:
                print("--- ERRORE FAST DOWNWARD ---")
                print(result.stderr)
                return None

            # leggo il piano dal file sas_plan nella cartella benchmarks/
            if os.path.exists(plan_file):
                with open(plan_file, "r") as f:
                    # filtro linee vuote o commenti
                    plan = [line.strip() for line in f if line.strip() and not line.startswith(";")]
                if plan:
                    return plan
                else:
                    print("Planner eseguito, ma il piano è vuoto.")
                    return None
            else:
                print(f"Planner eseguito, ma sas_plan non trovato in {self.workdir}")
                return None

        except Exception as e:
            print("Errore durante esecuzione planner:", e)
            return None


