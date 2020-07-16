import os
import json
import requests

from flask import Flask, make_response, render_template, request, jsonify

baseAPIURL = os.environ.get("API_URL", default="https://api.openrates.io/")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder="templates",instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # route to the currency converter frontend
    @app.route("/")
    def home():
        return render_template('index.html')



    # route to the currency converter API
    @app.route('/currency')
    def currency():       
        # grab base and target currency from URL
        base = request.args.get('base')
        target = request.args.get('target')

        # ensure that base and target are from [ZAR, USD, EUR, GBP]
        allowedCurrencies = ['ZAR', 'USD', 'EUR', 'GBP']

        if base not in allowedCurrencies :
            return base + " is not supported as a currency"

        if target not in allowedCurrencies :
            return target + " is not supported as a currency"

        if (base == 'EUR') and (target == 'EUR'):
            return "Conversion from " + base + " to " + base + " is not supported" 

        getZAREquivalent = baseAPIURL + "latest?symbols="+ target + "&base=" + base
        print(getZAREquivalent)
        response = requests.get(getZAREquivalent)
        r = response.json()

        targetEquiv = r["rates"].get(target)
        app.logger.debug("Converted " + base + " to " + target + " and " + target + " value was " + str(targetEquiv) )
        return jsonify(targetEquiv)

    return app