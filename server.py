import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
    "Who is the king of the gods in Greek mythology? \n a. Zeus\n b. Poseidon\n c. Hades\n d. Apollo",
    "Which Greek hero is known for his strength and twelve labors? \n a. Achilles\n b. Perseus\n c. Heracles (Hercules)\n d. Odysseus",
    "Who was the goddess of wisdom, warfare, and crafts? \n a. Aphrodite\n b. Athena\n c. Hera\n d. Demeter",
    "Which mythical creature had the head of a bull and the body of a man? \n a. Centaur\n b. Minotaur\n c. Cyclops\n d. Satyr",
    "Which Greek hero is known for his journey to the underworld to rescue his wife? \n a. Theseus\n b. Orpheus\n c. Jason\n d. Aeneas",
    "What is the name of the winged horse in Greek mythology? \n a. Pegasus\n b. Chiron\n c. Cerberus\n d. Medusa",
    "Who was cursed to turn everything she touched into gold? \n a. Pandora\n b. Medea\n c. Persephone\n d. King Midas",
    "Who was the goddess of love and beauty in Greek mythology? \n a. Hera\n b. Aphrodite\n c. Artemis\n d. Hestia",
    "Which titan was condemned to hold up the heavens for eternity? \n a. Atlas\n b. Prometheus\n c. Cronus\n d. Epimetheus",
    "What was the weapon used by the Greek hero Achilles? \n a. Spear\n b. Bow and arrow\n c. Sword\n d. Shield",
    "Who was the ferryman of the dead in Greek mythology? \n a. Hermes\n b. Hades\n c. Charon\n d. Ares",
    "What creature was half-man and half-goat, known for playing the flute? \n a. Siren\n b. Gorgon\n c. Harpy\n d. Satyr",
    "Who was cursed to turn into a spider after challenging the goddess Athena to a weaving contest? \n a. Arachne\n b. Medusa\n c. Eurydice\n d. Calliope",
    "What was the name of the ship sailed by Jason and the Argonauts in search of the Golden Fleece? \n a. Argo\n b. Odyssey\n c. Athena\n d. Hercules",
    "Who was the queen of the underworld and the wife of Hades? \n a. Persephone\n b. Demeter\n c. Hera\n d. Athena",
    "What was the punishment given to Sisyphus in the underworld? \n a. Chasing his shadow forever\n b. Endless thirst and hunger\n c. Rolling a boulder uphill, only for it to roll back down\n d. Being bound to a fiery wheel",
    "Who was the great hero of the Trojan War, known for his invulnerable heel? \n a. Ajax\n b. Hector\n c. Paris\n d. Achilles",
    "What was the name of the three-headed dog that guarded the gates of the Underworld? \n a. Cerberus\n b. Charybdis\n c. Scylla\n d. Hydra",
    "Who was the goddess of the hunt and the moon in Greek mythology? \n a. Demeter\n b. Artemis\n c. Aphrodite\n d. Hestia",
    "Which Greek hero was known for his intelligence and cunning, especially during the Trojan War? \n a. Odysseus\n b. Heracles\n c. Theseus\n d. Perseus",
]

answers = ['a', 'c', 'b', 'b', 'd', 'a', 'd', 'b', 'a', 'c', 'c', 'a', 'a', 'a', 'c', 'c', 'd', 'a', 'b', 'a']


print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this Greek Mythology Quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d!\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Congrats! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
