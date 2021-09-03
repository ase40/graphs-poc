#!/usr/bin/env python
import getopt, sys
from neo4j import GraphDatabase
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from pandas.io.json import json_normalize

# Global defaults, some based on our demo and some on the algo defaults.
DEFAULT_URI = "bolt://44.197.216.229:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASS = "actions-checkpoints-addition"
DEFAULT_REL = "IN_GENRE"
DEFAULT_LABEL = "Movie"
DEFAULT_PROP = "clusterId"
DEFAULT_P = 1.0
DEFAULT_Q = 1.0
DEFAULT_D = 32
DEFAULT_WALK = 80
DEFAULT_K=6

NODE2VEC_CYPHER = """
CALL gds.beta.node2vec.stream({
  nodeProjection: $L,
  relationshipProjection: {
    EDGE: {
      type: $R,
      orientation: 'UNDIRECTED'
    }
  },
  embeddingDimension: $d,
  returnFactor: $p,
  inOutFactor: $q,
  walkLength: $l
}) YIELD nodeId, embedding
"""

UPDATE_CYPHER = """
UNWIND $updates AS updateMap
    MATCH (n) WHERE id(n) = updateMap.nodeId
    SET n += updateMap.valueMap
"""

embeddings_dict = {}
def extract_embeddings(driver, label=DEFAULT_LABEL, relType=DEFAULT_REL,
                       p=DEFAULT_P, q=DEFAULT_Q, d=DEFAULT_D, l=DEFAULT_WALK):
    embeddings = []
    with driver.session() as session:
        results = session.run(NODE2VEC_CYPHER, L=label, R=relType,
                              p=float(p), q=float(q), d=int(d), l=int(l))
        for result in results:
            embeddings.append(result)
            embeddings_dict[result['nodeId']]=result['embedding']

    print("...generated {} embeddings".format(len(embeddings)))
    return embeddings


def kmeans(embeddings, k=DEFAULT_K, clusterProp=DEFAULT_PROP):
    print("Performing K-Means clustering (k={}, clusterProp='{}')"
          .format(k, clusterProp))
    X = np.array([e["embedding"] for e in embeddings])
    kmeans = KMeans(n_clusters=int(k)).fit(X)
    
    #predict the labels of clusters.
    label = kmeans.predict(X)

    #Getting unique labels
    u_labels = np.unique(label)

    #plotting the results:
    # for i in u_labels:
        # plt.scatter(X[label == i , 0] , X[label == i , 1] , label = i)
        
    # plt.legend()
    # plt.show()

    results = []
#     for idx, cluster in enumerate(kmeans.predict(X)):
#         results.append({ "nodeId": embeddings[idx]["nodeId"],
#                          "valueMap": { clusterProp: int(cluster) }})
#     print("...clustering completed.")
    return results


def update_clusters(driver, clusterResults):
    with driver.session() as session:
        result = session.write_transaction(_update_tx, UPDATE_CYPHER, updates=clusterResults)
        print("...update complete: {}".format(result.counters))

def get_embeddingsDF(embeddings_dict):
    df = pd.DataFrame.from_dict(embeddings_dict, orient='index')
    df.index.name='nodeId'
    df.columns = ['dim_'+str(x) for x in df.columns]
    print(df.head())
    return None


if __name__ == '__main__':

    uri = DEFAULT_URI
    user = DEFAULT_USER
    password = DEFAULT_PASS
    relType = DEFAULT_REL
    label = DEFAULT_LABEL
    clusterProp = DEFAULT_PROP
    p = DEFAULT_P
    q = DEFAULT_Q
    d = DEFAULT_D
    k = DEFAULT_K
    l = DEFAULT_WALK

    print("Connecting to uri: {}".format(uri))
    driver = GraphDatabase.driver(uri, auth=(user, password))
    embeddings = extract_embeddings(driver, label=label, relType=relType,
                                    p=p, q=q, d=d, l=l)
    clusters = kmeans(embeddings, k=k, clusterProp=clusterProp)
#     update_clusters(driver, clusters)
    driver.close()
    get_embeddingsDF(embeddings_dict)