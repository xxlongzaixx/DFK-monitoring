from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from collections import OrderedDict
from operator import getitem
import time, datetime

########## Configuration String ##########

GRAPHQL_URL = "https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql"
HERO_ID = "700"

##########################################

transport = AIOHTTPTransport(url=GRAPHQL_URL)

client = Client(transport=transport, fetch_schema_from_transport=True)

graphQuery = """
{
  assistingAuctions(where: {tokenId: "HERO_ID"}, orderBy: id, orderDirection: desc) {
    id
    seller {
      id
    }
    tokenId {
      id
    }
    startingPrice
    endingPrice
    duration
    startedAt
    winner {
      id
    }
    endedAt
    open
    purchasePrice
  }
}

"""

graphQuery = graphQuery.replace("HERO_ID",HERO_ID)

query = gql(
    graphQuery
)

# Execute the query on the transport
result = client.execute(query)
print(f"Rental Data for Heroes #{HERO_ID}  ===")
for item in result['assistingAuctions']:
    status = ""
    if item['purchasePrice'] is not None:
        #print(item['purchasePrice'][:-18])
        status = u'\u2713'
    else:
        status = ""

    d = 'Open'
    if item['endedAt'] != None:
        d = datetime.datetime.fromtimestamp(int(item['endedAt'])).strftime("%d-%b-%y  %H: %M")
    #duration = item['endedAt'] - item['startedAt']

    print(d, " Price:" , item['startingPrice'][:-18], status, item['seller']['id'][-4:] )
