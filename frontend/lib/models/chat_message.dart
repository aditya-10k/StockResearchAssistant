import '../models/research_result.dart';

class ChatMessage {
  final String id;
  final String text;
  final bool isUser;
  final String? status;
  final String? activeStep;
  final ResearchResult? result;
  final bool isStructured;
  final bool isStreaming;

  ChatMessage({
    required this.id,
    required this.text,
    required this.isUser,
    this.status,
    this.activeStep,
    this.result,
    this.isStructured = false,
    this.isStreaming = false,
  });

  ChatMessage copyWith({
    String? id,
    String? text,
    bool? isUser,
    String? status,
    String? activeStep,
    ResearchResult? result,
    bool? isStructured,
    bool? isStreaming,
  }) {
    return ChatMessage(
      id: id ?? this.id,
      text: text ?? this.text,
      isUser: isUser ?? this.isUser,
      status: status ?? this.status,
      activeStep: activeStep ?? this.activeStep,
      result: result ?? this.result,
      isStructured: isStructured ?? this.isStructured,
      isStreaming: isStreaming ?? this.isStreaming,
    );
  }
}
