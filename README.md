# Projects
Here are all my projects!

## Setup
Requires Python 3.10+ (the Dijkstra project uses `X | None` type hints).

```
pip install -r requirements.txt
```

Each script can be run from any directory, e.g. `python "Connect-4 AI/Connect4.py"`.

| Folder | Run |
| --- | --- |
| Connect-4 AI | `python Connect4.py` (click a column to drop a piece) |
| Djikstra's Algorithm | `python search.py` (BFS / Dijkstra / A* on the included graphs) |
| MNIST Neural Network | `python testing.py --file 2025_10_21_0x1_Kleki.png` (uses the included `trained_params.pkl`; add `--invert` for black-on-white images). `python neuralNet.py` retrains the network and needs `tensorflow` to download MNIST |
| QR Factorization Polynomial Solver | `python QRFactorization.py` |
| RFC for Hazardous Asteroids | open `Assignment04.ipynb`; needs your own API keys, see below |
| SVD Image Compression | `python image_compression.py` (reads `cat.jpg`, writes the output images next to the script) |

## API keys (RFC for Hazardous Asteroids notebook)
The notebook reads keys from environment variables (or you can paste them over the placeholders in the notebook):

- `RAPIDAPI_KEY`: from https://rapidapi.com (subscribe to the exchangerate-api and yahoo-finance15 APIs)
- `NASA_API_KEY`: free from https://api.nasa.gov

Set them before launching Jupyter, e.g. `export RAPIDAPI_KEY=...` and `export NASA_API_KEY=...`.
