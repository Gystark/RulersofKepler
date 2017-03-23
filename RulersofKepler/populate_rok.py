import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RulersofKepler.settings')

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
        {"Username": "TestUser", },
        {"Username": "Robag", },
        {"Username": "Xela", },
        {"Username": "Naitsirc", },
        {"Username": "Ratep", },
        {"Username": "Rotkiv", },
    ]

    territories = [
        {"Name": "Scotchland",
         "Description": "A leading producer of scotch whisky and scotch tape, this country is part of the bloc known as the 'Eunion'. It also used to be a part of the Divided Republic (a republic divided in four regions), but the rest of the Republic didn't like the Eunion and decided to move somewhere else, while Scotchland opted to stay.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "243,264,287,250,325,179,308,138,329,77,288,119,182,128,107,174,68,245,150,227,156,268,248,260"},
        {"Name": "Franz",
         "Description": "Known for its delicious cheeses and wines, this country was named after a former ruler of one of its neighbouring countries - Franz Jonas of the empire of Hungry Ostrich",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "423,637,433,658,424,722,466,753,429,852,399,894,341,935,287,965,257,966,261,1064,262,1079,150,1141,47,1103,82,1062,51,954,71,858,94,836,102,806,182,725,238,745,319,683,329,631,410,634"},
        {"Name": "Gerfew",
         "Description": "Inhabited by the hardworking, beer-loving people known as the Gers, this land used to be known as Germany. But this didn't fit the kindness and modesty of the Gers, and thus they decided to change the name to Gerfew.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "451,624,495,517,620,480,616,497,708,476,758,461,743,391,760,470,845,511,923,635,823,788,798,802,824,865,824,911,804,939,767,881,740,882,440,841,472,750,432,709,441,663,431,635,447,629"},
        {"Name": "Hungry Ostrich",
         "Description": "A remnant of the empire of Hungry Ostrich, a country formed by the union of two territories who shared many common values, such as the love of invading neighbouring countries.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "817,813,947,613,1005,607,1091,637,1148,783,1044,830,930,859,832,822"},
        {"Name": "Na h-Eileanan an Siar",
         "Description": "This group of islands has very close ties to Scotchland. Its inhabitants mostly speak the ancient language known as Garlic. The name of these islands means 'Western Isles' in Garlic, despite the fact that they are located East of Scotchland. If you have a problem with that, keep it to yourself.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "619,200,692,317,759,336,774,204,754,198,652,141,614,169,601,210"},
        {"Name": "Macarony",
         "Description": "In this land you will find a friendly, laid-back population who loves good wines and cooks the most delicious pasta, which is what gave the country its name. Living here is a bliss, except for when the volcano erupts.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "384,924,431,943,527,993,577,1072,593,1110,618,1125,624,1169,663,1103,677,1087,730,1105,777,1070,811,1073,841,1057,800,1002,813,945,792,945,764,887,712,888,440,846,385,921"},
        {"Name": "Mess-a-donia",
         "Description": "This stunningly beautiful realm has sadly suffered a lot due to continuous conflicts between the different groups who live here. The wars that took place shocked even the rulers of the western lands, who famously said: 'What a mess! Might as well call it Mess-a-donia.'",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "850,1057,812,995,837,901,828,833,919,870,1105,823,1141,797,1150,836,1274,882,1262,952,1138,1058,1113,1039,1089,1128,1049,1127,994,1160,932,1129,947,1101,858,1060"},
        {"Name": "Lapland",
         "Description": "This snowy peninsula was discovered and claimed by the mighty vikings many centuries ago. The name of this land comes from the ancient viking tradition of running laps in the snow to improve their strength and perseverance.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "431,488,452,526,500,509,595,484,611,473,619,454,623,423,643,416,649,390,634,371,644,358,635,329,637,319,604,303,571,320,529,302,507,283,450,242,396,262,339,268,296,295,283,315,268,311,245,282,235,325,212,320,181,348,111,379,71,383,80,407,90,418,68,468,73,509,92,543,109,565,89,579,112,598,138,579,172,558,131,521,143,478,186,461,364,511,385,462,373,433,390,423,458,447,432,479"},
        {"Name": "Catalona",
         "Description": "A land with rich history, culture and cuisine, it was formerly know as Spainalona, until its people decided through a referendum to change it to Catalona as a sign of recognition and respect towards the many friendly cats who live in this area.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "264,978,269,1086,146,1153,40,1112,93,1242,154,1293,153,1351,156,1374,188,1345,274,1402,341,1399,324,1363,374,1335,456,1312,526,1191,538,1169,581,1187,588,1175,551,1123,578,1101,521,1000,373,926"},
        {"Name": "Severoslavia",
         "Description": "This land is mostly known for its openness towards the world and the peaceful relations it has held with all of its neighbours every since the 'Blue revolution', also known as the 'August revolution', when a peaceful protest led to the establishment of a transparent leadership based on a free market and respect towards human rights. Severoslavians are also known for refusing to consume any form of alcoholic beverages.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "755,384,824,352,898,303,948,281,970,123,998,75,1018,17,1045,73,1137,45,1257,60,1368,45,1412,135,1362,191,1394,198,1401,236,1480,286,1541,259,1590,277,1657,230,1699,235,1740,226,1687,287,1646,287,1632,412,1544,556,1496,538,1460,499,1407,505,1298,536,1209,546,1162,566,1105,503,1072,528,1087,557,1073,619,990,593,927,614,838,489,768,466"},
        {"Name": "Eucraine",
         "Description": "This place has very close diplomatic ties with the political alliance known as the 'Eunion', however it's closest friend is certainly Severoslavia. In a famous recent event, Eucraine willingly offered to give Severoslavia one of its own territories, known as Dumbass, however Severoslavia politely refused.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1153,768,1087,604,1095,542,1101,518,1163,582,1454,508,1541,576,1577,592,1552,657,1461,726,1351,754,1269,856,1348,775,1338,832,1274,865,1156,825,1151,789"},
        {"Name": "Arabia al Qadim",
         "Description": "This prosperous desert land attracts many travelers from abroad, especially food pilgrims who come to taste the famous delicacies found in the holy city of Mydinner",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "154,1859,228,1819,281,1848,305,1794,322,1740,530,1744,544,1796,599,1796,625,1632,593,1445,524,1469,505,1533,488,1516,427,1529,367,1410,343,1423,324,1474,312,1465,279,1481,214,1539,141,1634,92,1648,122,1695,79,1714,80,1782,124,1830,146,1856"},
        {"Name": "Constantinopelis",
         "Description": "The gateway between two worlds, this place was formerly known as Turkey, however its name was changed when emperor Constantine noticed that residents did not eat turkey too often.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1139,1060,1279,951,1398,989,1431,1010,1600,926,1664,876,1651,824,1671,883,1590,938,1613,1007,1667,1025,1665,1113,1601,1110,1482,1254,1401,1248,1250,1338,1147,1181,1212,1145,1287,1104,1248,1073,1150,1063"},
        {"Name": "Mess-a-potamia",
         "Description": "A land with a rich culture and history, Mess-a-potamia has suffered from the violence of its tyrants and the greed of other nations. Powerful people tried to profit as much as they could from this territory - and they made a huge mess",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1131,1174,1243,1343,1206,1421,1129,1499,1075,1587,1065,1594,1030,1569,948,1604,844,1520,797,1417,743,1388,770,1320,826,1336,919,1252,969,1209,1000,1233,1082,1230,1122,1176"},
        {"Name": "Thingystan",
         "Description": "The rulers of a few countries from the centre of the continent agreed to join their forces and form a powerful union of nations. This initiative came from a local nobleman named Stan, who famously said 'Let's make a union thingy!'",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1159,1476,1224,1418,1249,1341,1402,1255,1485,1261,1603,1116,1679,1119,1667,1175,1708,1189,1774,1160,1803,1167,1793,1253,1719,1294,1614,1293,1546,1319,1419,1332,1309,1394,1246,1452,1169,1475"},
        {"Name": "Persia",
         "Description": "A land with a rich cultural heritage, it is also known as I-ran, from the famous phrase 'I ran to Persia for some kebabs.'",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1729,1297,1705,1402,1756,1500,1701,1527,1631,1504,1609,1519,1601,1580,1523,1535,1441,1556,1369,1370,1432,1339,1586,1321,1625,1307,1701,1303"},
        {"Name": "Best Korea",
         "Description": "There used to be two neighbouring nations called Korea - one of them was a free, modern democracy while the other was ruled by a chubby and powerful autocrat. Eventually, the two countries united when the best one of them took complete control of the other.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1653,811,1682,899,1753,886,1763,832,1723,828,1681,757,1637,796"},
        {"Name": "Cathay",
         "Description": "One of the largest and most powerful nations in the world, it received its modern name when a former ruler, Rofl Mao, saw a cat playing in hay.",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1672,1016,1615,995,1603,942,1666,894,1686,910,1778,886,1832,919,1916,895,1918,978,2031,1106,2014,1317,1956,1455,1888,1511,1787,1474,1757,1484,1715,1393,1735,1308,1797,1259,1812,1169,1776,1148,1707,1177,1675,1170,1694,1117,1672,1109,1672,1022"},
        {"Name": "Endia",
         "Description": "The land at the end of the map, Endia is known for exporting delicious spices and quality soap opera films all across the world",
         "Food": def_food, "Army": def_army, "Gold": def_gold, "Population": def_pop,
         "Coordinates": "1078,1591,1171,1481,1255,1450,1362,1374,1436,1562,1394,1682,1421,1778,1498,1867,1525,1884,1487,2017,1239,1995,1142,2019,1076,1991,1042,1983,1052,1957,988,1939,966,1952,946,1914,1020,1777,941,1667,980,1642,1072,1714,1126,1685,1118,1632,1087,1595"},

    ]

    neighbours = {
        "Scotchland": ["Na h-Eileanan an Siar", "Lapland"],
        "Na h-Eileanan an Siar": ["Lapland", "Severoslavia"],
        "Lapland": ["Gerfew"],
        "Gerfew": ["Franz", "Hungry Ostrich", "Severoslavia", "Macarony", "Mess-a-donia"],
        "Franz": ["Catalona", "Macarony"],
        "Macarony": ["Mess-a-donia", "Catalona"],
        "Catalona": ["Arabia al Qadim"],
        "Hungry Ostrich": ["Severoslavia", "Eucraine", "Mess-a-donia"],
        "Eucraine": ["Mess-a-donia", "Severoslavia"],
        "Mess-a-donia": ["Constantinopelis"],
        "Constantinopelis": ["Cathay", "Thingystan", "Mess-a-potamia"],
        "Mess-a-potamia": ["Arabia al Qadim", "Endia", "Thingystan"],
        "Endia": ["Thingystan", "Persia"],
        "Persia": ["Thingystan", "Cathay"],
        "Cathay": ["Thingystan", "Best Korea"],

    }

    for t in territories:
        print(str(add_territory(t["Name"], t["Description"], t["Food"], t["Gold"], t["Army"], t["Population"],
                                t["Coordinates"])))

    for n in neighbours.keys():
        add_borders(n, neighbours[n])

    for u in users:
        print(str(add_user(u["Username"])))


def add_territory(name, desc, food, gold, army, pop, coord):
    t = Territory.objects.get_or_create(name=name)[0]
    t.description = desc
    t.default_food = food
    t.default_gold = gold
    t.default_army = army
    t.default_population = pop
    t.coordinates = coord
    t.save()
    return t


def add_borders(tname, borders):
    t = Territory.objects.get(name=tname)
    for bname in borders:
        b = Territory.objects.get(name=bname)
        if t.borders.filter(name=bname).count() == 0:
            t.borders.add(b)
        if b.borders.filter(name=tname).count() == 0:
            b.borders.add(t)
        print(t.name + " borders " + b.name)
    t.save()


def add_user(name):
    u = User.objects.get_or_create(username=name)[0]
    u.is_superuser = True
    u.is_staff = True
    u.set_password('testusrpwd')
    u.save()
    return u


populate()
