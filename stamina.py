from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from collections import OrderedDict
from operator import getitem
import time, math

########## Configuration String ##########

GRAPHQL_URL = "https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql"
ADDRESS  = "0xD688F76E844f2982a776cBf59235fa2aB79cF726"
HERO_SHOWN = 6 #number of heroes shown in results in each category
TQ_HEROES = ['1353','1759','73659','180273','43371','700','58270','63009','102956','177124','23915'] #heroes id which falls under training quests category

##########################################

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url=GRAPHQL_URL)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
graphQuery = """
{
heroes(where: {owner: "ADDRESS"}) {
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

def getXpNeeded(currentLevel):
  xpNeeded = 0
  nextLevel = currentLevel + 1;

  if currentLevel < 6:
    xpNeeded = nextLevel * 1000
  elif currentLevel < 9:
    xpNeeded = 4000 + (nextLevel - 5) * 2000
  elif currentLevel < 16:
    xpNeeded = 12000 + (nextLevel - 9) * 4000
  elif currentLevel < 36:
    xpNeeded = 40000 + (nextLevel - 16) * 5000
  elif currentLevel < 56:
      xpNeeded = 140000 + (nextLevel - 36) * 7500
  elif currentLevel >= 56:
      xpNeeded = 290000 + (nextLevel - 56) * 10000;
  return xpNeeded

def getCurrentStamina(id, staminaFullAt,stamina):
  ts = time.time()
  currentStamina = stamina - ((staminaFullAt-ts) / (20*60))
  return currentStamina

def getTimerCD(stamina):
    if stamina < 20:
        return ' (' + str(math.ceil((20 - stamina) * 20)) + ' min)'
    else:
        return ''

def printDetails(heroes,entries):
    for x in range(min(len(heroes),entries)):
      print(str(heroes[x]['id']) , ', ',
      str(heroes[x]['xpLeft']) , ', ' ,
      '{0:.2f}'.format(heroes[x]['currentStamina']) ,
      getTimerCD(heroes[x]['currentStamina']) , ', ',
      str(heroes[x]['status']), ', ',
      heroes[x]['mainClass'] , ' (' , heroes[x]['profession'] ,')' ,
      sep='')

graphQuery = graphQuery.replace("ADDRESS",ADDRESS)

query = gql(
    graphQuery
)

# Execute the query on the transport
result = client.execute(query)
for item in result['heroes']:
    xpNeeded = getXpNeeded(item['level'])
    xpLeft = xpNeeded - item ['xp']
    currentStamina = getCurrentStamina(item['id'], item['staminaFullAt'], item['stamina'])
    item.update( {"xpNeeded":xpNeeded})
    item.update( {"xpLeft":xpLeft})
    item.update( {"currentStamina":currentStamina})
    if item['currentQuest'] == '0x0000000000000000000000000000000000000000':
        item.update( {"status":"idle"})
    else:
        item.update( {"status":"questing"})
    if item['id'] in TQ_HEROES:
        item.update( {"isTQ":"true"})
    else:
        item.update( {"isTQ":"false"})

print("=== Experience  ===")
print("ID , XP NEEDED , CURRENT STAMINA , STATUS , HERO CLASS (PROFESSION)")
heroes = result['heroes']
heroes.sort(key=lambda x: x.get('xpLeft'))
printDetails(heroes,HERO_SHOWN)

print("\n\n=== Gardening Heroes  ===")
TimerQuestHeroes = list(filter(lambda x: x.get('currentQuest') == '0x0000000000000000000000000000000000000000' and x.get('profession') in ('gardening') and x.get('isTQ') == 'false', heroes))
TimerQuestHeroes.sort(key=lambda x: x.get('currentStamina'), reverse=True)
printDetails(TimerQuestHeroes,HERO_SHOWN)

print("\n\n=== Mining Heroes  ===")
TimerQuestHeroes = list(filter(lambda x: x.get('currentQuest') == '0x0000000000000000000000000000000000000000' and x.get('profession') in ('mining') and x.get('isTQ') == 'false', heroes))
TimerQuestHeroes.sort(key=lambda x: x.get('currentStamina'), reverse=True)
printDetails(TimerQuestHeroes,HERO_SHOWN)

print("\n\n=== Fishing Heroes  ===")
idleHeroes = list(filter(lambda x: x.get('currentQuest') == '0x0000000000000000000000000000000000000000' and x.get('profession') in ('fishing') and x.get('isTQ') == 'false', heroes))
idleHeroes.sort(key=lambda x: x.get('currentStamina'), reverse=True)
printDetails(idleHeroes,HERO_SHOWN)

print("\n\n=== Foraging Heroes  ===")
idleHeroes = list(filter(lambda x: x.get('currentQuest') == '0x0000000000000000000000000000000000000000' and x.get('profession') in ('foraging') and x.get('isTQ') == 'false', heroes))
idleHeroes.sort(key=lambda x: x.get('currentStamina'), reverse=True)
printDetails(idleHeroes,HERO_SHOWN)

print("\n\n=== Training Quest Heroes  ===")
idleHeroes = list(filter(lambda x: x.get('currentQuest') == '0x0000000000000000000000000000000000000000' and x.get('isTQ') == 'true', heroes))
idleHeroes.sort(key=lambda x: x.get('currentStamina'), reverse=True)
printDetails(idleHeroes,HERO_SHOWN)
