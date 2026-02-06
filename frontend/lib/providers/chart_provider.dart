import 'package:flutter/material.dart';
import '../services/api_service.dart'; // <--- This line is what was failing
import '../models/natal_chart.dart';

class ChartProvider extends ChangeNotifier {
  final ApiService _api = ApiService();
  
  NatalChart? _chart;
  Map<String, dynamic>? _rawChartJson; 
  
  bool _loading = false;
  String? _error;

  // AI Specific State
  bool _aiLoading = false;
  String? _aiResponse;

  NatalChart? get chart => _chart;
  bool get loading => _loading;
  String? get error => _error;
  
  bool get aiLoading => _aiLoading;
  String? get aiResponse => _aiResponse;

  Future<void> generateChart(DateTime dt, double lat, double lon) async {
    _loading = true;
    _error = null;
    _aiResponse = null; 
    notifyListeners();

    try {
      final data = await _api.fetchChart(dt: dt, lat: lat, lon: lon);
      _rawChartJson = data; 
      _chart = NatalChart.fromJson(data);
    } catch (e) {
      _error = e.toString();
      debugPrint("Provider Error: $e");
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  Future<void> askAI(String question) async {
    if (_rawChartJson == null) return;

    _aiLoading = true;
    notifyListeners();

    try {
      final response = await _api.getAIInterpretation(
        chartData: _rawChartJson!,
        question: question,
      );
      _aiResponse = response['answer'];
    } catch (e) {
      _aiResponse = "Error: $e";
    } finally {
      _aiLoading = false;
      notifyListeners();
    }
  }
}