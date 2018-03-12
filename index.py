from nba_py import player
import plotly.offline as po
import plotly.graph_objs as pgo


def get_player_current(pid, nb_games, name):

    total_fp = []
    game_n_fp = []

    for idx in range(nb_games, 0, -1):
        splits = player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base",
                                             last_n_games=idx, per_mode='Totals').overall()

        total_fp.append(splits['NBA_FANTASY_PTS'].values[0])

    game_n_fp.append(total_fp[len(total_fp) - 1])

    for idx in range(len(total_fp) - 1, 0, -1):
        game_n_fp.append(total_fp[idx - 1] - total_fp[idx])

    trace = pgo.Scatter( x=range(len(game_n_fp), 0, -1),
                         y=game_n_fp,
                         mode='lines+markers')
    data = [trace]

    po.plot(data, filename='line %s.html' % name)


def main():

    deck = [
        ["Chris", "Paul"],
        ["Ben", "Simmons"],
        ["Draymond", "Green"],
        ["Rudy", "Gobert"],
        ["DeMar", "DeRozan"],
        ["Karl-Anthony", "Towns"],
        ["Paul", "George"],
    ]

    nb_games = 5

    # -----------------------------------------------------------------------------------------------

    names = []
    last_n_games_fp = []
    overall_fp = []
    overall_gp = []

    for first_name, last_name in deck:
        pid = player.get_player(first_name, last_name, season="2017-18")

        info = player.PlayerSummary(pid).info()
        names.append('%s %s' % (info['FIRST_NAME'].values[0], info['LAST_NAME'].values[0]))

        last_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=nb_games).overall()
        last_n_games_fp.append(last_splits['NBA_FANTASY_PTS'].values[0])

        overall_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()
        overall_fp.append(overall_splits['NBA_FANTASY_PTS'].values[0])
        overall_gp.append(overall_splits['GP'].values[0])

        name = first_name + " " + last_name
        get_player_current(pid, nb_games, name)


    print "FANTASY POINTS avg over last %d games / season overall (games played)" % nb_games
    print "------------------------------------------- ------------------------"

    for idx in range(len(deck)):
        print "%s:  %.1f / %.1f (%d)" % (names[idx], last_n_games_fp[idx], overall_fp[idx], overall_gp[idx])


    trace1 = pgo.Bar(x=names, y=last_n_games_fp, name='last %d games fp avg' % nb_games)

    trace2 = pgo.Bar(x=names, y=overall_fp, name='season overall fp avg')

    data = [trace1, trace2]

    layout = pgo.Layout(barmode='group', xaxis=dict(tickangle=-45))

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='grouped-bar.html')


if __name__ == "__main__":
    # execute only if run as a script
    main()