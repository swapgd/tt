import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/auth_response.dart';
import '../services/api_service.dart';
import '../services/credential_service.dart';

class AuthState {
  final AuthResponse? session;
  final bool isLoading;
  final String? error;

  AuthState({this.session, this.isLoading = false, this.error});

  bool get isLoggedIn => session != null;

  AuthState copyWith({AuthResponse? session, bool? isLoading, String? error, bool clearSession = false}) {
    return AuthState(
      session: clearSession ? null : (session ?? this.session),
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService _api = ApiService();
  final CredentialService _creds = CredentialService();

  AuthNotifier() : super(AuthState()) {
    _restoreSession();
  }

  Future<void> _restoreSession() async {
    final session = await _creds.getSession();
    if (session != null) {
      state = state.copyWith(session: session);
    }
  }

  Future<bool> login(String username, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final session = await _api.login(username, password);
      await _creds.saveSession(session);
      await _creds.saveCredentials(username, password);
      state = state.copyWith(session: session, isLoading: false);
      return true;
    } on DioException catch (e) {
      final msg = e.response?.statusCode == 401
          ? 'Invalid email or password'
          : 'Connection error';
      state = state.copyWith(isLoading: false, error: msg);
      return false;
    } catch (e) {
      state = state.copyWith(isLoading: false, error: 'Connection error');
      return false;
    }
  }

  Future<void> logout() async {
    await _creds.clearAll();
    state = AuthState();
  }

  Future<bool> refreshSession() async {
    final creds = await _creds.getSavedCredentials();
    if (creds == null) return false;
    try {
      final session = await _api.login(creds['username']!, creds['password']!);
      await _creds.saveSession(session);
      state = state.copyWith(session: session);
      return true;
    } catch (_) {
      return false;
    }
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});
