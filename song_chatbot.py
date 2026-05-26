# song_chatbot.py

from typing import List, Tuple, Callable, Any


# =========================================================
# SONG DATABASE
# =========================================================

# tuple format:
# (song_title, artist, album, year, genre)

song_db: List[Tuple[str, str, str, int, str]] = [
    ("humble", "kendrick lamar", "damn", 2017, "hip hop"),
    ("dna", "kendrick lamar", "damn", 2017, "hip hop"),
    ("bad guy", "billie eilish", "when we all fall asleep", 2019, "pop"),
    ("blinding lights", "the weeknd", "after hours", 2020, "pop"),
    ("yellow", "coldplay", "parachutes", 2000, "alternative"),
    ("numb", "linkin park", "meteora", 2003, "rock"),
    ("shape of you", "ed sheeran", "divide", 2017, "pop"),
    ("bohemian rhapsody", "queen", "a night at the opera", 1975, "rock"),
]


# =========================================================
# PROJECTION FUNCTIONS
# =========================================================

def get_title(song: Tuple[str, str, str, int, str]) -> str:
    return song[0]


def get_artist(song: Tuple[str, str, str, int, str]) -> str:
    return song[1]


def get_album(song: Tuple[str, str, str, int, str]) -> str:
    return song[2]


def get_year(song: Tuple[str, str, str, int, str]) -> int:
    return song[3]


def get_genre(song: Tuple[str, str, str, int, str]) -> str:
    return song[4]


# =========================================================
# ACTION FUNCTIONS
# =========================================================

def songs_by_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []

    for song in song_db:
        if get_year(song) == year:
            result.append(get_title(song))

    return result


def songs_before_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []

    for song in song_db:
        if get_year(song) < year:
            result.append(get_title(song))

    return result


def songs_after_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []

    for song in song_db:
        if get_year(song) > year:
            result.append(get_title(song))

    return result


def artist_by_song(matches: List[str]) -> List[str]:
    title = matches[0]
    result = []

    for song in song_db:
        if get_title(song) == title:
            result.append(get_artist(song))

    return result


def album_by_song(matches: List[str]) -> List[str]:
    title = matches[0]
    result = []

    for song in song_db:
        if get_title(song) == title:
            result.append(get_album(song))

    return result


def genre_by_song(matches: List[str]) -> List[str]:
    title = matches[0]
    result = []

    for song in song_db:
        if get_title(song) == title:
            result.append(get_genre(song))

    return result


def year_by_song(matches: List[str]) -> List[Any]:
    title = matches[0]
    result = []

    for song in song_db:
        if get_title(song) == title:
            result.append(get_year(song))

    return result


def songs_by_artist(matches: List[str]) -> List[str]:
    artist = matches[0]
    result = []

    for song in song_db:
        if get_artist(song) == artist:
            result.append(get_title(song))

    return result


def songs_by_album(matches: List[str]) -> List[str]:
    album = matches[0]
    result = []

    for song in song_db:
        if get_album(song) == album:
            result.append(get_title(song))

    return result


# dummy argument ignored
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# =========================================================
# MATCH FUNCTION
# =========================================================

def match(pattern: List[str], source: List[str]) -> List[str]:
    """
    % matches zero or more words
    _ matches exactly one word
    """

    sind = 0
    pind = 0
    result: List[str] = []

    while pind != len(pattern) or sind != len(source):

        if pind == len(pattern):
            return None

        elif pattern[pind] == "%":

            if pind == (len(pattern) - 1):
                return result + [" ".join(source[sind:])]

            else:
                accum = ""
                pind += 1

                while pattern[pind] != source[sind]:
                    accum += " " + source[sind]
                    sind += 1

                    if sind >= len(source):
                        return None

                result.append(accum.strip())

        elif sind == len(source):
            return None

        elif pattern[pind] == "_":
            result += [source[sind].strip()]
            pind += 1
            sind += 1

        elif pattern[pind] == source[sind]:
            pind += 1
            sind += 1

        else:
            return None

    return result


# =========================================================
# PATTERN-ACTION LIST
# =========================================================

pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [

    (str.split("what songs were released in _"), songs_by_year),

    (str.split("what songs were released before _"), songs_before_year),

    (str.split("what songs were released after _"), songs_after_year),

    (str.split("who sings %"), artist_by_song),

    (str.split("what album is % on"), album_by_song),

    (str.split("what genre is %"), genre_by_song),

    (str.split("when was % released"), year_by_song),

    (str.split("what songs did % make"), songs_by_artist),

    (str.split("what songs are on %"), songs_by_album),

    (["bye"], bye_action),
]


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_pa_list(src: List[str]) -> List[str]:

    for pat, act in pa_list:

        mat = match(pat, src)

        if mat is not None:

            answer = act(mat)

            return answer if answer else ["No answers"]

    return ["I don't understand"]


# =========================================================
# QUERY LOOP
# =========================================================

def query_loop() -> None:

    print("Welcome to the song database!\n")

    while True:

        try:

            print()

            query = input("Your query? ")

            query = query.replace("?", "").lower().split()

            answers = search_pa_list(query)

            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nGoodbye!\n")


# =========================================================
# TESTS
# =========================================================

if __name__ == "__main__":

    assert sorted(songs_by_year(["2017"])) == sorted(
        ["humble", "dna", "shape of you"]
    )

    assert sorted(artist_by_song(["humble"])) == sorted(
        ["kendrick lamar"]
    )

    assert sorted(album_by_song(["numb"])) == sorted(
        ["meteora"]
    )

    assert sorted(genre_by_song(["yellow"])) == sorted(
        ["alternative"]
    )

    assert sorted(year_by_song(["bad guy"])) == sorted(
        [2019]
    )

    assert sorted(songs_by_artist(["kendrick lamar"])) == sorted(
        ["humble", "dna"]
    )

    assert sorted(songs_by_album(["damn"])) == sorted(
        ["humble", "dna"]
    )

    assert sorted(search_pa_list(
        ["who", "sings", "yellow"]
    )) == sorted(
        ["coldplay"]
    )

    assert sorted(search_pa_list(
        ["what", "album", "is", "numb", "on"]
    )) == sorted(
        ["meteora"]
    )

    assert sorted(search_pa_list(
        ["hello"]
    )) == sorted(
        ["I don't understand"]
    )

    print("All tests passed!")

    query_loop()
