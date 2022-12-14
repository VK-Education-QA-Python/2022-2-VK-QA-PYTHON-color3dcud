from faker import Faker
from fastapi import FastAPI, HTTPException

fake = Faker()
app = FastAPI()


@app.get('/vk_id/{username}')
async def vk_id(username):
    if username == 'test_mock':
        return {'vk_id': username}

    elif username.lower() != 'no_username':
        vk_id_value = f"{username}_{fake.profile()['username']}"
        return {'vk_id': vk_id_value}

    else:
        raise HTTPException(status_code=404)
