def make_album(artist, title):
    return {'artist': artist.title(), 'title': title.title()}

while True:
    print("\nPlease tell me about an album:")
    print("(enter 'q' at any time to quit)")
    
    artist = input("Who is the artist? ")
    if artist == 'q':
        break
        
    title = input("What is the title? ")
    if title == 'q':
        break
        
    album = make_album(artist, title)
    print(album)