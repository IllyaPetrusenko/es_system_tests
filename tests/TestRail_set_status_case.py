import testrail

client = testrail.APIClient('https://ustudiocompany.testrail.io')  # do not include index.php?/api/v2
client.user = 'noreply@ustudio.company'  # TestRail email address
client.password = 'add2uStudio'  # TestRail password or API token

post_body = {
    "status_id": 5,
    "comment": "Не обнаружен путь на паблик точке55"
}
client.send_post(f'add_result_for_case/{667}/{27029}', post_body)