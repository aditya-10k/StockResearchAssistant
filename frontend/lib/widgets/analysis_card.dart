import 'package:flutter/material.dart';
import 'app_theme.dart';

class AnalysisCard extends StatelessWidget {
  final Map<String, dynamic> analysis;
  final String? verificationResult;
  const AnalysisCard({super.key, required this.analysis, this.verificationResult});

  @override
  Widget build(BuildContext context) {
    final directAnswer = analysis['direct_answer']?.toString();
    final summary = analysis['summary']?.toString();
    final thesis = analysis['investment_thesis']?.toString();
    final valuation = analysis['valuation']?.toString();
    final conclusion = analysis['conclusion']?.toString();
    final strengths = analysis['strengths'] is List ? List<dynamic>.from(analysis['strengths']) : [];
    final risks = analysis['risks'] is List ? List<dynamic>.from(analysis['risks']) : [];

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.card,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(width: 7, height: 7, decoration: const BoxDecoration(color: AppColors.cyan, shape: BoxShape.circle)),
              const SizedBox(width: 8),
              const Text(
                'AI RESEARCH SYNTHESIS & VERDICT',
                style: TextStyle(fontSize: 10, color: AppColors.cyan, letterSpacing: 1.5, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 12),

          if (directAnswer != null && directAnswer.isNotEmpty) ...[
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.surface,
                border: Border.all(color: AppColors.border),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('DIRECT VERDICT', style: TextStyle(fontSize: 8, color: AppColors.textMuted, letterSpacing: 1.0, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text(
                    directAnswer,
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.textPrimary, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),
          ],

          if (summary != null && summary.isNotEmpty) ...[
            _sectionBlock('EXECUTIVE SUMMARY', summary, AppColors.textSecondary),
            const SizedBox(height: 10),
          ],

          if (thesis != null && thesis.isNotEmpty) ...[
            _sectionBlock('INVESTMENT THESIS', thesis, AppColors.textSecondary),
            const SizedBox(height: 10),
          ],

          if (strengths.isNotEmpty || risks.isNotEmpty) ...[
            LayoutBuilder(
              builder: (context, constraints) {
                final isWide = constraints.maxWidth > 550;
                final strengthsWidget = strengths.isNotEmpty
                    ? _bulletBlock('KEY STRENGTHS', strengths, AppColors.green)
                    : const SizedBox.shrink();
                final risksWidget = risks.isNotEmpty
                    ? _bulletBlock('KEY RISKS', risks, AppColors.red)
                    : const SizedBox.shrink();

                if (isWide && strengths.isNotEmpty && risks.isNotEmpty) {
                  return Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(child: strengthsWidget),
                      const SizedBox(width: 10),
                      Expanded(child: risksWidget),
                    ],
                  );
                }
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (strengths.isNotEmpty) strengthsWidget,
                    if (strengths.isNotEmpty && risks.isNotEmpty) const SizedBox(height: 8),
                    if (risks.isNotEmpty) risksWidget,
                  ],
                );
              },
            ),
            const SizedBox(height: 10),
          ],

          if (valuation != null && valuation.isNotEmpty) ...[
            _sectionBlock('VALUATION OUTLOOK', valuation, AppColors.amber),
            const SizedBox(height: 10),
          ],

          if (conclusion != null && conclusion.isNotEmpty) ...[
            _sectionBlock('CONCLUSION', conclusion, AppColors.textPrimary),
            const SizedBox(height: 10),
          ],

          if (verificationResult != null && verificationResult!.isNotEmpty) ...[
            const Divider(color: AppColors.border, height: 16),
            Row(
              children: [
                Container(width: 6, height: 6, decoration: const BoxDecoration(color: AppColors.green, shape: BoxShape.circle)),
                const SizedBox(width: 6),
                const Text('SOURCE GROUNDED & VERIFIED', style: TextStyle(fontSize: 8, color: AppColors.green, letterSpacing: 1.0, fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 4),
            Text(verificationResult!, style: const TextStyle(fontSize: 11, color: AppColors.textSecondary, height: 1.4)),
          ],
        ],
      ),
    );
  }

  Widget _sectionBlock(String label, String text, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontSize: 8, color: AppColors.textMuted, letterSpacing: 1.0, fontWeight: FontWeight.bold)),
        const SizedBox(height: 3),
        Text(text, style: TextStyle(fontSize: 13, color: color, height: 1.45)),
      ],
    );
  }

  Widget _bulletBlock(String label, List<dynamic> items, Color color) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: color.withOpacity(0.04),
        border: Border.all(color: color.withOpacity(0.2)),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: TextStyle(fontSize: 8, color: color, letterSpacing: 1.0, fontWeight: FontWeight.bold)),
          const SizedBox(height: 6),
          ...items.map((item) => Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  margin: const EdgeInsets.only(top: 5),
                  width: 4,
                  height: 4,
                  decoration: BoxDecoration(color: color, shape: BoxShape.circle),
                ),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(item.toString(), style: TextStyle(fontSize: 12, color: color, height: 1.35)),
                ),
              ],
            ),
          )),
        ],
      ),
    );
  }
}
