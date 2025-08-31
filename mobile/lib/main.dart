import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AppLanguage extends ChangeNotifier {
  Locale _locale = const Locale('en');
  Locale get locale => _locale;
  void setLocale(Locale l) {
    _locale = l;
    notifyListeners();
  }
}

void main() {
  runApp(ChangeNotifierProvider(
    create: (_) => AppLanguage(),
    child: const EduMateApp(),
  ));
}

class EduMateApp extends StatelessWidget {
  const EduMateApp({super.key});
  @override
  Widget build(BuildContext context) {
    final appLang = Provider.of<AppLanguage>(context);
    const green = Color(0xFF167678);
    const red = Color(0xFFD13264);
    return MaterialApp(
      title: 'EduMateBD',
      debugShowCheckedModeBanner: false,
      locale: appLang.locale,
      supportedLocales: const [Locale('en'), Locale('bn')],
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: green, primary: green, secondary: red),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appLang = Provider.of<AppLanguage>(context);
    final isBn = appLang.locale.languageCode == 'bn';
    return Scaffold(
      appBar: AppBar(
        title: Text(isBn ? 'EduMateBD (বাংলা)' : 'EduMateBD (English)'),
        actions: [
          IconButton(
            onPressed: () => appLang.setLocale(Locale(isBn ? 'en' : 'bn')),
            icon: const Icon(Icons.translate),
            tooltip: 'Toggle Language',
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              isBn ? 'স্বাগতম! প্রশ্ন করুন।' : 'Welcome! Ask a question.',
              style: const TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {},
              child: Text(isBn ? 'AI টিউটর' : 'AI Tutor'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: () {},
              child: Text(isBn ? 'গণিত সমাধান' : 'Math Solver'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: () {},
              child: Text(isBn ? 'পরীক্ষা প্রস্তুতি' : 'Exam Practice'),
            ),
          ],
        ),
      ),
    );
  }
}

