import cv2
import config
import overlay

hero_icons_mapping = {
    "Tracer": "tracer.png",
    "Junkrat": "junkrat.png",
    "Brigitte": "brigitte.png",
    "Orisa": "orisa.png",
    "Zarya": "zarya.png",
    "Doomfist": "doomfist.png",
    "Baptiste": "baptiste.png",
    "Bastion": "bastion.png",
    "Roadhog": "roadhog.png",
    "D.Va": "dva.png",
    "Wrecking Ball": "wrecking-ball.png",
    "Mercy": "mercy.png",
    "Ana": "ana.png",
    "Winston": "winston.png",
    "Sigma": "sigma.png",
    "Lucio": "lucio.png",
    "Moira": "moira.png",
    "Hanzo": "hanzo.png",
    "Reinhardt": "reinhardt.png",
    "Pharah": "pharah.png",
    "Sombra": "sombra.png",
    "Ashe": "ashe.png",
    "Reaper": "reaper.png",
    "Widowmaker": "widowmaker.png",
    "Mei": "mei.png",
    "Soldier: 76": "soldier.png",
    "Zenyatta": "zenyatta.png",
    "McCree": "mccree.png",
    "Genji": "genji.png",
    "Torbjorn": "torbjorn.png",
    "Symmetra": "symmetra.png",
    "Echo": "echo.png"
}


# checks if box bounding is too similar
def same_box(box1, box2):
    point1_min = min(box1[0], box2[0])
    point1_max = max(box1[0], box2[0])
    point2_min = min(box1[1], box2[1])
    point2_max = max(box1[1], box2[1])
    point3_min = min(box1[2], box2[2])
    point3_max = max(box1[2], box2[2])
    point4_min = min(box1[3], box2[3])
    point4_max = max(box1[3], box2[3])

    return point1_min + 0.05 > point1_max and \
           point2_min + 0.05 > point2_max and \
           point3_min + 0.05 > point3_max and \
           point4_min + 0.05 > point4_max


# extract the coordinates of the rectangle that's to be drawn on the image
def draw_boxes(height, width, box, img, label):
    # starting coordinates of the box
    ymin = int(max(1, (box[0] * height)))
    xmin = int(max(1, (box[1] * width)))
    # last coordinates of the box
    ymax = int(min(height, (box[2] * height)))
    xmax = int(min(width, (box[3] * width)))

    # draw a rectangle using the coordinates
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (10, 255, 0), 1)
    cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)


