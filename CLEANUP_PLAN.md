# Plan porządków — my-fancy-crazy-prompts

Stan na `1df9a50` (2026-11-03). Ten plik jest propozycją. Nic poza nim nie zostało przeniesione, usunięte ani przepisane.

Repozytorium jest publiczne: `ZieMat/my-fancy-crazy-prompts`. Wartości sekretów i danych osobowych nie są tu cytowane.

## 1. Diagnoza

Biblioteka promptów ma ok. 1,5 MB treści (263 pliki poza `.git` i `node_modules`) i jest zasypana zależnościami: **3433 ścieżki w `.kilocode/node_modules`**, ok. 51 MB, wszystkie śledzone przez gita. Drzewo robocze ma ok. 72 MB, z czego ok. 58 MB to `node_modules`, a `.git` ok. 11 MB. Historia ma 269 commitów, w tym **230** o treści `Sync Grok skill: …` (te same skille, wielokrotnie).

`README.md` to sam nagłówek. `AGENTS.md` opisuje drzewo, którego nie ma: obiecuje `.qwen/`, a katalog jest w `.gitignore` i go nie ma. Nie wymienia `agents/`, `bot-tuneup/`, `prompts/`, `rules/`, `workflows/`, `video-study-notes/` ani plików w korzeniu. Nie ma `.github/` ani innego linta.

### Gdzie leżą prompty

Pięć równoległych korzeni skilli, plus luźne pliki:

| Miejsce | Co tam jest |
|---|---|
| `skills/global/custom/python/` | skille Pythona, w tym 13 par bliźniaków |
| `skills/global/custom/python-project-setup/` | kopia skilla zagnieżdżonego obok |
| `skills/workspace/` | python, cybersec, experimental |
| `skills/nmap-enumerator/` | druga, identyczna kopia nmapa |
| `skills/grok/` | komendy `/alt`, `/joke`, … oraz skille ofensywne i `test-sync` |
| `video-study-notes/` | skill w korzeniu, nie pod `skills/` |
| `.agents/skills/` | `skill-creator` (wpis w `skills-lock.json`) i `harness-auditor` |
| korzeń | `grok-build-final-boss.md`, `kilo-code-final-boss.md` |

`skills/global/marketplace_skills` to plik tekstowy z trzema odnośnikami (`anthropics/skills/skill-creator`, `vercel-labs/skills/find-skills`, `github/awesome-copilot@create-agentsmd`). Zainstalowany jest tylko `skill-creator` (symlink `.kilocode/skills/skill-creator` → `../../.agents/skills/skill-creator`). `skills/global/README.md` indeksuje jeden skill autorski i podaje `find-skills` jakby leżał w repo.

### Duplikaty

Porównanie SHA-256 całej treści poza `node_modules`: **42 grupy identycznych plików, 132 pliki**.

Dokładne kopie całych drzew:

- `skills/nmap-enumerator/` i `skills/workspace/cybersec/nmap-enumerator/` — po 62 pliki, te same hasze (`SKILL.md`, `evals/evals.json`, `scripts/grade.py`, cały `nmap-enumerator-workspace/`).
- Wewnątrz każdego z tych drzew nazwane scenariusze są drugą kopią `eval-N`: `web-app-assessment` = `eval-1`, `multi-service-server` = `eval-2`, `minimal-surface` = `eval-3` (także `discovery.xml`, ok. 140 KB, leży cztery razy).
- `skills/workspace/pentest-report-assistant/` i `skills/workspace/cybersec/pentest-report-assistant/` — identyczne `SKILL.md` i `assets/VULNERABILITY_REFERENCES.md`.
- `skills/global/custom/python-project-setup/` i `skills/global/custom/python/python-project-setup/` — identyczne `SKILL.md` i `evals/evals.json`. Wersja zagnieżdżona ma dodatkowo `evals/README.md`.
- `config_files/kilo.jsonc` i `config_files/opencode.jsonc` — ten sam plik (inne narzędzia, ta sama treść). `config_files/qwen.json` trzyma tę samą listę modeli w innym schemacie.

Bliźniaki, nie kopie bajtowe. Pod `skills/global/custom/python/testing/` jest 13 par `python-<nazwa>` / `<nazwa>`. Podobieństwo linii 0,964–0,989. Wersja z prefiksem ma otwierające `---`, zgodne `name` i miejscami wstawione słowo „pytest”. Wersja bez prefiksu zaczyna się od `name:` (frontmatter się nie parsuje) i różni się głównie tym.

