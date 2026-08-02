# USATT Ratings Flutter App

## Overview
Mobile app (iOS + Android) for viewing USA Table Tennis player ratings. Authenticates against a backend API server and displays player ratings, search results, and detailed profiles.

## Architecture
- **State management**: flutter_riverpod (StateNotifier pattern)
- **HTTP**: dio
- **Routing**: go_router (configured but currently using simple MaterialApp home)
- **Secure storage**: flutter_secure_storage (credentials + session tokens)
- **Theme**: Dark theme with accent color `#00D4FF`, background `#1A1A2E`, surface `#16213E`

## Project Structure
```
lib/
├── main.dart              # App entry, AuthGate (shows Login or Home based on auth state)
├── models/
│   ├── auth_response.dart # Login response model (token, playerId, name)
│   ├── player_profile.dart# Full player profile with rating history
│   └── ranked_player.dart # Search result player model
├── providers/
│   ├── auth_provider.dart # AuthNotifier – login, logout, auto-refresh session
│   ├── rating_provider.dart # Loads logged-in user's rating
│   └── search_provider.dart # Player search with pagination
├── screens/
│   ├── home_screen.dart   # Bottom nav: My Rating | Search
│   ├── login_screen.dart  # USATT credential login
│   ├── my_rating_screen.dart # Shows logged-in user's rating via PlayerCard
│   ├── player_detail_screen.dart # Full player profile view
│   └── search_screen.dart # Search players by name
├── services/
│   ├── api_service.dart   # All HTTP calls to backend (base URL: http://100.23.239.84:8080)
│   └── credential_service.dart # Secure read/write of session + credentials
└── widgets/
    └── player_card.dart   # Reusable player rating display card
```

## Backend API
- Base URL: `http://100.23.239.84:8080`
- Endpoints:
  - `POST /api/login` – body: `{username, password}` → AuthResponse
  - `GET /api/my-rating?player_id=&token=` → PlayerProfile
  - `GET /api/search?q=&token=&page=` → `{players: [...]}`
  - `GET /api/player/:id?token=` → PlayerProfile
- On HTTP 500 from backend, treat as expired session and auto re-login

## Key Patterns
- Auth flow: credentials stored in secure storage, session auto-restored on app start
- Session refresh: if a request fails with 500, AuthNotifier.refreshSession() re-logs in with saved credentials
- Pull-to-refresh on rating screen

## Build & Run
```bash
flutter pub get
flutter run            # debug on connected device/simulator
flutter build ios      # iOS release
flutter build apk     # Android release
```

## Conventions
- Use Riverpod StateNotifier for all state
- Keep services stateless (no singletons with state)
- Dark theme colors are hardcoded constants (no theme extension yet)
- No tests currently — add if modifying core logic
