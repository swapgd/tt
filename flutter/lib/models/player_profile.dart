class PlayerProfile {
  final String playerId;
  final String playerName;
  final String memberId;
  final int highestRating;
  final int highestLeagueRating;
  final int totalTournaments;
  final int totalMatches;
  final int totalWins;
  final int totalLosses;
  final double winPercentage;

  PlayerProfile({
    required this.playerId,
    required this.playerName,
    required this.memberId,
    required this.highestRating,
    required this.highestLeagueRating,
    required this.totalTournaments,
    required this.totalMatches,
    required this.totalWins,
    required this.totalLosses,
    required this.winPercentage,
  });

  factory PlayerProfile.fromJson(Map<String, dynamic> json) {
    return PlayerProfile(
      playerId: json['playerId']?.toString() ?? '',
      playerName: json['playerName']?.toString() ?? '',
      memberId: json['memberId']?.toString() ?? '',
      highestRating: (json['highestRating'] ?? 0) as int,
      highestLeagueRating: (json['highestLeagueRating'] ?? 0) as int,
      totalTournaments: (json['totalTournaments'] ?? 0) as int,
      totalMatches: (json['totalMatches'] ?? 0) as int,
      totalWins: (json['totalWins'] ?? 0) as int,
      totalLosses: (json['totalLosses'] ?? 0) as int,
      winPercentage: (json['winPercentage'] ?? 0.0).toDouble(),
    );
  }
}
