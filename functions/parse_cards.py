import requests
import json
import sqlite3


# role_cards = [1404, 1401, 1701]
# actions_cards = [214041, 312401, 321002, 321003, 321003, 321004, 321006, 322001, 322002, 322007, 322010, 331401, 331401, 331402, 331402, 332001, 332001, 332002, 332002, 332003, 332004, 332004, 332005, 332006, 332006, 332007, 332012, 333002, 333003, 333003]
#
# payload = '"filters":[],"menu_id":"17","page_num":3,"page_size":30,"use_es":true'
# url = 'https://sg-wiki-api.hoyolab.com/hoyowiki/genshin/wapi/get_entry_page_list'
# payload = '{' + payload + '}'
# r = requests.post(url, data=payload).json()
#
# print(r)

f = open('temp_json')
data = json.load(f)
# json_string = '{ "retcode": 0, "message": "OK", "data": { "list": [ { "entry_page_id": "4945", "name": "Millennial Pearl Seahorse", "icon_url": "https://act-webstatic.hoyoverse.com/event-static-hoyowiki-admin/2024/01/29/dba478ce69e1dc5244bc59ba7f9a4e26_1364664288877760586.png", "display_field": { "tcg_hp": "8", "tcg_cost_icon_type_any": "", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_element": { "values": [ "Electro" ], "value_types": [ { "id": "2109", "value": "Electro" } ] } }, "desc": "" }, { "entry_page_id": "4944", "name": "Cryo Hypostasis", "icon_url": "https://act-webstatic.hoyoverse.com/event-static-hoyowiki-admin/2024/01/29/8d7de2636087ba94e7195a1b0007e1ef_6874961881922603162.png", "display_field": { "tcg_hp": "8", "tcg_cost_icon_type_any": "", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_element": { "values": [ "Cryo" ], "value_types": [ { "id": "2069", "value": "Cryo" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] } }, "desc": "" }, { "entry_page_id": "4943", "name": "Sayu", "icon_url": "https://act-webstatic.hoyoverse.com/event-static-hoyowiki-admin/2024/01/29/6b3ba7a3bc965e6fdf30d22d77f691b6_5912831956380332113.png", "display_field": { "tcg_cost_icon_type": "", "tcg_hp": "10", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_weapon_type": { "values": [ "Claymore" ], "value_types": [ { "id": "1917", "value": "Claymore" } ] }, "card_character_camp": { "values": [ "Inazuma" ], "value_types": [ { "id": "2203", "value": "Inazuma" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_element": { "values": [ "Anemo" ], "value_types": [ { "id": "2164", "value": "Anemo" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] } }, "desc": "" }, { "entry_page_id": "4942", "name": "Thoma", "icon_url": "https://act-webstatic.hoyoverse.com/event-static-hoyowiki-admin/2024/01/29/d9c37e1c054b20133c2976ee1bf8ea35_842725637516277490.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_cost_icon_type": "", "tcg_hp": "10" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_weapon_type": { "values": [ "Polearm" ], "value_types": [ { "id": "1949", "value": "Polearm" } ] }, "card_character_camp": { "values": [ "Inazuma" ], "value_types": [ { "id": "2203", "value": "Inazuma" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_element": { "values": [ "Pyro" ], "value_types": [ { "id": "2106", "value": "Pyro" } ] } }, "desc": "" }, { "entry_page_id": "4739", "name": "Azhdaha", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/59c9f48b45fef7fae67645f57f3631bc_8264828271882490187.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] }, "card_character_element": { "values": [ "Geo" ], "value_types": [ { "id": "2135", "value": "Geo" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] } }, "desc": "" }, { "entry_page_id": "4738", "name": "Dvalin", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/497160d9f34a61f72b6943c550530da9_5939975145222897039.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_element": { "values": [ "Anemo" ], "value_types": [ { "id": "2164", "value": "Anemo" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] } }, "desc": "" }, { "entry_page_id": "4737", "name": "Thunder Manifestation", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/ecd209677ca0b1de5a950f6326411772_2249349134942577610.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] }, "card_character_element": { "values": [ "Electro" ], "value_types": [ { "id": "2109", "value": "Electro" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] } }, "desc": "" }, { "entry_page_id": "4736", "name": "Eremite Scorching Loremaster", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/4c87f22791f0d74525336e65e42b8eee_6950078156731850202.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_element": { "values": [ "Pyro" ], "value_types": [ { "id": "2106", "value": "Pyro" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] } }, "desc": "" }, { "entry_page_id": "4734", "name": "La Signora", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/f09b3e68802998c038891d55f147417a_765139832123847343.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_camp": { "values": [ "Fatui" ], "value_types": [ { "id": "2235", "value": "Fatui" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] }, "card_character_element": { "values": [ "Cryo" ], "value_types": [ { "id": "2069", "value": "Cryo" } ] } }, "desc": "" }, { "entry_page_id": "4733", "name": "Alhaitham", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/cc517735a326b0d767ba31565caa8974_2836508264759442202.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_camp": { "values": [ "Sumeru" ], "value_types": [ { "id": "2219", "value": "Sumeru" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Dendro" ], "value_types": [ { "id": "2141", "value": "Dendro" } ] } }, "desc": "" }, { "entry_page_id": "4732", "name": "Gorou", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/39df61d2d536e9aa7e075451fcfaa03f_737685111642262838.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Geo" ], "value_types": [ { "id": "2135", "value": "Geo" } ] }, "card_character_camp": { "values": [ "Inazuma" ], "value_types": [ { "id": "2203", "value": "Inazuma" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Bow" ], "value_types": [ { "id": "1933", "value": "Bow" } ] } }, "desc": "" }, { "entry_page_id": "4731", "name": "Lynette", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/78b8152971f3e86ee63fbdac9ad93ce9_551810639909458104.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_camp": { "values": [ "Fatui", "Fontaine" ], "value_types": [ { "id": "2235", "value": "Fatui" }, { "id": "3293", "value": "Fontaine" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Anemo" ], "value_types": [ { "id": "2164", "value": "Anemo" } ] }, "card_character_arkhe": { "values": [ "Ousia" ], "value_types": [ { "id": "3284", "value": "Ousia" } ] } }, "desc": "" }, { "entry_page_id": "4730", "name": "Lyney", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/7cf60c81302c7ec463bac6b7773633a7_2051412540486708098.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_arkhe": { "values": [ "Pneuma" ], "value_types": [ { "id": "3264", "value": "Pneuma" } ] }, "card_character_camp": { "values": [ "Fatui", "Fontaine" ], "value_types": [ { "id": "2235", "value": "Fatui" }, { "id": "3293", "value": "Fontaine" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Bow" ], "value_types": [ { "id": "1933", "value": "Bow" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Pyro" ], "value_types": [ { "id": "2106", "value": "Pyro" } ] } }, "desc": "" }, { "entry_page_id": "4729", "name": "Yelan", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/ea02ad09186e3019b31113b83b6011a6_1600311718962682118.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Hydro" ], "value_types": [ { "id": "2082", "value": "Hydro" } ] }, "card_character_camp": { "values": [ "Liyue" ], "value_types": [ { "id": "2187", "value": "Liyue" } ] }, "card_character_charging_point": { "values": [ "3" ], "value_types": [ { "id": "1849", "value": "3" } ] }, "card_character_weapon_type": { "values": [ "Bow" ], "value_types": [ { "id": "1933", "value": "Bow" } ] } }, "desc": "" }, { "entry_page_id": "4728", "name": "Layla", "icon_url": "https://act-upload.hoyoverse.com/event-ugc-hoyowiki/2023/12/17/35428890/59e4f4025a5c966987d7f8785aff5d3b_6584399564804565437.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Cryo" ], "value_types": [ { "id": "2069", "value": "Cryo" } ] }, "card_character_camp": { "values": [ "Sumeru" ], "value_types": [ { "id": "2219", "value": "Sumeru" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] } }, "desc": "" }, { "entry_page_id": "4561", "name": "Nilou", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/11/06/35428890/033f882b518370bd8324a363400eee70_5600088712767626495.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_element": { "values": [ "Hydro" ], "value_types": [ { "id": "2082", "value": "Hydro" } ] }, "card_character_camp": { "values": [ "Sumeru" ], "value_types": [ { "id": "2219", "value": "Sumeru" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] } }, "desc": "" }, { "entry_page_id": "4560", "name": "Dori", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/11/06/35428890/bf1f638bd916f081af948d6406d3fac4_8144202466622630031.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_weapon_type": { "values": [ "Claymore" ], "value_types": [ { "id": "1917", "value": "Claymore" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Electro" ], "value_types": [ { "id": "2109", "value": "Electro" } ] }, "card_character_camp": { "values": [ "Sumeru" ], "value_types": [ { "id": "2219", "value": "Sumeru" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] } }, "desc": "" }, { "entry_page_id": "4559", "name": "Baizhu", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/11/06/35428890/8530ed16338ca3786d7e7da69a895036_4246396938207022251.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_weapon_type": { "values": [ "Catalyst" ], "value_types": [ { "id": "1903", "value": "Catalyst" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Dendro" ], "value_types": [ { "id": "2141", "value": "Dendro" } ] }, "card_character_camp": { "values": [ "Liyue" ], "value_types": [ { "id": "2187", "value": "Liyue" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] } }, "desc": "" }, { "entry_page_id": "4366", "name": "Yaoyao", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/09/25/35428890/9ae11dc0f2551b8b7f40e04339c04cf8_7148132234708599230.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Polearm" ], "value_types": [ { "id": "1949", "value": "Polearm" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Dendro" ], "value_types": [ { "id": "2141", "value": "Dendro" } ] }, "card_character_camp": { "values": [ "Liyue" ], "value_types": [ { "id": "2187", "value": "Liyue" } ] } }, "desc": "" }, { "entry_page_id": "4365", "name": "Wanderer", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/09/25/35428890/ce89cee858b7e18759cc60ce9eb7657b_1073946105460778740.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_charging_point": { "values": [ "3" ], "value_types": [ { "id": "1849", "value": "3" } ] }, "card_character_weapon_type": { "values": [ "Catalyst" ], "value_types": [ { "id": "1903", "value": "Catalyst" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Anemo" ], "value_types": [ { "id": "2164", "value": "Anemo" } ] } }, "desc": "" }, { "entry_page_id": "4364", "name": "Dehya", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/09/25/35428890/b40d49c80cc633d60f771fb8ddf755c4_5881462082921564282.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_camp": { "values": [ "Sumeru" ], "value_types": [ { "id": "2219", "value": "Sumeru" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Claymore" ], "value_types": [ { "id": "1917", "value": "Claymore" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Pyro" ], "value_types": [ { "id": "2106", "value": "Pyro" } ] } }, "desc": "" }, { "entry_page_id": "4015", "name": "Qiqi", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/08/14/35428890/0edf905560ff08d4b819cd5bb21578eb_1444940328250211968.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_camp": { "values": [ "Liyue" ], "value_types": [ { "id": "2187", "value": "Liyue" } ] }, "card_character_charging_point": { "values": [ "3" ], "value_types": [ { "id": "1849", "value": "3" } ] }, "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Cryo" ], "value_types": [ { "id": "2069", "value": "Cryo" } ] } }, "desc": "" }, { "entry_page_id": "4013", "name": "Albedo", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/08/14/35428890/6d991f4917ed756cad5d44ab166cf5f7_7669117281211049983.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Geo" ], "value_types": [ { "id": "2135", "value": "Geo" } ] }, "card_character_camp": { "values": [ "Mondstadt" ], "value_types": [ { "id": "2179", "value": "Mondstadt" } ] } }, "desc": "" }, { "entry_page_id": "4011", "name": "Lisa", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/08/14/35428890/81211fd394258d684252bc7b66079637_3840330357066508243.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Catalyst" ], "value_types": [ { "id": "1903", "value": "Catalyst" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Electro" ], "value_types": [ { "id": "2109", "value": "Electro" } ] }, "card_character_camp": { "values": [ "Mondstadt" ], "value_types": [ { "id": "2179", "value": "Mondstadt" } ] } }, "desc": "" }, { "entry_page_id": "3961", "name": "Kaedehara Kazuha", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/07/15/35428890/86860a04df9541ce4306a533190e469b_5882281887450879321.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Anemo" ], "value_types": [ { "id": "2164", "value": "Anemo" } ] }, "card_character_camp": { "values": [ "Inazuma" ], "value_types": [ { "id": "2203", "value": "Inazuma" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Sword" ], "value_types": [ { "id": "1884", "value": "Sword" } ] } }, "desc": "" }, { "entry_page_id": "3960", "name": "Yanfei", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/07/12/35428890/96cf1ba5e8affb67f2427407e37f0e10_2129265012373908943.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "10", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Pyro" ], "value_types": [ { "id": "2106", "value": "Pyro" } ] }, "card_character_camp": { "values": [ "Liyue" ], "value_types": [ { "id": "2187", "value": "Liyue" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Catalyst" ], "value_types": [ { "id": "1903", "value": "Catalyst" } ] } }, "desc": "" }, { "entry_page_id": "3957", "name": "Candace", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/07/12/77454259/3bdee71bcb8a499d2f94bf25cb812e84_602718134922892016.png", "display_field": { "tcg_hp": "10", "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "" }, "filter_values": { "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Polearm" ], "value_types": [ { "id": "1949", "value": "Polearm" } ] }, "card_character_obtaining_method": { "values": [ "Character Invitations" ], "value_types": [ { "id": "1727", "value": "Character Invitations" } ] }, "card_character_element": { "values": [ "Hydro" ], "value_types": [ { "id": "2082", "value": "Hydro" } ] }, "card_character_camp": { "values": [ "Sumeru" ], "value_types": [ { "id": "2219", "value": "Sumeru" } ] } }, "desc": "" }, { "entry_page_id": "3844", "name": "Electro Hypostasis", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/05/21/35428890/a18a61786bc99b67ad9fde145786cbe3_7462426228164417551.png", "display_field": { "tcg_cost_icon_type_any": "", "tcg_hp": "8", "tcg_cost_icon_type": "" }, "filter_values": { "card_character_element": { "values": [ "Electro" ], "value_types": [ { "id": "2109", "value": "Electro" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] }, "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] } }, "desc": "" }, { "entry_page_id": "3843", "name": "Abyss Lector: Fathomless Flames", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/05/21/35428890/269b19028f15db0e54a4b0b36ee13627_8763341806207986302.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "6" }, "filter_values": { "card_character_charging_point": { "values": [ "2" ], "value_types": [ { "id": "1831", "value": "2" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] }, "card_character_element": { "values": [ "Pyro" ], "value_types": [ { "id": "2106", "value": "Pyro" } ] }, "card_character_camp": { "values": [ "Monster" ], "value_types": [ { "id": "2259", "value": "Monster" } ] } }, "desc": "" }, { "entry_page_id": "3842", "name": "Fatui Cryo Cicin Mage", "icon_url": "https://upload-static.hoyoverse.com/hoyolab-wiki/2023/05/21/35428890/cbcfb53b8523957d330a6f9396f03167_6553006868301593753.png", "display_field": { "tcg_cost_icon_type": "", "tcg_cost_icon_type_any": "", "tcg_hp": "10" }, "filter_values": { "card_character_camp": { "values": [ "Fatui" ], "value_types": [ { "id": "2235", "value": "Fatui" } ] }, "card_character_charging_point": { "values": [ "3" ], "value_types": [ { "id": "1849", "value": "3" } ] }, "card_character_weapon_type": { "values": [ "Other Weapons" ], "value_types": [ { "id": "1973", "value": "Other Weapons" } ] }, "card_character_obtaining_method": { "values": [ "Tavern Challenges" ], "value_types": [ { "id": "1739", "value": "Tavern Challenges" } ] }, "card_character_element": { "values": [ "Cryo" ], "value_types": [ { "id": "2069", "value": "Cryo" } ] } }, "desc": "" } ], "total": "75" } }'
# data = json.loads(json_string)

# type_of_cards = 'role_cards'
type_of_cards = 'action_cards'

sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
cursor = sqlite_connection.cursor()


i = 1

# print(data['data']['list'])
for card in data['data']['list']:
    wiki_id = card['entry_page_id']
    name = card['name']
    url = card['icon_url']

    card_code = ''

    # print(f"'{name}'")

    cursor.execute(f"SELECT code FROM main.{type_of_cards} WHERE card_name_eng = ?", (name,))
    role_cards = cursor.fetchall()
    if role_cards != []:
        card_code = role_cards[0][0]

    if card_code != '':
        continue
        img_data = requests.get(url).content
        with open(f'{type_of_cards}/{card_code}.png', 'wb') as handler:
            handler.write(img_data)
    else:
        print("Error: "+name+' - '+wiki_id+' - '+url)
        continue
        img_data = requests.get(url).content
        with open(f'{type_of_cards}/{name}.png', 'wb') as handler:
            handler.write(img_data)

    cursor.execute(f"UPDATE main.{type_of_cards} SET wiki_code = ? WHERE card_name_eng = ?", (wiki_id, name,))
    sqlite_connection.commit()

    # print(wiki_id)
    # break
    print(i)
    i+=1

# print(len(data['data']['list']))

cursor.close()