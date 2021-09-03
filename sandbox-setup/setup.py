from neo4j import GraphDatabase, basic_auth

MOVIES_CSV = "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/movies.csv"
GENRES_CSV = "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/genre.csv"
ACTORS_CSV = "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/actors.csv"
DIRECTORS_CSV = (
    "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/directors.csv"
)
USERS_CSV = "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/users.csv"

driver = GraphDatabase.driver(
    "bolt://44.197.216.229:7687", auth=basic_auth("neo4j", "actions-checkpoints-addition")
)

cypher_query_list = [
    """LOAD CSV WITH HEADERS FROM $movies AS row
  CREATE (n:Movie)
  SET n = row""",
    """LOAD CSV WITH HEADERS FROM $genres AS row
  CREATE (n:Genre)
  SET n = row""",
    """LOAD CSV WITH HEADERS FROM $actors AS row
  CREATE (n:Actor)
  SET n = row""",
    """LOAD CSV WITH HEADERS FROM $directors AS row
  CREATE (n:Director)
  SET n = row""",
    """LOAD CSV WITH HEADERS FROM $users AS row
  CREATE (n:User)
  SET n = row""",
    """CREATE INDEX ON :User(`relationship.start`)""",
    """CREATE INDEX ON :Actor(`relationship.start`)""",
    """CREATE INDEX ON :Director(`relationship.start`)""",
    """CREATE INDEX ON :Movie(`n.identity`)""",
    """CREATE INDEX ON :Genre(`relationship.end`)""",
    """MATCH (m:Movie),(a:User)
  WHERE m.`n.identity` = a.`relationship.end`
  CREATE (a)-[:RATED {rating: a.`relationship.properties.rating`, timestamp: a.`relationship.properties.timestamp`}]->(m)""",
    """MATCH (m:Movie),(a:Director)
  WHERE m.`n.identity` = a.`relationship.end`
  CREATE (a)-[:DIRECTED {role: a.`relationship.properties.role`}]->(m)""",
    """MATCH (m:Movie),(a:Actor)
  WHERE m.`n.identity` = a.`relationship.end`
  CREATE (a)-[:ACTED_IN {role: a.`relationship.properties.role`}]->(m)""",
    """MATCH (m:Movie),(g:Genre) WHERE m.`n.identity` = g.`relationship.start` CREATE (m)-[:IN_GENRE]->(g)""",
]

with driver.session(database="neo4j") as session:

    for query in cypher_query_list:

        session.run(
            query,
            movies=MOVIES_CSV,
            genres=GENRES_CSV,
            actors=ACTORS_CSV,
            directors=DIRECTORS_CSV,
            users=USERS_CSV,
        )

driver.close()
