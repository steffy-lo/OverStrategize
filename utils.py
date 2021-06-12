import cv2
import config

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


def draw_hero_switch_results(hero, img, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst):
    if hero["from"] is not None:
        # best hero switches
        from_icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[hero["from"]["hero"]], -1)
        draw_hero_icon(x_offset_best, y_offset_best, from_icon, img)
        cv2.putText(img, hero["from"]["hero"], (x_offset_best, y_offset_best + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (10, 255, 0),
                    2)
        cv2.putText(img, str(hero["from"]["score"]), (x_offset_best + 50, y_offset_best + 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (10, 255, 0), 2)

        cv2.putText(img, "->", (x_offset_best + 95, y_offset_best + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (10, 255, 0), 2)
        for best_hero_switch in hero["to_best"]:
            to_icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[best_hero_switch["hero"]], -1)
            draw_hero_icon(x_offset_best + 140, y_offset_best, to_icon, img)
            cv2.putText(img, str(best_hero_switch["score"]), (x_offset_best + 140, y_offset_best + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (10, 255, 0), 2)
            x_offset_best += 60

        y_offset_best += 80

        # worst hero switches
        from_icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[hero["from"]["hero"]], -1)
        draw_hero_icon(x_offset_worst, y_offset_worst, from_icon, img)
        cv2.putText(img, hero["from"]["hero"], (x_offset_worst, y_offset_worst + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (10, 255, 0), 2)
        cv2.putText(img, str(hero["from"]["score"]), (x_offset_worst + 50, y_offset_worst + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (10, 255, 0), 2)

        cv2.putText(img, "->", (x_offset_worst + 95, y_offset_worst + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (10, 255, 0), 2)
        for worst_hero_switch in hero["to_worst"]:
            to_icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[worst_hero_switch["hero"]], -1)
            draw_hero_icon(x_offset_worst + 140, y_offset_worst, to_icon, img)
            cv2.putText(img, str(worst_hero_switch["score"]), (x_offset_worst + 140, y_offset_worst + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (10, 255, 0), 2)
            x_offset_worst += 60

        y_offset_worst += 80
    else:
        for best_hero in hero["to_best"]:
            icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[best_hero["hero"]], -1)
            draw_hero_icon(x_offset_best, y_offset_best, icon, img)
            cv2.putText(img, best_hero["hero"], (x_offset_best, y_offset_best + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
            cv2.putText(img, str(best_hero["score"]), (x_offset_best + 50, y_offset_best + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (10, 255, 0), 2)
            y_offset_best += 80

        for worst_hero in hero["to_worst"]:
            icon = cv2.imread(config.hero_icons_path + "/" + hero_icons_mapping[worst_hero["hero"]], -1)
            draw_hero_icon(x_offset_worst, y_offset_worst, icon, img)
            cv2.putText(img, worst_hero["hero"], (x_offset_worst, y_offset_worst + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
            cv2.putText(img, str(worst_hero["score"]), (x_offset_worst + 50, y_offset_worst + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (10, 255, 0), 2)
            y_offset_worst += 80

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
        y_offset_best, y_offset_worst = draw_hero_switch_results(tank, img, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst)

    y_offset_best = int(height * 0.40)
    y_offset_worst = int(height * 0.40)

    for dps in recommendations[1]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(dps, img, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst)

    y_offset_best = int(height * 0.65)
    y_offset_worst = int(height * 0.65)

    for support in recommendations[2]:
        y_offset_best, y_offset_worst = draw_hero_switch_results(support, img, x_offset_best, x_offset_worst, y_offset_best, y_offset_worst)