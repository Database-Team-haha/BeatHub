import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:spotify/loginScreen.dart';
import 'package:spotify/constants.dart';

import 'playingScreen.dart';

class AccountScreen extends StatefulWidget {
  const AccountScreen({super.key, required this.title});
  final String title;

  @override
  State<AccountScreen> createState() => _AccountScreenState();
}

class _AccountScreenState extends State<AccountScreen> {
  String username = "";
  String fullName = "";
  String email = "";
  String dateJoined = "";
  String profilePicture = "";
  List<Map<String, dynamic>> likedSongs = [];
  bool isLoaded = false;

  @override
  void initState() {
    super.initState();
    _loadUserInfo();
  }


  Future<void> _loadUserInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final userInfo = prefs.getString('user_info');
    if (userInfo != null) {
      final data = jsonDecode(userInfo);
      setState(() {
        username = data['username'] ?? "";
        fullName = data['full_name'] ?? "";
        email = data['email'] ?? "";
        dateJoined = data['date_joined'] ?? "";
        profilePicture = data['profile_picture'] ?? "";
      });
      _fetchLikedSongs();
    }
  }

  Future<void> _fetchLikedSongs() async {
    try {
      // Fetch liked songs from the API
      final response = await http.get(
        Uri.parse('http://172.20.10.3:8000/users/$username/liked_songs/'),
      );

      if (response.statusCode == 200) {
        final data = List<Map<String, dynamic>>.from(jsonDecode(response.body));
        setState(() {
          likedSongs = data;
          isLoaded = true;
        });
      } else {
        print('Failed to fetch liked songs: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching liked songs: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SingleChildScrollView( // Wrap the entire body in a scrollable view
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 35, left: 15, right: 15),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const Text(
                    "Account",
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 25,
                      color: Colors.white,
                      fontFamily: "SpotifyCircularBold",
                    ),
                  ),
                  IconButton(
                    onPressed: () {},
                    icon: const Icon(Icons.settings_outlined, color: Colors.white),
                  )
                ],
              ),
            ),
            Center(
              child: Column(
                children: [
                  if (profilePicture.isNotEmpty)
                    CircleAvatar(
                      radius: 50,
                      backgroundImage: NetworkImage(profilePicture),
                    )
                  else
                    const CircleAvatar(
                      radius: 50,
                      backgroundColor: Colors.grey,
                      child: Icon(Icons.person, size: 50, color: Colors.white),
                    ),
                  const SizedBox(height: 20),
                  Text(
                    fullName,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 10),
                  Text(
                    '@$username',
                    style: const TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            const Padding(
              padding: EdgeInsets.only(left: 15, right: 15, top: 20),
              child: Divider(color: Colors.white24),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 15),
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.email, color: Colors.white70),
                    title: Text(
                      email,
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                  ListTile(
                    leading: const Icon(Icons.calendar_today, color: Colors.white70),
                    title: Text(
                      'Joined: $dateJoined',
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                ],
              ),
            ),
            const Padding(
              padding: EdgeInsets.only(left: 15, right: 15, top: 20),
              child: Divider(color: Colors.white24),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 15),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Liked Songs",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 10),
                  isLoaded
                      ? Container(
                    height: 120, // Set the height of the container to prevent overflow
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: likedSongs.length,
                      itemBuilder: (context, index) {
                        final song = likedSongs[index];
                        return Padding(
                          padding: const EdgeInsets.only(right: 10),
                            child: Column(
                              children: [
                                Container(
                                  height: 80, // Set the height for the image container
                                  width: 80,  // Ensure it fits within the available space
                                  decoration: BoxDecoration(
                                    image: DecorationImage(
                                      image: NetworkImage(song['cover_image']),
                                      fit: BoxFit.cover,
                                    ),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                ),
                                const SizedBox(height: 5),
                                Text(
                                  song['title'],
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 12,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                                Text(
                                  song['artist']['full_name'],
                                  style: const TextStyle(
                                    color: Colors.white54,
                                    fontSize: 10,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ],
                            ),
                          );
                      },
                    ),
                  )

                      : const Center(child: CircularProgressIndicator()),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Center(
              child: ElevatedButton(
                onPressed: () async {
                  final prefs = await SharedPreferences.getInstance();
                  await prefs.remove('user_info');
                  // Navigate to login screen after logout
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => const LoginScreen(title: 'Login')),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white12,
                  padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 40),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18.0),
                  ),
                ),
                child: const Text(
                  'Logout',
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
              ),
            ),
            const SizedBox(height: 140),
          ],
        ),
      ),
    );
  }
}
