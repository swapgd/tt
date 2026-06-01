import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/player_profile.dart';
import '../services/api_service.dart';
import 'auth_provider.dart';

class RatingState {
  final PlayerProfile? profile;
  final bool isLoading;
  final String? error;

  RatingState({this.profile, this.isLoading = false, this.error});
}

class RatingNotifier extends StateNotifier<RatingState> {
  final Ref _ref;
  final ApiService _api = ApiService();

  RatingNotifier(this._ref) : super(RatingState());

  Future<void> loadMyRating() async {
    final auth = _ref.read(authProvider);
    if (!auth.isLoggedIn) return;

    state = RatingState(isLoading: true);
    try {
      final profile = await _api.myRating(auth.session!.playerId, auth.session!.token);
      state = RatingState(profile: profile);
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        final refreshed = await _ref.read(authProvider.notifier).refreshSession();
        if (refreshed) {
          return loadMyRating();
        }
      }
      state = RatingState(error: 'Failed to load rating');
    } catch (_) {
      state = RatingState(error: 'Failed to load rating');
    }
  }
}

final ratingProvider = StateNotifierProvider<RatingNotifier, RatingState>((ref) {
  return RatingNotifier(ref);
});
