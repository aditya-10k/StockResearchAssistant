import 'dart:convert';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;
import '../models/chat_message.dart';
import '../models/research_result.dart';
import '../config.dart';

abstract class ChatEvent {}

class SendMessageEvent extends ChatEvent {
  final String query;
  SendMessageEvent(this.query);
}

class ChatState {
  final List<ChatMessage> messages;
  final bool isLoading;
  ChatState({required this.messages, this.isLoading = false});
}

class ChatBloc extends Bloc<ChatEvent, ChatState> {
  ChatBloc() : super(ChatState(messages: [])) {
    on<SendMessageEvent>(_onSend);
  }

  Future<void> _onSend(SendMessageEvent event, Emitter<ChatState> emit) async {
    final timestamp = DateTime.now().microsecondsSinceEpoch.toString();
    final userMsg = ChatMessage(
      id: 'user_' + timestamp,
      text: event.query,
      isUser: true,
    );
    final botId = 'bot_' + timestamp;
    final botMsg = ChatMessage(
      id: botId,
      text: '',
      isUser: false,
      status: 'Running guardrail & intent check...',
      activeStep: 'guardrail',
      isStreaming: true,
    );

    List<ChatMessage> msgs = [...state.messages, userMsg, botMsg];
    emit(ChatState(messages: msgs, isLoading: true));

    void emitProgress(ResearchResult result, String status, String step, {bool isStructured = false}) {
      msgs = msgs.map((m) => m.id == botId
          ? m.copyWith(
              status: status,
              activeStep: step,
              result: result,
              isStructured: isStructured,
              isStreaming: true,
            )
          : m).toList();
      emit(ChatState(messages: msgs, isLoading: true));
    }

    void finish(ResearchResult result) {
      msgs = msgs.map((m) => m.id == botId
          ? m.copyWith(
              status: '',
              activeStep: 'done',
              result: result,
              isStructured: true,
              isStreaming: false,
            )
          : m).toList();
      emit(ChatState(messages: msgs, isLoading: false));
    }

    final history = state.messages
        .where((m) => m.text.isNotEmpty)
        .map((m) => {'role': m.isUser ? 'user' : 'assistant', 'content': m.text})
        .toList();

    var accumulator = ResearchResult();

    try {
      final req = http.Request('POST', Uri.parse('${AppConfig.backendUrl}/query/stream'));
      req.headers['Content-Type'] = 'application/json';
      req.body = jsonEncode({'query': event.query, 'chat_history': history});

      final res = await http.Client().send(req);
      if (res.statusCode != 200) {
        accumulator = accumulator.copyWith(errorMessage: 'Server returned HTTP ' + res.statusCode.toString());
        finish(accumulator);
        return;
      }

      String currentEvent = '';
      final lineStream = res.stream.transform(utf8.decoder).transform(const LineSplitter());

      await for (final line in lineStream) {
        if (line.startsWith('event: ')) {
          currentEvent = line.substring(7).trim();
          if (currentEvent == 'guardrail') {
            emitProgress(accumulator, 'Running safety & domain checks...', 'guardrail');
          } else if (currentEvent == 'planner') {
            emitProgress(accumulator, 'Formulating execution research plan...', 'planner');
          } else if (currentEvent == 'executor') {
            emitProgress(accumulator, 'Fetching real-time market data & financials...', 'executor');
          } else if (currentEvent == 'analysis') {
            emitProgress(accumulator, 'Synthesizing equity research & verdict...', 'analysis', isStructured: accumulator.marketData.isNotEmpty);
          } else if (currentEvent == 'verification') {
            emitProgress(accumulator, 'Verifying claims against document evidence...', 'verification', isStructured: true);
          }
        } else if (line.startsWith('data: ')) {
          final raw = line.substring(6).trim();
          if (raw.isNotEmpty && raw != '{}') {
            try {
              final d = jsonDecode(raw);
              if (d is Map<String, dynamic>) {
                bool hasUpdate = false;

                // 1. Market Data & Fundamentals (Extract whenever available)
                if (d.containsKey('market_data') && d['market_data'] is List && (d['market_data'] as List).isNotEmpty) {
                  accumulator = accumulator.copyWith(
                    marketData: List<Map<String, dynamic>>.from(
                      (d['market_data'] as List).map((x) => Map<String, dynamic>.from(x as Map))
                    ),
                  );
                  hasUpdate = true;
                }

                // 2. News Data (Extract whenever available)
                if (d.containsKey('news_data') && d['news_data'] is Map && (d['news_data'] as Map).isNotEmpty) {
                  accumulator = accumulator.copyWith(
                    newsData: Map<String, dynamic>.from(d['news_data'] as Map),
                  );
                  hasUpdate = true;
                }

                // 3. Other services
                if (d.containsKey('financials_data') && d['financials_data'] is Map) {
                  accumulator = accumulator.copyWith(
                    financialsData: Map<String, dynamic>.from(d['financials_data'] as Map),
                  );
                }
                if (d.containsKey('recommendations_data') && d['recommendations_data'] is Map) {
                  accumulator = accumulator.copyWith(
                    recommendationsData: Map<String, dynamic>.from(d['recommendations_data'] as Map),
                  );
                }
                if (d.containsKey('earnings_data') && d['earnings_data'] is Map) {
                  accumulator = accumulator.copyWith(
                    earningsData: Map<String, dynamic>.from(d['earnings_data'] as Map),
                  );
                }

                if (hasUpdate && accumulator.marketData.isNotEmpty) {
                  emitProgress(accumulator, 'Market data & news loaded! Synthesizing AI research & verdict...', 'analysis', isStructured: true);
                }

                // 4. AI Analysis
                if (d.containsKey('analysis') && d['analysis'] != null && d['analysis'] is Map) {
                  accumulator = accumulator.copyWith(analysis: Map<String, dynamic>.from(d['analysis'] as Map));
                  emitProgress(accumulator, 'AI Verdict generated! Grounding and verifying claims...', 'verification', isStructured: true);
                }

                // 5. Grounding & Verification
                if (d.containsKey('verification_result') && d['verification_result'] != null) {
                  accumulator = accumulator.copyWith(verificationResult: d['verification_result'].toString());
                  emitProgress(accumulator, 'Grounding complete.', 'done', isStructured: true);
                }

                // 6. Blocked / Errors
                if (currentEvent == 'blocked' || (d.containsKey('guardrail') && d['guardrail'] is Map && d['guardrail']['is_safe'] == false)) {
                  final blockedReason = d['analysis']?['summary'] ?? d['guardrail']?['reason'] ?? 'Request was blocked.';
                  accumulator = accumulator.copyWith(blockedMessage: blockedReason.toString());
                  finish(accumulator);
                  return;
                } else if (currentEvent == 'error' && d['message'] != null) {
                  accumulator = accumulator.copyWith(errorMessage: d['message'].toString());
                  finish(accumulator);
                  return;
                }
              }
            } catch (e) {
              // Partial parse safe ignore
            }
          }
          if (currentEvent == 'done') {
            finish(accumulator);
            return;
          }
        }
      }
      finish(accumulator);
    } catch (e) {
      accumulator = accumulator.copyWith(errorMessage: 'Connection error: ' + e.toString());
      finish(accumulator);
    }
  }
}
