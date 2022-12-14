FROM python:3.11

ADD /requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD / /vk_project

WORKDIR /vk_project

CMD ["pytest", "-s", "-l", "-v", "-n2", "--selenoid", "--alluredir", "./allure", "tests"]
