# encoding: UTF-8

require 'elo'

# Array.prototype.forEach.call(document.getElementsByClassName("Grid-u-1-2"), function(x) { console.log(x.innerText) })

teams = {
  jared: ["👉👻👉👌💥💦"],
  richard: ["Caelestral"],
  aditya: ["SF 4th and 9ers", "Bane Gabbert"],
  stephen: ["Not Karena"],
  larry: ["Considerate Ninjas"],
  chinmay: ["Late Bloomer", "I Peaked"],
  kuan: ["404", "No star to the right"],
  kevin: ["BendItLikeBeckhamJr"],
  justin: ["Fitz not my Forte"],
  daniel: ["Carnage w/ Barnidge", "Learn 2 Reed"]
}

players = {}

teams.each_key { |name| players[name] = Elo::Player.new }

games = {
  "week_1" => [
    [[135.16, "👉👻👉👌💥💦"], [103.64, "Caelestral"]],
    [[139.72, "SF 4th and 9ers"], [130.60, "Not Karena"]],
    [[99.54, "Considerate Ninjas"], [85.02, "Late Bloomer"]],
    [[137.14, "404"], [105.22, "BendItLikeBeckhamJr"]],
    [[123.14, "Fitz not my Forte"], [79.60, "Carnage w/ Barnidge"]]
  ],
  "week_2" => [
    [[128.46, "👉👻👉👌💥💦"], [104.74, "Considerate Ninjas"]],
    [[107.14, "SF 4th and 9ers"], [128.90, "Caelestral"]],
    [[68.60, "Not Karena"], [104.24, "Carnage w/ Barnidge"]],
    [[116.26, "404"], [83.70, "Late Bloomer"]],
    [[87.16, "Fitz not my Forte"], [117.44, "BendItLikeBeckhamJr"]]
  ],
  "week_3" => [
    [[171.92, "👉👻👉👌💥💦"], [116.48, "404"]],
    [[147.82, "SF 4th and 9ers"], [124.70, "Considerate Ninjas"]],
    [[71.44, "Not Karena"], [114.72, "Caelestral"]],
    [[138.38, "Fitz not my Forte"], [150.20, "Late Bloomer"]],
    [[94.60, "BendItLikeBeckhamJr"], [103.46, "Carnage w/ Barnidge"]]
  ],
  "week_4" => [
    [[91.96, "👉👻👉👌💥💦"], [103.06, "Fitz not my Forte"]],
    [[108.04, "SF 4th and 9ers"], [103.76, "404"]],
    [[93.08, "Not Karena"], [84.38, "Considerate Ninjas"]],
    [[81.44, "Caelestral"], [99.32, "Carnage w/ Barnidge"]],
    [[77.24, "BendItLikeBeckhamJr"], [104.58, "Late Bloomer"]]
  ],
  "week_5" => [
    [[87.44, "👉👻👉👌💥💦"], [118.56, "BendItLikeBeckhamJr"]],
    [[93.50, "SF 4th and 9ers"], [113.38, "Fitz not my Forte"]],
    [[86.84, "Not Karena"], [120.66, "404"]],
    [[135.14, "Caelestral"], [112.12, "Considerate Ninjas"]],
    [[114.64, "Late Bloomer"], [98.74, "Carnage w/ Barnidge"]]
  ],
  "week_6" => [
    [[78.50, "👉👻👉👌💥💦"], [123.08, "Late Bloomer"]],
    [[131.78, "SF 4th and 9ers"], [94.80, "BendItLikeBeckhamJr"]],
    [[85.28, "Not Karena"], [121.26, "Fitz not my Forte"]],
    [[131.92, "Caelestral"], [99.50, "404"]],
    [[116.24, "Considerate Ninjas"], [159.90, "Carnage w/ Barnidge"]]
  ],
  "week_7" => [
    [[120.28, "👉👻👉👌💥💦"], [168.94, "Carnage w/ Barnidge"]],
    [[120.20, "SF 4th and 9ers"], [108.82, "Late Bloomer"]],
    [[83.80, "Not Karena"], [110.44, "BendItLikeBeckhamJr"]],
    [[120.58, "Caelestral"], [120.88, "Fitz not my Forte"]],
    [[104.40, "Considerate Ninjas"], [136.30, "404"]]
  ],
  "week_8" => [
    [[130.82, "👉👻👉👌💥💦"], [123.94, "SF 4th and 9ers"]],
    [[126.16, "Not Karena"], [103.04, "Late Bloomer"]],
    [[94.74, "Caelestral"], [109.74, "BendItLikeBeckhamJr"]],
    [[84.70, "Considerate Ninjas"], [113.70, "Fitz not my Forte"]],
    [[103.58, "404"], [83.98, "Carnage w/ Barnidge"]]
  ],
  "week_9" => [
    [[131.62, "👉👻👉👌💥💦"], [136.98, "Not Karena"]],
    [[119.06, "SF 4th and 9ers"], [115.24, "Carnage w/ Barnidge"]],
    [[155.66, "Caelestral"], [101.82, "Late Bloomer"]],
    [[122.74, "Considerate Ninjas"], [90.00, "BendItLikeBeckhamJr"]],
    [[127.16, "404"], [113.04, "Fitz not my Forte"]]
  ],
  "week_10" => [
    [[115.52, "👉👻👉👌💥💦"], [91.58, "Caelestral"]],
    [[103.36, "SF 4th and 9ers"], [122.52, "Not Karena"]],
    [[83.98, "Considerate Ninjas"], [97.04, "Late Bloomer"]],
    [[113.96, "404"], [121.46, "BendItLikeBeckhamJr"]],
    [[99.62, "Fitz not my Forte"], [93.86, "Carnage w/ Barnidge"]]
  ]
}

games.each do |week, games_in_week|
  games_in_week.each do |game|
    player_1_score = game[0][0]
    player_1_name = game[0][1]
    player_2_score = game[1][0]
    player_2_name = game[1][1]
    if player_1_score > player_2_score
      winner = player_1_name
      loser = player_2_name
    else
      winner = player_2_name
      loser = player_1_name
    end
    players[winner].wins_from(players[loser])
  end
end

players.each do |name, player|
  puts "#{player.rating}\t#{name}"
end
