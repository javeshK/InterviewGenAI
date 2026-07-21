"""
evaluation_service.py

Responsible for validating and normalizing AI evaluation results.

Responsibilities
----------------
- Validate Gemini JSON output
- Fill missing values
- Clamp scores to valid ranges
- Calculate overall score if missing
- Return a consistent dictionary
"""

from typing import Any


class EvaluationService:

    REQUIRED_FIELDS = [
        "technical_score",
        "communication_score",
        "confidence_score",
        "overall_score",
        "ideal_answer",
        "feedback",
    ]

    @staticmethod
    def _clamp_score(value: Any) -> float:
        """
        Convert a score to float and clamp between 0 and 10.
        """

        try:
            score = float(value)
        except (TypeError, ValueError):
            return 0.0

        return max(0.0, min(10.0, score))

    @classmethod
    def validate(
        cls,
        evaluation: dict
    ) -> dict:
        """
        Validate and normalize Gemini evaluation output.
        """

        if not isinstance(evaluation, dict):
            raise ValueError(
                "Evaluation must be a dictionary."
            )

        for field in cls.REQUIRED_FIELDS:

            if field not in evaluation:

                evaluation[field] = ""

        technical = cls._clamp_score(
            evaluation.get("technical_score")
        )

        communication = cls._clamp_score(
            evaluation.get("communication_score")
        )

        confidence = cls._clamp_score(
            evaluation.get("confidence_score")
        )

        overall = evaluation.get("overall_score")

        if overall in ("", None):

            overall = (
                technical +
                communication +
                confidence
            ) / 3

        overall = cls._clamp_score(overall)

        evaluation["technical_score"] = technical
        evaluation["communication_score"] = communication
        evaluation["confidence_score"] = confidence
        evaluation["overall_score"] = overall

        evaluation["ideal_answer"] = str(
            evaluation.get(
                "ideal_answer",
                ""
            )
        ).strip()

        evaluation["feedback"] = str(
            evaluation.get(
                "feedback",
                ""
            )
        ).strip()

        return evaluation

    @staticmethod
    def average_score(
        evaluations: list[dict]
    ) -> float:
        """
        Calculate average overall score.
        """

        if not evaluations:
            return 0.0

        total = sum(
            e["overall_score"]
            for e in evaluations
        )

        return round(
            total / len(evaluations),
            2
        )

    @staticmethod
    def average_technical(
        evaluations: list[dict]
    ) -> float:

        if not evaluations:
            return 0.0

        return round(
            sum(
                e["technical_score"]
                for e in evaluations
            ) / len(evaluations),
            2
        )

    @staticmethod
    def average_communication(
        evaluations: list[dict]
    ) -> float:

        if not evaluations:
            return 0.0

        return round(
            sum(
                e["communication_score"]
                for e in evaluations
            ) / len(evaluations),
            2
        )

    @staticmethod
    def average_confidence(
        evaluations: list[dict]
    ) -> float:

        if not evaluations:
            return 0.0

        return round(
            sum(
                e["confidence_score"]
                for e in evaluations
            ) / len(evaluations),
            2
        )
    
    def validate_evaluation(self, evaluation: dict) -> None:
        """
        Validates Gemini evaluation response.
        """

        required_fields = [
            "technical_score",
            "communication_score",
            "confidence_score",
            "overall_score",
            "feedback",
            "ideal_answer",
        ]

        for field in required_fields:
            if field not in evaluation:
                raise ValueError(
                    f"Missing evaluation field: {field}"
                )

        score_fields = [
            "technical_score",
            "communication_score",
            "confidence_score",
            "overall_score",
        ]

        for field in score_fields:
            if not isinstance(evaluation[field], (int, float)):
                raise ValueError(
                    f"{field} must be numeric."
                )