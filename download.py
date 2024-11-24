from kagglehub import dataset_download
from shutil import move

p = dataset_download("nikhileswarkomati/suicide-watch")
print(f"path: {p}")
move(f"{p}/Suicide_Detection.csv", "data.csv")
print("moved to data.csv")
