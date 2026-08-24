import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class ApiService {
  final String baseUrl = AppConfig.backendUrl;

  Stream<String> queryStream(String query) async* {
    final request = http.Request('POST', Uri.parse('${baseUrl}/query/stream'));
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
