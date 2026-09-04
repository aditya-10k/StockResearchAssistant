import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'app_theme.dart';

class NewsCard extends StatelessWidget {
  final Map<String, dynamic>? newsData;
  const NewsCard({super.key, required this.newsData});

  Future<void> _openArticle(String? urlString) async {
    if (urlString == null || urlString.isEmpty) return;
    try {
      final uri = Uri.tryParse(urlString);
      if (uri != null) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      }
    } catch (_) {}
  }

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
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: const [
              Text('RECENT NEWS', style: TextStyle(fontSize: 10, color: AppColors.textSecondary, letterSpacing: 1.2)),
              Text('TAP HEADLINE TO READ', style: TextStyle(fontSize: 8, color: AppColors.cyan, letterSpacing: 0.8, fontFamily: 'monospace')),
            ],
          ),
          const SizedBox(height: 12),
          ...allNews.take(6).map((item) {
            final content = item['content'] is Map ? Map<String, dynamic>.from(item['content']) : <String, dynamic>{};
            final title = content['title'] ?? content['headline'] ?? item['title'] ?? item['headline'] ?? 'Market Update';
            final provider = content['provider'] is Map ? content['provider'] : null;
            final source = (provider != null ? provider['displayName'] : null) ?? item['publisher'] ?? item['source'] ?? '';
            final url = (content['canonicalUrl'] is Map ? content['canonicalUrl']['url'] : null) ??
                (content['clickThroughUrl'] is Map ? content['clickThroughUrl']['url'] : null) ??
                item['link'] ??
                item['url'];

            final hasUrl = url != null && url.toString().isNotEmpty;

            return Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: MouseRegion(
                cursor: hasUrl ? SystemMouseCursors.click : SystemMouseCursors.basic,
                child: InkWell(
                  onTap: hasUrl ? () => _openArticle(url.toString()) : null,
                  borderRadius: BorderRadius.circular(4),
                  hoverColor: AppColors.surface,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 2),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          margin: const EdgeInsets.only(top: 6),
                          width: 4,
                          height: 4,
                          decoration: const BoxDecoration(color: AppColors.cyan, shape: BoxShape.circle),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Expanded(
                                    child: Text(
                                      title.toString(),
                                      style: const TextStyle(
                                        fontSize: 12,
                                        color: AppColors.textPrimary,
                                        height: 1.4,
                                        fontWeight: FontWeight.w500,
                                      ),
                                      maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                  if (hasUrl) ...[
                                    const SizedBox(width: 6),
                                    const Icon(Icons.open_in_new, size: 12, color: AppColors.cyan),
                                  ],
                                ],
                              ),
                              if (source.toString().isNotEmpty) ...[
                                const SizedBox(height: 2),
                                Text(
                                  source.toString(),
                                  style: const TextStyle(fontSize: 10, color: AppColors.textSecondary),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            );
          }),
        ],
      ),
    );
  }
}
