from flask import Flask, url_for, render_template, request
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)


# Task-1. Creating Start Page
@app.get("/start/")
@app.get("/")
def start():
    req = url_for("requirements")
    gen = url_for("generate_users")
    mean = url_for("mean_hw")
    space = url_for("space_num")
    return render_template("start_page.html", req=req, gen=gen, mean=mean, space=space)


# Task-1. Return the contents of a file with python packages (requirements.txt): PATH: /requirements/ --
# open requirements.txt file and return its contents
@app.route("/requirements/")
def requirements():
    with open("requirements.txt") as file:
        content = file.read()
    return render_template("render_file.html", filename="requirements.txt", content=content)


# Task-2. Output 100 randomly generated users (mail + name) For example - 'Dmytro aasdasda@mail.com'
# (you can use - https://pypi.org/project/Faker/ )
# PATH: /generate-users/ + GET parameter, that adjusts the number users (/generate-users/?count=100)<
@app.route("/generate-users/")
def generate_users():
    from faker import Faker
    fake = Faker()
    num = escape(request.args.get('count'))
    try:
        if int(escape(num)) < 0:
            return f"Value of '?count' '{escape(num)}' is less than 0."
    except (ValueError, TypeError):
        return f"Value of '?count' '{escape(num)}' is not a number."
    fake_users = [fake.name() for _ in range(int(escape(num))+1)]
    fake_users_dict = {(i + 1): (f"{fake_users[i].split()[1].lower()}.{fake_users[i].split()[0].lower()}@hillel.ua",
                                 fake_users[i]) for i in range(int(escape(num)))}
    with open("templates/fake_users.txt", "w") as file:
        for key, value in fake_users_dict.items():
            file.write(str(f"{key} User:\nmail: {value[0]},  name: {value[1]}\n"))
    with open("templates/fake_users.txt", "r") as file:
        content = file.read()
    return render_template("render_file.html", filename="fake_users.txt", content=content)


# Task-3. Display average height, average weight (cm, kg) (from the attached file hw.csv)
# PATH: /mean/ PAY ATTENTION TO THE UNITS OF MEASUREMENT
@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename != "hw.csv":
            content = f"Choose hw.csv, not '{f.filename}'"
            return render_template("render_file.html", filename="hw.csv", content=content)
        f.save(f"uploads/"
               f"{secure_filename(f.filename)}")
        return render_template("acknowledgement.html", name=f.filename)


@app.route("/mean/")
def mean_hw():
    import csv
    height = []
    weight = []
    try:
        with open("uploads/hw.csv", 'r') as csv_file:
            csv_reader = list(csv.reader(csv_file))
    except FileNotFoundError:
        content = 'First upload file hw.csv!'
        return render_template("render_file.html", filename="hw.csv", content=content)
    for el in range(1, len(csv_reader)):
        if len(csv_reader[el]) > 0:
            height.append(float(csv_reader[el][1]))
            weight.append(float(csv_reader[el][2]))
    avg_height = sum(map(lambda h: h * 2.54, height)) / len(height)  # 2.54 cm in one inch
    avg_weight = sum(map(lambda w: w * 0.454, weight)) / len(weight)  # 0.454 kg in one pound
    content = f"The average height is {avg_height} cm, the average weight is {avg_weight} kg\n" \
              f"(from the attached file hw.csv)"
    return render_template("render_file.html", filename="hw.csv", content=content)


# Task-4. Print the number of astronauts at the moment (API source http://api.open-notify.org/astros.json)
# (use the library https://pypi.org/project/requests/ ) PATH: /space/
@app.route("/space/")
def space_num():
    import requests
    from requests.exceptions import HTTPError
    import json
    url = "http://api.open-notify.org/astros.json"
    response_astros = None
    try:
        response_astros = requests.get(url)
        response_astros.raise_for_status()
    except HTTPError as http_err_astros:
        print(f'HTTP error occurred: {http_err_astros}')
        exit()
    except Exception as err_astros:
        print(f'Other error occurred: {err_astros}')
        exit()
    r_astros = response_astros.content
    json_loads = json.loads(r_astros)
    numbers = json_loads["number"]
    content = f"At the moment there are {numbers} of astronauts"
    return render_template("render_file.html", filename="http://api.open-notify.org/astros.json", content=content)


if __name__ == '__main__':
    app.run()
