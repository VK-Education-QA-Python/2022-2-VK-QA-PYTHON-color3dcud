from static.app_config import APP_CONFIG

RESPONSE_BODY = {
    'auth_correct': {
        'code': 302
    },
    'auth_incorrect': {
        'code': 401
    },
    'auth_blocked': {
        'code': 401
    },
    'create_full_user_unauthorized': {
        'body': {'detail': 'session not present', 'status': 'error', 'url': f'{APP_CONFIG["APP_URL"]}/api/user'},
        'code': 401
    },
    'delete_user_unauthorized': {
        'body': {
            'detail': 'session not present',
            'status': 'error',
            'url': f'{APP_CONFIG["APP_URL"]}/api/user/delete_user'
        },
        'code': 401
    },
    'change_pass_unauthorized': {
        'body': {
            'detail': 'session not present',
            'status': 'error',
            'url': f'{APP_CONFIG["APP_URL"]}/api/user/test_user/change-password'
        },
        'code': 401
    },
    'block_unauthorized': {
        'body': {
            'detail': 'session not present',
            'status': 'error',
            'url': f'{APP_CONFIG["APP_URL"]}/api/user/test_user/block'
        },
        'code': 401
    },
    'unblock_unauthorized': {
        'body': {
            'detail': 'session not present',
            'status': 'error',
            'url': f'{APP_CONFIG["APP_URL"]}/api/user/test_user/accept'
        },
        'code': 401
    },
    'create_full_user': {
        'body': {'detail': 'User was added', 'status': 'success'},
        'code': 201
    },
    'create_user_without_name': {
        'body': {'detail': "Not exists required field ('name')", 'status': 'failed'},
        'code': 400
    },
    'name_len_zero': {'code': 400},
    'name_len_overfull': {'code': 400},
    'create_user_without_surname': {
        'body': {'detail': "Not exists required field ('surname')", 'status': 'failed'},
        'code': 400
    },
    'surname_len_zero': {'code': 400},
    'surname_len_overfull': {'code': 400},
    'create_user_without_middle_name': {
        'body': {'detail': 'User was added', 'status': 'success'},
        'code': 201
    },
    'middle_name_len_zero': {'code': 400},
    'middle_name_len_overfull': {'code': 400},
    'create_user_without_username': {
        'body': {'detail': "Not exists required field ('username')", 'status': 'failed'},
        'code': 400
    },
    'username_len_zero': {'code': 400},
    'username_len_overfull': {'code': 400},
    'username_repeated': {
        'body': {'detail': 'User already exists', 'status': 'failed'},
        'code': 400
    },
    'create_user_without_email': {
        'body': {'detail': "Not exists required field ('email')", 'status': 'failed'},
        'code': 400
    },
    'email_len_zero': {'code': 400},
    'email_len_overfull': {'code': 400},
    'email_wrong_mask': {'code': 400},
    'email_repeated': {
        'body': {'detail': 'User already exists', 'status': 'failed'},
        'code': 400
    },
    'create_user_without_password': {
        'body': {'detail': "Not exists required field ('password')", 'status': 'failed'},
        'code': 400
    },
    'password_len_zero': {'code': 400},
    'password_len_overfull': {'code': 400},
    'delete_existing_user': {'code': 204},
    'delete_non_existing_user': {
        'body': {'detail': 'User does not exist!', 'status': 'failed'},
        'code': 404},
    'change_pass_new': {'code': 200},
    'change_pass_old': {
        'body': {'detail': 'This password is already in use', 'status': 'failed'},
        'code': 400
    },
    'change_pass_non_existing_user': {
        'body': {'detail': 'User does not exist', 'status': 'failed'},
        'code': 404
    },
    'block_active_user': {
        'body': {'detail': 'User was blocked', 'status': 'success'},
        'code': 200
    },
    'block_blocked_user': {
        'body': {'detail': 'User is already blocked', 'status': 'failed'},
        'code': 400
    },
    'block_non_existing_user': {
        'body': {'detail': 'User does not exist', 'status': 'failed'},
        'code': 404
    },
    'unblock_blocked_user': {
        'body': {'detail': 'User access granted', 'status': 'success'},
        'code': 200
    },
    'unblock_active_user': {
        'body': {'detail': 'User is already active', 'status': 'failed'},
        'code': 400
    },
    'unblock_non_existing_user': {
        'body': {'detail': 'User does not exist', 'status': 'failed'},
        'code': 404
    },
    'get_status': {
        'body': {'status': 'ok'},
        'code': 200
    }
}
