from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from collections import OrderedDict
from operator import getitem
import time, datetime
import pandas as pd

########## Configuration String ##########

GRAPHQL_URL = "https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql"
HERO_ID = [211611,230177,194969,1759,1353,700]

##########################################

transport = AIOHTTPTransport(url=GRAPHQL_URL)
client = Client(transport=transport, fetch_schema_from_transport=True)

graphQuery = """
{
  heroes(where:{id_in:HERO_ID}, orderBy:nextSummonTime, orderDirection:asc){
    id
    mainClass
    nextSummonTime
  }
}
"""

graphQuery = graphQuery.replace("HERO_ID",str(HERO_ID))

query = gql(
    graphQuery
)

# Execute the query on the transport
result = client.execute(query)

for item in result['heroes']:
    item.update({"nextSummonTime":datetime.datetime.fromtimestamp(int(item['nextSummonTime'])).strftime("%d-%b-%y  %H: %M") })

df = pd.json_normalize(result['heroes'])
df.columns = ['ID', 'Class', 'Next Summon Time']

print(df.to_string(index=False))
