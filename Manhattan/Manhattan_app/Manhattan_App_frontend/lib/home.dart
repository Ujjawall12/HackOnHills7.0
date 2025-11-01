import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:intl/intl.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final storage = const FlutterSecureStorage();
  List<dynamic> operatingSystems = [];
  bool isLoading = true;
  String errorMessage = '';

  // Java website color scheme - Dark theme
  static const Color primaryOrange = Color(0xFFED8B00);
  static const Color darkBackground = Color(0xFF1A1A1A);
  static const Color cardBackground = Color(0xFF2D2D2D);
  static const Color darkSurface = Color(0xFF252525);
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB0B0B0);
  static const Color errorRed = Color(0xFFE53E3E);
  static const Color javaBlue = Color(0xFF4A90E2);

  @override
  void initState() {
    super.initState();
    fetchOSInfo();
  }

  Future<void> fetchOSInfo() async {
    try {
      final token = await storage.read(key: 'token');

      if (token == null) {
        setState(() {
          isLoading = false;
          errorMessage = 'Not authenticated. Please log in again.';
        });
        return;
      }

      final response = await http.get(
        Uri.parse('https://sih-backend-u1dv.onrender.com/api/auth/os-info'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          operatingSystems = data['operatingSystems'];
          isLoading = false;
        });
      } else {
        setState(() {
          isLoading = false;
          errorMessage = 'Failed to load data: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        isLoading = false;
        errorMessage = 'Error: $e';
      });
    }
  }

  Future<void> _logout() async {
    await storage.delete(key: 'token');
    await storage.delete(key: 'user');
    Navigator.pushReplacementNamed(context, '/login');
  }

  String _formatDate(String dateString) {
    try {
      final dateTime = DateTime.parse(dateString);
      return DateFormat('MMM dd, yyyy - hh:mm a').format(dateTime);
    } catch (e) {
      return dateString;
    }
  }

  int _getCrossAxisCount(double width) {
    if (width < 600) return 1;
    if (width < 900) return 2;
    if (width < 1200) return 3;
    return 4;
  }

  double _getChildAspectRatio(double width) {
    if (width < 600) return 2.2; // More horizontal for mobile
    if (width < 900) return 1.8;
    return 1.6;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: darkBackground,
      appBar: AppBar(
        title: const Text(
          'Mannhattan',
          style: TextStyle(fontWeight: FontWeight.bold, color: textPrimary),
        ),
        centerTitle: true,
        backgroundColor: primaryOrange,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: textPrimary),
            onPressed: _logout,
            tooltip: 'Logout',
          ),
          IconButton(
            icon: const Icon(Icons.refresh, color: textPrimary),
            onPressed: fetchOSInfo,
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: isLoading
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(
                    valueColor: AlwaysStoppedAnimation<Color>(primaryOrange),
                  ),
                  SizedBox(height: 16),
                  Text(
                    'Loading OS Information...',
                    style: TextStyle(fontSize: 16, color: textSecondary),
                  ),
                ],
              ),
            )
          : errorMessage.isNotEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(
                          Icons.error_outline,
                          size: 64,
                          color: errorRed,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          errorMessage,
                          style: const TextStyle(
                            fontSize: 18,
                            color: errorRed,
                          ),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 20),
                        ElevatedButton(
                          onPressed: fetchOSInfo,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: primaryOrange,
                            foregroundColor: textPrimary,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 12,
                            ),
                          ),
                          child: const Text('Retry'),
                        ),
                      ],
                    ),
                  ),
                )
              : operatingSystems.isEmpty
                  ? Center(
                      child: Padding(
                        padding: const EdgeInsets.all(20.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(
                              Icons.info_outline,
                              size: 64,
                              color: javaBlue,
                            ),
                            const SizedBox(height: 16),
                            const Text(
                              'No operating systems found',
                              style: TextStyle(
                                fontSize: 18,
                                color: javaBlue,
                              ),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 20),
                            ElevatedButton(
                              onPressed: fetchOSInfo,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: primaryOrange,
                                foregroundColor: textPrimary,
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 24,
                                  vertical: 12,
                                ),
                              ),
                              child: const Text('Refresh'),
                            ),
                          ],
                        ),
                      ),
                    )
                  : LayoutBuilder(
                      builder: (context, constraints) {
                        final crossAxisCount = _getCrossAxisCount(constraints.maxWidth);
                        final aspectRatio = _getChildAspectRatio(constraints.maxWidth);

                        return SingleChildScrollView(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'List of certificates',
                                style: TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: textPrimary,
                                ),
                              ),
                              const SizedBox(height: 16),
                              GridView.builder(
                                shrinkWrap: true,
                                physics: const NeverScrollableScrollPhysics(),
                                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                                  crossAxisCount: crossAxisCount,
                                  crossAxisSpacing: 12,
                                  mainAxisSpacing: 12,
                                  childAspectRatio: aspectRatio,
                                ),
                                itemCount: operatingSystems.length,
                                itemBuilder: (context, index) {
                                  final os = operatingSystems[index];
                                  return _buildOSCard(os);
                                },
                              ),
                              const SizedBox(height: 20),
                            ],
                          ),
                        );
                      },
                    ),
    );
  }

  Widget _buildOSCard(Map<String, dynamic> os) {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              cardBackground,
              darkSurface,
            ],
          ),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: primaryOrange.withOpacity(0.3),
            width: 1,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header with OS name and icon
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(6),
                    decoration: BoxDecoration(
                      color: primaryOrange.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Icon(
                      _getOSIcon(os['name']),
                      size: 20,
                      color: primaryOrange,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      os['name'] ?? 'Unknown OS',
                      style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: textPrimary,
                      ),
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              
              // Custom String section
              Text(
                'Custom String:',
                style: TextStyle(
                  fontSize: 11,
                  color: textSecondary,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 2),
              Expanded(
                child: Text(
                  os['customString'] ?? 'N/A',
                  style: const TextStyle(
                    fontSize: 12,
                    color: textPrimary,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              
              // Bottom section with ID
              const SizedBox(height: 4),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Flexible(
                    child: Text(
                      'Added',
                      style: TextStyle(
                        fontSize: 10,
                        color: textSecondary,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 6,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: primaryOrange.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      'ID: ${os['_id']?.substring(0, 6) ?? 'N/A'}',
                      style: TextStyle(
                        fontSize: 9,
                        color: primaryOrange,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getOSIcon(String? osName) {
    if (osName == null) return Icons.usb;

    final lowerName = osName.toLowerCase();
    if (lowerName.contains('windows')) {
      return Icons.usb;
    } else if (lowerName.contains('mac') || lowerName.contains('ios')) {
      return Icons.storage;
    } else if (lowerName.contains('linux')) {
      return Icons.cable;
    } else if (lowerName.contains('android')) {
      return Icons.usb_outlined;
    }
    return Icons.usb;
  }
}