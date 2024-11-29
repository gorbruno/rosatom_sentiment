from jira import JIRA
from settings.app_settings import settings

jira = JIRA(basic_auth=(settings.JIRA_LOGIN, settings.JIRA_PASSWORD), server=settings.JIRA_SERVER)


def search_all_comments_in_issue(issue_key):
    """Return dict with all issue key is name autor of comment, value is list with all comment this autor.
    Function accepts an object of type issue."""
    issue = jira.issue(issue_key)

    all_comment_in_issue = {
        'task_id': issue.id,
        'task_name': issue.key,
        'creation_date': issue.fields.created,
        'messages': [

        ]
    }
    if len(issue.fields.comment.comments):
        for comment in issue.fields.comment.comments:
            all_comment_in_issue['messages'].append(
                {
                    'text': comment.body,
                    'message_id': comment.id,
                    'publication_date': comment.created,
                    'user_id': comment.author.name
                }
            )

    return all_comment_in_issue


def serch_all_issue_in_project(project_key):
    """return all issue in project. Function accepts names of project type string."""
    all_issue = jira.search_issues('project=' + project_key)
    return all_issue


def serch_all_projects():
    """return list of name all projects on jira. function accpets object type jira."""
    return jira.projects()


def search_all_comment_in_project(project_key):
    """return dict key = author name of comment value = list of all coment. Function accept name project type string"""
    all_issue = jira.search_issues('project=' + project_key)
    all_comment = {}
    for issue in all_issue:
        if issue.name not in all_comment:
            all_comment[issue.name] = [issue.body]
        else:
            all_comment[issue.name].append(issue.body)
    return all_issue
