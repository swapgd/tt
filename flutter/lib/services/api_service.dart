import 'package:dio/dio.dart';
import '../models/auth_response.dart';
import '../models/player_profile.dart';
import '../models/ranked_player.dart';

class ApiService {
  static const _baseUrl = 'http://100.23.239.84:8080';

  final Dio _dio = Dio(BaseOptions(
    baseUrl: _baseUrl,
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  Future<AuthResponse> login(String username, String password) async {
    final resp = await _dio.post('/api/login', data: {
      'username': username,
      'password': password,
    });
    return AuthResponse.fromJson(resp.data);
  }

  Future<PlayerProfile> myRating(String playerId, String token) async {
    final resp = await _dio.get('/api/my-rating', queryParameters: {
      'player_id': playerId,
      'token': token,
    });
    return PlayerProfile.fromJson(resp.data);
  }

  Future<List<RankedPlayer>> search(String query, String token, {int page = 1}) async {
    final resp = await _dio.get('/api/search', queryParameters: {
      'q': query,
      'token': token,
      'page': page,
    });
    final data = resp.data;
    final players = (data['players'] as List?) ?? [];
    return players.map((p) => RankedPlayer.fromJson(p)).toList();
  }

  Future<PlayerProfile> playerDetail(String playerId, String token) async {
    final resp = await _dio.get('/api/player/$playerId', queryParameters: {
      'token': token,
    });
    return PlayerProfile.fromJson(resp.data);
  }
}
