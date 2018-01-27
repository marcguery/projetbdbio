# BDBIO : projets et commandes tp

# Projet
------------------------------------------
Pour générer la base de données intégrée :

```
python3 intersector.py
```

Qui crée un fichier _EbvDatabase.sqlite_ utilisable dans sqlitestudio

**Ressources originales utilisées** : _interactions-PMID-17446270.json_ et _tp4.ttl_

**Ressources modifiées utilisées** : _tp2.sql_ -> _tp2Virus.sqlite_ et _tp3.xml_ -> _tp3corrected.xml_ (strip namespaces)

Le script n'est pas commenté, mais il est organisé en fonctions dont les noms sont (plus ou moins) explicites...

Il est de plus très mal optimisé, c'est pourquoi **le temps d'exécution est très long** (entre 5 et 10 minutes).

------------------------------------------
# Commandes TP
------------------------------------------
Les requetes utilisées pour les questions des TP 2, 3 et 4 sont dans le dossier _commandsTP_

------------------------------------------

# Remarques et améliorations
------------------------------------------
Si vous avez un problème dans l'interprétation de certaines lignes de code ou dans les requetes, n'hésitez pas à me demander !

Si vous voulez améliorer le script (surtout coté **optimisation** et **adaptabilité**) ou les requetes, proposez moi vos idées !