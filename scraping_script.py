import asyncio
import json
import aiohttp
import pandas as pd
from understat import Understat

# Script to get data


async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        fixtures = await understat.get_league_fixtures(
            "epl",
            2020)
        return(fixtures)

loop = asyncio.get_event_loop()
fixt = loop.run_until_complete(main())


away = [games["a"]["title"] for games in fixt]
home = [games["h"]["title"] for games in fixt]
date_time = [games["datetime"] for games in fixt]


games = pd.DataFrame({'home_team': home, 'away_team': away, 'date': date_time})

games.to_csv("Fixtures.csv")

# Define season (first year)
year = 2020


async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_results(
            "epl",
            year)
        return(results)

loop = asyncio.get_event_loop()
test = loop.run_until_complete(main())
df = pd.DataFrame(test)
ids = df.id.tolist()
ids = [int(i) for i in ids]


async def first_match():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        first = await understat.get_match_shots(ids[0])
        return(first)


loop = asyncio.get_event_loop()
test2 = loop.run_until_complete(first_match())
df2 = pd.DataFrame(test2["h"])
df2 = df2.append(pd.DataFrame(test2["a"]))

for game_id in ids[1:]:
    async def main():
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            rest = await understat.get_match_shots(game_id)
            return(rest)

    loop = asyncio.get_event_loop()
    test2 = loop.run_until_complete(main())
    df = pd.DataFrame(test2["h"])
    df_a = pd.DataFrame(test2["a"])
    df2 = df2.append(df)
    df2 = df2.append(df_a)

# Define filename
output_filename = "Pl20.csv"

df2.to_csv(output_filename)
