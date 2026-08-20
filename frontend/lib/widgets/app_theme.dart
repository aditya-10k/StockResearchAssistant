import 'package:flutter/material.dart';

class AppColors {
  static const bg = Color(0xFF0C0D12);
  static const surface = Color(0xFF13151D);
  static const card = Color(0xFF181B24);
  static const border = Color(0xFF262B3A);
  static const green = Color(0xFF00E676);
  static const red = Color(0xFFFF3366);
  static const amber = Color(0xFFFFB300);
  static const cyan = Color(0xFF00E5FF);
  static const textPrimary = Color(0xFFF1F3F9);
  static const textSecondary = Color(0xFF9096A8);
  static const textMuted = Color(0xFF596075);
}

class Formatters {
  static String price(dynamic v) {
    if (v == null) return 'N/A';
    final n = (v as num).toDouble();
    return '\$' + n.toStringAsFixed(2);
  }

  static String change(dynamic price, dynamic prev) {
    if (price == null || prev == null) return '';
    final p = (price as num).toDouble();
    final pv = (prev as num).toDouble();
    final diff = p - pv;
    final pct = pv != 0 ? (diff / pv) * 100 : 0.0;
    final sign = diff >= 0 ? '+' : '-';
    return sign + '\$' + diff.abs().toStringAsFixed(2) + ' (' + sign + pct.abs().toStringAsFixed(2) + '%)';
  }

  static String cap(dynamic v) {
    if (v == null) return 'N/A';
    final n = (v as num).toDouble();
    if (n >= 1e12) return '\$' + (n / 1e12).toStringAsFixed(2) + 'T';
    if (n >= 1e9) return '\$' + (n / 1e9).toStringAsFixed(2) + 'B';
    if (n >= 1e6) return '\$' + (n / 1e6).toStringAsFixed(2) + 'M';
    return '\$' + n.toStringAsFixed(0);
  }

  static String vol(dynamic v) {
    if (v == null) return 'N/A';
    final n = (v as num).toDouble();
    if (n >= 1e9) return (n / 1e9).toStringAsFixed(1) + 'B';
    if (n >= 1e6) return (n / 1e6).toStringAsFixed(1) + 'M';
    if (n >= 1e3) return (n / 1e3).toStringAsFixed(0) + 'K';
    return n.toStringAsFixed(0);
  }

  static String percent(dynamic v, [int decimals = 1]) {
    if (v == null) return 'N/A';
    final n = (v as num).toDouble();
    return (n * 100).toStringAsFixed(decimals) + '%';
  }

  static String numVal(dynamic v, [int decimals = 2]) {
    if (v == null) return 'N/A';
    return (v as num).toDouble().toStringAsFixed(decimals);
  }

  static String cash(dynamic v) {
    if (v == null) return 'N/A';
    final n = (v as num).toDouble();
    final sign = n < 0 ? '-' : '';
    final absN = n.abs();
    if (absN >= 1e9) return sign + '\$' + (absN / 1e9).toStringAsFixed(1) + 'B';
    if (absN >= 1e6) return sign + '\$' + (absN / 1e6).toStringAsFixed(1) + 'M';
    return sign + '\$' + absN.toStringAsFixed(0);
  }
}
