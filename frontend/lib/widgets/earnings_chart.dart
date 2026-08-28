import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'app_theme.dart';

class EarningsBarChart extends StatelessWidget {
  final Map<String, dynamic>? earningsData;
  const EarningsBarChart({super.key, required this.earningsData});

  @override
  Widget build(BuildContext context) {
    if (earningsData == null || earningsData!.isEmpty) return const SizedBox.shrink();

    List<Widget> charts = [];
    for (var entry in earningsData!.entries) {
      final ticker = entry.key;
      final data = entry.value;
      if (data is Map && data['quarterly_earnings'] != null) {
        final chart = _buildChart(ticker, data['quarterly_earnings']);
        if (chart != null) charts.add(chart);
      }
    }

    if (charts.isEmpty) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.card,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('QUARTERLY EARNINGS', style: TextStyle(fontSize: 10, color: AppColors.textSecondary, letterSpacing: 1.2)),
          const SizedBox(height: 12),
          ...charts,
        ],
      ),
    );
  }

  Widget? _buildChart(String ticker, dynamic rawData) {
    if (rawData is! Map) return null;
    final epsActual = rawData['epsActual'];
    if (epsActual is! Map || epsActual.isEmpty) return null;

    final entries = epsActual.entries.toList();
    entries.sort((a, b) => a.key.compareTo(b.key));
    final recent = entries.take(8).toList();
    if (recent.isEmpty) return null;

    final bars = recent.asMap().entries.map((e) {
      final val = e.value.value;
      final v = val != null ? (val as num).toDouble() : 0.0;
      return BarChartGroupData(
        x: e.key,
        barRods: [
          BarChartRodData(
            toY: v,
            color: v >= 0 ? AppColors.green : AppColors.red,
            width: 14,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(2)),
          ),
        ],
      );
    }).toList();

    final allVals = recent.map((e) => e.value.value != null ? (e.value.value as num).toDouble() : 0.0).toList();
    final maxY = allVals.reduce((a, b) => a > b ? a : b) * 1.3;
    final minY = allVals.reduce((a, b) => a < b ? a : b) * 1.3;

    final labels = recent.map((e) {
      final k = e.key.toString();
      return k.length >= 10 ? k.substring(5, 10) : k;
    }).toList();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(ticker, style: const TextStyle(fontSize: 11, color: AppColors.textSecondary, letterSpacing: 0.8)),
        const SizedBox(height: 8),
        SizedBox(
          height: 120,
          child: BarChart(
            BarChartData(
              maxY: maxY > 0 ? maxY : 5,
              minY: minY < 0 ? minY : 0,
              gridData: FlGridData(
                show: true,
                horizontalInterval: (maxY - minY).abs() / 4,
                getDrawingHorizontalLine: (v) => FlLine(color: AppColors.border, strokeWidth: 0.5),
                drawVerticalLine: false,
              ),
              borderData: FlBorderData(show: false),
              titlesData: FlTitlesData(
                leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    getTitlesWidget: (v, _) {
                      final idx = v.toInt();
                      if (idx < 0 || idx >= labels.length) return const SizedBox.shrink();
                      return Padding(
                        padding: const EdgeInsets.only(top: 4),
                        child: Text(labels[idx], style: const TextStyle(fontSize: 8, color: AppColors.textSecondary)),
                      );
                    },
                  ),
                ),
              ),
              barGroups: bars,
            ),
          ),
        ),
        const SizedBox(height: 16),
      ],
    );
  }
}
