class ResearchResult {
  final List<Map<String, dynamic>> marketData;
  final Map<String, dynamic>? newsData;
  final Map<String, dynamic>? financialsData;
  final Map<String, dynamic>? recommendationsData;
  final Map<String, dynamic>? earningsData;
  final Map<String, dynamic>? analysis;
  final String? verificationResult;
  final String? blockedMessage;
  final String? errorMessage;

  ResearchResult({
    this.marketData = const [],
    this.newsData,
    this.financialsData,
    this.recommendationsData,
    this.earningsData,
    this.analysis,
    this.verificationResult,
    this.blockedMessage,
    this.errorMessage,
  });

  ResearchResult copyWith({
    List<Map<String, dynamic>>? marketData,
    Map<String, dynamic>? newsData,
    Map<String, dynamic>? financialsData,
    Map<String, dynamic>? recommendationsData,
    Map<String, dynamic>? earningsData,
    Map<String, dynamic>? analysis,
    String? verificationResult,
    String? blockedMessage,
    String? errorMessage,
  }) {
    return ResearchResult(
      marketData: marketData ?? this.marketData,
      newsData: newsData ?? this.newsData,
      financialsData: financialsData ?? this.financialsData,
      recommendationsData: recommendationsData ?? this.recommendationsData,
      earningsData: earningsData ?? this.earningsData,
      analysis: analysis ?? this.analysis,
      verificationResult: verificationResult ?? this.verificationResult,
      blockedMessage: blockedMessage ?? this.blockedMessage,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}
