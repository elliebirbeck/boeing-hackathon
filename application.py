from flask import Flask, send_from_directory, send_file, request, render_template
from werkzeug.contrib.cache import SimpleCache
import pandas as pd
import recipefinder
import sys
import food_loc_finder
import json
# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username


# EB looks for an 'application' callable by default.
application = Flask(__name__)
cache = SimpleCache()
recipes = recipefinder.preProcessData('recipes.csv')
country_locations = pd.read_csv('countries.csv')
finder = food_loc_finder.FoodLocationFinder('ingredientsHS.json')
#ratemyplate.com/meals?recipe=spghetti

@application.route('/meals')
def get_recipe_breakdown():
    recipe_name = request.args.get('recipe');   
    print(recipe_name, file=sys.stderr)
    ingredients = recipefinder.findIngredients(recipe_name,recipes,True)
    countries = finder.get_producers_for_recipe(ingredients, 826)
    producers = [x[1] for x in countries]
    country_codes = [x[0] for x in countries]
    locations = get_locations(country_codes)
    return render_template("index.html", recipe=json.dumps(recipe_name), ingredients=json.dumps(ingredients), producers=json.dumps(producers), locations=json.dumps(locations))

@application.route('/icons/<path:path>')
def send_icon(path):
    return send_from_directory('icons', path)

@application.route('/<path:path>')
def send_meal_breakdown(path):
    return send_from_directory('static', path)


def get_locations(producers):
    locations = []
    for producer in producers:
        match = country_locations.loc[country_locations['country'] == producer]
        locations.append((match['latitude'].item(), match['longitude'].item()))
    return locations
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()