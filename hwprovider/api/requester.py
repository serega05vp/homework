import requests
from django.conf import settings

host_url = settings.HOST_URL
PROD_AIU_API = settings.PROD_AIU_API

def aiu_auth_token(login, password):
    # Получение токена
    headers = {"Content-Type": "application/json"}
    json_response = requests.post(PROD_AIU_API + 'login_check', headers=headers,
                                  data='{"username":"' + login + '","password":"' + password + '"}')  # Отправляем post-запрос на сервер
    return json_response.json()['token']


def aiu_hw_assign(access_token, student_email, hw_id):
    # получение id пользователя
    RUSERS = PROD_AIU_API + 'v2/users'
    headers = {"Content-Type": "application/json", "Authorization": 'Bearer {}'.format(access_token)}
    json_response = requests.get(RUSERS, headers=headers, params = {'username': f'{student_email}'})
    data = json_response.json()
    if data['hydra:totalItems'] == 0:
        return {'answer' : -1}
    user_id = data['hydra:member'][0]['id']

    # проверка на наличие домашки
    # hw_check = requests.get(PROD_AIU_API + 'v2/homework_results/' + str(hw_id), headers=headers)

    # if hw_check.status_code == 200:
    #     return {'answer' : -2}

    # Зачет ДЗ
    curator_id = 93854
    RHW = PROD_AIU_API + 'v2/homework_results'
    params = {
        "homework": f"/api/v2/homework/{hw_id}",
        "description": "",
        "student": f"/api/v2/users/{user_id}",
        "canComment": True,
        "vision": 0,
        "points": 1,
        "status": 4,
        "curator": f"/api/v2/users/{curator_id}"
    }
    response = requests.post(RHW, headers=headers, json=params)
    homeworkResult = response.json()['@id']


    # Добавление комментария
    RHWR = PROD_AIU_API + 'v2/comment_tree_homework_results'
    params = {
        "homeworkResult": homeworkResult,
        "forEvaluation": True,
        "author": f"/api/v2/users/{curator_id}",
        "text": "Всё верно! Ваша работа принята!"
    }
    comment_response = requests.post(RHWR, headers=headers, json=params)
    return {'answer' : 1}


