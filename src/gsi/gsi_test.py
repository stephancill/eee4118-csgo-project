from server import GSIServer
import time

if __name__ == "__main__":
    # pipenv run python src/gsi/gsi.py
    server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    server.start_server()
    print("done")

    ammo = 0
    while True:
        print(server.gamestate.payload)
        new_ammo = server.gamestate.player.weapons["weapon_3"]["ammo_clip"]
        if ammo != new_ammo:
            ammo = new_ammo
            print("ammo", ammo)

        print(server.gamestate.payload)
        
        time.sleep(1)