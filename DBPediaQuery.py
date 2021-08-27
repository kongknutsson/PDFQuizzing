from SPARQLWrapper import SPARQLWrapper, JSON
import spotlight

"""
This class sends queries to DBPedia.
The queries get the "comment" part in DBPedia,
which works as a definition. It also gets the
subjects of the word.
"""

class DBPediaQuery:
    def __init__(self):
        self.definitions = {}
        self.sub_cat = {}
        self.annotations = []

    def get_definitions(self):
        return self.definitions

    def get_subcagetories(self):
        return self.sub_cat

    # Sends a sparql query to DBPedia to retrieve the rdfs:comment
    # of a specific word. This is then used as a definition of the word.
    def generate_definitions(self):
        if len(self.annotations) == 0:
            print("WARNING. Generate annotations first!")
            return
        for i in self.annotations:
            tmp = i["URI"].split("/")[-1]
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setQuery("""
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?comment
                WHERE {dbr:"""+tmp+""" rdfs:comment ?comment.
                FILTER (langMatches(lang(?comment), "en"))
                }
            """)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                self.definitions[tmp] = result["comment"]["value"]

    # Sends a sparql query to DBPedia, retrieving the subjects of
    # a word. Later quizzes on subjects.
    def generate_subcategories(self):
        if len(self.annotations) == 0:
            print("WARNING. Generate annotations first!")
            return
        for i in self.annotations:
            tmp = i["URI"].split("/")[-1]
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setQuery("""
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?subjectlabel
                WHERE {dbr:"""+tmp+""" dct:subject ?subject.
                ?subject rdfs:label ?subjectlabel
                }
            """)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                if tmp not in self.sub_cat:
                    self.sub_cat[tmp] = []
                self.sub_cat[tmp].append(result["subjectlabel"]["value"])

    # Spotlights words to see what can be queried.
    def spotlight_annotate(self, big_list):
        big_string = " ".join(big_list)
        url = "https://api.dbpedia-spotlight.org/en/annotate"
        self.annotations = spotlight.annotate(url, big_string, confidence=0.2)


