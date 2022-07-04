from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from itertools import groupby
import pandas as pd

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
ADDRESS =   [
             "0x2E7669F61eA77F02445A015FBdcFe2DE47083E02"
             ,"0x0A81cacC9Fd26f34363A415B6dD69c45cA1837e4"
            ]


graphQuery = """
{
  heroes(where: {owner_in: ADDRESS}) {
    owner {
      id
      name
    }
    xp
    level
    id
    staminaFullAt
    stamina
    currentQuest
    mainClass
    profession
  }
}

"""

graphQuery = graphQuery.replace("ADDRESS", str(ADDRESS).replace("\'", "\""))

query = gql(
    graphQuery
)

result = client.execute(query)

for item in result['heroes']:
    item.update( {"index":ADDRESS.index(item['owner']['id'])})

print("Total Heroes: ", len(result['heroes']), "\n")

def key_index(x):
    return x['index']

def key_profession(x):
    return x['profession']

heroes_by_user = sorted(result['heroes'], key=key_index)

for key, value in groupby(heroes_by_user, key_index):
    profession_by_heroes = sorted(list(value), key=key_profession)

    print(profession_by_heroes[0]["owner"]['name'], "({})".format(len(profession_by_heroes)))

    data = {}

    for key, value in groupby(profession_by_heroes, key_profession):
        data[key] = [len(list(value))]

    df = pd.DataFrame(data)

    print(df.to_string(index=False), "\n")
