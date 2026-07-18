import json

from pandas import DataFrame

from app.services.recommendations.models import RecommendationsSnapshot


def _serialize_frame(frame: DataFrame | None) -> dict | None:
    if frame is None:
        return None
    return json.loads(frame.to_json(orient="split", date_format="iso"))


def map_recommendations(
    ticker: str, recommendations: dict[str, DataFrame | None]
) -> RecommendationsSnapshot:
    return RecommendationsSnapshot(
        ticker=ticker.upper(),
        recommendations=_serialize_frame(recommendations["recommendations"]),
        recommendations_summary=_serialize_frame(recommendations["recommendations_summary"]),
        upgrades_downgrades=_serialize_frame(recommendations["upgrades_downgrades"]),
    )
