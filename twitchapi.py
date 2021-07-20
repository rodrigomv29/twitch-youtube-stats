import twitch

Client_ID = 'eedwgqusvmegsz5mwo0bm7qofps313'
Client_Secret = 'haxnb9q65oi0efb9mh2bvrjnd4ac4d'

helix = twitch.Helix(Client_ID, Client_Secret)

for user in helix.users(['sodapoppin', 'reckful', 24250859]):
    print(user.display_name)
    # print(user.created_at)
    print(user.view_count)


