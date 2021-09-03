//step1 - load movies
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/movies.csv" AS row
CREATE (n:Movie)
SET n = row

//step2 - load genres
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/genre.csv" AS row
CREATE (n:Genre)
SET n = row

//step3 - load actors
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/actors.csv" AS row
CREATE (n:Actor)
SET n = row

//step4 - load directors
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/directors.csv" AS row
CREATE (n:Director)
SET n = row

//step5 - load users
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/ase40/graphs-poc/main/data/users.csv" AS row
CREATE (n:User)
SET n = row

//step6 - create index on users
CREATE INDEX ON :User(`relationship.start`)

//step7 - create index on actors
CREATE INDEX ON :Actor(`relationship.start`)

//step8 - create index on directors
CREATE INDEX ON :Director(`relationship.start`)

//step9 - create index on movies
CREATE INDEX ON :Movie(`n.identity`)

//step10 - create index on genre
CREATE INDEX ON :Genre(`relationship.end`)

//step11 - create RATED relationship
MATCH (m:Movie),(a:User)
WHERE m.`n.identity` = a.`relationship.end`
CREATE (a)-[:RATED {rating: a.`relationship.properties.rating`, timestamp: a.`relationship.properties.timestamp`}]->(m)

//step12 - create DIRECTED relationship
MATCH (m:Movie),(a:Director)
WHERE m.`n.identity` = a.`relationship.end`
CREATE (a)-[:DIRECTED {role: a.`relationship.properties.role`}]->(m)

//step13 - create ACTED_IN relationship
MATCH (m:Movie),(a:Actor)
WHERE m.`n.identity` = a.`relationship.end`
CREATE (a)-[:ACTED_IN {role: a.`relationship.properties.role`}]->(m)

//step14 - create IN_GENRE relationship
MATCH (m:Movie),(g:Genre)
WHERE m.`n.identity` = g.`relationship.start`
CREATE (m)-[:IN_GENRE]->(g)

