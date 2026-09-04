import 'package:flutter/material.dart';
import 'app_theme.dart';

class NewsCard extends StatelessWidget {
  final Map<String, dynamic>? newsData;
  const NewsCard({super.key, required this.newsData});

  @override
  Widget build(BuildContext context) {
    if (newsData == null || newsData!.isEmpty) return const SizedBox.shrink();

    List<Map<String, dynamic>> allNews = [];
    for (var entry in newsData!.entries) {
      final newsList = entry.value;
      if (newsList is List) {
        for (var item in newsList.take(3)) {
          if (item is Map) allNews.add(Map<String, dynamic>.from(item));
        }
      }
    }

    if (allNews.isEmpty) return const SizedBox.shrink();

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
          const Text('RECENT NEWS', style: TextStyle(fontSize: 10, color: AppColors.textSecondary, letterSpacing: 1.2)),
          const SizedBox(height: 12),
          ...allNews.take(6).map((item) {
            final content = item['content'] is Map ? Map<String, dynamic>.from(item['content']) : <String, dynamic>{};
            final title = content['title'] ?? content['headline'] ?? item['title'] ?? item['headline'] ?? 'Market Update';
            final provider = content['provider'] is Map ? content['provider'] : null;
            final source = (provider != null ? provider['displayName'] : null) ?? item['publisher'] ?? item['source'] ?? '';
            return Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    margin: const EdgeInsets.only(top: 5),
                    width: 3,
                    height: 3,
                    decoration: const BoxDecoration(color: AppColors.cyan, shape: BoxShape.circle),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(title.toString(), style: const TextStyle(fontSize: 12, color: AppColors.textPrimary, height: 1.4), maxLines: 2, overflow: TextOverflow.ellipsis),
                        if (source.toString().isNotEmpty)
                          Text(source.toString(), style: const TextStyle(fontSize: 10, color: AppColors.textSecondary)),
                      ],
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}