Osobny przypadek: dwa różne dokumenty o `name: python-linter` (podobieństwo ok. 0,24):

- `skills/global/custom/python/python-linter/SKILL.md` — naprawiać każde znalezisko ruff/ty, pole `compatibility`.
- `skills/workspace/python/python-linter/SKILL.md` — odpalić sprawdzenie, bez umowy „napraw wszystko”.

`skills/workspace/python/python-pytest/SKILL.md` nie ma pary.

### Nazwy i formaty

56 plików `SKILL.md`. Konwencja katalogu jest dobra tam, gdzie frontmatter działa: `name` zgadza się z nazwą katalogu.

15 skilli nie ma otwierającego `---`, więc blok metadanych jest zwykłym tekstem:

- 13 wersji bez prefiksu w `skills/global/custom/python/testing/**/SKILL.md`
- `video-study-notes/SKILL.md` (zamykające `---` jest w linii 8, otwierającego nie ma)

Klucze frontmattera: 37 plików ma tylko `name` + `description`, 4 mają dodatkowo `compatibility`, `skills/grok/grok-build-setup/SKILL.md` ma `when-to-use` i `argument-hint`. Nie ma wspólnych pól `tool`, `tags`, `status`.

Inne formaty obok siebie: `.md`, `.txt` (`bot-tuneup/instructions/`), `.json` i `.jsonc`, `.tmpl` w `skills/grok/grok-build-setup/references/`. MCP: `mcp/servers/git.jsonc`, `kubernetes.jsonc` i `drawio.jsonc` to płaski obiekt serwera; `mcp/servers/hexstrike/mcp.json` owija to w `mcpServers`. `skills/workspace/pentest-report-assistant/assets/VULNERABILITY_REFERENCES.md` jest jedyną nazwą w WIELKICH_LITERACH.

Dwa źródła tych samych komend: `personalize/personalize.md` (`/alt`, `/arg`, `/joke`, `/links`, `/more`, `/q`, `/redo`, `/review`, `/summary`) oraz katalogi w `skills/grok/`. Osobno `rules/git-workflow-rules.md` każe robić `git add .` i commitować wszystko, a `workflows/example/commit.md` każe commitować tylko to, co już jest w stagingu.

### Martwe i mylące

- `skills/grok/test-sync/SKILL.md` — atrapa „czy sync do GitHuba działa”. 15 commitów sync tego pliku.
- `sync-llm-dirs` — rsync całego drzewa między zahardkodowanymi katalogami, potem `git add .`, commit i push. To jest mechanizm, który wciąga `node_modules` i powiela commity. Literówka w zmiennej: `IGNORE_PATTERS`.
- `workflows/README.md` wskazuje `.qwen/commands`, `.clinerules/workflows`, `.kilocode/workflows`. Żadnej z tych ścieżek w repo nie ma.
- `grok-build-final-boss.md` w korzeniu dubluje temat `skills/grok/grok-build-setup/` (skill odsyła do `references/structure.md`).
- Commit `rm agents folder` w historii, a `agents/` z powrotem jest. Indeks tego nie tłumaczy.

### Sekrety i dane osobowe

Żywych kluczy API w plikach własnych nie widać. Placeholdery są w `config_files/qwen.json` (`<env-key>`, `<openai-compatible-api-url>`), `config_files/kilo.jsonc` / `opencode.jsonc` (ten sam placeholder URL) oraz w MCP (`<host-path>`, `IPADDRESS` w `mcp/servers/hexstrike/mcp.json`). Adresy w raportach nmap (`192.168.x`) pochodzą z fixture’ów ewaluacji, zdublowanych jak wyżej.

Dane osobowe są w publicznym drzewie. Wartości nie przepisuję:

| Ścieżka | Co jest | Gdzie |
|---|---|---|
| `bot-tuneup/instructions/grok-bot.txt` | adres e-mail | ok. linia 4 |
| `bot-tuneup/instructions/pedalarz-expert.txt` | wzrost, waga, rozmiary, miasto, budżet | cały plik |
| `bot-tuneup/instructions/shopping-assistant.txt` | nawyki zakupowe, imię | cały plik |
| `bot-tuneup/changelog.md` | imię, identyfikatory botów, daty, miasto | cały plik |
| `sync-llm-dirs` | nazwa konta i ścieżka katalogu domowego | linie 9–10 |

