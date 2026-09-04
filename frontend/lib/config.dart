class AppConfig {
  static const String backendUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'https://stockresearchassistant-6fcv.onrender.com',
  );
}
