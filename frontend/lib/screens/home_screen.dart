import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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

  List<Map<String, dynamic>> _recentSessions = [];
  bool _isLoadingSessions = false;

  @override
  void initState() {
    super.initState();
    // 1. Immediately ping healthcheck on site open to wake up Render container
    _pingHealth();
    // 2. Keep pinging every 25 seconds to keep the free-tier container warm while user is browsing
    _healthTimer = Timer.periodic(const Duration(seconds: 25), (_) => _pingHealth());

    // 3. Load recent chat sessions from PostgreSQL
    _loadRecentSessions();

    // 4. Check if a shared session URL is being opened (?session=...)
    _checkUrlSharedSession();
  }

  Future<void> _checkUrlSharedSession() async {
    try {
      final sharedId = Uri.base.queryParameters['session'];
      if (sharedId != null && sharedId.isNotEmpty) {
        final data = await ApiService.getSharedChat(sharedId);
        if (data != null && mounted) {
          context.read<ChatBloc>().add(LoadSessionEvent(data, isShared: true));
        }
      }
    } catch (_) {}
  }

  Future<void> _loadRecentSessions() async {
    if (!mounted) return;
    setState(() => _isLoadingSessions = true);
    final sessions = await ApiService.getRecentChats();
    if (mounted) {
      setState(() {
        _recentSessions = sessions;
        _isLoadingSessions = false;
      });
    }
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
      // Re-fetch sessions after a short delay
      Future.delayed(const Duration(seconds: 5), _loadRecentSessions);
    }
  }

  Future<void> _copyShareLink(String sessionId) async {
    final url = '${Uri.base.origin}/?session=$sessionId';
    await Clipboard.setData(ClipboardData(text: url));
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppColors.surface,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(4),
            side: const BorderSide(color: AppColors.cyan, width: 0.8),
          ),
          content: Row(
            children: [
              const Icon(Icons.link, color: AppColors.cyan, size: 16),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  'Shareable link copied: $url',
                  style: const TextStyle(fontSize: 12, color: AppColors.textPrimary, fontFamily: 'monospace'),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          duration: const Duration(seconds: 4),
        ),
      );
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
    return BlocBuilder<ChatBloc, ChatState>(
      builder: (context, chatState) {
        return Scaffold(
          backgroundColor: AppColors.bg,
          drawer: _buildDrawer(context, chatState),
          appBar: AppBar(
            backgroundColor: AppColors.surface,
            elevation: 0,
            leading: Builder(
              builder: (ctx) => IconButton(
                icon: const Icon(Icons.menu, size: 20, color: AppColors.cyan),
                tooltip: 'Recent Research Sessions',
                onPressed: () {
                  _loadRecentSessions();
                  Scaffold.of(ctx).openDrawer();
                },
              ),
            ),
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
              TextButton.icon(
                onPressed: () {
                  context.read<ChatBloc>().add(NewSessionEvent());
                },
                icon: const Icon(Icons.add, size: 14, color: AppColors.cyan),
                label: const Text(
                  'NEW',
                  style: TextStyle(fontSize: 11, color: AppColors.cyan, fontFamily: 'monospace', fontWeight: FontWeight.bold),
                ),
              ),
              if (chatState.currentSessionId != null)
                IconButton(
                  icon: const Icon(Icons.share_outlined, size: 18, color: AppColors.cyan),
                  tooltip: 'Share Research Report',
                  onPressed: () => _copyShareLink(chatState.currentSessionId!),
                ),
              const SizedBox(width: 8),
            ],
          ),
          body: Column(
            children: [
              if (chatState.isSharedView)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(
                    color: AppColors.cyan.withOpacity(0.1),
                    border: const Border(bottom: BorderSide(color: AppColors.cyan, width: 0.5)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.visibility_outlined, size: 14, color: AppColors.cyan),
                      const SizedBox(width: 8),
                      const Expanded(
                        child: Text(
                          'VIEWING SHARED RESEARCH REPORT',
                          style: TextStyle(fontSize: 10, color: AppColors.cyan, letterSpacing: 1.2, fontFamily: 'monospace', fontWeight: FontWeight.bold),
                        ),
                      ),
                      GestureDetector(
                        onTap: () => context.read<ChatBloc>().add(NewSessionEvent()),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            border: Border.all(color: AppColors.cyan, width: 0.6),
                            borderRadius: BorderRadius.circular(2),
                          ),
                          child: const Text('START YOUR OWN', style: TextStyle(fontSize: 9, color: AppColors.cyan, fontFamily: 'monospace')),
                        ),
                      ),
                    ],
                  ),
                )
              else if (!_isBackendOnline)
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
                                ResearchResultView(
                                  result: msg.result!,
                                  onShare: chatState.currentSessionId != null
                                      ? () => _copyShareLink(chatState.currentSessionId!)
                                      : null,
                                ),
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
      },
    );
  }

  Widget _buildDrawer(BuildContext context, ChatState chatState) {
    return Drawer(
      backgroundColor: AppColors.surface,
      child: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
              decoration: const BoxDecoration(
                border: Border(bottom: BorderSide(color: AppColors.border, width: 1)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.history, color: AppColors.cyan, size: 20),
                  const SizedBox(width: 10),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'RESEARCH SESSIONS',
                          style: TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.5,
                            fontFamily: 'monospace',
                          ),
                        ),
                        SizedBox(height: 2),
                        Text(
                          'POSTGRESQL HISTORY',
                          style: TextStyle(
                            color: AppColors.textMuted,
                            fontSize: 9,
                            fontFamily: 'monospace',
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.refresh, color: AppColors.textSecondary, size: 18),
                    tooltip: 'Refresh list',
                    onPressed: _loadRecentSessions,
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.of(context).pop();
                  context.read<ChatBloc>().add(NewSessionEvent());
                },
                icon: const Icon(Icons.add, size: 16, color: AppColors.cyan),
                label: const Text(
                  'NEW RESEARCH',
                  style: TextStyle(
                    fontSize: 11,
                    color: AppColors.cyan,
                    letterSpacing: 1.2,
                    fontFamily: 'monospace',
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: AppColors.cyan, width: 0.8),
                  backgroundColor: AppColors.cyan.withOpacity(0.05),
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
                ),
              ),
            ),
            const Divider(height: 1, color: AppColors.border),
            Expanded(
              child: _isLoadingSessions
                  ? const Center(
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: AppColors.cyan,
                      ),
                    )
                  : _recentSessions.isEmpty
                      ? Center(
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.folder_open, size: 36, color: AppColors.textMuted.withOpacity(0.5)),
                                const SizedBox(height: 10),
                                const Text(
                                  'NO SAVED SESSIONS',
                                  style: TextStyle(
                                    fontSize: 11,
                                    color: AppColors.textMuted,
                                    fontFamily: 'monospace',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                const Text(
                                  'Submit a research query to create and persist your first session in PostgreSQL.',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(fontSize: 11, color: AppColors.textMuted),
                                ),
                              ],
                            ),
                          ),
                        )
                      : ListView.separated(
                          itemCount: _recentSessions.length,
                          separatorBuilder: (_, __) => const Divider(height: 1, color: AppColors.border),
                          itemBuilder: (context, index) {
                            final session = _recentSessions[index];
                            final sessionId = session['id']?.toString() ?? '';
                            final title = session['title']?.toString() ?? 'Research Session';
                            final count = session['message_count'] ?? 0;
                            final isSelected = sessionId == chatState.currentSessionId;

                            return Container(
                              color: isSelected ? AppColors.cyan.withOpacity(0.08) : Colors.transparent,
                              child: ListTile(
                                dense: true,
                                contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
                                leading: Icon(
                                  isSelected ? Icons.folder_open : Icons.description_outlined,
                                  size: 18,
                                  color: isSelected ? AppColors.cyan : AppColors.textSecondary,
                                ),
                                title: Text(
                                  title,
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: isSelected ? AppColors.cyan : AppColors.textPrimary,
                                    fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                                    fontFamily: 'monospace',
                                  ),
                                ),
                                subtitle: Text(
                                  '$count updates',
                                  style: const TextStyle(
                                    fontSize: 10,
                                    color: AppColors.textMuted,
                                    fontFamily: 'monospace',
                                  ),
                                ),
                                trailing: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    IconButton(
                                      icon: const Icon(Icons.share_outlined, size: 15, color: AppColors.textSecondary),
                                      tooltip: 'Copy share link',
                                      onPressed: () => _copyShareLink(sessionId),
                                    ),
                                    IconButton(
                                      icon: const Icon(Icons.delete_outline, size: 15, color: AppColors.red),
                                      tooltip: 'Delete session',
                                      onPressed: () async {
                                        final chatBloc = context.read<ChatBloc>();
                                        final ok = await ApiService.deleteChatSession(sessionId);
                                        if (ok && mounted) {
                                          setState(() {
                                            _recentSessions.removeWhere((s) => s['id'] == sessionId);
                                          });
                                          if (chatState.currentSessionId == sessionId) {
                                            chatBloc.add(NewSessionEvent());
                                          }
                                        }
                                      },
                                    ),
                                  ],
                                ),
                                onTap: () async {
                                  final chatBloc = context.read<ChatBloc>();
                                  Navigator.of(context).pop();
                                  final fullData = await ApiService.getChatSession(sessionId);
                                  if (fullData != null && mounted) {
                                    chatBloc.add(LoadSessionEvent(fullData, isShared: false));
                                  }
                                },
                              ),
                            );
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }
}
