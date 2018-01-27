#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3
import wrappers.wrapper_sql as sql
import wrappers.wrapper_xml as xml
import wrappers.wrapper_json as json
import wrappers.wrapper_rdf as rdf
import pprint as pp

con = sqlite3.connect("EbvDatabase.sqlite")
cur = con.cursor()

def resetDb():
	cur.executescript("""
		DROP TABLE IF EXISTS Transcript;
		CREATE TABLE Transcript(
		IdT   INTEGER NOT NULL ,
		nomT  TEXT ,
		idG   INTEGER ,
		idP   INTEGER ,
		PRIMARY KEY (IdT) ,
		
		FOREIGN KEY (idG) REFERENCES Gene(idG),
		FOREIGN KEY (idP) REFERENCES Proteine(idP)
	);
	DROP TABLE IF EXISTS Laboratoire;
	CREATE TABLE Laboratoire(
		IdL       INTEGER NOT NULL ,
		nom       TEXT ,
		acronyme  TEXT ,
		PRIMARY KEY (IdL)
	);

	DROP TABLE IF EXISTS Gene;
	CREATE TABLE Gene(
		idG           VARCHAR NOT NULL ,
		nomG          TEXT ,
		tagLocusG     TEXT ,
		coordonneeG1  INTEGER ,
		coordonneeG2  INTEGER ,
		referenceG    TEXT ,
		PRIMARY KEY (idG)
	);

	DROP TABLE IF EXISTS Maladie;
	CREATE TABLE Maladie(
		idM   INTEGER NOT NULL ,
		nomM  TEXT ,
		PRIMARY KEY (idM)
	);

	DROP TABLE IF EXISTS Proteine;
	CREATE TABLE Proteine(
		idP         TEXT ,
		nomP        TEXT ,
		poidsP      TEXT ,
		longueurP   INTEGER ,
		organismeP   VARCHAR,
		IdT         INTEGER ,
		PRIMARY KEY (idP) ,
		
		FOREIGN KEY (IdT) REFERENCES Transcript(IdT)
	);

	DROP TABLE IF EXISTS ReferenceP;
	CREATE TABLE ReferenceP(
		idR    TEXT ,
		idP    TEXT ,
		PRIMARY KEY (idR) ,
		
		FOREIGN KEY (idP) REFERENCES Proteine(idP)
	);


	DROP TABLE IF EXISTS Interaction;
	CREATE TABLE Interaction(
		idI         VARCHAR ,
		idP1        VARCHAR,
		idP2        VARCHAR,
		typeI       TEXT ,
		referenceI  TEXT ,
		PRIMARY KEY (idI)
	);

	DROP TABLE IF EXISTS Detection;
	CREATE TABLE Detection(
		idDe     INTEGER NOT NULL ,
		labelDe  TEXT ,
		idDe_1   INTEGER ,
		PRIMARY KEY (idDe) ,
		
		FOREIGN KEY (idDe_1) REFERENCES Detection(idDe)
	);

	DROP TABLE IF EXISTS Chercheuse;
	CREATE TABLE Chercheuse(
		idCh    INTEGER NOT NULL ,
		nomCh   TEXT ,
		paysCh  TEXT ,
		PRIMARY KEY (idCh)
	);

	DROP TABLE IF EXISTS Article;
	CREATE TABLE Article(
		idA         VARCHAR ,
		titreA      VARCHAR ,
		journalA    VARCHAR ,
		anneeA      VARCHAR ,
		referenceA  VARCHAR ,
		idI         VARCHAR ,
		PRIMARY KEY (idA) ,
		
		FOREIGN KEY (idI) REFERENCES Interaction(idI)
	);

	DROP TABLE IF EXISTS Condition;
	CREATE TABLE Condition(
		idCo    INTEGER NOT NULL ,
		typeCo  TEXT ,
		PRIMARY KEY (idCo)
	);

	DROP TABLE IF EXISTS DateObservation;
	CREATE TABLE DateObservation(
		dateDa  NUMERIC NOT NULL ,
		PRIMARY KEY (dateDa)
	);

	DROP TABLE IF EXISTS Observe;
	CREATE TABLE Observe(
		IdL     INTEGER NOT NULL ,
		idCo    INTEGER NOT NULL ,
		dateDa  NUMERIC NOT NULL ,
		IdT     INTEGER NOT NULL ,
		PRIMARY KEY (IdL,idCo,dateDa,IdT) ,
		
		FOREIGN KEY (IdL) REFERENCES Laboratoire(IdL),
		FOREIGN KEY (idCo) REFERENCES Condition(idCo),
		FOREIGN KEY (dateDa) REFERENCES DateObservation(dateDa),
		FOREIGN KEY (IdT) REFERENCES Transcript(IdT)
	);

	DROP TABLE IF EXISTS estAffecte;
	CREATE TABLE estAffecte(
		idM  INTEGER NOT NULL ,
		idG  INTEGER NOT NULL ,
		PRIMARY KEY (idM,idG) ,
		
		FOREIGN KEY (idM) REFERENCES Maladie(idM),
		FOREIGN KEY (idG) REFERENCES Gene(idG)
	);
	DROP TABLE IF EXISTS Possede;
	CREATE TABLE Possede(
		idP1  VARCHAR ,
		idI  VARCHAR,
		PRIMARY KEY (idP1,idI) ,
		
		FOREIGN KEY (idP1) REFERENCES Proteine(idP),
		FOREIGN KEY (idI) REFERENCES Interaction(idI)
	);

	DROP TABLE IF EXISTS estDetecte;
	CREATE TABLE estDetecte(
		idI   INTEGER NOT NULL ,
		idDe  INTEGER NOT NULL ,
		PRIMARY KEY (idI,idDe) ,
		
		FOREIGN KEY (idI) REFERENCES Interaction(idI),
		FOREIGN KEY (idDe) REFERENCES Detection(idDe)
	);

	DROP TABLE IF EXISTS Cosigne;
	CREATE TABLE Cosigne(
		ordreAuteur  INTEGER ,
		idCh         INTEGER NOT NULL ,
		idA          INTEGER NOT NULL ,
		PRIMARY KEY (idCh,idA) ,
		
		FOREIGN KEY (idCh) REFERENCES Chercheuse(idCh),
		FOREIGN KEY (idA) REFERENCES Article(idA)
	);
	DROP TABLE IF EXISTS Cite_maladie;
	CREATE TABLE Cite_maladie(
		idA  INTEGER NOT NULL ,
		idM  INTEGER NOT NULL ,
		PRIMARY KEY (idA,idM) ,
		
		FOREIGN KEY (idA) REFERENCES Article(idA),
		FOREIGN KEY (idM) REFERENCES Maladie(idM)
	);
	DROP TABLE IF EXISTS Cite_prot;
	CREATE TABLE Cite_prot(
		idA  TEXT NOT NULL ,
		idR  TEXT NOT NULL ,
		PRIMARY KEY (idA,idR) ,
		
		FOREIGN KEY (idA) REFERENCES Article(idA),
		FOREIGN KEY (idR) REFERENCES ReferenceP(idR)
	);
	""")

