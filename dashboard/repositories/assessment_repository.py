from dashboard.domain.assessment import Assessment


class AssessmentRepository:

    def __init__(self):

        self._assessments = {}

    def add(self, assessment: Assessment):

        self._assessments[
            assessment.assessment_id
        ] = assessment

    def get(self, assessment_id: str):

        return self._assessments.get(
            assessment_id
        )

    def list(self):

        return list(
            self._assessments.values()
        )


repository = AssessmentRepository()
