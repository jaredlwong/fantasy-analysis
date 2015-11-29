from collections import defaultdict
import csv
import itertools
import random

import numpy as np
import matplotlib.pyplot as plt
from pymc import *
from scipy.stats import poisson

def read_data():
    data = []
    with open('fantasy.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def read_players(data):
    players = set()
    for row in data:
        players.add(row['player_1'])
        players.add(row['player_2'])
    return list(players)


def get_num_rounds(data):
    last_round = None
    for row in data:
        last_round = max(last_round, int(row['week'])) if last_round else int(row['week'])
    return last_round


def player_scores_by_week(data):
    scores = dict()
    for row in data:
        scores[(int(row['week']), row['player_1'])] = float(row['player_1_score'])
        scores[(int(row['week']), row['player_2'])] = float(row['player_2_score'])
    return scores


def generate_round_robin_schedule(num_players, num_rounds):
    round_robin_schedule = [[None]*num_rounds for _ in range(num_players)]
    for p in range(num_players):
        for r in range(num_rounds):
            round_robin_schedule[p][r] = ((num_players - p - 1) - r) % num_players
    return round_robin_schedule


def get_standings(scores, schedule, ids_to_players):
    player_win_loss = defaultdict(lambda: [0, 0])
    for pid in range(len(schedule)):
        # weeks range from 1-n
        for week in range(1, len(schedule[pid])+1):
            opid = schedule[pid][week-1]
            player = ids_to_players[pid]
            opponent = ids_to_players[opid]
            player_score = scores[(week, player)]
            opponent_score = scores[(week, opponent)]
            if player_score > opponent_score:
                player_win_loss[player][0] += 1
            else:
                player_win_loss[player][1] += 1
    return dict(player_win_loss)


def generate_model(wins):
    lambda_ = Uniform('lambda_', lower=0, upper=15)
    process = Poisson('process', mu=lambda_, value=wins, observed=True)
    return locals()


def generate_models(players, scores, num_rounds, schedule, num_schedules_to_simulate):
    samples = defaultdict(list)

    for i in range(num_schedules_to_simulate):
        random.shuffle(players)
        ids_to_players = dict(enumerate(players))
        standings = get_standings(scores, schedule, ids_to_players)
        for player in standings:
            wins, losses = standings[player]
            samples[player].append(wins)
        if i % 10000 == 0:
            print "simulated {}".format(i)

    player_models = dict()
    for player, wins in samples.iteritems():
        wins = map(float, wins)
        model = MCMC(generate_model(wins))
        player_models[player] = model

    return player_models


markers = itertools.cycle([
    'o',  # circle marker
    'v',  # triangle_down marker
    's',  # square marker
    'p',  # pentagon marker
    '*',  # star marker
    'h',  # hexagon1 marker
    'x',  # x marker
    '+',  # plus marker
    'D',  # diamond marker
    '1',  # tri_down marker
    '2',  # tri_up marker
    '3',  # tri_left marker
    '4',  # tri_right marker
    'H',  # hexagon2 marker
    'd',  # thin_diamond marker
    '^',  # triangle_up marker
    '<',  # triangle_left marker
    '>',  # triangle_right marker
])


if __name__ == '__main__':
    data = read_data()
    players = read_players(data)
    scores = player_scores_by_week(data)
    num_schedules_to_simulate = 100000
    num_samples_for_modeling = 1500 #2000

    num_rounds = get_num_rounds(data)
    schedule = generate_round_robin_schedule(len(players), num_rounds)
    player_models = generate_models(players, scores, num_rounds, schedule, num_schedules_to_simulate)

    for player, model in player_models.iteritems():
        model.sample(iter=num_samples_for_modeling)

    fig = plt.figure()

    ax = fig.add_subplot(1,1,1)
    ax.set_title("Through Week {}".format(num_rounds))
    ax.set_xlabel('Number of Wins')
    ax.set_ylabel('Probability of Number of Wins')
    ax.set_xlim(0, num_rounds)
    for player, model in player_models.iteritems():
        stats = model.stats()
        x = np.array(range(num_rounds+1))
        plt.plot(x, poisson.pmf(x, stats['lambda_']['mean']), '-' + markers.next(), label=player)
    ax.legend()
    plt.show()
    #stats = model.stats()
