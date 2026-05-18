# Runbooks — Simplon RAG

## LatenceP95Haute

**Description** : La latence p95 sur `/messages` dépasse 2 secondes.

**Causes possibles** :
- Requête LLM lente (timeout, surcharge)
- Requête BDD lente (index manquant, connexions saturées)
- Recherche vectorielle lente (trop de chunks)

**Actions** :
1. Vérifier les logs : `docker logs simplon_rag_api | grep messages`
2. Vérifier la BDD : `docker logs simplon_rag_postgres_pgvector`
3. Vérifier Prometheus : `http://localhost:9090`
4. Réduire le nombre de chunks retournés par la recherche vectorielle
5. Redémarrer l'API si nécessaire : `docker restart simplon_rag_api`

---

## TauxErreur5xxEleve

**Description** : Le taux d'erreurs 5xx dépasse 5% sur 5 minutes.

**Causes possibles** :
- Erreur de connexion à la BDD
- Erreur LLM (clé API invalide, quota dépassé)
- Bug applicatif

**Actions** :
1. Vérifier les logs : `docker logs simplon_rag_api --tail 50`
2. Vérifier la BDD : `docker ps | grep postgres`
3. Vérifier la clé API LLM dans le `.env`
4. Redémarrer les services : `docker compose restart api`