`git rm` zdejmuje to tylko z czubka gałęzi. Bloby zostają w historii i na GitHubie, dopóki nie będzie osobnego przepisywania historii. Do tego czasu adres e-mail trzeba traktować jak już upubliczniony.

`prompts/bot-tuneup-prompt.md` nie zawiera tych danych. To ogólna procedura tune-upu.

## 2. Docelowa struktura

Jedna biblioteka autorska, vendor zostaje tam, gdzie ładuje go host, dane osobowe schodzą z publicznego drzewa.

```
.
├── README.md                     # opis + indeks między markerami
├── AGENTS.md                     # jak dodać prompt; mapa odsyła do README
├── CLEANUP_PLAN.md               # ten plan, do skasowania po wdrożeniu
├── skills-lock.json
├── .agents/skills/               # vendor i skille tego repo ładowane przez hosta
│   ├── skill-creator/            # bez zmian; trzyma go skills-lock
│   └── harness-auditor/
├── .kilocode/                    # package.json + lock; node_modules poza gitem
│   └── skills/skill-creator      # istniejący symlink
├── skills/
│   ├── python/<nazwa>/SKILL.md
│   ├── security/<nazwa>/SKILL.md
│   ├── grok/<nazwa>/SKILL.md
│   └── general/<nazwa>/SKILL.md
├── agents/
│   ├── python-code-quality-engineer.md
│   └── examples/qwen-test-engineer.md
├── prompts/
│   ├── personas/grok-kibol-mode.md
│   ├── platforms/kilo-layout.md
│   ├── bots/bot-tuneup.md
│   └── workflows/
├── personalize/                  # nakładka zachowania; zostaje
├── platforms/
│   ├── kilo.jsonc
│   ├── opencode.jsonc
│   ├── qwen.json
│   └── mcp/
├── archive/                      # nie-osobowe duplikaty i atrapy
└── scripts/check_prompts.py
```

`skills/global` i `skills/workspace` znikają. Różnicę „globalny / lokalny” zapisuje pole `scope`, nie drugi korzeń.

### Nazwy

- Katalog skilla: `kebab-case`, identyczny z `name`.
- Jeden skill, jeden katalog, jeden `SKILL.md`.
- Bez pary `foo` i `python-foo`.
- Pliki pomocnicze: `kebab-case.md` (`vulnerability-references.md`, nie `VULNERABILITY_REFERENCES.md`).
- Szablony zostają przy skillu, sufiks `.tmpl`.
- Konfiguracja platformy: `platforms/<narzędzie>.jsonc` albo `.json`, gdy plik jest czystym JSON-em.

### Minimalny frontmatter

`name` i `description` zostają, bo po nich hosty odkrywają skill. `description` jest celem i warunkiem odpalenia. Nowe pola są krótkie i ignorowane przez stare loadery.

```yaml
---
name: python-find-edge-cases
description: Jedno zdanie celu i zdanie, kiedy skill odpalić.
tool: any            # any | grok | kilo | qwen | opencode
tags: [python, testing]
status: active       # draft | active | archived
---
```

Opcjonalnie, tylko gdy skill już to ma: `compatibility`, `when-to-use`, `argument-hint`. Agenci z polami `model` i `tools` (wzorzec: `agents/python-code-quality-engineer.md`) tych pól nie gubią.

`status: archived` oznacza „nie używać”. Plik i tak ląduje w `archive/`, żeby nie ładował się z `skills/`.

### README

Ręczny wstęp (po co jest repo, gdzie są dane prywatne, jak dodać skill) plus sekcja generowana:

```markdown
<!-- INDEX:START -->
<!-- INDEX:END -->
```

Skrypt wstawia tam tabelę: nazwa, ścieżka, `tool`, `status`, pierwsze zdanie `description`. `AGENTS.md` skraca się do reguł dodawania i odsyłacza do tego indeksu. `skills/README.md` i `skills/global/README.md` odpadają po wygenerowaniu indeksu, żeby nie było trzech map.

## 3. Mapa migracji

Wiersz katalogu oznacza całe drzewo (`git mv`). Kanon przy duplikacie to jedna ścieżka; druga znika z drzewa i zostaje w historii gita. Do `archive/` idą tylko pliki bez danych osobowych.

