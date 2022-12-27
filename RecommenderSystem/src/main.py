import top_genres as tg
import content_based as cb
import collaborative_filtering as cf
import os

def main():
    while True:
        os.system('clear')
        print("0 - Exit")
        print("1 - Top 10 movies by genre")
        print("2 - Top 10 recommendations content-based")
        print("3 - Top 10 collaborative recommendations")
        text = input("Choose option: ")
        if text == "0":
            exit()
        elif text == "1":
            print("Available genres: Action/Adventure/Comedy/Crime/Drama/Family/Fantasy/Romance/Thriller/War")
            genre = input("Choose genre: ")
            print("Top 10 recommended %s movies:" % genre)
            print("=================================")
            print(tg.get_genre_recommendation(genre))
        elif text == "2":
            title = input("Provide a movie title: ")
            print("Top 10 recommended movies based on %s:" % title)
            print("=================================")
            print(cb.get_recommendations(title))
        elif text == "3":
            print("Choose:")
            print("0 - New user")
            print("1 - Existing user")
            option = input("Choose option: ")
            if option == "0":
                print("Choose 3 movie genres:")
                print("Available genres: Action/Adventure/Comedy/Crime/Drama/Family/Fantasy/Romance/Thriller/War")
                g1 = input("1st genre: ")
                g2 = input("2nd genre: ")
                g3 = input("3rd genre: ")
                print("\nTop 10 recommended %s movies:" % g1)
                print("=================================")
                print(tg.get_genre_recommendation(g1))
                print("\nTop 10 recommended %s movies:" % g2)
                print("=================================")
                print(tg.get_genre_recommendation(g2))
                print("\nTop 10 recommended %s movies:" % g3)
                print("=================================")
                print(tg.get_genre_recommendation(g3))
            elif option == "1":
                userId = input("Choose user id: ")
                movieName = input("Choose movie name: ")
                print(cf.hybrid(userId, movieName))
            else:
                print("Option not found. Please try again.")
        else:
            print("Option not found. Please try again.")
        text = input("Press any key to continue...")    
if __name__ == "__main__":
    main()