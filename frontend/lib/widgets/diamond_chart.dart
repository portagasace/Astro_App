import 'package:flutter/material.dart';

class DiamondChart extends StatelessWidget {
  final Map<String, dynamic> layoutData;
  final List<dynamic> cells; 

  const DiamondChart({super.key, required this.layoutData, required this.cells});

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: CustomPaint(
        painter: _ChartPainter(layoutData: layoutData, cells: cells),
      ),
    );
  }
}

class _ChartPainter extends CustomPainter {
  final Map<String, dynamic> layoutData;
  final List<dynamic> cells;

  _ChartPainter({required this.layoutData, required this.cells});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final w = size.width;
    final h = size.height;

    // 1. Draw the Diamond Frame
    canvas.drawRect(Rect.fromLTWH(0, 0, w, h), paint); // Box
    canvas.drawLine(Offset(0, 0), Offset(w, h), paint); // Cross
    canvas.drawLine(Offset(w, 0), Offset(0, h), paint); // Cross
    
    Path path = Path();
    path.moveTo(w / 2, 0);
    path.lineTo(0, h / 2);
    path.lineTo(w / 2, h);
    path.lineTo(w, h / 2);
    path.close();
    canvas.drawPath(path, paint);

    // 2. Draw Planets & Signs
    final textPainter = TextPainter(textDirection: TextDirection.ltr, textAlign: TextAlign.center);
    final housesConfig = layoutData['houses']; 

    // Sign Number Mapping
    final signMap = {"Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4, 
                     "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8, 
                     "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12};

    for (var cell in cells) {
      int houseNum = cell['house'];
      String houseKey = houseNum.toString();
      
      if (housesConfig != null && housesConfig.containsKey(houseKey)) {
        // Normalize coordinates (0-100 to screen pixels)
        double nx = (housesConfig[houseKey]['x'] as num).toDouble() / 100.0;
        double ny = (housesConfig[houseKey]['y'] as num).toDouble() / 100.0;
        
        Offset center = Offset(nx * w, ny * h);
        
        int signNum = signMap[cell['sign']] ?? 0;
        List planets = cell['planets'] ?? [];

        // Draw Sign Number (Gray)
        _drawText(canvas, "$signNum", center + const Offset(0, -15), 
            const TextStyle(color: Colors.grey, fontSize: 12), textPainter);

        // Draw Planets (Red)
        if (planets.isNotEmpty) {
           _drawText(canvas, planets.join("\n"), center + const Offset(0, 5), 
               const TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 10), textPainter);
        }
      }
    }
  }

  void _drawText(Canvas c, String text, Offset pos, TextStyle style, TextPainter tp) {
    tp.text = TextSpan(text: text, style: style);
    tp.layout();
    tp.paint(c, Offset(pos.dx - tp.width / 2, pos.dy - tp.height / 2));
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}