| Stara ścieżka | Nowa ścieżka | Akcja | Uzasadnienie |
|---|---|---|---|
| `bot-tuneup/instructions/` | — | usuń z drzewa | dane osobowe w publicznym repo; nie kopiować do `archive/` |
| `bot-tuneup/changelog.md` | — | usuń z drzewa | j.w. |
| `prompts/bot-tuneup-prompt.md` | `prompts/bots/bot-tuneup.md` | przenieś | procedura bez danych osobowych |
| `sync-llm-dirs` | — | usuń z drzewa | ścieżka domowa i `git add .`; historia i tak zostaje |
| `.kilocode/node_modules/` | — | usuń z gita | zależności, 3433 ścieżki; `package.json` i lock zostają |
| `skills/nmap-enumerator/` | — | usuń z drzewa | identyczne z kopią w `skills/workspace/cybersec/` |
| `skills/workspace/cybersec/nmap-enumerator/` | `skills/security/nmap-enumerator/` | przenieś | kanon; patrz wiersz o ewaluacjach |
| `skills/security/nmap-enumerator/nmap-enumerator-workspace/iteration-1/eval-{1,2,3}/` | — | usuń z drzewa | bajt w bajt te same pliki co `web-app-assessment`, `multi-service-server`, `minimal-surface` |
| `skills/workspace/cybersec/pentest-report-assistant/` | `skills/security/pentest-report-assistant/` | przenieś | kanon; plik assetów zmienić na `kebab-case` przy okazji |
| `skills/workspace/pentest-report-assistant/` | — | usuń z drzewa | identyczna kopia |
| `skills/workspace/cybersec/offensive-security-engine/` | `skills/security/offensive-security-engine/` | przenieś | jeden skill, bez pary |
| `skills/workspace/cybersec/offensive-security-engine-workspace/` | `skills/security/offensive-security-engine/evals/workspace/` | przenieś | wyniki ewaluacji trzymać przy skillu |
| `skills/workspace/experimental/htb-writeup-assistant/` | `skills/security/htb-writeup-assistant/` | przenieś | skill, nie persona; ma `evals/evals.json` |
| `skills/global/custom/python/python-project-setup/` | `skills/python/python-project-setup/` | przenieś | ma `evals/README.md` |
| `skills/global/custom/python-project-setup/` | — | usuń z drzewa | kopia bez `evals/README.md` |
| `skills/global/custom/python/python-*/` (poza linterem) | `skills/python/<nazwa>/` | przenieś | poprawny frontmatter |
| 13 katalogów bez prefiksu, lista niżej | `archive/python-testing-unprefixed/<nazwa>/` | archiwizuj | ok. 97% treści bliźniaka, zepsuty frontmatter |
| `skills/global/custom/python/python-linter/` | `skills/python/python-linter/` | przenieś | pełniejsza umowa (naprawiaj znaleziska) |
| `skills/workspace/python/python-linter/` | `archive/python-linter-check/SKILL.md` | archiwizuj | inne zachowanie, ta sama `name`; nie scalać automatycznie |
| `skills/workspace/python/python-pytest/` | `skills/python/python-pytest/` | przenieś | brak pary |
| `skills/global/custom/python/python-dead-code/` | `skills/python/python-dead-code/` | przenieś | brak pary |
| `skills/grok/test-sync/` | `archive/test-sync/` | archiwizuj | atrapa syncu |
| `skills/grok/` (reszta) | `skills/grok/` | zostaw | nazwy już są `kebab-case` i zgodne z `name` |
| `video-study-notes/` | `skills/general/video-study-notes/` | przenieś | skill z korzenia; dopisać otwierające `---` |
| `experimental/grok-kibol-mode.md` | `prompts/personas/grok-kibol-mode.md` | przenieś | persona bez frontmattera; `status: experimental` |
| `grok-build-final-boss.md` | `archive/notes/grok-build-final-boss.md` | archiwizuj | temat pokrywa `skills/grok/grok-build-setup/` |
| `kilo-code-final-boss.md` | `prompts/platforms/kilo-layout.md` | przenieś | jedyny opis układu Kilo; nie ma bliźniaka-skilla |
| `agents/` | `agents/` | zostaw | ma już frontmatter z `model` i `tools` |
| `personalize/` | `personalize/` | zostaw | nakładka; nie scalać na siłę ze `skills/grok/` |
| `config_files/kilo.jsonc` | `platforms/kilo.jsonc` | przenieś | identyczny z opencode; oba zostają, lint pilnuje listy modeli |
| `config_files/opencode.jsonc` | `platforms/opencode.jsonc` | przenieś | j.w. |
| `config_files/qwen.json` | `platforms/qwen.json` | przenieś | inny schemat, ta sama lista modeli |
| `mcp/servers/` | `platforms/mcp/` | przenieś | schemat hexstrike ujednolicić później |
| `rules/git-workflow-rules.md` | `archive/rules/git-workflow-rules.md` | archiwizuj | każe `git add .`; w konflikcie z `workflows/example/commit.md` |
| `workflows/` | `prompts/workflows/` | przenieś | przykłady; README poprawić, bo wskazuje nieistniejące ścieżki |
| `skills/global/marketplace_skills` | `platforms/skill-sources.txt` | przenieś | lista źródeł, nie zainstalowane skille |
| `skills/README.md`, `skills/global/README.md` | — | usuń z drzewa | zastępuje je indeks w `README.md` |
| `.agents/skills/skill-creator/` | bez zmian | zostaw | vendor, `skills-lock.json`, symlink z `.kilocode` |
| `.agents/skills/harness-auditor/` | bez zmian | zostaw | skill tego repo, ładowany z `.agents/skills` |
| `.gitignore` | dopisać `node_modules/` | przepisz jedną sekcję | dziś jest tylko `.qwen/` |

