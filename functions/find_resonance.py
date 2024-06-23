from db.base import KkiDb


def find_resonance(role_cards):

    elements = []
    duplicate_elements = []
    all_resonances = [
        'anemo', 'geo', 'electro', 'hydro', 'dendro', 'pyro', 'frost',
        'mond', 'liue', 'inazuma', 'sumeru', 'font',
        'fatui', 'monster'
    ]
    resonance = []

    database = KkiDb()
    for role_card in role_cards:
        r = database.get_role_card_element(role_card)[0][0]
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
