from collections import defaultdict
import csv
import itertools
import random

import numpy as np
import matplotlib.pyplot as plt
from pymc import *
from scipy import stats

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


def player_scores_by_week(data, num_rounds, players):
    scores = {p:[0]*(num_rounds+1) for p in players}
    for row in data:
        scores[row['player_1']][int(row['week'])] = float(row['player_1_score'])
        scores[row['player_2']][int(row['week'])] = float(row['player_2_score'])
    return scores


def generate_round_robin_schedule(num_players, num_rounds):
    round_robin_schedule = [[None]*(num_players-1) for _ in range(num_players)]
    for p in range(num_players):
        for r in range(num_players-1):
            round_robin_schedule[p][r] = ((num_players - p - 1) - r) % num_players
    round_robin_schedule = np.array(round_robin_schedule)
    schedule = np.concatenate((round_robin_schedule, round_robin_schedule[:,:(num_rounds-(num_players-1))]), axis=1)
    return schedule


def get_standings(scores, schedule, players):
    player_win_loss = defaultdict(lambda: [0, 0])
    for pid in range(len(schedule)):
        # weeks range from 1-n
        for week in range(1, len(schedule[pid])+1):
            opid = schedule[pid][week-1]
            player = players[pid]
            opponent = players[opid]
            player_score = scores[player][week]
            opponent_score = scores[opponent][week]
            if player_score > opponent_score:
                player_win_loss[player][0] += 1
            else:
                player_win_loss[player][1] += 1
    return dict(player_win_loss)


def generate_model(wins):
    lambda_ = Uniform('lambda_', lower=0, upper=15)
    process = Poisson('process', mu=lambda_, value=wins, observed=True)
    return locals()


def simulate_games(players, scores, schedule, num_schedules_to_simulate):
    simulations = defaultdict(list)
    i = 0
    for players_permuted in itertools.permutations(players):
        i += 1
        standings = get_standings(scores, schedule, players_permuted)
        for player in standings:
            wins, losses = standings[player]
            simulations[player].append(wins)
        if i % 10000 == 0:
            print "simulated {}".format(i)
        if i >= num_schedules_to_simulate:
            break
    return simulations


def generate_models(simulations):
    player_models = dict()
    for player, wins in simulations.iteritems():
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


def fantasy_models():
    data = read_data()
    players = read_players(data)
    num_rounds = get_num_rounds(data)
    scores = player_scores_by_week(data, num_rounds, players)
    num_schedules_to_simulate = 10000000
    num_samples_for_modeling = 1500 #2000

    schedule = generate_round_robin_schedule(len(players), num_rounds)
    simulations = simulate_games(players, scores, schedule, num_schedules_to_simulate)
    player_models = generate_models(simulations)

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
        plt.plot(x, stats.poisson.pmf(x, stats['lambda_']['mean']), '-' + markers.next(), label=player)
    ax.legend()
    plt.show()


def fantasy_simulations():
    data = read_data()
    players = read_players(data)
    num_rounds = get_num_rounds(data)
    scores = player_scores_by_week(data, num_rounds, players)
    num_schedules_to_simulate = 10000000

    schedule = generate_round_robin_schedule(len(players), num_rounds)
    simulations = simulate_games(players, scores, schedule, num_schedules_to_simulate)

    fig = plt.figure()

    ax = fig.add_subplot(1,1,1)
    ax.set_title("Through Week {}".format(num_rounds))
    ax.set_xlabel('Number of Wins')
    ax.set_ylabel('Probability of Number of Wins')
    ax.set_xlim(0, num_rounds)
    for player, wins in simulations.iteritems():
        x = np.array(range(num_rounds+1))
        y = [0]*(num_rounds+1)
        for w in wins:
            y[w] += 1
        print player, y
        y = np.array(y)/float(len(wins))
        plt.plot(x, y, '-' + markers.next(), label=player)
    ax.legend()
    plt.show()

if __name__ == '__main__':
    fantasy_simulations()