resetDb()

def geneSqlToSchema ():

	tp2db = sql.WrapperSQLite("sources/tp2Virus.sqlite")
	tp2db.connect_db("sources/tp2Virus.sqlite")
	queryRef = 'SELECT T.UniProtKBTrEMBL FROM Genes G INNER JOIN Transcripts T ON T.GeneID = G.GeneID;'
	queryId = 'SELECT G.GeneID FROM Genes G;'
	queryNom ='SELECT G.gene FROM Genes G;'
	queryLocus ='SELECT G.locus_tag FROM Genes G;'
	queryStart ='SELECT G.start FROM Genes G;'
	queryStop = 'SELECT G.stop FROM Genes G;'
	reference = tp2db.query_select(queryRef)
	ident = tp2db.query_select(queryId)
	nom = tp2db.query_select(queryNom)
	locus = tp2db.query_select(queryLocus)
	start = tp2db.query_select(queryStart)
	stop = tp2db.query_select(queryStop)
	return reference, ident, nom, locus, start, stop

resGeneSql=geneSqlToSchema()

def insertGeneSql (result):
	reference=result[0]
	ident=result[1]
	nom=result[2]
	locus=result[3]
	start=result[4]
	stop=result[5]
	for index in range(0,len(reference)):
		datas = "'"+str(ident[index][0])+"'"+","+"'"+str(nom[index][0])+"'"+","+"'"+str(locus[index][0])+"'"+","+"'"+str(start[index][0])+"'"+","+"'"+str(stop[index][0])+"'"+","+"'"+str(reference[index][0])+"'"
		cur.executescript("""INSERT INTO 
			Gene(idG, 
			nomG, 
			tagLocusG, 
			coordonneeG1, 
			coordonneeG2, 
			referenceG) 
			VALUES ("""+datas+""");
			""")


