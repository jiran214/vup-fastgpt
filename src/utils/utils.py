from typing import List

from pydantic import BaseModel
from scipy import spatial


class Record(BaseModel):
    event: dict
    prompt: str
    speech: str
    action: str
    time: str



def top_n_indices_from_embeddings(
        query_embedding: List[float],
        embeddings: List[List[float]],
        distance_metric="cosine",
        top=1
) -> list:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    top_n_indices = np.argsort(distances)[:top]
    return top_n_indices