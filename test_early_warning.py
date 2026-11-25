from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from early_warning import get_warning

SNAPSHOT = (
    "Sprint ends in 2 days. 3 of 5 tickets are still 'In Progress'. "
    "Ana wrote 'waiting on API access' in her last 3 standups."
)


def test_warning_is_relevant():
    # 1. Run the app (black-box: we only look at input and output)
    output = get_warning(SNAPSHOT)

    # 2. Package input + output as a test case
    test_case = LLMTestCase(input=SNAPSHOT, actual_output=output)

    # 3. The judge (Gemini) scores how relevant the answer is, from 0 to 1
    metric = AnswerRelevancyMetric(threshold=0.7)

    # 4. Fail the test if the score is below 0.7
    assert_test(test_case, [metric])
