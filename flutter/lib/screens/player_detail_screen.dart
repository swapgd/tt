import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/search_provider.dart';
import '../widgets/player_card.dart';

class PlayerDetailScreen extends ConsumerStatefulWidget {
  final String playerId;

  const PlayerDetailScreen({super.key, required this.playerId});

  @override
  ConsumerState<PlayerDetailScreen> createState() => _PlayerDetailScreenState();
}

class _PlayerDetailScreenState extends ConsumerState<PlayerDetailScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(
      () => ref.read(searchProvider.notifier).loadPlayerDetail(widget.playerId),
    );
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final search = ref.watch(searchProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF1A1A2E),
      appBar: AppBar(
        title: const Text('Player Detail'),
        backgroundColor: const Color(0xFF1A1A2E),
        foregroundColor: const Color(0xFF00D4FF),
        elevation: 0,
      ),
      body: _buildBody(search),
    );
  }

  Widget _buildBody(SearchState search) {
    if (search.isLoadingDetail) {
      return const Center(
        child: CircularProgressIndicator(color: Color(0xFF00D4FF)),
      );
    }
    if (search.error != null) {
      return Center(
        child: Text(search.error!, style: const TextStyle(color: Color(0xFFFF6B6B))),
      );
    }
    if (search.selectedPlayer != null) {
      return ListView(
        padding: const EdgeInsets.all(16),
        children: [PlayerCard(profile: search.selectedPlayer!)],
      );
    }
    return const SizedBox.shrink();
  }
}
