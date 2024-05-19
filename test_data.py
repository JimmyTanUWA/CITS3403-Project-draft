from app import db
from app.models import movie

shining=movie(name="Shining", tag="horror", address="https://image.tmdb.org/t/p/original/ji94IIScMTk0SARR3XIgBgLjuYB.jpg",
              rating="8.4/10", release_date="May 23, 1980", runtime="146 minutes", 
              plot="The story follows Jack Torrance, an aspiring writer and recovering alcoholic, who takes a job as the winter caretaker of the isolated Overlook Hotel in the Colorado Rockies. Jack moves in with his wife, Wendy, and his young son, Danny, who possesses psychic abilities known as 'the shining.' As the winter snow traps them in the hotel, Jack's sanity begins to unravel, influenced by the malevolent spirits haunting the Overlook and the hotel's dark history.")
spirited=movie(name="Spirited Away", tag="animation", address="https://pic.nximg.cn/file/20170618/9413594_232044240000_2.jpg",
              rating="8.6/10", release_date="July 20, 2001", runtime="125 minutes", 
              plot="The film tells the story of Chihiro Ogino, a sullen ten-year-old girl who, while moving to a new neighborhood, becomes trapped in an alternate reality that is inhabited by spirits and monsters. After her parents are transformed into pigs by the witch Yubaba, Chihiro takes a job working in Yubaba's bathhouse to find a way to free herself and her parents and return to the human world.")
lala=movie(name="La La Land", tag="romance", address="https://media.themoviedb.org/t/p/w440_and_h660_face/5yCZrZT4REVfYhNczVyWk5593aZ.jpg",
              rating="8.1/10", release_date="December 9, 2016", runtime="128 minutes", 
              plot="This film follows the story of a couple aspiring to become Hollywood stars, navigating through love, ambition, and challenges on their pursuit of dreams. It blends romantic love with musical theater, showcasing the ups and downs of the protagonists' journey towards their dreams.")
budapest=movie(name="The Grand Budapest Hotel", tag="comedy", address="https://media.themoviedb.org/t/p/w440_and_h660_face/lGJWIUSKmcnnxeGTtxb0Qob05Bv.jpg",
               rating="8.1/10", release_date="March 7, 2014", runtime="99 minutes",
               plot="In the fictional Republic of Zubrowka, a legendary concierge named Gustave H. and his loyal lobby boy, Zero Moustafa, become embroiled in a series of adventures involving a priceless painting, a family inheritance, and the changing landscape of Europe between the World Wars. ")
ring2=movie(name="Ring2", tag="horror", address="https://image.tmdb.org/t/p/original/HREqYQWkGnH2viRQEXupCSX7ID.jpg", 
            rating="5.4/10", release_date="March 18, 2005", runtime="110 minutes",
            plot="In 'Ring 2', the sequel to the terrifying 'Ring', the curse of the videotape continues to haunt those who have seen it. Investigative journalist Mai Takano tries to uncover the mystery behind the deadly tape while protecting her young son from its evil grasp.")
totoro=movie(name="My Neighbor Totoro", tag="animation", address="https://image.tmdb.org/t/p/original/bPBYikmzC8vP1Njdm6iUQv8eTKD.jpg",
             rating="8.2/10", release_date="April 16, 1988", runtime="86 minutes",
             plot="In 'My Neighbor Totoro', two young sisters, Satsuki and Mei, move to the countryside with their father and discover magical creatures living in the nearby forest, including the friendly giant spirit Totoro. As they explore their new surroundings, they embark on enchanting adventures and form a deep connection with the natural world.")
gone=movie(name="Gone With Wind", tag="romance", address="https://image.tmdb.org/t/p/original/wFkNY16JaUImuvBIBbYCaAG3RH0.jpg",
           rating="8.1/10", release_date="December 15, 1939", runtime="238 minutes",
           plot="Set against the backdrop of the American Civil War and Reconstruction era, 'Gone with the Wind' follows the story of Scarlett O'Hara, a headstrong Southern belle, and her tumultuous romantic entanglements with the charming rogue Rhett Butler and the honorable Ashley Wilkes. As Scarlett struggles to navigate the challenges of war and societal upheaval, her resilience and determination define her journey through love, loss, and survival in a changing world.")
home=movie(name="Home Alone", tag="comedy", address="https://image.tmdb.org/t/p/original/onTSipZ8R3bliBdKfPtsDuHTdlL.jpg",
           rating="7.6/10", release_date="November 16, 1990", runtime="103 minutes",
           plot="In 'Home Alone', 8-year-old Kevin McCallister is accidentally left behind when his family flies to Paris for Christmas. While home alone, Kevin must protect his house from two bumbling burglars, Harry and Marv, using an array of creative and hilarious booby traps. As Kevin learns to fend for himself and embrace the spirit of the holiday season, chaos and laughter ensue in this heartwarming comedy classic.")
