class RankedPlayer {
  final String playerId;
  final String playerName;
  final String memberId;
  final String prefixedRank;
  final int finalRating;
  final String? address;
  final String? clubName;
  final int totalWins;
  final int totalLost;

  RankedPlayer({
    required this.playerId,
    required this.playerName,
    required this.memberId,
    required this.prefixedRank,
    required this.finalRating,
    this.address,
    this.clubName,
    required this.totalWins,
    required this.totalLost,
  });

  factory RankedPlayer.fromJson(Map<String, dynamic> json) {
    return RankedPlayer(
      playerId: json['playerId']?.toString() ?? '',
      playerName: json['playerName']?.toString() ?? '',
      memberId: json['memberId']?.toString() ?? '',
      prefixedRank: json['prefixedRank']?.toString() ?? '',
      finalRating: (json['finalRating'] ?? 0) as int,
      address: json['address'] as String?,
      clubName: json['clubName'] as String?,
      totalWins: (json['totalWins'] ?? 0) as int,
      totalLost: (json['totalLost'] ?? 0) as int,
    );
  }
}
