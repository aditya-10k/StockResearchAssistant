import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class ApiService {
  static final String baseUrl = AppConfig.backendUrl;

  static Future<bool> checkHealth() async {
    try {
      final res = await http.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(const Duration(seconds: 40));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  static Future<List<Map<String, dynamic>>> getRecentChats() async {
    try {
      final res = await http.get(
        Uri.parse('$baseUrl/chats'),
      ).timeout(const Duration(seconds: 15));
      if (res.statusCode == 200) {
        final decoded = jsonDecode(res.body);
        if (decoded is List) {
          return List<Map<String, dynamic>>.from(
            decoded.map((x) => Map<String, dynamic>.from(x as Map))
          );
        }
      }
    } catch (_) {}
    return [];
  }

  static Future<Map<String, dynamic>?> getChatSession(String sessionId) async {
    try {
      final res = await http.get(
        Uri.parse('$baseUrl/chats/$sessionId'),
      ).timeout(const Duration(seconds: 20));
      if (res.statusCode == 200) {
        final decoded = jsonDecode(res.body);
        if (decoded is Map) {
          return Map<String, dynamic>.from(decoded);
        }
      }
    } catch (_) {}
    return null;
  }

  static Future<Map<String, dynamic>?> getSharedChat(String sessionId) async {
    try {
      final res = await http.get(
        Uri.parse('$baseUrl/chats/share/$sessionId'),
      ).timeout(const Duration(seconds: 20));
      if (res.statusCode == 200) {
        final decoded = jsonDecode(res.body);
        if (decoded is Map) {
          return Map<String, dynamic>.from(decoded);
        }
      }
    } catch (_) {}
    return null;
  }

  static Future<bool> deleteChatSession(String sessionId) async {
    try {
      final res = await http.delete(
        Uri.parse('$baseUrl/chats/$sessionId'),
      ).timeout(const Duration(seconds: 15));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  Stream<String> queryStream(String query) async* {
    final request = http.Request('POST', Uri.parse('$baseUrl/query/stream'));
    request.headers['Content-Type'] = 'application/json';
    request.body = jsonEncode({"query": query});

    final response = await http.Client().send(request);

    if (response.statusCode == 200) {
      await for (var chunk in response.stream.transform(utf8.decoder)) {
        final lines = chunk.split('\n');
        for (var line in lines) {
          if (line.startsWith('event: ')) {
            yield line.substring(7).trim(); // Yield the event name
          }
        }
      }
    } else {
      throw Exception('Failed to connect to stream');
    }
  }
}
