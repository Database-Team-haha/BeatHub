import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class PlayingScreen extends StatefulWidget {
  const PlayingScreen({
    super.key,
    required this.title,
    required this.image,
    required this.name,
    required this.id,
  });

  final String title;
  final String image;
  final String name;
  final int id;

  @override
  State<PlayingScreen> createState() => _PlayingScreenState();
}

class _PlayingScreenState extends State<PlayingScreen> {
  late AudioPlayer _audioPlayer;
  bool _isPlaying = false;
  double _progress = 0.0;
  String username = "";
  bool _isLiked = false;

  @override
  void initState() {
    super.initState();
    _audioPlayer = AudioPlayer();
    _initialize();
  }

  Future<void> _initialize() async {
    await _loadUserInfo(); // Ensure username is loaded first
    _loadAudio();
    _checkIfLiked();
    _updateListening();
  }

  Future<void> _loadAudio() async {
    try {
      final url = 'http://172.20.10.3:8000/songs/${widget.id}/stream/';
      await _audioPlayer.setUrl(url);

      // Listen for position updates
      _audioPlayer.positionStream.listen((position) {
        setState(() {
          _progress = position.inMilliseconds /
              (_audioPlayer.duration?.inMilliseconds ?? 1);
        });
      });
    } catch (e) {
      print('Error loading audio: $e');
    }
  }

  Future<void> _loadUserInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final userInfo = prefs.getString('user_info');
    if (userInfo != null) {
      final data = jsonDecode(userInfo);
      setState(() {
        username = data['username'] ?? "";
      });
    }
  }

  Future<void> _updateListening() async {
    try {
      final response = await http.post(
        Uri.parse('http://172.20.10.3:8000/listenings/'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: '''
      {
        "song_id": ${widget.id},
        "username": "$username"
      }
      ''',
      );

      if (response.statusCode == 200) {
        print('Listening updated successfully');
      } else {
        print('Failed to update listening: ${response.statusCode}');
      }
    } catch (e) {
      print('Error updating listening: $e');
    }
  }

  Future<void> _checkIfLiked() async {
    // Check if the song is already liked by the user
    try {
      final response = await http.get(
        Uri.parse('http://172.20.10.3:8000/users/$username/liked_songs/'),
      );

      if (response.statusCode == 200) {
        final likedSongs = jsonDecode(response.body);
        setState(() {
          _isLiked = likedSongs.any((song) => song['id'] == widget.id);
        });
      }
    } catch (e) {
      print('Error checking like status: $e');
    }
  }

  Future<void> _toggleLike() async {
    try {
      final url = _isLiked
          ? 'http://172.20.10.3:8000/songs/${widget.id}/dislike/'
          : 'http://172.20.10.3:8000/songs/${widget.id}/like/';
      final method = 'POST'; // Always POST for both like and dislike actions

      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'username': username}),
      );

      if (response.statusCode == 200) {
        setState(() {
          _isLiked = !_isLiked; // Toggle the like status
        });
        print(_isLiked ? 'Song liked' : 'Song disliked');
      } else {
        print('Failed to toggle like/dislike: ${response.statusCode}');
      }
    } catch (e) {
      print('Error toggling like/dislike: $e');
    }
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  void _togglePlayPause() {
    if (_isPlaying) {
      _audioPlayer.pause();
    } else {
      _audioPlayer.play();
    }
    setState(() {
      _isPlaying = !_isPlaying;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.black, Colors.grey, Colors.black],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          leading: IconButton(
            icon: const Icon(Icons.keyboard_arrow_down, color: Colors.white, size: 30),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
          actions: [
            IconButton(
              icon: const Icon(Icons.more_vert, color: Colors.white),
              onPressed: () {
                // Add functionality here
              },
            ),
          ],
        ),
        body: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            // Album Cover
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.network(
                  widget.image,
                  height: MediaQuery.of(context).size.height * 0.4,
                  width: double.infinity,
                  fit: BoxFit.cover,
                ),
              ),
            ),

            // Song Title and Artist
            Column(
              children: [
                Text(
                  widget.title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  widget.name,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 16,
                  ),
                ),
              ],
            ),

            // Like/Dislike Button
            IconButton(
              icon: Icon(
                _isLiked ? Icons.favorite : Icons.favorite_border,
                color: _isLiked ? Colors.red : Colors.white,
                size: 36,
              ),
              onPressed: _toggleLike,
            ),

            // Progress Bar
            Column(
              children: [
                Slider(
                  value: _progress,
                  onChanged: (value) {
                    final duration = _audioPlayer.duration;
                    if (duration != null) {
                      final newPosition = Duration(
                          milliseconds: (duration.inMilliseconds * value).toInt());
                      _audioPlayer.seek(newPosition);
                    }
                  },
                  activeColor: Colors.white,
                  inactiveColor: Colors.grey,
                  min: 0,
                  max: 1,
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        _formatDuration(_audioPlayer.position),
                        style: const TextStyle(color: Colors.grey, fontSize: 12),
                      ),
                      Text(
                        _formatDuration(_audioPlayer.duration ?? Duration.zero),
                        style: const TextStyle(color: Colors.grey, fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ],
            ),

            // Playback Controls
            Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  IconButton(
                    icon: const Icon(Icons.shuffle, color: Colors.white, size: 28),
                    onPressed: () {
                      // Shuffle functionality
                    },
                  ),
                  IconButton(
                    icon: const Icon(Icons.skip_previous, color: Colors.white, size: 36),
                    onPressed: () {
                      // Previous song functionality
                    },
                  ),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      shape: const CircleBorder(),
                      backgroundColor: Colors.white,
                    ),
                    onPressed: _togglePlayPause,
                    child: Icon(
                      _isPlaying ? Icons.pause : Icons.play_arrow,
                      color: Colors.black,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.skip_next, color: Colors.white, size: 36),
                    onPressed: () {
                      // Next song functionality
                    },
                  ),
                  IconButton(
                    icon: const Icon(Icons.repeat, color: Colors.white, size: 28),
                    onPressed: () {
                      // Repeat functionality
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatDuration(Duration duration) {
    final minutes = duration.inMinutes;
    final seconds = duration.inSeconds % 60;
    return '$minutes:${seconds.toString().padLeft(2, '0')}';
  }
}
