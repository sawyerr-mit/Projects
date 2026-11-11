# Projects
Hello, I'm Sawyer Rooney, an MIT student. Here is my personal GitHub where I keep track of all my current and past projects.

## Setup
Requires Python 3.10+

```
pip install -r requirements.txt
```

Each script can be run from any directory, e.g. `python "Connect-4 AI/Connect4.py"`.

| Folder | Run |
| --- | --- |
| Connect-4 AI | `python Connect4.py` (click a column to drop a piece) |
| Djikstra's Algorithm | `jupyter notebook visualize.ipynb` (BFS / Dijkstra / A* on the included graphs. You may need to download some extra dependencies if you want to re-run) |
| MNIST Neural Network | `python testing.py --file 2025_10_21_0x1_Kleki.png` (uses the included `trained_params.pkl`; add `--invert` for black-on-white images). `python neuralNet.py` retrains the network and needs `tensorflow` to download MNIST |
| QR Factorization Polynomial Solver | `python QRFactorization.py` |
| RFC for Hazardous Asteroids | open `NASA_Asteroid_Hazard_Classifier.ipynb`; needs your own API keys, see below |
| SVD Image Compression | `python image_compression.py` (you need to edit the image path if you want to run on your own images) |

## API keys (RFC for Hazardous Asteroids notebook)
The notebook reads keys from an environment variable (paste your personal keys over the placeholders in the notebook):

- `NASA_API_KEY`: free from https://api.nasa.gov

Set before launching Jupyter: `export NASA_API_KEY=...`.