def draw_hero_scores(height, width, box, img, score):
    # last coordinates of the box
    ymax = int(min(height, (box[2] * height)))
    xmin = int(max(1, (box[1] * width)))

    cv2.putText(img, str(score), (xmin, ymax + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)


def draw_hero_icon(x_offset, y_offset, icon, img):
    icon = cv2.resize(icon, (40, 40))

    y1, y2 = y_offset, y_offset + icon.shape[0]
    x1, x2 = x_offset, x_offset + icon.shape[1]

    alpha_s = icon[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha_s * icon[:, :, c] +
                                alpha_l * img[y1:y2, x1:x2, c])


def draw_overall_test_results(height, width, img, ally_score, enemy_score, recommendations):
    cv2.putText(img, "Ally Score: " + str(ally_score), (int(width * 0.2), int(height * 0.45)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (234, 185, 63), 2)
    cv2.putText(img, "Enemy Score: " + str(enemy_score), (int(width * 0.2), int(height * 0.41)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (26, 1, 243), 2)

    # best heroes
    cv2.putText(img, "Best Heroes", (int(width * 0.82), int(height * 0.10)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (10, 255, 0), 2)
    y_offset = int(height * 0.15)
    x_offset = int(width * 0.82)
    for tank in recommendations["best"][0][:2]:
        icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[tank["hero"]], -1)
        draw_hero_icon(x_offset, y_offset, icon, img)
        cv2.putText(img, tank["hero"], (x_offset, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(img, str(tank["score"]), (x_offset + 60, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (10, 255, 0), 2)
        y_offset += 80

    y_offset += 25
    for dps in recommendations["best"][1][:3]:
        icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[dps["hero"]], -1)
        draw_hero_icon(x_offset, y_offset, icon, img)
        cv2.putText(img, dps["hero"], (x_offset, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(img, str(dps["score"]), (x_offset + 60, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (10, 255, 0),
                    2)
        y_offset += 80

    y_offset += 25
    for support in recommendations["best"][2][:2]:
        icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[support["hero"]], -1)
        draw_hero_icon(x_offset, y_offset, icon, img)
        cv2.putText(img, support["hero"], (x_offset, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(img, str(support["score"]), (x_offset + 60, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (10, 255, 0), 2)
        y_offset += 80

    # worst heroes
    cv2.putText(img, "Worst Heroes", (int(width * 0.05), int(height * 0.10)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (10, 255, 0), 2)
    x_offset = int(width * 0.05)
    y_offset = int(height * 0.15)
    for tank in recommendations["worst"][0][:2]:
        icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[tank["hero"]], -1)
        draw_hero_icon(x_offset, y_offset, icon, img)
        cv2.putText(img, tank["hero"], (x_offset, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(img, str(tank["score"]), (x_offset + 60, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (10, 255, 0), 2)
        y_offset += 80

    y_offset += 25
    for dps in recommendations["worst"][1][:3]:
        icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[dps["hero"]], -1)
        draw_hero_icon(x_offset, y_offset, icon, img)
        cv2.putText(img, dps["hero"], (x_offset, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(img, str(dps["score"]), (x_offset + 60, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (10, 255, 0), 2)
        y_offset += 80

    y_offset += 25
    for support in recommendations["worst"][2][:2]:
        icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[support["hero"]], -1)
        draw_hero_icon(x_offset, y_offset, icon, img)
        cv2.putText(img, support["hero"], (x_offset, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(img, str(support["score"]), (x_offset + 60, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (10, 255, 0), 2)
        y_offset += 80


def draw_hero_switch_results(hero, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst, img):
    if hero["from"] is not None:
        # best hero switches
        from_hero_icon_path = config.hero_icons_path + "/" + hero_icons_mapping[hero["from"]["hero"]]
        from_hero = hero["from"]["hero"]
        from_hero_score = str(hero["from"]["score"])
        if img is not None:
            from_icon = cv2.imread(from_hero_icon_path, -1)
            draw_hero_icon(x_offset_best, y_offset_best, from_icon, img)
            cv2.putText(img, from_hero, (x_offset_best, y_offset_best + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (10, 255, 0),
                        2)
            cv2.putText(img, from_hero_score, (x_offset_best + 50, y_offset_best + 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (10, 255, 0), 2)
            cv2.putText(img, "->", (x_offset_best + 95, y_offset_best + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (10, 255, 0), 2)
        else:
            # production
            overlay.Draw.display_image(from_hero_icon_path, x_offset_best, y_offset_best)
            overlay.Draw.text(x_offset_best, y_offset_best + 70, overlay.Draw.green, from_hero)
            overlay.Draw.text(x_offset_best + 90, y_offset_best + 40, overlay.Draw.green, from_hero_score)
            overlay.Draw.text(x_offset_best + 135, y_offset_best + 40, overlay.Draw.green, "->")

        for best_hero_switch in hero["to_best"]:
            to_hero_icon_path = config.hero_icons_path + "/" + hero_icons_mapping[best_hero_switch["hero"]]
            to_hero_score = str(best_hero_switch["score"])
            if img is not None:
                to_icon = cv2.imread(to_hero_icon_path, -1)
                draw_hero_icon(x_offset_best + 140, y_offset_best, to_icon, img)
                cv2.putText(img, to_hero_score, (x_offset_best + 140, y_offset_best + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (10, 255, 0), 2)
            else:
                # production
                overlay.Draw.display_image(to_hero_icon_path, x_offset_best + 170, y_offset_best)
                overlay.Draw.text(x_offset_best + 185, y_offset_best + 70, overlay.Draw.green, to_hero_score)
            x_offset_best += 70
        y_offset_best += 100

        # worst hero switches
        from_hero_icon_path = config.hero_icons_path + "/" + hero_icons_mapping[hero["from"]["hero"]]
        from_hero = hero["from"]["hero"]
        from_hero_score = str(hero["from"]["score"])
        if img is not None:
            from_icon = cv2.imread(from_hero_icon_path, -1)
            draw_hero_icon(x_offset_worst, y_offset_worst, from_icon, img)
            cv2.putText(img, from_hero, (x_offset_worst, y_offset_worst + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (10, 255, 0), 2)
            cv2.putText(img, from_hero_score, (x_offset_worst + 50, y_offset_worst + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (10, 255, 0), 2)

            cv2.putText(img, "->", (x_offset_worst + 95, y_offset_worst + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (10, 255, 0), 2)
        else:
            # production
            overlay.Draw.display_image(from_hero_icon_path, x_offset_worst, y_offset_worst)
            overlay.Draw.text(x_offset_worst, y_offset_worst + 70, overlay.Draw.green, from_hero)
            overlay.Draw.text(x_offset_worst + 90, y_offset_worst + 40, overlay.Draw.green, from_hero_score)
            overlay.Draw.text(x_offset_worst + 135, y_offset_worst + 40, overlay.Draw.green, "->")

        for worst_hero_switch in hero["to_worst"]:
            to_hero_icon_path = config.hero_icons_path + "/" + hero_icons_mapping[worst_hero_switch["hero"]]
            to_hero_score = str(worst_hero_switch["score"])
            if img is not None:
                to_icon = cv2.imread(to_hero_icon_path, -1)
                draw_hero_icon(x_offset_worst + 140, y_offset_worst, to_icon, img)
                cv2.putText(img, to_hero_score, (x_offset_worst + 140, y_offset_worst + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (10, 255, 0), 2)
            else:
                # production
                overlay.Draw.display_image(to_hero_icon_path, x_offset_worst + 170, y_offset_worst)
                overlay.Draw.text(x_offset_worst + 185, y_offset_worst + 70, overlay.Draw.green, to_hero_score)

            x_offset_worst += 70
        y_offset_worst += 100

    else:
        for best_hero in hero["to_best"]:
            best_hero_path = config.hero_icons_path + "/" + hero_icons_mapping[best_hero["hero"]]
            best_hero_name = best_hero["hero"]
            best_hero_score = str(best_hero["score"])
            icon = cv2.imread(best_hero_path, -1)
            if img is not None:
                draw_hero_icon(x_offset_best, y_offset_best, icon, img)
                cv2.putText(img, best_hero_name, (x_offset_best, y_offset_best + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
                cv2.putText(img, best_hero_score, (x_offset_best + 50, y_offset_best + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (10, 255, 0), 2)
            else:
                # production
                overlay.Draw.display_image(best_hero_path, x_offset_best, y_offset_best)
                overlay.Draw.text(x_offset_best, y_offset_best + 70, overlay.Draw.green, best_hero_name)
                overlay.Draw.text(x_offset_best + 90, y_offset_best + 30, overlay.Draw.green, best_hero_score)
            y_offset_best += 100

        for worst_hero in hero["to_worst"]:
            worst_hero_path = config.hero_icons_path + "/" + hero_icons_mapping[worst_hero["hero"]]
            worst_hero_name = worst_hero["hero"]
            worst_hero_score = str(worst_hero["score"])
            icon = cv2.imread(worst_hero_path, -1)
            if img is not None:
                draw_hero_icon(x_offset_worst, y_offset_worst, icon, img)
                cv2.putText(img, worst_hero_name, (x_offset_worst, y_offset_worst + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
                cv2.putText(img, worst_hero_score, (x_offset_worst + 50, y_offset_worst + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (10, 255, 0), 2)
            else:
                # production
                overlay.Draw.display_image(worst_hero_path, x_offset_worst, y_offset_worst)
                overlay.Draw.text(x_offset_worst, y_offset_worst + 70, overlay.Draw.green, worst_hero_name)
                overlay.Draw.text(x_offset_worst + 90, y_offset_worst + 30, overlay.Draw.green, worst_hero_score)
            y_offset_worst += 100

    return y_offset_best, y_offset_worst


def draw_overall_test_results_ver_b(height, width, img, ally_score, enemy_score, recommendations):
    cv2.putText(img, "Ally Score: " + str(ally_score), (int(width * 0.2), int(height * 0.45)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (234, 185, 63), 2)
    cv2.putText(img, "Enemy Score: " + str(enemy_score), (int(width * 0.2), int(height * 0.41)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (26, 1, 243), 2)

    # best heroes
    cv2.putText(img, "Best Heroes", (int(width * 0.82), int(height * 0.10)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (10, 255, 0), 2)
    y_offset_best = int(height * 0.15)
    x_offset_best = int(width * 0.82)

    # worst heroes
    cv2.putText(img, "Worst Heroes", (int(width * 0.05), int(height * 0.10)), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                (10, 255, 0), 2)
    y_offset_worst = int(height * 0.15)
    x_offset_worst = int(width * 0.05)

    for tank in recommendations[0]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(tank, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst, img)

    y_offset_best = int(height * 0.40)
    y_offset_worst = int(height * 0.40)

    for dps in recommendations[1]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(dps, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst, img)

    y_offset_best = int(height * 0.65)
    y_offset_worst = int(height * 0.65)

    for support in recommendations[2]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(support, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst, img)


def draw_results_to_overlay(height, width, ally_score, enemy_score, recommendations):
    import OpenGL.GLUT as glut
    #  A pointer to a font style..
    #  Fonts supported by GLUT are: GLUT_BITMAP_8_BY_13,
    #  GLUT_BITMAP_9_BY_15, GLUT_BITMAP_TIMES_ROMAN_10,
    #  GLUT_BITMAP_TIMES_ROMAN_24, GLUT_BITMAP_HELVETICA_10,
    #  GLUT_BITMAP_HELVETICA_12, and GLUT_BITMAP_HELVETICA_18.
    font_style = glut.GLUT_BITMAP_TIMES_ROMAN_24
    overlay.Draw.text(int(width * 0.23), int(height * 0.545), overlay.Draw.cyan, "Ally Score: " + str(ally_score), font_style)
    overlay.Draw.text(int(width * 0.23), int(height * 0.59), overlay.Draw.alert, "Enemy Score: " + str(enemy_score), font_style)

    # best heroes
    overlay.Draw.text(int(width * 0.82), int(height * 0.90), overlay.Draw.green, "Best Heroes Picks")
    overlay.Draw.line(int(width * 0.82), int(height * 0.90) - 10, int(width * 0.9), int(height * 0.90) - 10, 2, overlay.Draw.green)
    y_offset_best = int(height * 0.15)
    x_offset_best = int(width * 0.82)

    # worst heroes
    overlay.Draw.text(int(width * 0.05), int(height * 0.90), overlay.Draw.green, "Worst Heroes Picks")
    overlay.Draw.line(int(width * 0.05), int(height * 0.90) - 10, int(width * 0.12), int(height * 0.90) - 10, 2, overlay.Draw.green)
    y_offset_worst = int(height * 0.15)
    x_offset_worst = int(width * 0.05)

    for tank in recommendations[0]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(tank, x_offset_best, x_offset_worst,
                                                                 y_offset_best, y_offset_worst, None)

    y_offset_best = int(height * 0.40)
    y_offset_worst = int(height * 0.40)

    for dps in recommendations[1]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(dps, x_offset_best, x_offset_worst, y_offset_best,
                                                                 y_offset_worst, None)

    y_offset_best = int(height * 0.65)
    y_offset_worst = int(height * 0.65)

    for support in recommendations[2]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(support, x_offset_best, x_offset_worst,
                                                                 y_offset_best, y_offset_worst, None)
    return None