dune=movie(name="Dune", tag="sci-fi", address="https://image.tmdb.org/t/p/original/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
           rating="7.5/10", release_date="October 22, 2021", runtime="155 minutes",
           plot="In 'Dune', set in a distant future, it follows the story of Paul Atreides, a young nobleman whose family assumes control of the desert planet Arrakis. As the only source of the most valuable substance in the universe, Arrakis becomes the target of rival noble families and political intrigue. Paul must navigate this dangerous landscape, unlock his latent powers, and lead a rebellion against oppressive forces.")
phantom=movie(name="Star Wars: Episode I - The Phantom Menace", tag="sci-fi", address="https://image.tmdb.org/t/p/original/6wkfovpn7Eq8dYNKaG5PY3q2oq6.jpg",
              rating="6.5/10", release_date="May 19, 1999", runtime="136 minutes",
              plot="In 'Star Wars: Episode I - The Phantom Menace', set decades before the original trilogy, the Galactic Republic is threatened by a trade blockade imposed by the Trade Federation. Jedi Knights Qui-Gon Jinn and Obi-Wan Kenobi are sent to negotiate, leading them into a complex web of events involving young Anakin Skywalker, who possesses incredible potential in the Force. As tensions escalate and dark forces stir, the fate of the galaxy hangs in the balance.")
smith=movie(name="Mr. & Mrs. Smith", tag="action", address="https://image.tmdb.org/t/p/original/wzIO3ytxeSNt1wRpXLIdkNbGoDm.jpg",
            rating="6.5/10", release_date="June 10, 2005", runtime="120 minutes",
            plot="In 'Mr. & Mrs. Smith', John and Jane Smith appear to be a typical suburban couple, but they are actually highly skilled assassins working for competing organizations. When they discover each other's true identities, their marriage is put to the ultimate test as they are assigned to eliminate one another. As they engage in a deadly game of cat and mouse, John and Jane must navigate their personal and professional lives while keeping their lethal secrets from each other.")
kill=movie(name="Kill Bill", tag="action", address="https://image.tmdb.org/t/p/original/tf1nUtw3LJGUGv1EFFi23iz6ngr.jpg",
           rating="8.1/10", release_date="October 10, 2003", runtime="111 minutes",
           plot="A former assassin known as The Bride seeks revenge on her ex-colleagues who betrayed her on her wedding day. Left for dead, she awakens from a coma with a fierce determination to eliminate each member of the Deadly Viper Assassination Squad. Armed with deadly skills and driven by vengeance, The Bride embarks on a relentless quest for retribution, leading to intense and stylized confrontations.")
shawshank=movie(name="The Shawshank Redemption", tag="drama", address="https://image.tmdb.org/t/p/original/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg",
                rating="9.3/10", release_date="September 23, 1994", runtime="142 minutes",
                plot="Banker Andy Dufresne is wrongly convicted of murder and sentenced to life in Shawshank State Penitentiary. Despite harsh conditions, Andy befriends inmate Red and uses his skills to navigate prison life, all while planning a daring escape.")
gump=movie(name="Forrest Gump", tag="drama", address="https://image.tmdb.org/t/p/original/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
           rating="8.8/10", release_date="July 6, 1994", runtime="142 minutes",
           plot="Forrest Gump recounts the extraordinary life journey of a man with limited intelligence. Despite facing various challenges, Forrest achieves remarkable success in multiple fields and demonstrates unwavering loyalty and love for his childhood friend, Jenny. He unwittingly becomes a witness to significant historical events, touching the lives of many and proving that simplicity and kindness can lead to profound impact and happiness.")
harry1=movie(name="Harry Potter and the Sorcerer's Stone", tag="adventure", address="https://image.tmdb.org/t/p/original/czc2qzAYReO8DaALtQnZSF7FmGy.jpg",
             rating="7.6/10", release_date="November 16, 2001", runtime="152 minutes",
             plot="young Harry Potter discovers he is a wizard on his eleventh birthday and enrolls at Hogwarts School of Witchcraft and Wizardry. Alongside his friends Hermione Granger and Ron Weasley, Harry uncovers secrets about his past and confronts dark forces threatening the wizarding world, learning valuable lessons about courage and friendship along the way.")
harry2=movie(name="Harry Potter and the Chamber of Secrets", tag="adventure", address="https://media.themoviedb.org/t/p/w440_and_h660_face/sdEOH0992YZ0QSxgXNIGLq1ToUi.jpg",
             rating="7.4/10", release_date="November 15, 2002", runtime="161 minutes",
             plot="Harry returns to Hogwarts for his second year and discovers a hidden chamber within the school that holds dark secrets. With Hermione Granger and Ron Weasley by his side, Harry investigates the chamber to confront the malevolent presence endangering Hogwarts. Through bravery and friendship, Harry uncovers the truth and faces the challenges posed by the Chamber of Secrets.")
db.session.add(harry2)
db.session.commit()

