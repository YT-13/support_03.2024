from issues.models import Issue


def main():
    issues = Issue.object.all()
    print(issues)


if __name__ == "__main__":
    main()