insertGeneSql(resGeneSql)

def transSqlToSchema ():
	tp2db = sql.WrapperSQLite("sources/tp2Virus.sqlite")
	tp2db.connect_db("sources/tp2Virus.sqlite")
	queryTransId = 'SELECT CDS_id FROM Transcripts;'
	queryNom ='SELECT product FROM Transcripts;'
	queryGeneId = 'SELECT GeneID FROM Transcripts;'
	queryProtId = 'SELECT protein_id FROM Transcripts;'
	identTrans = tp2db.query_select(queryTransId)
	nom = tp2db.query_select(queryNom)
	identGene = tp2db.query_select(queryGeneId)
	identProt = tp2db.query_select(queryProtId)
	return identTrans, nom, identGene, identProt

resTransSql = transSqlToSchema ()

def insertTransSql (result):
	identTrans=result[0]
	nom=None
	identGene=result[2]
	identProt=result[3]
	for index in range(0,len(identTrans)):
		datas = str(identTrans[index][0])+","+'"'+str(nom)+'"'+","+str(identGene[index][0])+","+'"'+str(identProt[index][0])+'"'
		cur.executescript("""INSERT INTO 
			Transcript(idT, 
			nomT, 
			idG,
			idP) 
			VALUES ("""+datas+""");
			""")
insertTransSql(resTransSql)

def protSqlToSchema ():
	tp2db = sql.WrapperSQLite("sources/tp2Virus.sqlite")
	tp2db.connect_db("sources/tp2Virus.sqlite")
	queryProtId = 'SELECT protein_id FROM Transcripts'
	queryNom ='SELECT product FROM Transcripts'
	queryLongueur = 'SELECT LENGTH(translation) FROM Transcripts'
	queryReference = 'SELECT UniProtKBTrEMBL FROM Transcripts'
	queryTransId = 'SELECT CDS_id FROM Transcripts'
	identProt = tp2db.query_select(queryProtId)
	nom = tp2db.query_select(queryNom)
	poids = None
	longueur = tp2db.query_select(queryLongueur)
	reference = tp2db.query_select(queryReference)
	identTrans = tp2db.query_select(queryTransId)
	return identProt, nom, poids, longueur, reference, identTrans

resProtSql = protSqlToSchema ()

def insertProtSql (result):
	identProt=result[0]
	nom=result[1]
	poids=None
	longueur=result[3]
	reference=result[4]
	identTrans=result[5]
	for index in range(0,len(identProt)):
		datas = '"'+str(identProt[index][0])+'"'+","+'"'+str(nom[index][0])+'"'+","+'"'+str(poids)+'"'+","+str(longueur[index][0])+","+'"'+"ebv"+'"'+","+str(identTrans[index][0])
		datasRef = '"'+str(reference[index][0])+'"'+","+'"'+str(identProt[index][0])+'"'
		cur.executescript("""INSERT INTO 
			Proteine(idP, 
			nomP, 
			poidsP,
			longueurP,
			organismeP,
			idT) 
			VALUES ("""+datas+""");
			""")
		if '"'+str(reference[index][0])+'"' != '"'+str(None)+'"':
			cur.executescript("""INSERT INTO
							ReferenceP(idR,
							idP)
							VALUES ("""+datasRef+""");
							""")
insertProtSql(resProtSql)

