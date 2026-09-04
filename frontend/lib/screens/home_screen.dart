import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../blocs/chat_bloc.dart';
import '../screens/research_result_view.dart';
import '../services/api_service.dart';
import '../widgets/progress_status_bar.dart';
import '../widgets/app_theme.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  bool _isBackendOnline = false;
  bool _isCheckingHealth = true;
  Timer? _healthTimer;

  @override
  void initState() {
    super.initState();
    // 1. Immediately ping healthcheck on site open to wake up Render container
    _pingHealth();
    // 2. Keep pinging every 25 seconds to keep the free-tier container warm while user is browsing
    _healthTimer = Timer.periodic(const Duration(seconds: 25), (_) => _pingHealth());
  }

  Future<void> _pingHealth() async {
    final online = await ApiService.checkHealth();
    if (mounted) {
      setState(() {
        _isBackendOnline = online;
        _isCheckingHealth = false;
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _send() {
    final text = _controller.text.trim();
    if (text.isNotEmpty) {
      context.read<ChatBloc>().add(SendMessageEvent(text));
      _controller.clear();
    }
  }

  @override
  void dispose() {
    _healthTimer?.cancel();
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.surface,
        elevation: 0,
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(1),
          child: Container(height: 1, color: AppColors.border),
        ),
        title: Row(
          children: [
            Container(
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                color: _isBackendOnline ? AppColors.green : AppColors.amber,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 8),
            const Text(
              'RESEARCH TERMINAL',
              style: TextStyle(
                color: AppColors.textPrimary,
                fontSize: 13,
                fontWeight: FontWeight.w600,
                letterSpacing: 2.0,
                fontFamily: 'monospace',
              ),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: _isBackendOnline
                    ? AppColors.green.withOpacity(0.12)
                    : AppColors.amber.withOpacity(0.12),
                border: Border.all(
                  color: _isBackendOnline ? AppColors.green : AppColors.amber,
                  width: 0.5,
                ),
                borderRadius: BorderRadius.circular(3),
              ),
              child: Text(
                _isBackendOnline ? 'LIVE' : (_isCheckingHealth ? 'PINGING...' : 'WAKING UP SERVER...'),
                style: TextStyle(
                  fontSize: 9,
                  color: _isBackendOnline ? AppColors.green : AppColors.amber,
                  fontFamily: 'monospace',
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        actions: [
          const Padding(
            padding: EdgeInsets.only(right: 16),
            child: Text('AI-POWERED EQUITY RESEARCH', style: TextStyle(fontSize: 10, color: AppColors.textMuted, letterSpacing: 1)),
          ),
        ],
      ),
      body: Column(
        children: [
          if (!_isBackendOnline)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              decoration: BoxDecoration(
                color: AppColors.amber.withOpacity(0.08),
                border: const Border(bottom: BorderSide(color: AppColors.amber, width: 0.5)),
              ),
              child: Row(
                children: const [
                  SizedBox(
                    width: 10,
                    height: 10,
                    child: CircularProgressIndicator(strokeWidth: 1.5, color: AppColors.amber),
                  ),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      'Backend is waking up from idle sleep on free Render tier (~30s). Initial query may take a moment.',
                      style: TextStyle(fontSize: 11, color: AppColors.amber),
                    ),
                  ),
                ],
              ),
            ),
          Expanded(
            child: BlocConsumer<ChatBloc, ChatState>(
              listener: (ctx, state) => _scrollToBottom(),
              builder: (ctx, state) {
                if (state.messages.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text('EQUITY RESEARCH ASSISTANT', style: TextStyle(fontSize: 16, color: AppColors.textSecondary, letterSpacing: 3, fontFamily: 'monospace')),
                        const SizedBox(height: 8),
                        const Text('Ask about any publicly traded stock or company', style: TextStyle(fontSize: 13, color: AppColors.textMuted)),
                        const SizedBox(height: 32),
                        Wrap(
                          spacing: 8, runSpacing: 8,
                          alignment: WrapAlignment.center,
                          children: ['Compare AAPL and MSFT', 'Analyze NVDA', 'Is TSLA a good buy?', 'Top Indian IT stocks'].map((q) =>
                            GestureDetector(
                              onTap: () { _controller.text = q; _send(); },
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                                decoration: BoxDecoration(border: Border.all(color: AppColors.border), borderRadius: BorderRadius.circular(3)),
                                child: Text(q, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                              ),
                            ),
                          ).toList(),
                        ),
                      ],
                    ),
                  );
                }

                return ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                  itemCount: state.messages.length,
                  itemBuilder: (ctx, index) {
                    final msg = state.messages[index];

                    if (msg.isUser) {
                      return Align(
                        alignment: Alignment.centerRight,
                        child: Container(
                          margin: const EdgeInsets.only(bottom: 12, left: 60),
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                          decoration: BoxDecoration(
                            color: AppColors.surface,
                            border: Border.all(color: AppColors.border),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(msg.text, style: const TextStyle(fontSize: 13, color: AppColors.textPrimary)),
                        ),
                      );
                    }

                    return Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: msg.isStructured && msg.result != null
                          ? Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                if (msg.isStreaming) ...[
                                  ProgressStatusBar(
                                    currentStatus: msg.status,
                                    activeStep: msg.activeStep,
                                  ),
                                  const SizedBox(height: 12),
                                ],
                                ResearchResultView(result: msg.result!),
                              ],
                            )
                          : ProgressStatusBar(
                              currentStatus: msg.status,
                              activeStep: msg.activeStep,
                            ),
                    );
                  },
                );
              },
            ),
          ),
          Container(
            decoration: const BoxDecoration(
              color: AppColors.surface,
              border: Border(top: BorderSide(color: AppColors.border)),
            ),
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: AppColors.textPrimary, fontSize: 13),
                    cursorColor: AppColors.cyan,
                    onSubmitted: (_) => _send(),
                    decoration: InputDecoration(
                      hintText: 'Enter ticker, company, or research question...',
                      hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
                      filled: true,
                      fillColor: AppColors.card,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(3), borderSide: const BorderSide(color: AppColors.border)),
                      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(3), borderSide: const BorderSide(color: AppColors.border)),
                      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(3), borderSide: const BorderSide(color: AppColors.cyan, width: 1)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
                      prefixIcon: const Icon(Icons.terminal, color: AppColors.textMuted, size: 16),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                BlocBuilder<ChatBloc, ChatState>(
                  builder: (ctx, state) => GestureDetector(
                    onTap: state.isLoading ? null : _send,
                    child: Container(
                      width: 42, height: 42,
                      decoration: BoxDecoration(
                        color: state.isLoading ? AppColors.border : AppColors.cyan,
                        borderRadius: BorderRadius.circular(3),
                      ),
                      child: state.isLoading
                          ? const Padding(padding: EdgeInsets.all(10), child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.textSecondary))
                          : const Icon(Icons.send_rounded, color: AppColors.bg, size: 18),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
