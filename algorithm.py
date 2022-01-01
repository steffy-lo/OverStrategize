import config
from data import hero_info, hero_tiers, hero_adc, hero_maps, hero_counters, hero_synergies, map_info


def hero_scores(allies, enemies, rank, map=None, ad=None, point=None):
    ally_hero_scores = {}
    for hero in config.labels.values():
        ally_hero_scores[hero] = hero_tiers.data["All"][hero]
        synergy_score = 0
        counter_score = 0
        for hero_counter in enemies:
            counter_score += hero_counters.data[hero][hero_counter]
        for hero_synergy in allies:
            if hero != hero_synergy:
                synergy_score += hero_synergies.data[hero][hero_synergy]
        ally_hero_scores[hero] += synergy_score + counter_score

    enemy_hero_scores = {}
    for hero in enemies:
        enemy_hero_scores[hero] = hero_tiers.data["All"][hero]
        synergy_score = 0
        counter_score = 0
        for hero_synergy in enemies:
            if hero != hero_synergy:
                synergy_score += hero_synergies.data[hero][hero_synergy]
        for hero_counter in allies:
            counter_score += hero_counters.data[hero][hero_counter]
        enemy_hero_scores[hero] += synergy_score + counter_score

    return ally_hero_scores, enemy_hero_scores


def team_scores(ally_hero_scores, allies, enemy_hero_scores, enemies):
    ally_score = 0
    for hero in allies:
        ally_score += ally_hero_scores[hero]

    enemy_score = 0
    for hero in enemies:
        enemy_score += enemy_hero_scores[hero]

    return ally_score, enemy_score


def hero_recommendations(ally_hero_scores, allies):
    remaining_tank = []
    remaining_dps = []
    remaining_support = []

    for hero, score in ally_hero_scores.items():
        if hero not in allies:
            # hero is not already picked
            if hero_info.data[hero]["generalRol"] == "Tank":
                remaining_tank.append({
                    "hero": hero,
                    "score": score
                })
            elif hero_info.data[hero]["generalRol"] == "Support":
                remaining_support.append({
                    "hero": hero,
                    "score": score
                })
            elif hero_info.data[hero]["generalRol"] == "Damage":
                remaining_dps.append({
                    "hero": hero,
                    "score": score
                })
            else:
                raise ValueError("Unknown hero: " + hero)

    # sort by score
    tank = sorted(remaining_tank, key=lambda k: k['score'], reverse=True)
    dps = sorted(remaining_dps, key=lambda k: k['score'], reverse=True)
    support = sorted(remaining_support, key=lambda k: k['score'], reverse=True)

    return {"best": [tank, dps, support],
            "worst": [tank[::-1], dps[::-1], support[::-1]]}


def hero_recommendation_by_line(line, line_num, ally_hero_scores, allies, enemies):
    line_recommendation = []
    if len(line) >= 2:
        i = 0
        for hero in line:
            line_recommendation.append({
                "from": hero,
                "to_best": [],
                "to_worst": []
            })
            allies_remove_one = list(filter(lambda x: x != hero["hero"], allies))
            ally_hero_scores_remove_one, enemy_hero_scores = hero_scores(allies_remove_one, enemies, "All")
            recommendations = hero_recommendations(ally_hero_scores_remove_one, allies_remove_one)
            line_recommendation[i]["to_best"] = recommendations["best"][line_num][:2]
            line_recommendation[i]["to_worst"] = recommendations["worst"][line_num][:2]
            i += 1

    elif len(line) == 1:
        recommendations = hero_recommendations(ally_hero_scores, allies)
        line_recommendation.append({
            "from": None,
            "to_best": recommendations["best"][line_num][:2],
            "to_worst": recommendations["worst"][line_num][:2]
        })
        line_recommendation.append({
            "from": line[0],
            "to_best": [],
            "to_worst": []
        })
        allies_remove_one = list(filter(lambda x: x != line[0]["hero"], allies))
        ally_hero_scores_remove_one, enemy_hero_scores = hero_scores(allies_remove_one, enemies, "All")
        recommendations = hero_recommendations(ally_hero_scores_remove_one, allies_remove_one)
        line_recommendation[1]["to_best"] = recommendations["best"][line_num][:2]
        line_recommendation[1]["to_worst"] = recommendations["worst"][line_num][:2]

    else:
        recommendations = hero_recommendations(ally_hero_scores, allies)
        line_recommendation.append({
            "from": None,
            "to_best": recommendations["best"][line_num][:3],
            "to_worst": recommendations["worst"][line_num][:3]
        })

    return line_recommendation


def hero_recommendation_ver_b(ally_hero_scores, allies, enemies):
    tank_line = []
    dps_line = []
    support_line = []

    for hero, score in ally_hero_scores.items():
        if hero in allies:
            if hero_info.data[hero]["generalRol"] == "Tank":
                tank_line.append({
                    "hero": hero,
                    "score": score
                })
            elif hero_info.data[hero]["generalRol"] == "Support":
                support_line.append({
                    "hero": hero,
                    "score": score
                })
            elif hero_info.data[hero]["generalRol"] == "Damage":
                dps_line.append({
                    "hero": hero,
                    "score": score
                })
            else:
                raise ValueError("Unknown hero: " + hero)

    tank_recommendations = hero_recommendation_by_line(tank_line, 0, ally_hero_scores, allies, enemies)
    dps_recommendations = hero_recommendation_by_line(dps_line, 1, ally_hero_scores, allies, enemies)
    support_recommendations = hero_recommendation_by_line(support_line, 2, ally_hero_scores, allies, enemies)

    return [tank_recommendations, dps_recommendations, support_recommendations]


