import re
from bs4 import BeautifulSoup
import urllib.parse

def utfdecode(InputData):
    InputData=re.sub('\\x00|\\x01|\\x02|\\x03|\\x04|\\x05|\\x06|\\x07|\\x08|\\x0b|\\x0e|\\x0f|\\x10|\\x11|\\x12|\\x13|\\x14|\\x15|\\x16|\\x17|\\x18|\\x19|\\x1a|\\x1b|\\x1c|\\x1d|\\x1e|\\x1f|\\x7f|\\x80|\\x81|\\x82|\\x83|\\x84|\\x85|\\x86|\\x87|\\x88|\\x89|\\x8a|\\x8b|\\x8c|\\x8d|\\x8e|\\x8f|\\x90|\\x91|\\x92|\\x93|\\x94|\\x95|\\x96|\\x97|\\x98|\\x99|\\x9a|\\x9b|\\x9c|\\x9d|\\x9e|\\x9f','',InputData)
    modefiyData=InputData
    regex_rule=re.compile('(?:\\\\x[a-zA-Z0-9][a-zA-Z0-9])+')	
    encodeList= (regex_rule.findall(InputData))
    encodeList=list(set(encodeList))
    
    if(len(encodeList)==0):
        return (modefiyData)

    for utfstr in encodeList:
        origin=utfstr
        utfstr=(utfstr.replace("\\x",''))
        utfstr=bytes.fromhex(utfstr)
        decodestr=(utfstr.decode('utf-8','ignore'))
        modefiyData=modefiyData.replace(origin,str(decodestr))
        regex_rule=re.compile('.(?:\\\\x[a-zA-Z0-9][a-zA-Z0-9])+')
        encodeList=regex_rule.findall(modefiyData)
        encodeList=list(set(encodeList))

    for utfstr in encodeList:
        origin=utfstr
        
        if(utfstr[0]!='\\x'):
            utfstr=utfstr[1:]\
                
        utfstr=utfstr.replace("\\x",'')
        utfstr=bytes.fromhex(utfstr)
        decodestr= (utfstr.decode('utf-8','ignore'))
        modefiyData=modefiyData.replace(origin,str(decodestr))

    regex_rule=re.compile('(?:\\\\x[a-zA-Z0-9][a-zA-Z0-9])+.')
    encodeList= (regex_rule.findall(modefiyData))
    encodeList=list(set(encodeList))
	
    for utfstr in encodeList:
        origin=utfstr
        utfstr=utfstr[:-1]
        utfstr=(utfstr.replace('\\x',''))

        utfstr=bytes.fromhex(utfstr)
        decodestr=(utfstr.decode('utf-8','ignore'))
        modefiyData=modefiyData.replace(origin,str(decodestr))

    return (modefiyData)

def analysis(htmlcode):		
		urldecode_text=urllib.parse.unquote(htmlcode)	

		utfdecode_text=utfdecode(urldecode_text)
		textcode=(BeautifulSoup(utfdecode_text))

		return (textcode)