def refXmlToSchema ():
	tp3db = xml.WrapperXML("sources/tp3corrected.xml")
	listAcc =[]
	for elm in tp3db.query_xpath(".//entry"):
		listChild =[]
		for child in elm:
			if 'accession' in str(child):
				listChild.append(child.text)
		listAcc.append(listChild) 
	return listAcc
resRefXml=refXmlToSchema()

def insertReftXml(resultProt, resultAcc):
	identProt=resultProt[0]
	reference=resultProt[4]
	for index2,prot in enumerate(resultAcc):
		for acc in prot:
			for index in range(0, len(identProt)):
				if acc==reference[index][0]:
					for allAcc in resultAcc[index2]:
						if allAcc != acc:
							datas='"'+str(allAcc)+'"'+","+'"'+str(identProt[index][0])+'"'
							cur.executescript("""INSERT INTO
								ReferenceP(idR,
								idP)
								VALUES ("""+datas+""");
								""")


insertReftXml(resProtSql, resRefXml)

def loadJson (resultRefXml):
	jsondb=json.WrapperJSON("sources/interactions-PMID-17446270.json")
	jsonconn=jsondb.parse()
	identProt = []
	for ids in resultRefXml:
		for idAll in ids:
			identProt.append(idAll)

	for index,inter in enumerate(jsonconn['data']):
		idI=inter['interactionIdentifiers'][0]
		typeI=inter['interactionTypes'][0]
		refI=inter['sourceDatabases'][0]
		idA=inter['idA'][0].split(":")[1]
		orgA=inter['taxidA'][0].split(":")[1].split("(")[1].rstrip(')')
		idB=inter['idB'][0].split(":")[1]
		orgB=inter['taxidB'][0].split(":")[1].split("(")[1].rstrip(')')
		datasInt='"'+str(idI)+'"'+","+'"'+str(idA)+'"'+","+'"'+str(idB)+'"'+","+'"'+str(typeI)+'"'+","+'"'+str(refI)+'"'
		if idA not in identProt:
			identProt.append(idA)
			datasProt='"'+str(index*2)+'"'+","+'"'+str(None)+'"'+","+'"'+str(None)+'"'+","+'"'+str(None)+'"'+","+'"'+str(orgA)+'"'+","+'"'+str(None)+'"'
			datasRef='"'+str(idA)+'"'+","+'"'+str(index*2)+'"'
			cur.executescript("""INSERT INTO 
			Proteine(idP, 
			nomP, 
			poidsP,
			longueurP,
			organismeP,
			idT) 
			VALUES ("""+datasProt+""");
			""")
			cur.executescript("""INSERT INTO
							ReferenceP(idR,
							idP)
							VALUES ("""+datasRef+""");
							""")
		if idB not in identProt:
			identProt.append(idB)
			datasProt='"'+str(index*2-1)+'"'+","+'"'+str(None)+'"'+","+'"'+str(None)+'"'+","+'"'+str(None)+'"'+","+'"'+str(orgB)+'"'+","+'"'+str(None)+'"'
			datasRef='"'+str(idB)+'"'+","+'"'+str(index*2-1)+'"'
			cur.executescript("""INSERT INTO 
			Proteine(idP, 
			nomP, 
			poidsP,
			longueurP,
			organismeP,
			idT) 
			VALUES ("""+datasProt+""");
			""")
			cur.executescript("""INSERT INTO
							ReferenceP(idR,
							idP)
							VALUES ("""+datasRef+""");
							""")
		cur.executescript("""INSERT INTO 
			Interaction(idI, 
			idP1, 
			idP2,
			typeI,
			referenceI) 
			VALUES ("""+datasInt+""");
			""")

loadJson(resRefXml)

