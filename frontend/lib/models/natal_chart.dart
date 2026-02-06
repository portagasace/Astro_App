class NatalChart {
  final double ascendant;
  final String ascSign;
  final Map<String, dynamic> layout; // The coordinates from layout.py
  final Map<String, dynamic> views;  // The cell data for drawing

  NatalChart({
    required this.ascendant,
    required this.ascSign,
    required this.layout,
    required this.views,
  });

  factory NatalChart.fromJson(Map<String, dynamic> json) {
    return NatalChart(
      ascendant: json['ascendant'],
      ascSign: json['asc_rashi'],
      layout: json['layout'],
      views: json['views'],
    );
  }
}