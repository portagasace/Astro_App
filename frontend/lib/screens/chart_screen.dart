import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/chart_provider.dart';
import '../widgets/diamond_chart.dart';

class ChartScreen extends StatelessWidget {
  const ChartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final chartData = Provider.of<ChartProvider>(context).chart;

    if (chartData == null) return const Scaffold(body: Center(child: Text("No Data")));

    // Python sends views["rashi"]["cells"]
    final rashiCells = chartData.views["rashi"]["cells"] as List;

    return Scaffold(
      appBar: AppBar(title: Text("Lagna Chart (${chartData.ascSign})")),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: DiamondChart(
            layoutData: chartData.layout,
            cells: rashiCells,
          ),
        ),
      ),
    );
  }
}