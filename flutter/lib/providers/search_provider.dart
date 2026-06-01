import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/ranked_player.dart';
import '../models/player_profile.dart';
import '../services/api_service.dart';
import 'auth_provider.dart';

class SearchState {
  final List<RankedPlayer> results;
  final bool isLoading;
  final String? error;
  final PlayerProfile? selectedPlayer;
  final bool isLoadingDetail;

  SearchState({
    this.results = const [],
    this.isLoading = false,
    this.error,
    this.selectedPlayer,
    this.isLoadingDetail = false,
  });
}

class SearchNotifier extends StateNotifier<SearchState> {
  final Ref _ref;
  final ApiService _api = ApiService();

  SearchNotifier(this._ref) : super(SearchState());

  Future<void> search(String query) async {
    if (query.trim().isEmpty) return;
    final auth = _ref.read(authProvider);
    if (!auth.isLoggedIn) return;

    state = SearchState(isLoading: true);
    try {
      final results = await _api.search(query, auth.session!.token);
      state = SearchState(results: results);
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        final refreshed = await _ref.read(authProvider.notifier).refreshSession();
        if (refreshed) {
          return search(query);
        }
      }
      state = SearchState(error: 'Search failed');
    } catch (_) {
      state = SearchState(error: 'Search failed');
    }
  }

  Future<void> loadPlayerDetail(String playerId) async {
    final auth = _ref.read(authProvider);
    if (!auth.isLoggedIn) return;

    state = SearchState(
      results: state.results,
      isLoadingDetail: true,
    );
    try {
      final profile = await _api.playerDetail(playerId, auth.session!.token);
      state = SearchState(
        results: state.results,
        selectedPlayer: profile,
      );
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        final refreshed = await _ref.read(authProvider.notifier).refreshSession();
        if (refreshed) {
          return loadPlayerDetail(playerId);
        }
      }
      state = SearchState(results: state.results, error: 'Failed to load player');
    } catch (_) {
      state = SearchState(results: state.results, error: 'Failed to load player');
    }
  }

  void clearDetail() {
    state = SearchState(results: state.results);
  }
}

final searchProvider = StateNotifierProvider<SearchNotifier, SearchState>((ref) {
  return SearchNotifier(ref);
});
