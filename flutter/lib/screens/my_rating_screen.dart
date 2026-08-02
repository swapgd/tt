import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';
import '../providers/rating_provider.dart';
import '../widgets/player_card.dart';

class MyRatingScreen extends ConsumerStatefulWidget {
  const MyRatingScreen({super.key});

  @override
  ConsumerState<MyRatingScreen> createState() => _MyRatingScreenState();
}

class _MyRatingScreenState extends ConsumerState<MyRatingScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(ratingProvider.notifier).loadMyRating());
  }

  @override
  Widget build(BuildContext context) {
    final rating = ref.watch(ratingProvider);
    final auth = ref.watch(authProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF1A1A2E),
      appBar: AppBar(
        title: const Text('🏓 Table Tennis Ratings'),
        centerTitle: true,
        backgroundColor: const Color(0xFF1A1A2E),
        foregroundColor: const Color(0xFF00D4FF),
        elevation: 0,
        actions: [
          TextButton(
            onPressed: () => ref.read(authProvider.notifier).logout(),
            child: const Text(
              'Logout',
              style: TextStyle(color: Color(0xFF666666), fontSize: 12),
            ),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => ref.read(ratingProvider.notifier).loadMyRating(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (auth.session != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Text(
                  'Hi, ${auth.session!.name}',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Color(0xFF888888), fontSize: 14),
                ),
              ),
            if (rating.isLoading)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(40),
                  child: CircularProgressIndicator(color: Color(0xFF00D4FF)),
                ),
              )
            else if (rating.error != null)
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(40),
                  child: Text(
                    rating.error!,
                    style: const TextStyle(color: Color(0xFFFF6B6B)),
                  ),
                ),
              )
            else if (rating.profile != null)
              PlayerCard(profile: rating.profile!),
          ],
        ),
      ),
    );
  }
}