13 katalogów do archiwum (zostaje wersja `python-*`):

`choose-test-level`, `convert-bug-report-to-test`, `design-high-value-tests`, `design-regression-tests`, `detect-brittle-tests`, `detect-risk-areas`, `find-edge-cases`, `find-missing-test-cases`, `fix-failing-tests`, `generate-integration-tests`, `generate-unit-tests`, `identify-critical-scenarios`, `stabilize-flaky-tests`.

Leżą w `skills/global/custom/python/testing/{analyze,implementation,project,review-maintenance}/`.

Decyzja przed scaleniem, nie w ciemno: czy z `archive/python-linter-check/` wrócić fragmentami komend do kanonicznego `python-linter`. Domyślnie kanonem jest wersja z `compatibility`, która każe naprawiać znaleziska.

## 4. Proces, żeby bałagan nie wrócił

Trzy mechanizmy. Bez obowiązkowych recenzji, szablonów zgłoszeń i komitetu.

1. **`scripts/check_prompts.py`** (sam Python, bez zależności). Sprawdza każdy `SKILL.md` i pliki w `prompts/` oraz `agents/`:
   - plik zaczyna się od `---`;
   - są `name`, `description`, `tool`, `tags`, `status`;
   - `name` jest `kebab-case` i równa się katalogowi skilla;
   - `name` jest unikalne w repo;
   - `status` należy do `draft | active | archived`;
   - `git ls-files` nie zawiera `node_modules`;
   - ostrzeżenie, gdy dwa pliki poza `archive/` mają ten sam SHA-256.
2. **CI**: jeden workflow na push i pull request, uruchamia ten skrypt. Najpierw tryb ostrzeżenia. Błąd dopiero, gdy cały bieżący zbiór przejdzie na czysto. Nowe pliki od PR-u z linterem muszą przechodzić od razu.
3. **Indeks**: ten sam skrypt z `--write-index` wstawia tabelę między `<!-- INDEX:START -->` a `<!-- INDEX:END -->`. Odpalany ręcznie w PR, który dodaje skill. CI sprawdza, że indeks jest aktualny (`--check-index`), bez commita z CI.

Reguły pisane, krótkie, w `AGENTS.md`:

- Nowy prompt autorski: `skills/<domena>/<nazwa>/SKILL.md` albo `prompts/<rodzaj>/<nazwa>.md`.
- Skill, który ma się ładować w tym repo, może dostać symlink z `.agents/skills/`. Kopia plików nie.
- `archive/` nie jest ładowane. `status: archived` i katalog `archive/` idą w parze.
- Dane osobowe i sekrety nie wchodzą do tego repo. Instrukcje botów z życiem prywatnym zostają w prywatnym repozytorium.
- Commit dotyczy plików zadania. Zakaz `git add .` w korzeniu (to wciągnęło `node_modules`).
- Sync z drugim repo, jeśli nadal potrzebny, dostaje jawną listę katalogów i wyklucza `node_modules`, `archive/` i pliki prywatne. Skrypt nie robi `git push`.

