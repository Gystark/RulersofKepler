
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','RulersofKepler.settings')

import django

django.setup()

from game.models import Territory, User

# Default parameters for territories
def_food = 100
def_gold = 100
def_pop = 100
def_army = 100

def populate():
    users = [
        {"Username": "TestUser",}
    ]

    territories = [
        {"Name":"Scotchland",
        "Description":"A leading producer of scotch whisky and scotch tape, this country is part of the bloc known as the 'Eunion'. " + \
                      "It also used to be a part of the Divided Republic (a republic divided in four regions), but the rest of the Republic didn't like the Eunion and decided to move somewhere else, " + \
                      "while Scotchland opted to stay.",
        "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Franz",
         "Description": "Known for its delicious cheeses and wines, this country was named after a former ruler of one of its neighbouring countries - Franz Jonas of the empire of Hungry Ostrich",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Gerfew",
         "Description": "Inhabited by the hardworking, beer-loving people known as the Gers, this land used to be known as Germany. "+   \
                        "But this didn't fit the kindness and modesty of the Gers, and thus they decided to change the name to Gerfew. ",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Hungry Ostrich",
         "Description": "A remnant of the empire of Hungry Ostrich, a country formed by the union of two territories who shared many common values, such as the love of invading neighbouring countries",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Na h-Eileanan an Siar",
         "Description": "This group of islands has very close ties to Scotchland. Its inhabitants mostly speak the ancient language known as Garlic. " + \
                        "The name of these islands means 'Western Isles' in Garlic, despite the fact that they are located East of Scotchland. If you have a problem with that, keep it to yourself.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Macarony",
         "Description": "In this land you will find a friendly, laid-back population who loves good wines and cooks the most delicious pasta, which is what gave the country its name. " + \
                        "Living here is a bliss, except for when the volcano erupts.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Mess-a-donia",
         "Description": "This stunningly beautiful realm has sadly suffered a lot due to continuous conflicts between the different groups who live here. " + \
                        "The wars that took place shocked even the rulers of the western lands, who famously said: 'What a mess! Might as well call it Mess-a-donia.'",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Lapland",
         "Description": "This snowy peninsula was discovered and claimed by the mighty vikings many centuries ago. The name of this land comes from the ancient" + \
                        " viking tradition of running laps in the snow to improve their strength and perseverance.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Catalona",
         "Description": "A land wich rich history, culture and cuisine, it was formerly know as Spainalona, until its people decided through a referendum to change it" + \
                        " To Catalona as a sign of recognition and respect towards the many friendly cats who live in this area.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Severoslavia",
         "Description": "This land is mostly known for its openness towards the world and the peaceful relations it has held with all of its neighbours every since the " + \
                        "'Blue revolution', also known as the 'August revolution', when a peaceful protest led to the establishment of a transparent leadership based on a free market and " + \
                        "respect towards human rights. Severoslavians are also known for refusing to consume any form of alcoholic beverages.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        {"Name": "Eucraine",
         "Description": "This place has very close diplomatic ties with the political alliance known as the 'Eunion', however it's losest friend is certainly Severoslavia. " + \
                        "In a famous recent event, Eucraine willingly offered to give Severoslavia one of its own territories, known as Dumbass, however Severoslavia politely refused.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,},
        ]

    for t in territories:
        print (str(add_territory(t["Name"], t["Description"], t["Food"], t["Gold"], t["Army"], t["Population"])))

    for u in users:
        print (str(add_user(u["Username"])))


def add_territory(name, desc, food, gold, army, pop):
    t = Territory.objects.get_or_create(name=name)[0]
    t.description = desc
    t.food = food
    t.gold = gold
    t.army = army
    t.population = pop
    t.save()
    return t

def add_user(name):
    u = User.objects.get_or_create(username = name)[0]
    u.is_staff = True
    u.set_password('testusrpwd')
    u.save()
    return u

populate()