def make_album(artist, title, songs=None):
    album_dict = {'artist': artist.title(), 'title': title.title()}
    if songs:
        album_dict['songs'] = songs
    return album_dict

album_1 = make_album('the beatles', 'abbey road')
album_2 = make_album('pink floyd', 'the dark side of the moon')
album_3 = make_album('iron maiden', 'the wall', songs=10)

print(album_1)
print(album_2)
print(album_3)