
from collections import defaultdict, OrderedDict, Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
import glob
from rdflib.namespace import XSD, Namespace
from rdflib.term import URIRef
import pandas as pd
import re


def checkDate(v):
    try:
        d = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S').date()
    except ValueError:
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})', v)
        d = datetime(int(m.groups()[0]), int(m.groups()[1]), 28).date()
    return d

DATATYPECONVERTERS = {
      str(XSD.integer):  int,
      str(XSD.decimal):  float,
      str(XSD.date):     lambda v: datetime.strptime(v, '%Y-%m-%d').date(),
      str(XSD.dateTime): checkDate,
      'uri':  URIRef
  }

def convertDatatype(obj):
    return DATATYPECONVERTERS.get(obj.get('datatype') or obj.get('type'), str)(obj.get('value')) 

def convertDatatypes(results):
    res = results["results"]["bindings"]
    return [dict([(k, convertDatatype(v)) for k,v in r.items()]) for r in res]

def JSON2Pandas(results):
    res = results["results"]["bindings"]
    data = [dict([(k, convertDatatype(v)) for k,v in r.items()]) for r in res]
    return pd.DataFrame(data)

DATATYPECONVERTERS2 = {
      str(XSD.integer):  int,
      str(XSD.decimal):  float,
      str(XSD.date):     lambda v: datetime.strptime(v, '%Y-%m-%d').date(),
      str(XSD.dateTime): checkDate,
      'uri':  str
  }

def convertDatatype2(obj):
    return DATATYPECONVERTERS2.get(obj.get('datatype') or obj.get('type'), str)(obj.get('value')) 

def convertDatatypes2(results):
    res = results["results"]["bindings"]
    return [dict([(k, convertDatatype2(v)) for k,v in r.items()]) for r in res]

def JSON2Pandas2(results):
    res = results["results"]["bindings"]
    data = [dict([(k, convertDatatype2(v)) for k,v in r.items()]) for r in res]
    return pd.DataFrame(data)



def to_tokens(s, stopwords=None, min_chars=1):
    """
    Transforms sentence to list of tokens.  

    Basic: transform special characters to ascii + lowercase.  
    Options:  
    - remove stopwords (provide list of stopwords)  
    - set minimum length for tokens: will remove any shorter token. 
    
    Returns sorted tokens
    """
    #s = unidecode(str(s)) # convert to ASCII to remove special characters
    s = s.lower() # lowercase
    tokens = s.split(";") # split the string into a list of words
    
    if min_chars > 1:
        tokens = [word for word in tokens if len(word) >= min_chars] # remove any shorter words
    
    if stopwords is not None:
          tokens = [word for word in tokens if word not in stopwords] # remove words if they appear in our stopwords list
    
    tokens = set(tokens) # transforming a list to a set removes duplicates
    tokens = sorted(tokens) # converts our set back to a list and sorts words in alphabetical order
    return tokens