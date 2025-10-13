import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATA_DIR = os.path.join(BASE_DIR, "data")


PROJECT_CSV_PATH = os.path.join(DATA_DIR, "project.csv")
ADDRESS_CSV_PATH = os.path.join(DATA_DIR, "ProjectAddress.csv")
CONFIG_CSV_PATH = os.path.join(DATA_DIR, "ProjectConfiguration.csv")
VARIANT_CSV_PATH = os.path.join(DATA_DIR, "ProjectConfigurationVariant.csv")

MAX_RESULTS_TO_DISPLAY = 10