import 'package:flutter/material.dart';
import '../models/research_result.dart';
import '../widgets/stock_header_card.dart';
import '../widgets/analysis_card.dart';
import '../widgets/news_card.dart';
import '../widgets/earnings_chart.dart';
import '../widgets/app_theme.dart';

class ResearchResultView extends StatelessWidget {
  final ResearchResult result;
  final VoidCallback? onShare;
  const ResearchResultView({super.key, required this.result, this.onShare});

  @override
  Widget build(BuildContext context) {
    if (result.blockedMessage != null) {
      return _statusCard(result.blockedMessage!, AppColors.amber, 'REQUEST BLOCKED BY GUARDRAIL');
    }
    if (result.errorMessage != null) {
      return _statusCard(result.errorMessage!, AppColors.red, 'EXECUTION ERROR');
    }

    final stocks = result.marketData;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // 1. Comparative Stock Fundamentals (Side-by-Side when >= 2 stocks) - ABOVE VERDICT
        if (stocks.isNotEmpty) ...[
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
            child: Row(
              children: [
                const Icon(Icons.show_chart, size: 14, color: AppColors.cyan),
                const SizedBox(width: 6),
                Text(
                  stocks.length > 1 ? 'COMPARATIVE STOCK DATA' : 'MARKET OVERVIEW',
                  style: const TextStyle(fontSize: 10, color: AppColors.textSecondary, letterSpacing: 1.5, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),

          LayoutBuilder(
            builder: (context, constraints) {
              final isDesktop = constraints.maxWidth > 700;

              // If multiple stocks and enough screen width, render SIDE BY SIDE!
              if (stocks.length >= 2 && isDesktop) {
                return Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: stocks.map((stock) => Expanded(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 4),
                      child: StockHeaderCard(company: stock),
                    ),
                  )).toList(),
                );
              }

              // Otherwise stack vertically
              return Column(
                children: stocks.map((stock) => Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: StockHeaderCard(company: stock),
                )).toList(),
              );
            },
          ),
          const SizedBox(height: 14),
        ],

        // 2. Quarterly Earnings Chart (if present)
        if (result.earningsData != null && result.earningsData!.isNotEmpty) ...[
          EarningsBarChart(earningsData: result.earningsData),
          const SizedBox(height: 12),
        ],

        // 3. Recent News Headlines (if present)
        if (result.newsData != null && result.newsData!.isNotEmpty) ...[
          NewsCard(newsData: result.newsData),
          const SizedBox(height: 12),
        ],

        // 4. AI Analysis & Final Verdict (Rendered at the ABSOLUTE END)
        if (result.analysis != null) ...[
          AnalysisCard(
            analysis: result.analysis!,
            verificationResult: result.verificationResult,
          ),
          const SizedBox(height: 12),
          if (onShare != null) ...[
            Center(
              child: OutlinedButton.icon(
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: AppColors.cyan, width: 0.8),
                  backgroundColor: AppColors.surface,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
                ),
                onPressed: onShare,
                icon: const Icon(Icons.share_outlined, size: 14, color: AppColors.cyan),
                label: const Text(
                  'SHARE THIS REPORT',
                  style: TextStyle(fontSize: 10, color: AppColors.cyan, letterSpacing: 1.2, fontFamily: 'monospace', fontWeight: FontWeight.bold),
                ),
              ),
            ),
            const SizedBox(height: 12),
          ],
        ] else if (stocks.isNotEmpty) ...[
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            decoration: BoxDecoration(
              color: AppColors.card,
              border: Border.all(color: AppColors.border),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Row(
              children: [
                const SizedBox(
                  width: 12,
                  height: 12,
                  child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.cyan),
                ),
                const SizedBox(width: 10),
                const Text(
                  'Synthesizing AI research synthesis & verdict...',
                  style: TextStyle(fontSize: 12, color: AppColors.cyan, fontFamily: 'monospace'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
        ],
      ],
    );
  }

  Widget _statusCard(String message, Color color, String label) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.06),
        border: Border.all(color: color.withOpacity(0.4)),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: TextStyle(fontSize: 9, color: color, letterSpacing: 1.5, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text(message, style: const TextStyle(fontSize: 13, color: AppColors.textPrimary, height: 1.5)),
        ],
      ),
    );
  }
}
