from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "bolt://18.204.217.64:7687",
  auth=basic_auth("neo4j", "workings-nut-cardboard"))

cypher_query = '''
LOAD CSV WITH HEADERS FROM "https://uc58d6d190849ad2ac0a4a7ac6ba.dl.dropboxusercontent.com/cd/0/get/BVaF6brWWUQu0kx6Qcl_aIWJ6tG2SDJzUMqMkxMfWeOZQriv3oT12NmNBXmJjCW-_J-eFw8Blsbx9Kf9kHBUSeFfyYCwvixS7LAhElZRSgA90tNZZrIwJ_bpkqZclDZcBQIm8hw2yfCz9zfGP0YSVFv6/file#" AS row
CREATE (n:Movie)
SET n = row
'''

with driver.session(database="neo4j") as session:
  session.run(cypher_query)

driver.close()
