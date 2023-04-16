import pickle
from typing import List
import pandas as pd
from pathlib import Path

p = Path(__file__)


def load_model(path: Path = p.parent.joinpath("rf_model.pkl")):
    with open(path, "rb") as f:
        model_open = pickle.load(f)

    return model_open


def predictions(
    model, origin: List[str], month: List[int], airline: List[str]
) -> List[float]:
    df = pd.DataFrame({"Origin": origin, "Month": month, "Airline": airline})

    return list(map(lambda x: round(x * 100, 3), model.predict_proba(df)[0]))
