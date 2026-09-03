import 'package:flutter/material.dart';
import 'app_theme.dart';

class ProgressStatusBar extends StatelessWidget {
  final String? currentStatus;
  final String? activeStep;
  const ProgressStatusBar({super.key, this.currentStatus, this.activeStep});

  static const _steps = ['guardrail', 'planner', 'executor', 'analysis', 'verification'];
  static const _labels = ['Guardrail', 'Planner', 'Market Data', 'AI Verdict', 'Verify'];

  int _getStepIndex() {
    if (activeStep != null && activeStep!.isNotEmpty) {
      final idx = _steps.indexOf(activeStep!.toLowerCase());
      if (idx != -1) return idx;
    }
    if (currentStatus == null) return 0;
    final s = currentStatus!.toLowerCase();
    for (int i = _steps.length - 1; i >= 0; i--) {
      if (s.contains(_steps[i])) return i;
    }
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    final curIdx = _getStepIndex();

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      decoration: BoxDecoration(
        color: AppColors.card,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              const SizedBox(
                width: 12,
                height: 12,
                child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.cyan),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  currentStatus ?? 'Processing query...',
                  style: const TextStyle(fontSize: 12, color: AppColors.textPrimary, fontFamily: 'monospace'),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: List.generate(_steps.length, (i) {
                final isDone = i < curIdx;
                final isActive = i == curIdx;
                final nodeColor = isDone ? AppColors.green : isActive ? AppColors.cyan : AppColors.textMuted;
                final icon = isDone ? Icons.check_circle_outline : isActive ? Icons.radio_button_checked : Icons.radio_button_unchecked;

                return Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: isActive ? AppColors.cyan.withOpacity(0.1) : isDone ? AppColors.green.withOpacity(0.08) : Colors.transparent,
                        borderRadius: BorderRadius.circular(3),
                        border: Border.all(color: isActive ? AppColors.cyan.withOpacity(0.4) : isDone ? AppColors.green.withOpacity(0.3) : AppColors.border, width: 0.8),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(icon, size: 11, color: nodeColor),
                          const SizedBox(width: 5),
                          Text(
                            _labels[i],
                            style: TextStyle(fontSize: 10, color: nodeColor, fontWeight: isActive ? FontWeight.bold : FontWeight.normal),
                          ),
                        ],
                      ),
                    ),
                    if (i < _steps.length - 1)
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 4),
                        child: Text('>', style: TextStyle(fontSize: 10, color: isDone ? AppColors.green : AppColors.textMuted)),
                      ),
                  ],
                );
              }),
            ),
          ),
        ],
      ),
    );
  }
}
