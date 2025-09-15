# acr-target-branch-blocked

Arquivo config.json

```json
{
    "data": {
        "description": "Não é possível entregar correções nesta branch porque ela já está no status `${STATUS}`<br>Ou seja, a correção deve ser entregue na branch `${CORRECT_BRANCH}`<br>Em caso de dúvida verifique com seu LT",
        "provider": "JIRA",
        "providerData": {
            "jiraUrl": "",
            "jiraToken": "",
            "boardId": 0
        },
        "blocks": [
            {
                "status": "HOMOLOGAÇÃO",
                "correctBranch": "homolog"
            }
        ]
    },
    "path_output": "output.json",
    "merge": {
        "branch": {
            "target": "branch-name"
        }
    }
}
```
