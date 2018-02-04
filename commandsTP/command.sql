SELECT G.gene_id || ', ' || G.start || ', ' || G.stop || ', ' || G.gene || ', ' || G.GeneID  || ', ' || G.locus_tag AS Coords FROM Genes G;
SELECT * FROM Genes G WHERE G.locus_tag IS NOT NULL ORDER BY G.gene DESC;
SELECT T.CDS_id, G.gene_id, G.Gene FROM Transcripts T INNER JOIN Genes G ON T.GeneID=G.GeneID WHERE T.product LIKE '%hypothetical%';
SELECT T.CDS_id, T.product FROM Transcripts T INNER JOIN Genes G ON T.locus_tag=G.locus_tag;
SELECT (T1.CDS_id || ', ' || T1.product) AS T1, (T2.CDS_id || ', ' || T2.product) AS T2 FROM Transcripts T1 INNER JOIN Transcripts T2 ON T1.CDS_id < T2.CDS_id WHERE T1.strand = T2.strand AND T1.locus_tag IN (SELECT G.locus_tag FROM Genes G WHERE G.gene LIKE 'BALF%' AND G.locus_tag IS NOT NULL) AND T2.locus_tag IN (SELECT G.locus_tag FROM Genes G WHERE G.gene LIKE 'BALF%' AND G.locus_tag IS NOT NULL);
SELECT G.gene FROM Genes G WHERE G.locus_tag LIKE '%P%' UNION SELECT G.gene FROM Genes G INNER JOIN Exons E ON G.gene=E.gene WHERE E.product IS NOT NULL;
SELECT COUNT (T.CDS_id) FROM Transcripts T INNER JOIN Genes G ON T.GeneID=G.GeneID GROUP BY G.gene ORDER BY COUNT (T.CDS_id) DESC;
SELECT MIN(LENGTH(T.translation)) AS MinTrans, MAX(LENGTH(T.Translation)) AS MaxTrans FROM Transcripts T INNER JOIN Genes G ON T.GeneID=G.GeneID WHERE G.gene IN (SELECT E.gene FROM Exons E);
SELECT E.gene, COUNT(E.exon_id) AS NbExon, COUNT(E.number) AS Nbnumber, COUNT(DISTINCT(E.number)) AS NbnumberDiff FROM Exons E GROUP BY E.gene HAVING COUNT (E.exon_id) > 1;
SELECT E.gene, E.number FROM Exons E ORDER BY E.number;


SELECT O.titre, D.nom FROM Oeuvre O INNER JOIN Dragon D On O.idO=D.idO WHERE O.annee > 1970 AND D.couleur LIKE '_o%';
SELECT O.titre FROM Oeuvre O WHERE O.annee > 2000 UNION SELECT O.titre FROM Oeuvre O INNER JOIN Dragon D ON O.idO=D.idO WHERE D.couleur = 'noir';
SELECT D.nom FROM Dragon D WHERE D.envergure > (SELECT D.envergure FROM Dragon D WHERE D.nom ='Viserion');
SELECT O.* FROM Oeuvre O WHERE O.idO NOT IN (SELECT D.idO FROM Dragon D WHERE D.nom LIKE '%e%');
SELECT O.*, D.* FROM Oeuvre O INNER JOIN Dragon D ON O.idO=D.idO WHERE O.annee < (SELECT MAX(O.annee) FROM Oeuvre O WHERE O.categorie = 'roman');
SELECT COUNT (D.nom) FROM Dragon D;
SELECT O.categorie, COUNT (D.nom) FROM Oeuvre O LEFT OUTER JOIN Dragon D ON D.idO=O.idO GROUP BY O.categorie;
SELECT O.titre, SUM(D.envergure)/COUNT(D.envergure) AS Moy_envergure FROM Oeuvre O LEFT OUTER JOIN Dragon D ON O.idO=D.idO WHERE O.annee < 2000 GROUP BY O.idO, O.titre;
SELECT O.idO, COUNT(D.nom) FROM Oeuvre O LEFT OUTER JOIN Dragon D ON O.idO=D.idO GROUP BY O.idO HAVING COUNT(D.nom) > -1;
SELECT O.categorie, COUNT(DISTINCT(D.couleur)) AS Nb_couleur FROM Oeuvre O LEFT OUTER JOIN Dragon D ON O.idO=D.idO GROUP BY O.categorie HAVING Nb_couleur > -1;