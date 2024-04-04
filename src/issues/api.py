import random
import string
from django.http import HttpRequest, JsonResponse
from issues.models import Issue


def get_issues(request: HttpRequest) -> JsonResponse:
    # issues = Issue.objects.create()
    # issues = Issue.objects.update()
    # issues = Issue.objects.get()
    # issues = Issue.objects.delete()
    issues: list[Issue] = Issue.objects.all()

    results: list[dict] = [
        {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "junior_id": issue.junior_id,
            "senior_id": issue.senior_id,
        }
        for issue in issues
    ]

    return JsonResponse(data={"results": results})


def _random_string(length: HttpRequest) -> JsonResponse:
    return "".join(
        [random.choice(string.ascii_letters) for i in range(length)]
    )


def create_issues(request: HttpRequest) -> JsonResponse:
    issue = Issue.objects.create(
        tittle=_random_string(20),
        body=_random_string(30),
        senior_id=1,
        junior_id=2,
    )

    result = {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "junior_id": issue.junior_id,
        "senior_id": issue.senior_id,
    }

    return JsonResponse(data=result)