import 'dart:async';
import 'package:flutter/material.dart';
import 'package:marquee/marquee.dart';
import 'package:spotify/widgets/dashboardScreenWidgets/artistAndPodcastersColumn.dart';
import 'package:spotify/widgets/dashboardScreenWidgets/recentPlaylistContainer.dart';
import 'package:spotify/widgets/dashboardScreenWidgets/recentlyPlayed.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class homeScreen extends StatefulWidget {
  final List<Map<String, dynamic>> recentPlayedItems;
  final List<Map<String, dynamic>> recentPlaylistItems;
  final List<Map<String, dynamic>> artistAndPodcastersItems;

  const homeScreen(
      {Key? key,
        required this.recentPlayedItems,
        required this.recentPlaylistItems,
        required this.artistAndPodcastersItems})
      : super(key: key);

  @override
  State<homeScreen> createState() => _homeScreenState();
}

class _homeScreenState extends State<homeScreen> {
  late Map<String, dynamic> _listenings = {};
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _getUserListenings();
    _startListeningUpdates();
  }

  void _startListeningUpdates() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      _getUserListenings();
    });
  }

  Future<void> _getUserListenings() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final userInfo = prefs.getString('user_info');
      String username = "";

      if (userInfo != null) {
        final data = jsonDecode(userInfo);
        username = data['username'] ?? "";
      }

      if (username.isEmpty) {
        print('No username found');
        return;
      }

      final response = await http.get(
        Uri.parse('http://172.20.10.3:8000/listenings/?username=$username'),
      );

      if (response.statusCode == 200) {
        print('Successfully fetched listenings');
        setState(() {
          _listenings = jsonDecode(response.body);  // Update the _listenings map
          print(_listenings['song_id']);
        });
      } else {
        print('Failed to fetch listenings: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching listenings: $e');
    }
  }



  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        SingleChildScrollView(
          primary: true,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(top: 35),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    const Padding(
                      padding: EdgeInsets.only(left: 15),
                      child: Text("Good morning",
                          style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 25,
                              color: Colors.white,
                              fontFamily: "SpotifyCircularBold")),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(right: 15),
                      child: Row(children: [
                        IconButton(
                            onPressed: () {},
                            icon: const Icon(Icons.notifications_none_sharp,
                                color: Colors.white)),
                        IconButton(
                            onPressed: () {},
                            icon: const Icon(Icons.access_time_sharp,
                                color: Colors.white)),
                        IconButton(
                            onPressed: () {},
                            icon: const Icon(Icons.settings_outlined,
                                color: Colors.white))
                      ]),
                    )
                  ],
                ),
              ),
              GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  mainAxisSpacing: 10,
                  crossAxisSpacing: 10,
                  childAspectRatio: 3.125,
                ),
                primary: false,
                padding: const EdgeInsets.only(left: 15, right: 15),
                shrinkWrap: true,
                itemCount: widget.recentPlaylistItems.length > 5
                    ? 5
                    : widget.recentPlaylistItems.length,
                itemBuilder: (BuildContext context, index) {
                  return recentPlaylistContainer(
                    name: widget.recentPlaylistItems[index]["name"],
                    image: widget.recentPlaylistItems[index]["image"],
                    artist: widget.recentPlaylistItems[index]["artist"],
                    id: widget.recentPlaylistItems[index]["id"],
                  );
                },
              ),
              const Padding(
                  padding: EdgeInsets.only(
                      top: 30, left: 15, right: 15, bottom: 15),
                  child: SizedBox(
                    width: double.infinity,
                    child: Text("Recently played",
                        style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 25,
                            color: Colors.white,
                            fontFamily: "SpotifyCircularBold"),
                        textAlign: TextAlign.left),
                  )),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15),
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      for (int i = 0; i < 50; i = i + 10)
                        recentlyPlayed(
                          name: widget.recentPlayedItems[i]['artist'] ?? 'Unknown Artist',
                          image: widget.recentPlayedItems[i]['artistImage'] ?? "http://172.20.10.3:8000/picture/Billie_Eilish.jpg",
                          border_radius: 100,
                          artistAndPodcastersItems: widget.artistAndPodcastersItems,
                        ),
                    ],
                  ),
                ),
              ),
              const Padding(
                  padding: EdgeInsets.only(
                      top: 15, left: 15, right: 15, bottom: 15),
                  child: SizedBox(
                    width: double.infinity,
                    child: Text(
                      "Artists",
                      style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 25,
                          color: Colors.white,
                          fontFamily: "SpotifyCircularBold"),
                      textAlign: TextAlign.left,
                      maxLines: 2,
                    ),
                  )),
              Padding(
                padding: const EdgeInsets.only(left: 15, right: 15),
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      for (int i = 1; i < widget.artistAndPodcastersItems.length; i++)
                        artistAndPodcastersColumn(
                          name: widget.artistAndPodcastersItems[i]['artist'],
                          image: widget.artistAndPodcastersItems[i]['artistImage'] ?? "http://172.20.10.3:8000/picture/Billie_Eilish.jpg",
                          border_radius: 100,
                          artistAndPodcastersItems: widget.artistAndPodcastersItems,
                        ),
                    ],
                  ),
                ),
              ),
              const Padding(
                  padding: EdgeInsets.only(left: 15, right: 15),
                  child: SizedBox(height: 140, width: double.infinity))
            ],
          ),
        ),
        if (_listenings['title'] != null) ...[
          Positioned(
            bottom: 70,
            left: 10,
            child: Container(
              decoration: BoxDecoration(
                  color: Colors.indigo.shade900,
                  borderRadius: BorderRadius.circular(10)),
              width: MediaQuery.of(context).size.width - 20,
              height: 60,
              child: Padding(
                padding: const EdgeInsets.all(8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(5),
                      child: Image.network(
                        _listenings['cover_image'] ??
                            "http://172.20.10.3:8000/picture/Billie_Eilish.jpg",
                        height: 120,
                        width: 120,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        Text(
                          _listenings['title'] ?? "NUll",
                          style: TextStyle(
                              fontFamily: "SpotifyCircularBold",
                              color: Colors.white,
                              fontSize: 16,
                              fontWeight: FontWeight.bold),
                        ),
                        Text(
                          _listenings['artist_username'] ?? "NUll",
                          style: TextStyle(
                              fontFamily: "SpotifyCircularLight",
                              color: Colors.white,
                              fontSize: 14),
                        ),
                      ],
                    ),
                    const Spacer(),
                    IconButton(
                      onPressed: () {},
                      icon: const Icon(
                        Icons.play_arrow,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ]

      ],
    );
  }
}