`personalize/personalize.md` zostaje nakładką tonu. `skills/grok/` zostaje implementacją komend dla hostów ładujących skille. Przy zmianie komendy rusza się jedno miejsce i w opisie drugiego jest odsyłacz. Lint tego nie scala.

## 5. Kolejność PR-ów

Od rzeczy, które da się cofnąć bez szukania promptu po nowej ścieżce. Jeden temat na PR. `git mv`, żeby historia pliku została.

| # | PR | Ryzyko | Efekt |
|---|---|---|---|
| 0 | ten plik | żadne dla promptów | przegląd planu |
| 1 | zdjąć z drzewa `bot-tuneup/instructions/`, `bot-tuneup/changelog.md` i `sync-llm-dirs`; repo przełączyć na prywatne albo świadomie zostawić publiczne | niskie dla promptów, wysokie dla prywatności | z HEAD znika e-mail, dane ciała, miasto, ścieżka domowa |
| 2 | `git rm -r --cached .kilocode/node_modules` i `node_modules/` w `.gitignore` | niskie | −3433 pliki; build pluginu robi `npm install` |
| 3 | skrypt linta w trybie ostrzeżenia; dopisać otwierające `---` w `video-study-notes/SKILL.md` | niskie, diff mechaniczny | 15 plików znowu ma frontmatter; bliźniaki i tak idą do archiwum w PR 6 |
| 4 | markery indeksu w `README.md`, jedna linia w `AGENTS.md` | niskie | mapa bez ręcznego spisu |
| 5 | usunąć dokładne kopie: cały `skills/nmap-enumerator/`, `eval-{1,2,3}` w kopii kanonicznej, `skills/workspace/pentest-report-assistant/`, `skills/global/custom/python-project-setup/` | niskie, treść kanonu bez zmian | −132 pliki w grupach haszy, część grup zostaje do PR 6 |
| 6 | `git mv` 13 skilli bez prefiksu do `archive/python-testing-unprefixed/` | średnie | jedna `name` na parę; hosty widzą wersję z `---` |
| 7 | `git mv` `skills/workspace/python/python-linter` do `archive/python-linter-check/` | średnie, bo zachowanie inne | koniec kolizji `name: python-linter` |
| 8 | przeprowadzka domenami: `python`, potem `security`, potem `general` i `prompts/`, na końcu `platforms/` + `mcp/` | średnie, po jednej domenie | ścieżki z sekcji 2 |
| 9 | archiwum reszty: `test-sync`, `grok-build-final-boss.md`, `rules/git-workflow-rules.md`; przeniesienie `workflows/` | niskie | korzeń bez luźnych manifestów |
| 10 | dopisać `tool`, `tags`, `status` przy przeprowadzce domeny (albo tu, jeśli PR 8 tego nie wziął); lint przełączyć na błąd | niskie, gdy pola są uzupełnione | CI pilnuje nowych plików |
| 11 | opcjonalnie `git filter-repo` + force-push historii z `node_modules` i danymi osobowymi | wysokie, świadoma decyzja | klon przestaje nieść 51 MB i stary e-mail |

PR 1 nie czeka na resztę. Przepisanie historii (PR 11) jest osobną zgodą: psuje klony, a GitHub może trzymać stare bloby w cache. Samo przełączenie widoczności na prywatną nie kasuje danych z kopii, które już ktoś sklonował.

Po PR 8 skasować ten plan albo przenieść go do `archive/notes/`, żeby nie udawał bieżącej instrukcji.

## Czego nie wiem

- Czy `my-llm-stuff` z `sync-llm-dirs` nadal jest drugą kopią. Commit `synchro with private repo` na to wskazuje. Jeśli tak, PR 1 trzeba powtórzyć tam, a sync po PR 2 nie może z powrotem wgrać `node_modules`.
- Czy fixture’y nmap (surowe `.xml` / `.nmap`) mają zostać przy skillu, czy wystarczy `evals/evals.json` i `scripts/grade.py`. Plan zostawia jedną kopię nazwanych scenariuszy.
- Czy `@kilocode/plugin` w `.kilocode/package.json` jest jeszcze używany. Jak nie, PR 2 może zabrać też `package.json` i lock.
