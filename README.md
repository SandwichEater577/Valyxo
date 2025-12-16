# 🚀 Valyxo — Ekosystem Programistyczny XXI Wieku

> **Valyxo** = Terminal developer + AI Assistant + Ecosystem

```
     ██    ██  █████  ██       █████  ██   ██  ██████  
     ██    ██ ██   ██ ██      ██   ██  ██ ██  ██    ██ 
     ██    ██ ███████ ██      ███████   ███   ██    ██ 
     ██    ██ ██   ██ ██      ██   ██   ██    ██    ██ 
      ██████  ██   ██ ███████ ██   ██   ██     ██████  
                                                        
         Version 0.31+ | Powered by Zencoder AI
```

## 📋 Spis Treści

1. [O Projekcie](#o-projekcie)
2. [Architektura](#architektura)
3. [Komponenty](#komponenty)
4. [Instalacja](#instalacja)
5. [Użytkowanie](#użytkowanie)
6. [Roadmapa](#roadmapa)
7. [Licencja](#licencja)

---

## 🎯 O Projekcie

**Valyxo** to kompleksowy ekosystem dla programistów, składający się z trzech głównych komponentów:

| Komponent | Typ | Opis |
|-----------|-----|------|
| **ValyxoHub** | Terminal CLI | Środowisko programistyczne w terminalu |
| **ValyxoApp** | Aplikacja Desktop | Graficzny interfejs dla wizualizacji |
| **ValyxoGPT** | AI Assistant | Asystent oparty na Zencoder AI |
| **ValyxoScript** | Język | Lekki język skryptowy dla Valyxo |

### 🌟 Cechy Valyxo

- ✅ **Nowoczesna architektura** — modularny design, łatwy do rozszerzania
- ✅ **Terminal-first** — pełna moc w CLI dla developerów
- ✅ **AI-powered** — integracja z Zencoder AI
- ✅ **Cross-platform** — Linux, Windows, macOS
- ✅ **Open Source** — publiczny kod, transparent development
- ✅ **Bezpieczny** — hash haseł, walidacja, ochrona danych

---

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────────┐
│                   VALYXO ECOSYSTEM                      │
└─────────────────────────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼─────┐        ┌────▼─────┐      ┌─────▼─────┐
    │ TERMINAL │        │  DESKTOP │      │    WEB    │
    │(ValyxoHub)        │(ValyxoApp)      │(Platform) │
    └──────────┘        └──────────┘      └───────────┘
         │                  │                  │
         ├──────────────────┼──────────────────┤
         │                  │                  │
    ┌────▼──────────────────▼──────────────────▼─┐
    │           VALYXO CORE                      │
    │  ┌─────────────────────────────────────┐   │
    │  │ - Filesystem Operations             │   │
    │  │ - ValyxoScript Runtime              │   │
    │  │ - Job Management                    │   │
    │  │ - Manual System                     │   │
    │  │ - Color Theming                     │   │
    │  └─────────────────────────────────────┘   │
    └────┬──────────────────────────────────┬────┘
         │                                  │
    ┌────▼───────────────────────────┬─────▼────┐
    │                                │          │
┌───▼──────┐                   ┌─────▼───┐ ┌────▼─────┐
│ValyxoGPT │                   │ Zencoder│ │ Database  │
│(AI Core) │                   │   API   │ └──────────┘
└──────────┘                   └─────────┘
```

### 🎯 Trzy Główne Warstwy

#### 1️⃣ **ValyxoHub** — Terminal CLI
- Aplikacja konsolowa dla programistów
- Pełna moc edycji i uruchamiania kodu
- Wsparcie dla wielu języków (ValyxoScript, JS, Python, Java)
- AI Assistant w terminalu

#### 2️⃣ **ValyxoApp** — Aplikacja Desktop
- Interfejs graficzny (planowana, C++/Java/Rust)
- Wizualizacja projektów
- Integracja z ValyxoHub
- Nie zastępuje terminal, tylko go uzupełnia

#### 3️⃣ **Strona Internetowa** — Full Stack Platform
- Frontend: HTML5 + CSS3 + JavaScript
- Backend: Node.js + Express (REST API)
- Baza danych: PostgreSQL/SQLite
- Funkcje: Login, Register, Dashboard, AI Chat

---

## 🔧 Komponenty

### **ValyxoHub** (Terminal)

```bash
valyxohub                    # Uruchomienie terminalowego hubą
```

Komendy:
- `mkdir <path>` — Tworzenie katalogów
- `ls [path]` — Wylistowanie plików
- `cd <path>` — Zmiana katalogu
- `nano <file>` — Edytor plików
- `run <file>` — Uruchomienie skryptu
- `jobs` — Lista uruchomionych procesów
- `kill <pid>` — Zabicie procesu
- `enter ValyxoScript` — Wejście w interpreter skryptów
- `enter ValyxoGPT` — Rozmowa z AI asystentem
- `theme [list|set]` — Zarządzanie motywami
- `man <command>` — Dokumentacja

### **ValyxoScript**

Lekki język skryptowy:

```valyxoscript
set x = 10
set y = 20
set z = x + y
print z

if [z > 20] then [print "Wieksza!"] else [print "Mniejsza!"]

func add(a, b) {
  set result = a + b
  print result
}
```

### **ValyxoGPT**

AI Assistant w terminalu:

```bash
> enter ValyxoGPT
> How do I define a function in ValyxoScript?
AI: ValyxoScript functions: Use 'func name(params) { body }'...
```

---

## 📦 Instalacja

### Wymagania
- Python 3.8+
- Git
- npm (dla backendu strony)

### Krok 1: Klonowanie repozytorium

```bash
git clone https://github.com/yourusername/valyxo.git
cd valyxo
```

### Krok 2: Instalacja zależności

```bash
# Terminal CLI
pip install -r requirements.txt

# Strona internetowa (opcjonalnie)
cd website
npm install
```

### Krok 3: Uruchomienie ValyxoHub

```bash
python src/Valyxo.py
```

---

## 🎮 Użytkowanie

### Uruchamianie ValyxoHub

```bash
python src/Valyxo.py
```

Powinieneś zobaczyć:
```
Welcome to Valyxo v0.31 (Zencoder Integrated)
valyxo:~> 
```

### Podstawowe polecenia

```bash
# Tworzenie projektu
mkdir Projects/MyProject
cd Projects/MyProject

# Tworzenie pliku
nano main.vs

# Uruchomienie
run main.vs

# Rozmowa z AI
enter ValyxoGPT

# Pomoc
man valyxohub
```

---

## 🗺️ Roadmapa

### ✅ v0.31 (Obecna)
- [x] Modularny kod Valyxo
- [x] Usunięcie legacy NovaHub
- [x] Clean architektura
- [ ] Pełna dokumentacja

### 🔄 v0.32 (Planowana)
- [ ] ValyxoApp (Desktop Application)
- [ ] Rozszerzone moduły ValyxoScript
- [ ] Wtyczki (plugin system)
- [ ] Performance optimization

### 📅 v0.33+ (Future)
- [ ] Web IDE (Visual Studio Code-like)
- [ ] Collaboration tools
- [ ] Mobile app
- [ ] Cloud storage integration

---

## 📂 Struktura Projektu

```
valyxo/
├── src/
│   ├── Valyxo.py                 (Entry point)
│   ├── valyxo/
│   │   ├── core/                 (Core modules)
│   │   │   ├── colors.py
│   │   │   ├── constants.py
│   │   │   ├── utils.py
│   │   │   ├── filesystem.py
│   │   │   ├── gpt.py
│   │   │   ├── jobs.py
│   │   │   └── man.py
│   │   ├── shell/
│   │   ├── editor/
│   │   └── __init__.py
│   └── tests/
├── website/
│   ├── frontend/
│   │   ├── index.html
│   │   ├── css/
│   │   └── js/
│   ├── backend/
│   │   └── server.js
│   └── package.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── MANUAL.md
│   └── API.md
├── README.md
├── LICENSE
└── requirements.txt
```

---

## 🔒 Bezpieczeństwo

Valyxo jest zbudowany z myślą o bezpieczeństwie:

- ✅ **Haszowanie haseł** — bcrypt/argon2
- ✅ **Walidacja danych** — sanitizacja inputów
- ✅ **HTTPS** — szyfrowana komunikacja
- ✅ **Brak plaintext secrets** — environment variables
- ✅ **SQL Injection protection** — parameterized queries
- ✅ **CSRF Protection** — token validation
- ✅ **XSS Prevention** — output escaping

---

## 📚 Dokumentacja

- **[VALYXO_ARCHITECTURE.md](./VALYXO_ARCHITECTURE.md)** — Szczegółowa architektura
- **[VALYXO_QUICK_START.md](./VALYXO_QUICK_START.md)** — Quick reference
- **docs/API.md** — REST API documentation
- **docs/MANUAL.md** — Kompletny manual użytkownika

---

## 🤝 Contributing

Zapraszamy do contribucji! Aby zacząć:

1. Fork repozytorium
2. Utwórz branch (`git checkout -b feature/NewFeature`)
3. Commit zmiany (`git commit -m 'Add NewFeature'`)
4. Push do brancha (`git push origin feature/NewFeature`)
5. Otwórz Pull Request

---

## 📄 Licencja

Valyxo jest dostępny na licencji **MIT z ograniczeniami komercyjnymi**.

Szczegóły: [LICENSE](./LICENSE)

---

## 📞 Kontakt

- 🐙 GitHub: [github.com/...](https://github.com)
- 📧 Email: contact@valyxo.dev
- 🌐 Website: valyxo.dev (planowana)

---

## 🌟 Podziękowania

Dziękujemy:
- **Zencoder AI** — za integrację AI
- Społeczności open-source
- Wszystkim kontrybutorem

---

**Valyxo v0.31+** — The Developer's Ecosystem

_Zbudowanie przez programistów, dla programistów._

```
Made with ❤️ in Poland
```
