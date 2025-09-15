import automatic_code_review_commons as commons
import re
import requests
import os


def review(config):
    config_data = config['data']
    branch_name = config['merge']['branch']['target']
    
    print(f"acr-target-branch-blocked Verificando branch {branch_name}")

    if config_data['provider'] == "JIRA":
        print(f"acr-target-branch-blocked Verificando branch {branch_name} no jira")
        provider_data = config_data['providerData']

        status = _get_status_by_jira(
            basic_token=_get_by_config_or_enviroment(provider_data, 'jiraToken', 'JIRA_API_TOKEN'), 
            base_url=provider_data['jiraUrl'], 
            board_id=provider_data['boardId'], 
            branch_name=branch_name
        )
    else:
        status = ""
    
    print(f"acr-target-branch-blocked Status da branch {status}")

    comments = []

    if status == "":
        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id( "UNIQUE_ID" ),
            comment_path=None,
            comment_description="Não foi possível pegar o status da branch",
            comment_snipset=False,
            comment_end_line=None,
            comment_start_line=None,
            comment_language=None,
        ))

    else:
        blocks = config_data['blocks']

        for block in blocks:
            if status != block['status']:
                continue

            comment_description = config_data['description']
            comment_description = comment_description.replace("${STATUS}", block['status'])
            comment_description = comment_description.replace("${CORRECT_BRANCH}", block['correctBranch'])

            comments.append(commons.comment_create(
                comment_id=commons.comment_generate_id( "UNIQUE_ID" ),
                comment_path=None,
                comment_description=comment_description,
                comment_snipset=False,
                comment_end_line=None,
                comment_start_line=None,
                comment_language=None,
            ))
    
    print(f"acr-target-branch-blocked Quantidade de comentários gerados é de {len(comments)}")

    for comment in comments:
        print(f"acr-target-branch-blocked Comentário: {comment['comment']}")

    return comments


def _get_status_by_jira(
    basic_token: str,
    base_url: str,
    board_id: int,
    branch_name: str
) -> any:
    branch_for_jql = re.sub(r'[-/]+', ' ', branch_name).strip()

    jql = f'summary ~ "{branch_for_jql}" ORDER BY updated DESC'
    url = f"{base_url.rstrip('/')}/rest/agile/1.0/board/{board_id}/issue"
    headers = {
        "Authorization": f"Basic {basic_token}",
        "Accept": "application/json",
    }
    params = {
        "jql": jql,
        "fields": "status,summary",
    }

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()

    objs = resp.json()

    for obj in objs['issues']:
        fields = obj['fields']

        if fields['summary'] == branch_name:
            return fields['status']['name']
    
    return ""


def _get_by_config_or_enviroment(obj, obj_key, enviroment_key):
    if obj_key in obj:
        return obj[obj_key]

    return os.environ.get(enviroment_key)
