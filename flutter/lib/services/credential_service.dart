import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/auth_response.dart';

class CredentialService {
  static const _sessionKey = 'usatt_session';
  static const _credsKey = 'usatt_creds';

  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<AuthResponse?> getSession() async {
    final data = await _storage.read(key: _sessionKey);
    if (data == null) return null;
    return AuthResponse.fromJson(jsonDecode(data));
  }

  Future<void> saveSession(AuthResponse session) async {
    await _storage.write(key: _sessionKey, value: jsonEncode(session.toJson()));
  }

  Future<void> clearSession() async {
    await _storage.delete(key: _sessionKey);
  }

  Future<Map<String, String>?> getSavedCredentials() async {
    final data = await _storage.read(key: _credsKey);
    if (data == null) return null;
    final decoded = jsonDecode(data);
    return {
      'username': decoded['username'] as String,
      'password': decoded['password'] as String,
    };
  }

  Future<void> saveCredentials(String username, String password) async {
    await _storage.write(
      key: _credsKey,
      value: jsonEncode({'username': username, 'password': password}),
    );
  }

  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
