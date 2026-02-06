import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:flutter/foundation.dart'; // For kIsWeb

class ApiService {
  // Use 10.0.2.2 for Android Emulator, 127.0.0.1 for Web/iOS
  String get baseUrl {
    if (kIsWeb) return 'http://127.0.0.1:8000';
    if (Platform.isAndroid) return 'http://10.0.2.2:8000';
    return 'http://127.0.0.1:8000';
  }

  // 1. Fetch Natal Chart
  Future<Map<String, dynamic>> fetchChart({
    required DateTime dt,
    required double lat,
    required double lon,
  }) async {
    final url = Uri.parse('$baseUrl/api/natal-chart');
    
    final body = {
      "datetime_local": dt.toIso8601String(),
      "timezone": "Asia/Kolkata", 
      "location": {"lat": lat, "lon": lon},
      "node_type": "true",
      "bhava_house_system": "sripati"
    };

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Server Error: ${response.body}');
      }
    } catch (e) {
      throw Exception('Connection Failed. Is backend running? ($e)');
    }
  }

  // 2. Fetch AI Interpretation
  Future<Map<String, dynamic>> getAIInterpretation({
    required Map<String, dynamic> chartData, 
    required String question,
  }) async {
    final url = Uri.parse('$baseUrl/api/ai/interpret');
    
    final body = {
      "chart": chartData, 
      "question": question,
    };

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('AI Error: ${response.body}');
      }
    } catch (e) {
      throw Exception('Failed to connect to AI: $e');
    }
  }
}