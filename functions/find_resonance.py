import sqlite3

sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
cursor = sqlite_connection.cursor()


def find_resonance(role_cards):

    elements = []
    duplicate_elements = []
    all_resonances = [
        'anemo', 'geo', 'electro', 'hydro', 'dendro', 'pyro', 'frost',
        'mond', 'liue', 'inazuma', 'sumeru', 'font',
        'fatui', 'monster'
    ]
    resonance = []

    for role_card in role_cards:
        cursor.execute(f"SELECT element FROM main.role_cards WHERE {role_card} = code")
        r = cursor.fetchall()[0][0]
        r = str(r).split(", ")
        for element in r:
            elements.append(element.lower())

    for i in elements:
        if i in duplicate_elements and i in all_resonances:
            resonance.append(i)
            duplicate_elements.remove(i)
        else:
            duplicate_elements.append(i)

    # print(resonance)
    return resonance


# find_resonance(role_cards=[1404, 1401, 1701])
