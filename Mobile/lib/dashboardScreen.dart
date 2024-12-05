//import 'dart:js_util';
// ignore_for_file: file_names, non_constant_identifier_names

import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';
import 'package:spotify/constants.dart';
import 'package:spotify/searchScreen.dart';
import 'package:spotify/homeScreen.dart';

import 'accountScreen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key, required this.title});
  final String title;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  bool home = true;

  int currentIndex = 0;
  Color homeColor = Colors.white;
  Color searchColor = Colors.white54;
  Color libraryColor = Colors.white54;
  Color premiumColor = Colors.white54;
  double homeSize = 27;
  double homeTextSize = 15;
  double searchSize = 24;
  double searchTextSize = 13;
  double librarySize = 24;
  double libraryTextSize = 13;
  double premiumSize = 24;
  double premiumTextSize = 13;

  // Internet Connection Checker :---
  late ConnectivityResult result;
  late StreamSubscription subscription;
  var isDeviceConnected = false;

  @override
  void initState() {
    super.initState();
    checkInternet();
    startStreaming();
  }

  checkInternet() async {
    result = await Connectivity().checkConnectivity();
    if (result != ConnectivityResult.none) {
      isDeviceConnected = true;
      _loadData();
    } else {
      isDeviceConnected = false;
      showDialogBox();
    }
    setState(() {});
  }

  startStreaming() {
    subscription = Connectivity().onConnectivityChanged.listen((event) async {
      checkInternet();
    });
  }

  late List<Map<String, dynamic>> recentPlaylistItems;
  late List<Map<String, dynamic>> recentPlayedItems;
  late List<Map<String, dynamic>> artistAndPodcastersItems;

  bool isLoaded = false;

  _loadData() async {
    List<Map<String, dynamic>> recentPlaylistTempList = [];

    List<Map<String, dynamic>> recentPlayedTempList = [];

    List<Map<String, dynamic>> artistAndPodcastersTempList = [];
    var data_artistAndPodcasters = await Songs.fetchSongs();




    Songs.songDetails.forEach((artist, songsList) {
      artistAndPodcastersTempList.add({
        'artist': artist,
        'artistImage': songsList[0].artistImage,
        'song': songsList,
      });

      for (var song in songsList) {
        // Add the artist and song details to the temporary list
        recentPlaylistTempList.add({
          'artist': artist,
          'artistImage': song.artistImage,
          'name': song.name,
          'image': song.image,
          'song_path': song.songPath, // This could be null for podcasts
          'id': song.id,
        });
      }
    });

    setState(() {
      recentPlaylistItems = recentPlaylistTempList;
      recentPlayedItems = recentPlayedTempList;
      artistAndPodcastersItems = artistAndPodcastersTempList;
      isLoaded = true;
    });
  }
  // :---

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 0,
        backgroundColor: Palette.secondaryColor,
      ),
      backgroundColor: Palette.secondaryColor,
      body: isLoaded
          ? (currentIndex == 0
          ? homeScreen(
          recentPlayedItems: artistAndPodcastersItems,
          recentPlaylistItems: recentPlaylistItems,
          artistAndPodcastersItems: artistAndPodcastersItems)
          : currentIndex == 1
          ? const searchScreen()
          : const AccountScreen(title: "Account"))
          : Container(),
      extendBody: true,
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
              colors: [Colors.black, Colors.transparent],
              begin: Alignment.bottomCenter,
              end: Alignment.topCenter),
        ),
        height: 70,
        child: Theme(
          data: Theme.of(context).copyWith(
              splashColor: Colors.white24, highlightColor: Colors.transparent),
          child: BottomNavigationBar(
            currentIndex: currentIndex,
            onTap: (index) => setState(() {
              currentIndex = index;
              // Adjust other properties like sizes or colors here if necessary
            }),
            type: BottomNavigationBarType.fixed,
            backgroundColor: Colors.transparent,
            selectedItemColor: Colors.white,
            unselectedItemColor: Colors.white54,
            selectedFontSize: 15,
            unselectedFontSize: 13,
            items: <BottomNavigationBarItem>[
              BottomNavigationBarItem(
                  icon: Icon(Icons.home_filled, size: currentIndex == 0 ? 27 : 24),
                  label: "Home"),
              BottomNavigationBarItem(
                  icon: Icon(Icons.search, size: currentIndex == 1 ? 27 : 24),
                  label: "Search"),
              BottomNavigationBarItem(
                  icon: Icon(Icons.person, size: currentIndex == 2 ? 27 : 24),
                  label: "Account"),
            ],
          ),
        ),
      ),
    );
  }


  // Internet error Dialog Box
  showDialogBox() {
    return showDialog(
        barrierDismissible: false,
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: const Text(
                "No internet connection",
                style: TextStyle(
                    fontFamily: "SpotifyCircularBold", color: Colors.white),
              ),
              content: const Text(
                "Turn on mobile data or connect to Wi-Fi.",
                style: TextStyle(
                    fontFamily: "SpotifyCircularLight",
                    color: Colors.white,
                    fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(25)),
              backgroundColor: Palette.secondarySwatchColor,
              actionsAlignment: MainAxisAlignment.center,
              surfaceTintColor: Colors.red,
              actions: <Widget>[
                ElevatedButton(
                    onPressed: () async {
                      Navigator.pop(context);
                      checkInternet();
                    },
                    style: ElevatedButton.styleFrom(
                        backgroundColor: Palette.primaryColor,
                        foregroundColor: Colors.white,
                        elevation: 10,
                        textStyle: const TextStyle(
                            fontFamily: "SpotifyCircularBold",
                            color: Colors.white,
                            fontSize: 18),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(25)),
                        fixedSize: const Size(250, 50)),
                    child: const Text("Try Again"))
              ],
            ));
  }
  // :---
}
