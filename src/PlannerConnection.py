import subprocess
import os

class PlannerConnection:
    """
    Connector IDENTICO al comando shell:
    sudo docker run --rm \
      -v "$(pwd)":/benchmarks \
      aibasel/downward \
      --alias lama-first \
      --plan-file /benchmarks/plan.txt \
      /benchmarks/problem
    """

    def __init__(self):
        self.workdir = os.getcwd()  # == $(pwd)

    def run(self):
        plan_file = os.path.join(self.workdir, "plan.txt")

        cmd = [
            "sudo", "docker", "run", "--rm",
            "-v", f"{self.workdir}:/benchmarks",
            "aibasel/downward",
            "--alias", "lama-first",
            "--plan-file", "/benchmarks/plan.txt",
            "/benchmarks/problem.pddl"
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print("ERRORE FAST DOWNWARD:")
            print(result.stderr)
            return None

        if not os.path.exists(plan_file):
            print("plan.txt NON trovato")
            return None

        with open(plan_file) as f:
            return [
                line.strip()
                for line in f
                if line.strip() and not line.startswith(";")
            ]
