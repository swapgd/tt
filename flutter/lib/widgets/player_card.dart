import 'package:flutter/material.dart';
import '../models/player_profile.dart';

class PlayerCard extends StatelessWidget {
  final PlayerProfile profile;

  const PlayerCard({super.key, required this.profile});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF16213E),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            profile.playerName,
            style: const TextStyle(
              color: Color(0xFF00D4FF),
              fontSize: 18,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Member# ${profile.memberId}',
            style: const TextStyle(color: Color(0xFFEEEEEE), fontSize: 14),
          ),
          const SizedBox(height: 16),
          Text(
            '${profile.highestRating}',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 48,
              fontWeight: FontWeight.w700,
            ),
          ),
          const Text(
            'Tournament Rating',
            style: TextStyle(color: Color(0xFF888888), fontSize: 13),
          ),
          const SizedBox(height: 12),
          Text(
            '${profile.highestLeagueRating}',
            style: const TextStyle(
              color: Color(0xFFAAAAAA),
              fontSize: 28,
              fontWeight: FontWeight.w600,
            ),
          ),
          const Text(
            'League Rating',
            style: TextStyle(color: Color(0xFF888888), fontSize: 13),
          ),
          const SizedBox(height: 12),
          Text(
            '${profile.totalTournaments} tournaments  •  ${profile.totalMatches} matches  •  ${profile.totalWins}W-${profile.totalLosses}L (${profile.winPercentage.toStringAsFixed(0)}%)',
            style: const TextStyle(color: Color(0xFF888888), fontSize: 13),
          ),
        ],
      ),
    );
  }
}
