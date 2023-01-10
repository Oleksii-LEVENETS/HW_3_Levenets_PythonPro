import os
import csv
import json
import requests
from requests.exceptions import HTTPError
from faker import Faker
from flask import Flask, url_for, render_template, request
from markupsafe import escape
from werkzeug.utils import secure_filename


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'HW_4.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Task-1. Creating Start Page
    @app.route("/start/")
    @app.route("/")
    def start():
        req = url_for("requirements")
        gen = url_for("generate_users")
        mean = url_for("mean_hw")
        space = url_for("space_num")
        names = url_for("music.names")
        tracks = url_for("music.tracks")
        tracks_genre = url_for("music.tracks_genre")
        tracks_s = url_for("music.tracks_sec")
        tracks_s_stat = url_for("music.tracks_sec_stat")
        return render_template("start_page.html", req=req, gen=gen, mean=mean, space=space, names=names,
                               tracks=tracks, tracks_genre=tracks_genre, tracks_s=tracks_s, tracks_s_stat=tracks_s_stat)
    
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
        fake = Faker()
        num = escape(request.args.get('count'))
        try:
            if int(escape(num)) < 0:
                return f"Value of '?count' '{escape(num)}' is less than 0."
        except (ValueError, TypeError):
            return f"Value of '?count' '{escape(num)}' is not a number."
        fake_users = [fake.name() for _ in range(int(escape(num)) + 1)]
        fake_users_dict = {(i + 1): (f"{fake_users[i].split()[1].lower()}.{fake_users[i].split()[0].lower()}@hillel.ua",
                                     fake_users[i]) for i in range(int(escape(num)))}
        with open("HW_4/templates/fake_users.txt", "w") as file:
            for key, value in fake_users_dict.items():
                file.write(str(f"{key} User:\nmail: {value[0]},  name: {value[1]}\n"))
        with open("HW_4/templates/fake_users.txt", "r") as file:
            content = file.read()
        return render_template("render_file.html", filename="HW_4/templates/fake_users.txt", content=content)
    
    # Task-3. Display average height, average weight (cm, kg) (from the attached file hw.csv)
    # PATH: /mean/ PAY ATTENTION TO THE UNITS OF MEASUREMENT
    @app.route('/success', methods=['POST'])
    def success():
        if request.method == 'POST':
            f = request.files['file']
            if f.filename != "hw.csv":
                content = f"Choose hw.csv, not '{f.filename}'"
                return render_template("render_file.html", filename="hw.csv", content=content)
            f.save(f"HW_4/uploads/"
                   f"{secure_filename(f.filename)}")
            return render_template("acknowledgement.html", name=f.filename)
    
    @app.route("/mean/")
    def mean_hw():
        height = []
        weight = []
        try:
            with open("HW_4/uploads/hw.csv", 'r') as csv_file:
                csv_reader = list(csv.reader(csv_file))
        except FileNotFoundError:
            content = 'First upload file hw.csv!'
            return render_template("render_file.html", filename="HW_4/uploads/hw.csv", content=content)
        for el in range(1, len(csv_reader)):
            if len(csv_reader[el]) > 0:
                height.append(float(csv_reader[el][1]))
                weight.append(float(csv_reader[el][2]))
        avg_height = sum(map(lambda h: h * 2.54, height)) / len(height)  # 2.54 cm in one inch
        avg_weight = sum(map(lambda w: w * 0.454, weight)) / len(weight)  # 0.454 kg in one pound
        content = f"The average height is {avg_height} cm, the average weight is {avg_weight} kg\n" \
                  f"(from the attached file hw.csv)"
        return render_template("render_file.html", filename="HW_4/uploads/hw.csv", content=content)
    
    # Task-4. Print the number of astronauts at the moment (API source http://api.open-notify.org/astros.json)
    # (use the library https://pypi.org/project/requests/ ) PATH: /space/
    @app.route("/space/")
    def space_num():
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
    
    from . import db
    db.init_app(app)
    
    from . import music
    app.register_blueprint(music.bp)
    
    return app
