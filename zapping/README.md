# ZAPPING : studio Unreal + Claude Code

Le studio est prêt à ouvrir sur ton Mac. Il contient :

```
zapping/
  GDD.md                 le document de game design (règles, DA, plan de construction)
  prototype/index.html   le jeu jouable tout de suite dans le navigateur
  unreal/                le projet Unreal Engine 5.8, pré-réglé
    Zapping.uproject       plugins Unreal MCP + All Toolsets + Python activés
    .mcp.json              connexion de Claude Code à l'éditeur (127.0.0.1:8000/mcp)
    .claude/settings.json  installe le plugin Epic « Unreal Engine Skills » pour Claude Code
    Config/                réglages MacBook Air (sans Lumen ni Nanite), démarrage auto du serveur MCP
    preparer-mac.sh        vérifie ton Mac et ouvre le projet
```

## Installation sur ton Mac (une seule fois)

1. **Unreal Engine 5.8** : installe l'[Epic Games Launcher](https://www.epicgames.com/store/download), connecte-toi, onglet *Unreal Engine* > *Bibliothèque* > *+* > choisis **5.8** > *Installer*.
   Prévois environ 80 Go libres et une bonne heure de téléchargement.
2. **Claude Code** : suis [code.claude.com](https://code.claude.com) (installation en une commande dans le Terminal).
3. **Récupère ce dépôt** sur ton Mac (GitHub Desktop, ou `git clone`), branche `claude/hopeful-ramanujan-ezhmdn`.
4. *(Optionnel)* **Xcode** depuis l'App Store : inutile pour jouer dans l'éditeur, nécessaire pour exporter une application `.app`.

## Ouvrir le studio

Dans le Terminal, depuis le dossier du dépôt :

```bash
cd zapping/unreal
```

```bash
bash preparer-mac.sh
```

Le script vérifie la puce, la mémoire, le disque, Unreal et Claude Code, puis ouvre le projet.
La première ouverture compile les shaders : 10 à 30 minutes sur un MacBook Air. C'est normal.

Quand l'éditeur est ouvert, dans un **second** onglet du Terminal :

```bash
cd zapping/unreal && claude
```

Claude Code te propose d'installer le plugin *unreal-engine-skills-for-claude-code* : accepte.
Tape `/mcp` : `unreal-mcp` doit apparaître comme connecté. Puis essaie :

> Liste les acteurs du niveau courant.

Si ça répond, le studio fonctionne. Enchaîne avec l'étape 1 de `GDD.md`.

## Si quelque chose bloque

- **`unreal-mcp` non connecté** : dans l'éditeur, ouvre la console (touche `` ` ``) et tape `ModelContextProtocol.StartServer`. Puis `/mcp` dans Claude Code.
- **Aucun outil côté Unreal** : *Edit > Plugins*, vérifie que *Unreal MCP* et *All Toolsets* sont cochés, redémarre l'éditeur.
- **Port 8000 déjà pris** : `ModelContextProtocol.StartServer 8100` dans la console, puis `ModelContextProtocol.GenerateClientConfig ClaudeCode` pour réécrire `.mcp.json`.
- **Unreal installé ailleurs** que `/Users/Shared/Epic Games/UE_5.8` : `UE_RACINE="/ton/chemin/UE_5.8" bash preparer-mac.sh`.

## Sécurité (rappel d'Epic)

Le plugin donne à Claude un accès complet à l'éditeur, y compris l'exécution de Python.
Sauvegarde et commite avant chaque grosse étape. Évite `--dangerously-skip-permissions` sur ce projet.
