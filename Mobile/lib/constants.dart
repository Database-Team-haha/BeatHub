import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class Palette {
  static const MaterialColor primaryColor =
      MaterialColor(0xFF1DB954, <int, Color>{});

  static const MaterialColor secondaryColor =
      MaterialColor(0xFF121212, <int, Color>{});

  static const MaterialColor secondarySwatchColor =
      MaterialColor(0xFF2A2A2A, <int, Color>{});
}

class Song {
  final String name;
  final String image;
  final String? songPath; // Optional because not all songs may have a path
  final String? artistImage; // Added artist_image
  final int id;

  Song({
    required this.name,
    required this.image,
    this.songPath,
    this.artistImage,
    required this.id,
  });

  // Factory constructor to create a Song from a JSON response
  factory Song.fromJson(Map<String, dynamic> json) {
    return Song(
      name: json['title'], // Assuming 'title' is the song name in the API response
      image: json['cover_image'], // Assuming 'cover_image' is the image URL in the API response
      songPath: json['song_path'], // Assuming 'song_path' is the song file path in the API response
      artistImage: json['artist_picture'], // Assuming 'artist_picture' is the artist image URL
      id: json['id']
    );
  }
}

class Songs {
  // This will hold the song details by artist name
  static Map<String, List<Song>> songDetails = {};

  // This method will fetch songs and fill the songDetails map
  static Future<void> fetchSongs() async {
    final response = await http.get(Uri.parse('http://172.20.10.3:8000/songs/'));

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);

      // Iterate over the fetched data and organize it by artist
      for (var jsonData in data) {
        // Create a song instance from the JSON
        Song song = Song.fromJson(jsonData);

        // Get the artist's username and artist image from the JSON
        String artist = jsonData['artist']['full_name'];
        String? artistImage = song.artistImage;

        // Check if the artist already exists in the map; if not, create a new list
        if (!songDetails.containsKey(artist)) {
          songDetails[artist] = [];
        }

        // Add the song to the artist's list
        songDetails[artist]!.add(song);
      }
    } else {
      throw Exception('Failed to load songs');
    }
  }
}