def insertRdfToSchema():
	virusdb = sql.WrapperSQLite("EbvDatabase.sqlite")
	virusdb.connect_db("EbvDatabase.sqlite")
	queryRef = 'SELECT idP, idR FROM ReferenceP;'
	reference = virusdb.query_select(queryRef)
	tp4db= rdf.WrapperRDF('sources/tp4.ttl', 'n3')
	protName=tp4db.query_sparql("""PREFIX core:<http://purl.uniprot.org/core/>
SELECT ?id ?fullName
WHERE 
{
    ?id rdf:type core:Protein .
    ?id core:recommendedName ?recName .
    ?recName core:fullName ?fullName .
  }""")
	listAccName=[]
	for trip in protName:
		acc=trip[0].split('/')[-1].rstrip("'")
		name=trip[1]
		listAccName.append([acc,name])
	for accName in listAccName:
		for idRef in reference:
			if str(accName[0])==idRef[1]:
				cur.executescript("UPDATE Proteine SET nomP="+'"'+str(accName[1])+'"'+"WHERE idP="+'"'+idRef[0]+'"'+";")
	
	pub=tp4db.query_sparql("""PREFIX core: <http://purl.uniprot.org/core/>
PREFIX dcterm: <http://purl.org/dc/terms/>
SELECT ?idProt (concat (STR(?idA), '@',STR(?title) ,'@', STR(?date), '@', STR(?journal), '@', STR((GROUP_CONCAT(?auth)))) as ?info) ?cit 
WHERE
  {
  ?idProt rdf:type core:Protein .
  ?idProt  core:citation ?cit .
    ?cit core:title ?title .
    ?cit core:date ?date .
    ?cit core:name ?journal .
    ?cit core:author ?auth .
    ?cit dcterm:identifier ?idA .
     }
GROUP BY ?idProt ?cit ?idA ?title ?date ?journal
ORDER BY ?idProt ?cit""")
	listartRef=[]
	for trip in pub:
		ref=trip[0].split('/')[-1].rstrip("'")
		art=trip[1]
		listartRef.append([art, ref])
	listId=[]
	for artRef in listartRef:
		idA=artRef[0].split('@')[0]
		datasCit='"'+str(idA)+'"'+","+'"'+str(artRef[1])+'"'
		if idA not in listId:
			listId.append(idA)
			titreA=artRef[0].split('@')[1]
			journalA=artRef[0].split('@')[3]
			anneeA=artRef[0].split('@')[2]

			datasArt='"'+str(idA)+'"'+","+'"'+str(titreA)+'"'+","+'"'+str(journalA)+'"'+","+'"'+str(anneeA)+'"'+","+'"'+str(None)+'"'+","+'"'+str(None)+'"'
			cur.executescript("""INSERT INTO 
				Article(idA, 
				titreA, 
				journalA,
				anneeA,
				referenceA,
				idI) 
				VALUES ("""+datasArt+""");
				""")
		cur.executescript("""INSERT INTO
			Cite_prot(idA,
			idR)
			VALUES ("""+datasCit+""");
			""")
	gene=tp4db.query_sparql("""PREFIX core:<http://purl.uniprot.org/core/>
SELECT DISTINCT ?prot ?gene
WHERE 
{
    ?id core:transcribedFrom ?gene .
  ?prot rdfs:seeAlso ?id .
  }""")
	for index,trip in enumerate(gene):
		idGene=trip[1].split('/')[-1]
		idProt=trip[0].split('/')[-1]
		datasGene = "'"+str(idGene)+"'"+","+"'"+str(None)+"'"+","+"'"+str(None)+"'"+","+"'"+str(None)+"'"+","+"'"+str(None)+"'"+","+"'"+str(None)+"'"
		
		cur.executescript("""INSERT INTO 
			Gene(idG, 
			nomG, 
			tagLocusG, 
			coordonneeG1, 
			coordonneeG2, 
			referenceG) 
			VALUES ("""+datasGene+""");
			""")

		queryRef = 'SELECT idP, idR FROM ReferenceP;'
		reference = virusdb.query_select(queryRef)
		for idRef in reference:
			if idRef[1]==idProt:
				cur.executescript("UPDATE Proteine SET idT="+str(135+index)+" WHERE idP="+'"'+idRef[0]+'"'+";")
				datasTrans=str(135+index)+","+'"'+str(None)+'"'+","+'"'+str(idGene)+'"'+","+'"'+str(idRef[0])+'"'
				cur.executescript("""INSERT INTO 
			Transcript(idT,
			nomT,
			idG,
			idP)
			VALUES ("""+datasTrans+""");
			""")

insertRdfToSchema()



