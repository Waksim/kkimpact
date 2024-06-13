import json
import re
import time
import sqlite3
import requests

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    sqlite_connection = sqlite3.connect('../tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    cursor.execute(f"SELECT * FROM main.role_cards")
    role_cards = cursor.fetchall()

    print(role_cards)
    for role_card in role_cards:
        card_code = role_card[2]
        wiki_code = role_card[9]
        print(f"--------------\nWIKI: {wiki_code}, CODE: {card_code}")

        cursor.execute("SELECT EXISTS(SELECT * FROM role_cards_wiki where card_code = ?)", (card_code,))
        registered = cursor.fetchall()[0][0]

        if registered != 0:
            print("-CONTINUE-")
            continue

        # card_code = 2102
        # wiki_code = 4734

        page.goto(f"https://wiki.hoyolab.com/pc/genshin/entry/{wiki_code}?lang=en-us")
        # page.goto(f"https://wiki.hoyolab.com/pc/genshin/entry/4728?lang=en-us")
        time.sleep(3)

        card_name = page.query_selector("div.detail-header-common-name>span").inner_text()
        print(card_name)

        hp_number = page.query_selector_all("div.base-info-item>div.et-text-tiptap-wrapper")[2].inner_text()

        tags = page.query_selector_all("div.c-entry-tag-item")
        card_tags = []
        for tag in tags:
            card_tags.append(tag.inner_text())

        talents_clicks = page.query_selector_all("div.d-talent-keys-wrapper")
        talent_info = []
        talent_number = 1
        for talent_click in talents_clicks:
            talent_click.click()

            talent_img_src = talent_click.query_selector("div.default-img-wrapper>img.default-img").get_attribute('origin-src')

            talent_description = page.query_selector("div.d-talent-content").inner_text()
            costs = page.query_selector_all("section.tcg-action-point")
            talent_cost = []

            for cost in costs:
                talent_img = cost.query_selector("img.tcg-action-point-number")
                match = re.search(r'/_nuxt/img/hp_(\d)', str(talent_img.get_attribute("src")))
                count_of_dice = match[1]
                type_dice = cost.get_attribute("class").split(" ")[1]

                talent_cost.append([type_dice, count_of_dice])

            img_data = requests.get(talent_img_src).content
            with open(f'img/role_talents/{card_code}_{talent_number}.png', 'wb') as handler:
                handler.write(img_data)
            talent_number += 1

            talent_info.append({"cost": talent_cost, "icon_src": talent_img_src, "description": talent_description})

        page.locator("[id=\"\\34 9_gallery_character\"]").get_by_text("Avatar Icon").click()
        click_for_avatar = page.query_selector_all("div.m-d-btn-text")
        click_avatar_button_counter = 0
        for button in click_for_avatar:
            if button.inner_text() == 'Avatar Icon':
                break
            click_avatar_button_counter += 1
        img_avatar_src = page.query_selector_all("div.d-gallery-list-item>div>img.default-img")[click_avatar_button_counter].get_attribute('origin-src')
        img_data = requests.get(img_avatar_src).content
        with open(f'img/avatars/{card_code}.png', 'wb') as handler:
            handler.write(img_data)

        # img_avatar_src = page.locator("section").filter(has_text="/3 Avatar Icon").locator("img").nth(3).get_attribute('origin-src')
        # card_gif = page.query_selector("div.data-node-view-wrapper>div.custom-image-wrapper>img").get_attribute('src')

        card_gif = page.locator(".custom-image").first.get_attribute('src')
        img_data = requests.get(card_gif).content
        with open(f'img/role_gif/{card_code}.gif', 'wb') as handler:
            handler.write(img_data)

        print("КАРТА: ", card_name)
        print("XP: ", hp_number)
        print("ТЕГИ: ", card_tags)
        print("ТАЛАНТЫ: ", talent_info)
        print("АВАТАР: ", img_avatar_src)
        print("ГИФКА: ", card_gif)

        cursor.execute("""INSERT INTO main.role_cards_wiki 
                (wiki_code, card_name_eng, xp, tags,
                talents, avatar, gif, card_code) VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?);""",
                       (wiki_code, card_name, hp_number, json.dumps(card_tags),
                        json.dumps(talent_info), img_avatar_src, card_gif, card_code))

        sqlite_connection.commit()

    # ---------------------
    cursor.close()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
