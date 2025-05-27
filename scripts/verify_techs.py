import yaml
import pandas as pd
import requests
import io

# URLs and file paths
costs_csv_url = "https://raw.githubusercontent.com/PyPSA/technology-data/master/outputs/costs_2050.csv"
yaml_files = ["configs/config_47tech.yaml", "configs/config_148tech.yaml"]

# Load cost data from the online PyPSA GitHub repo
response = requests.get(costs_csv_url)
if response.status_code != 200:
    raise RuntimeError("Failed to fetch costs file from PyPSA repository.")

cost_df = pd.read_csv(io.StringIO(response.text))
cost_techs = set(cost_df["technology"].str.strip().unique())

# Function to verify technologies in YAML files
def verify_technologies(yaml_file, cost_techs):
    print(f"\nChecking technologies in '{yaml_file}':")
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)

    extendable_carriers = config.get("electricity", {}).get("extendable_carriers", {})
    all_techs = []
    for category, tech_list in extendable_carriers.items():
        all_techs.extend(tech_list)

    for tech in all_techs:
        if tech in cost_techs:
            print(f"✅ {tech}: WORKS")
        elif tech.strip() in cost_techs:
            print(f"❌ {tech}: ERROR (Whitespace Issue)")
        elif tech.lower() in (t.lower() for t in cost_techs):
            print(f"❌ {tech}: ERROR (Case sensitivity issue)")
        else:
            print(f"❌ {tech}: ERROR (Not found in costs_2050.csv)")

# Run verification for each YAML file
for yaml_file in yaml_files:
    verify_technologies(yaml_file, cost_techs)
