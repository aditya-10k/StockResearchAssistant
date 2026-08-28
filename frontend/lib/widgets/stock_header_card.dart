import 'package:flutter/material.dart';
import 'app_theme.dart';

class StockHeaderCard extends StatelessWidget {
  final Map<String, dynamic> company;
  const StockHeaderCard({super.key, required this.company});

  @override
  Widget build(BuildContext context) {
    final ticker = company['ticker']?.toString() ?? '';
    final name = company['company_name']?.toString() ?? company['short_name']?.toString() ?? '';
    final price = company['current_price'];
    final prev = company['previous_close'];
    final changeText = Formatters.change(price, prev);
    final isUp = changeText.startsWith('+');

    final priceVal = price != null ? (price as num).toDouble() : null;
    final low52 = company['fifty_two_week_low'] != null ? (company['fifty_two_week_low'] as num).toDouble() : null;
    final high52 = company['fifty_two_week_high'] != null ? (company['fifty_two_week_high'] as num).toDouble() : null;

    final rec = company['recommendation']?.toString().toUpperCase() ?? '';
    final targetMean = company['target_mean_price'] != null ? (company['target_mean_price'] as num).toDouble() : null;
    double? upside;
    if (targetMean != null && priceVal != null && priceVal > 0) {
      upside = ((targetMean - priceVal) / priceVal) * 100;
    }

    Color recColor = AppColors.textSecondary;
    if (rec.contains('BUY') || rec.contains('STRONG')) recColor = AppColors.green;
    if (rec.contains('SELL')) recColor = AppColors.red;
    if (rec.contains('HOLD') || rec.contains('NEUTRAL')) recColor = AppColors.amber;

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.card,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          ticker,
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textPrimary, fontFamily: 'monospace'),
                        ),
                        if (company['exchange'] != null) ...[
                          const SizedBox(width: 6),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                            decoration: BoxDecoration(color: AppColors.surface, border: Border.all(color: AppColors.border), borderRadius: BorderRadius.circular(2)),
                            child: Text(company['exchange'].toString(), style: const TextStyle(fontSize: 9, color: AppColors.textSecondary)),
                          ),
                        ],
                      ],
                    ),
                    const SizedBox(height: 2),
                    Text(
                      name,
                      style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    Formatters.price(price),
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textPrimary, fontFamily: 'monospace'),
                  ),
                  if (changeText.isNotEmpty) ...[
                    const SizedBox(height: 2),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: isUp ? AppColors.green.withOpacity(0.12) : AppColors.red.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(3),
                        border: Border.all(color: isUp ? AppColors.green : AppColors.red, width: 0.5),
                      ),
                      child: Text(
                        changeText,
                        style: TextStyle(fontSize: 10, color: isUp ? AppColors.green : AppColors.red, fontFamily: 'monospace', fontWeight: FontWeight.w600),
                      ),
                    ),
                  ],
                ],
              ),
            ],
          ),
          const SizedBox(height: 10),
          const Divider(color: AppColors.border, height: 1),
          const SizedBox(height: 8),

          Row(
            children: [
              _metricPill('MKT CAP', Formatters.cap(company['market_cap'])),
              const SizedBox(width: 4),
              _metricPill('P/E', Formatters.numVal(company['pe_ratio'])),
              const SizedBox(width: 4),
              _metricPill('FWD P/E', Formatters.numVal(company['forward_pe'])),
              const SizedBox(width: 4),
              _metricPill('EPS', Formatters.numVal(company['eps'])),
            ],
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              _metricPill('BETA', Formatters.numVal(company['beta'])),
              const SizedBox(width: 4),
              _metricPill('DIV YIELD', Formatters.percent(company['dividend_yield'])),
              const SizedBox(width: 4),
              _metricPill('EV/EBITDA', Formatters.numVal(company['enterprise_to_ebitda'])),
              const SizedBox(width: 4),
              _metricPill('P/B', Formatters.numVal(company['price_to_book'])),
            ],
          ),
          const SizedBox(height: 10),

          if (low52 != null && high52 != null && priceVal != null) ...[
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('52W RANGE', style: TextStyle(fontSize: 8, color: AppColors.textMuted, letterSpacing: 0.8, fontWeight: FontWeight.w600)),
                Text(
                  Formatters.price(priceVal),
                  style: const TextStyle(fontSize: 9, color: AppColors.cyan, fontFamily: 'monospace'),
                ),
              ],
            ),
            const SizedBox(height: 3),
            _rangeProgressBar(low52, high52, priceVal),
            const SizedBox(height: 2),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(Formatters.price(low52), style: const TextStyle(fontSize: 8, color: AppColors.red, fontFamily: 'monospace')),
                Text(Formatters.price(high52), style: const TextStyle(fontSize: 8, color: AppColors.green, fontFamily: 'monospace')),
              ],
            ),
            const SizedBox(height: 8),
          ],

          if (rec.isNotEmpty) ...[
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
              decoration: BoxDecoration(
                color: AppColors.surface,
                border: Border.all(color: AppColors.border),
                borderRadius: BorderRadius.circular(3),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: recColor.withOpacity(0.15),
                      border: Border.all(color: recColor, width: 0.6),
                      borderRadius: BorderRadius.circular(2),
                    ),
                    child: Text(rec, style: TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: recColor, letterSpacing: 0.5)),
                  ),
                  const SizedBox(width: 8),
                  if (targetMean != null)
                    Expanded(
                      child: Text(
                        'Target: ' + Formatters.price(targetMean),
                        style: const TextStyle(fontSize: 10, color: AppColors.textSecondary, fontFamily: 'monospace'),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  if (upside != null)
                    Text(
                      (upside >= 0 ? '+' : '') + upside.toStringAsFixed(1) + '%',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: upside >= 0 ? AppColors.green : AppColors.red,
                        fontFamily: 'monospace',
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 8),
          ],

          Row(
            children: [
              _finCell('GROSS MARGIN', Formatters.percent(company['gross_margin'])),
              const SizedBox(width: 4),
              _finCell('OP. MARGIN', Formatters.percent(company['operating_margin'])),
              const SizedBox(width: 4),
              _finCell('NET MARGIN', Formatters.percent(company['profit_margin'])),
            ],
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              _finCell('REV GROWTH', Formatters.percent(company['revenue_growth'])),
              const SizedBox(width: 4),
              _finCell('ROE', Formatters.percent(company['return_on_equity'])),
              const SizedBox(width: 4),
              _finCell('FREE CASH', Formatters.cash(company['free_cashflow'])),
            ],
          ),
        ],
      ),
    );
  }

  Widget _metricPill(String label, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
        decoration: BoxDecoration(
          color: AppColors.surface,
          border: Border.all(color: AppColors.border),
          borderRadius: BorderRadius.circular(3),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(fontSize: 7, color: AppColors.textMuted, letterSpacing: 0.5), maxLines: 1, overflow: TextOverflow.ellipsis),
            const SizedBox(height: 2),
            Text(value, style: const TextStyle(fontSize: 10, color: AppColors.textPrimary, fontFamily: 'monospace', fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }

  Widget _finCell(String label, String value) {
    final isNeg = value.startsWith('-');
    final isPos = !isNeg && value != 'N/A' && value.contains('%');
    final color = isNeg ? AppColors.red : isPos ? AppColors.green : AppColors.textPrimary;

    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
        decoration: BoxDecoration(
          color: AppColors.surface,
          border: Border.all(color: AppColors.border),
          borderRadius: BorderRadius.circular(3),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(fontSize: 7, color: AppColors.textMuted), maxLines: 1, overflow: TextOverflow.ellipsis),
            const SizedBox(height: 2),
            Text(value, style: TextStyle(fontSize: 10, color: color, fontFamily: 'monospace', fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }

  Widget _rangeProgressBar(double low, double high, double cur) {
    final pct = high == low ? 0.5 : ((cur - low) / (high - low)).clamp(0.0, 1.0);
    return Container(
      height: 4,
      width: double.infinity,
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(2),
      ),
      alignment: Alignment.centerLeft,
      child: LayoutBuilder(
        builder: (context, box) {
          final barWidth = (box.maxWidth * pct).clamp(0.0, box.maxWidth);
          return Container(
            width: barWidth,
            height: 4,
            decoration: BoxDecoration(
              color: AppColors.cyan,
              borderRadius: BorderRadius.circular(2),
            ),
          );
        },
      ),
    );
  }
}
