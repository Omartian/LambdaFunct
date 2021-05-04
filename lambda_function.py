import json
import http.client

conn = http.client.HTTPSConnection('natural-language-understanding-opc.mybluemix.net')
headers = {'Content-type': 'application/json'}

def lambda_handler(event, context):
    data = {
        "text": event["historial_clinico"],
        "features": {
            "keywords": {
                "sentiment": True,
                "emotion": True,
                "limit": 5
            },
            "entities": {
                "metions": True,
                "model": True,
                "sentiment": True,
                "emotion": True,
                "limit": 5
            }
        }
    }
    jsonData = json.dumps(data)
    conn.request('POST', '/api/analyze', jsonData, headers)

    response = conn.getresponse()
    jsonD = json.loads(response.read().decode("utf-8"))
    
    keywords = []
    entities = []
    
    keywords_desc = []
    entities_desc = []
    
    for keyword in jsonD["keywords"]:
        highest_emot_score = 0
        highest_emot_text = ''
        
        for key, value in keyword["emotion"].items():
            if value > highest_emot_score:
                highest_emot_score = value
                highest_emot_text = key
                
        keywords.append(keyword["text"])
        
        keywords_desc.append({
                "sentimiento": keyword["sentiment"]["label"],
                "relevancia": keyword["relevance"],
                "repeticiones": keyword["count"],
                "emocion": highest_emot_text
            })
            
    for entity in jsonD["entities"]:
        highest_emot_score = 0
        highest_emot_text = ''
        
        for key, value in entity["emotion"].items():
            if value > highest_emot_score:
                highest_emot_score = value
                highest_emot_text = key
        
        entities.append(entity["text"])
        
        entities_desc.append({
                "tipo": entity["type"],
                "sentimiento": entity["sentiment"]["label"],
                "relevancia": entity["relevance"],
                "emocion": highest_emot_text,
                "repeticiones": entity["count"],
                "porcentaje_confianza": entity["confidence"]
        })
        
        
    print(keywords_desc)
    
    
    return {
        "language": jsonD["language"],
        "keywords": keywords,
        "entities": entities,
        "keywords_desc": keywords_desc,
        "entities_desc": entities_desc,
    }