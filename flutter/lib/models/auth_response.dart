class AuthResponse {
  final String token;
  final String playerId;
  final String name;
  final int userId;

  AuthResponse({
    required this.token,
    required this.playerId,
    required this.name,
    required this.userId,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      token: json['token'] as String,
      playerId: json['playerId'] as String,
      name: json['name'] as String,
      userId: json['userId'] as int,
    );
  }

  Map<String, dynamic> toJson() => {
    'token': token,
    'playerId': playerId,
    'name': name,
    'userId': userId,
  };
}
