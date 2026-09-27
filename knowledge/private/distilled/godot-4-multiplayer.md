<!-- 1 Setting up a Server (pp. 3-18) -->
---
name: godot-enet-server-setup
topic: Godot 4 networking — server creation with ENetMultiplayerPeer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 1 (pp. 3-18)"]
---

## Rules
- Create the server peer with `ENetMultiplayerPeer.new()` then call `peer.create_server(PORT)`. Only the port argument is mandatory.
- Assign the peer to the node's built-in `multiplayer.multiplayer_peer` property; without this assignment the peer is inert. WHY: `multiplayer` is the per-node `MultiplayerAPI` instance that actually drives the connection.
- Use port `9999` as the project default and keep it identical on client and server. WHY: mismatched ports mean the peers never find each other.
- Use `"localhost"` as the address for local testing; it resolves to the local machine's own IP. WHY: avoids hardcoding a LAN IP while developing.
- `create_server()` optional arguments and their defaults:
  | Arg | Meaning | Default |
  |---|---|---|
  | `max_clients` | max simultaneous clients | 4095 |
  | `max_channels` | channels per client | unlimited |
  | `in_bandwidth` | max incoming bandwidth per client | unlimited |
  | `out_bandwidth` | max outgoing bandwidth per client | unlimited |
- Connect `multiplayer.peer_connected` to a callback taking `peer_id` to detect new clients. WHY: this is the only signal that tells you a handshake succeeded.
- Capture the return value of `create_server()`/`create_client()` into a variable and check it for errors. WHY: the call returns an error code rather than throwing.
- Verify a successful handshake by printing the `peer_id` received in `_on_peer_connected` on the server instance.

## Checklist
- [ ] `PORT` constant defined once and reused by both scripts.
- [ ] `peer` created with `ENetMultiplayerPeer.new()` before `_ready()` runs.
- [ ] `create_server(PORT)` called inside `_ready()`.
- [ ] `multiplayer.multiplayer_peer = peer` assigned after creation.
- [ ] `peer_connected` signal connected to a handler with a `peer_id` parameter.
- [ ] Server scene saved and run before the client attempts to connect.
- [ ] Error code from `create_server()` inspected.

## Anti-patterns
- Forgetting `multiplayer.multiplayer_peer = peer` — the peer object exists but nothing is listening.
- Hardcoding a LAN/public IP during development instead of `"localhost"`.
- Using different port numbers in client and server scripts.
- Assuming the server must be started after the client; the server must be listening first or the client's connect attempt fails.

---
name: godot-enet-client-setup
topic: Godot 4 networking — client connection with ENetMultiplayerPeer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 1 (pp. 3-18)"]
---

## Rules
- Create the client with `ENetMultiplayerPeer.new()` then `peer.create_client(ADDRESS, PORT)`. Address and port are the only required arguments.
- The address argument accepts either an IP string or a hostname.
- Assign the peer to `multiplayer.multiplayer_peer` immediately after `create_client()`. WHY: same as the server — the peer does nothing until registered with the node's MultiplayerAPI.
- `create_client()` optional arguments and their defaults:
  | Arg | Meaning | Default |
  |---|---|---|
  | `channel_count` | channels used to talk to the server | 1 |
  | `in_bandwidth` | max incoming bandwidth per connection | 0 (unlimited) |
  | `out_bandwidth` | max outgoing bandwidth per connection | 0 (unlimited) |
  | `local_port` | local port to bind to | 0 |
- Keep `ADDRESS` and `PORT` as constants at the top of the client script so they are easy to swap per environment.
- The client script needs no signal connections to establish the handshake; the server side observes the connection.

## Checklist
- [ ] `ADDRESS` constant set (`"localhost"` for local tests).
- [ ] `PORT` constant matches the server's port exactly.
- [ ] `peer.create_client(ADDRESS, PORT)` called in `_ready()`.
- [ ] `multiplayer.multiplayer_peer = peer` assigned.
- [ ] Server instance already running and listening before the client scene loads.

## Anti-patterns
- Calling `create_client()` before the server is listening and expecting a retry — there is no automatic reconnect here.
- Setting `channel_count` lower than the number of distinct data streams you plan to separate.
- Leaving bandwidth arguments at defaults when you intend to cap traffic; `0` means unlimited, not zero.

---
name: godot-multi-instance-testing
topic: Testing multiplayer locally with Godot's multiple-instance debugger
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 1 (pp. 3-18)"]
---

## Rules
- Enable extra debug instances via **Debug | Run Multiple Instances** (up to 4 options). Use 2 for a basic client/server test.
- Running the project with multiple instances launches N copies of the *same* scene, so build a role-selection menu instead of relying on separate run configurations.
- Menu structure: `Control` root named `MainMenu` → one `Label` ("Are you a...") + two `Button` nodes (`ClientButton`, `ServerButton`), centered.
- Wire each button's `pressed` signal to a handler that calls `get_tree().change_scene_to_file("res://Client.tscn")` or `"res://Server.tscn"`.
- Test order: press the server button in one instance first, then the client button in the other. WHY: the server must be listening before the client connects.
- Success criterion: the server instance's console prints the connecting client's `peer_id`.

## Checklist
- [ ] Multiple-instance count set to 2 in the Debug menu.
- [ ] MainMenu scene saved before running.
- [ ] Both button `pressed` signals connected to their handlers.
- [ ] Scene paths in `change_scene_to_file()` match the actual `.tscn` file names.
- [ ] Server instance started before client instance.

## Anti-patterns
- Running the project without the multi-instance option and wondering why only one window appears.
- Launching the client first and treating the failed connection as a code bug.
- Building separate export presets just to test two roles locally.

---
name: udp-vs-tcp-for-games
topic: Choosing a transport protocol for real-time multiplayer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 1 (pp. 3-18)"]
---

## Rules
- Use UDP-based transport (ENet) for real-time gameplay. WHY: UDP is connectionless, so it avoids handshake/acknowledgement overhead and keeps latency low.
- Prefer UDP when the latest state matters more than the full history — e.g. avatar positions: drop stale updates and apply only the newest.
- Accept that UDP gives no delivery guarantee, no ordering, and no duplicate suppression; design the game to tolerate packet loss and delay.
- Use TCP only where every byte must arrive in order and latency is not critical (e.g. turn-based or lobby/account traffic).
- Treat these three network quantities as distinct design constraints:
  | Term | Definition |
  |---|---|
  | Latency | time between sending and receiving data |
  | Throughput | how much data a route can carry per time period before being overwhelmed |
  | Bandwidth | size of the available communication channel |
- Use ENet's multi-channel support to separate independent data streams (e.g. voice vs. gameplay) over one connection.

## Checklist
- [ ] Decided per data type whether loss is acceptable (positions, input) or not (chat, purchases).
- [ ] Confirmed the game logic can discard out-of-order/stale packets.
- [ ] Planned mitigation for packet loss and jitter in later iterations.

## Anti-patterns
- Using TCP for per-frame position updates: every client must acknowledge every packet and ordering must be preserved, which stalls real-time play.
- Assuming UDP unreliability is purely a drawback — for game state it is the reason the transport stays responsive.
- Treating latency, throughput, and bandwidth as interchangeable; they constrain different parts of the design.

> CHECK: The chapter mentions a `create_server()` return value being stored in an `error` variable in the full script but the printed listing omits the assignment in one place — verify the exact final code against the book's GitHub repo.

<!-- 2 Sending and Receiving Data (pp. 19-46) -->
---
name: udp-packet-basics
topic: UDP packet fundamentals for games
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Use UDP for real-time gameplay data (positions, inputs, reactions) because it is fast and does not wait for per-packet acknowledgement; use TCP only when ordered, guaranteed delivery matters more than latency.
- Treat every UDP packet as self-contained: it must carry all addressing and payload info, since UDP has no connection state and no handshake.
- Never assume packet order or arrival. Design receivers to tolerate missing, duplicated, or reordered packets.
- Serialize only the fields the receiver needs to reconstruct the object (e.g. position, rotation, scale, texture path) instead of sending whole objects or binary blobs. WHY: smaller bandwidth, no executable code over the wire, safer and more reliable.
- Use JSON as the default serialization format for low-frequency messages (login, avatar, session checks) because it is human-readable and debuggable.
- In Godot 4, serialize with `JSON.stringify(data)` and deserialize with `JSON.parse_string(text)`; both map JSON values to native GDScript types (dicts, arrays, numbers, bools, strings).
- Use `PacketPeerUDP` on the client and `UDPServer` on the server; these are the low-level Godot 4 classes for raw UDP.
- Pick a fixed port constant (the book uses 9999) and a fixed address constant (127.0.0.1 for local testing) shared by client and server.

## Checklist
- [ ] Every message is a dictionary with a top-level "command" key (e.g. `authenticate_credentials`, `get_authentication_token`, `get_avatar`).
- [ ] Payload contains only reconstructable state, never node references or code.
- [ ] Client and server agree on the same port and address constants.
- [ ] Receiver handles unknown/missing keys without crashing.

## Anti-patterns
- Sending Godot objects or binary node data directly over the network.
- Relying on UDP ordering or delivery guarantees.
- Using JSON for high-frequency per-frame state (bandwidth and parse cost); use it for event-style messages instead.
- Hardcoding different ports/addresses on client and server.

> CHECK: The chapter does not specify a recommended packet size limit or MTU; verify against Godot docs if you need fragmentation guidance.

---
name: udp-client-send-receive
topic: Client-side UDP send and receive with PacketPeerUDP
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Create a peer per request with `PacketPeerUDP.new()`, then `packet.connect_to_host(ADDRESS, PORT)` before sending.
- Send with `packet.put_var(JSON.stringify(message))`; the peer serializes the string for transport.
- Wait for the reply with `while packet.wait() == OK:` — `wait()` returns `OK` when a packet arrives, otherwise an error constant.
- Deserialize the reply with `JSON.parse_string(packet.get_var())` before inspecting it.
- Branch on the presence of expected keys using the `in` operator (e.g. `if "token" in response:`), not on truthiness of the whole dict.
- `break` out of the wait loop after handling the first valid response to avoid blocking the game loop indefinitely.
- Store session state (user, token) in an Autoload singleton so it survives scene changes.

## Checklist
- [ ] Peer created and connected before `put_var`.
- [ ] Message serialized with `JSON.stringify`.
- [ ] Wait loop exits on success and on failure.
- [ ] Response validated by key presence before use.
- [ ] On success: update UI, store token/user, change scene, break.
- [ ] On failure: show error label, break.

## Anti-patterns
- Calling `packet.wait()` in a loop without a break condition (hangs the client).
- Assuming the response always contains the expected key.
- Storing the session token in a scene-local variable instead of an Autoload.

---
name: udp-server-listen-poll
topic: Server-side UDP listening with UDPServer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Create the server once: `var server = UDPServer.new()`.
- Bind the port in `_ready()` with `server.listen(PORT)`.
- Poll in `_process(delta)` with `server.poll()`; it is non-blocking, so it is safe in the game loop.
- Only call `server.take_connection()` when `server.is_connection_available()` returns true; `take_connection()` returns a `PacketPeerUDP` for that client.
- Read the message with `JSON.parse_string(peer.get_var())` and dispatch on a top-level command key.
- Use an `if/elif` chain on command keys (`authenticate_credentials`, `get_authentication_token`, `get_avatar`) to route to handler functions.
- Pass the `peer` into every handler so the handler can reply to the correct client.

## Checklist
- [ ] `listen(PORT)` called once in `_ready()`.
- [ ] `poll()` called every frame.
- [ ] `is_connection_available()` checked before `take_connection()`.
- [ ] Message parsed and dispatched by command key.
- [ ] Each handler replies via `peer.put_var(JSON.stringify(response))`.

## Anti-patterns
- Blocking the main loop while waiting for packets.
- Calling `take_connection()` without checking availability.
- Replying to a different peer than the one that sent the request.

---
name: json-serialization
topic: JSON serialization and deserialization in Godot 4
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Serialization = convert a complex object into a linear, transmittable representation; deserialization = rebuild it on the other side.
- Use `JSON.stringify(value)` to turn a dictionary/array/primitive into a JSON string.
- Use `JSON.parse_string(text)` to turn a JSON string back into GDScript types (dict, array, number, bool, string).
- Cherry-pick only the fields needed for reconstruction (e.g. `position`, `rotation`, `scale`, `texture_path` for a Sprite2D).
- Prefer JSON over binary for messages where debuggability matters; JSON is human-readable and editable in a text editor.
- Use `FileAccess.open(path, FileAccess.READ)` + `get_as_text()` + `JSON.parse_string()` to load JSON files from disk.

## Checklist
- [ ] Every network message is a dictionary serialized with `JSON.stringify`.
- [ ] Every received payload is parsed with `JSON.parse_string` before access.
- [ ] Only necessary fields are included in the payload.
- [ ] File-based JSON loaded via `FileAccess` with `FileAccess.READ`.

## Anti-patterns
- Sending raw objects or binary blobs instead of serialized data.
- Parsing JSON without checking for null/parse failure.
- Including executable code or full node dumps in the payload.

---
name: authentication-flow
topic: UDP login and session-token authentication flow
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Client sends `{"authenticate_credentials": {"user": ..., "password": ...}}` to the server.
- Server validates keys exist (`"user" in credentials and "password" in credentials`) before touching values.
- Server looks up the user in the database; if the user exists and the password matches, generate a token with `randi()`.
- Store the token server-side in a `logged_users` dictionary keyed by username.
- Reply with `{"token": token}` on success; reply with an empty string `""` on failure.
- Client stores the token in an Autoload (`AuthenticationCredentials.session_token`) so it persists across scenes.
- For later requests, client sends `{"get_authentication_token": true, "user": ..., "token": ...}`; server compares the supplied token against `logged_users[user]`.
- For avatar requests, client sends `{"get_avatar": true, "token": ..., "user": ...}`; server re-validates the token before returning avatar data.
- Server replies to avatar requests with `{"avatar": path, "name": nick}`; client loads the texture with `load(path)` and assigns it to a `TextureRect`.

## Checklist
- [ ] Credentials validated for key presence before use.
- [ ] Token generated and stored server-side per user.
- [ ] Token echoed to client and stored in Autoload.
- [ ] Every subsequent request re-validates the token.
- [ ] Failed auth returns an empty/failure response, not a token.

## Anti-patterns
- Trusting client-supplied user/token without server-side lookup.
- Storing the token only in a scene-local variable.
- Skipping token validation on later requests (avatar, session refresh).
- Shipping a plain-text password JSON database to production (the book explicitly warns this is educational only).

> CHECK: The book uses `randi()` for tokens; this is not cryptographically secure. Verify a secure token source before production use.

---
name: autoload-session-state
topic: Autoload singleton for client session state
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Create a scene with a `Node` root named `AuthenticationCredentials` and attach `AuthenticationCredentials.gd`.
- Declare `var user = ""` and `var session_token = ""` as the persistent session fields.
- Register the scene under Project Settings → Autoload with the name `AuthenticationCredentials` so it is globally accessible.
- Access fields from any script via `AuthenticationCredentials.user` / `AuthenticationCredentials.session_token`.
- Keep this Autoload on the client only; remove it from the server application.

## Checklist
- [ ] Autoload scene registered with the exact name used in code.
- [ ] Fields initialized to safe defaults (empty string).
- [ ] Autoload excluded from the server build.

## Anti-patterns
- Passing credentials manually between scenes via signals or `get_node` chains.
- Leaving the client-only Autoload in the server project.
- Storing credentials in a scene that gets freed on scene change.

---
name: json-file-database
topic: JSON file as a fake database (educational)
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 2 (pp. 19-46)"]
---
## Rules
- Structure: top-level dict keyed by username, each value a dict with `password`, `avatar` (resource path), and `name`.
- Load once at server startup in `_ready()` via `load_database(database_file_path)`.
- Load with `FileAccess.open(path, FileAccess.READ)` → `get_as_text()` → `JSON.parse_string()`.
- Keep the database file on the server only; never ship it to the client.
- Accept this approach only for prototypes/learning: JSON files do not scale to many concurrent users and lack query flexibility.

## Checklist
- [ ] Database loaded once at server start, not per request.
- [ ] Database file excluded from the client export.
- [ ] Passwords stored hashed (not plain text) before any real deployment.

## Anti-patterns
- Shipping the JSON database inside the client project.
- Storing plain-text passwords in production.
- Re-reading the database file on every request.
- Using JSON files as the database for a large concurrent-user game.

<!-- 3 Making a Lobby to Gather Players Together (pp. 47-72) -->
---
name: rpc-annotation-options
topic: Godot 4 @rpc annotation configuration
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Mark every function that must be callable over the network with `@rpc`; unmarked functions cannot be invoked remotely.
- Choose the **call mode**:
  - `call_remote` (default): executes only on other peers, not on the caller's local instance.
  - `call_local`: also executes on the caller's own instance — use when the caller must stay in sync with everyone else.
- Choose the **caller permission**:
  - `authority` (default): only the node's multiplayer authority may invoke it — use for server-driven state changes.
  - `any_peer`: any connected peer may invoke it — use for client→server requests (login, avatar fetch).
- Choose the **transfer mode**:
  - `reliable` (default): guaranteed delivery — use for authentication, chat messages, one-shot events.
  - `unreliable`: may drop or reorder — use for data where only the newest value matters.
  - `unreliable_ordered`: may drop but never reorders — use for position/state streams.
- Pass the channel number as an **integer and always as the last argument**; option order otherwise does not matter.
- Separate traffic by channel: e.g. channel 0 reliable for messages, channel 1 unreliable_ordered for positions, so a slow reliable stream never blocks position updates.
- WHY: defaults are safe but chatty; explicit options prevent both dropped critical data and head-of-line blocking.

## Checklist
- [ ] Every network-facing function carries `@rpc` with explicit options (don't rely on defaults silently).
- [ ] Channel argument, if used, is the final argument and is an int.
- [ ] Reliable channel reserved for events that must not be lost.
- [ ] Unreliable_ordered channel used for continuous state streams.
- [ ] Caller permission matches trust model: `any_peer` only for requests the server validates.

## Anti-patterns
- `@rpc(2, "any_peer", "unreliable_ordered")` — channel first; the annotation is silently invalid.
- Using `reliable` for per-frame position updates: wastes bandwidth and can stall the channel.
- Using `unreliable` for login/authentication: a dropped packet leaves the client stuck.
- Leaving `any_peer` on a function that mutates authoritative state without server-side validation.

> CHECK: OCR shows `@rpc("unreliable_order", ...)` in one example — verify the exact spelling is `unreliable_ordered`.

---
name: rpc-requirements-and-nodepath
topic: Prerequisites for RPC to work
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Establish an `ENetMultiplayerPeer` connection and assign it to `multiplayer.multiplayer_peer` before any RPC can be sent; RPCs outside an established ENet connection do nothing.
- The `NodePath` of the RPC target node must be **identical on every peer**. Mismatched paths mean the call is dropped or delivered to the wrong node.
- Give the root node of every networked scene the same name (the book uses `Main`) so paths line up across scenes.
- Every node that participates in RPC must declare **all** `@rpc` methods used anywhere in the network, even methods it never calls or implements (empty bodies are fine).
- The `@rpc` options on a shared method do **not** have to match between classes; only the method signature must exist.
- WHY: Godot resolves RPCs by node path plus method name; a missing method or divergent path breaks the call silently.

## Checklist
- [ ] `multiplayer.multiplayer_peer` assigned on server and every client.
- [ ] Root node name identical across all networked scenes.
- [ ] All `@rpc` method signatures duplicated in every participating script.
- [ ] Method names and parameter counts identical everywhere.

## Anti-patterns
- Different root node names per scene (e.g. `ServerLobby` vs `ClientLobby`) — paths diverge.
- Implementing an RPC only on the class that uses it — other peers fail to resolve it.
- Assuming RPCs work before the peer connection is set up.

---
name: multiplayer-authority
topic: Multiplayer authority and peer IDs
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Treat the multiplayer authority as the single peer allowed to decide a node's state; normally the server/host.
- Read the current authority with `Node.get_multiplayer_authority()`; change it with `Node.set_multiplayer_authority(peer_id)`.
- Identify the sender of an RPC with `multiplayer.get_remote_sender_id()`; use it to reply to the correct peer.
- Send a reply to one specific peer with `rpc_id(peer_id, "method", args...)`; broadcast to all with `rpc("method", args...)`.
- Keep authority over security-relevant nodes (health, inventory, score) on the server.
- WHY: a single decision-maker prevents conflicting concurrent writes and stops clients from cheating.

## Checklist
- [ ] Server holds authority for all gameplay-critical nodes.
- [ ] Client→server requests use `get_remote_sender_id()` to route the response.
- [ ] `set_multiplayer_authority()` used only where a client legitimately owns a node (e.g. its own input-driven avatar).

## Anti-patterns
- Granting a client authority over its own health/score node — the client can self-modify and become unkillable.
- Broadcasting a private response (session token, error) with `rpc()` instead of `rpc_id()`.
- Assuming authority is always the server without checking.

---
name: udp-vs-enet-choice
topic: Choosing between raw UDP and ENetMultiplayerPeer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Default to `ENetMultiplayerPeer` + RPCs for game networking: it handles connection management, ordering, and error correction.
- Use `UDPServer`/`PacketPeerUDP` only when you need fine-grained control over packet layout or timing that ENet cannot express.
- With raw UDP you must serialize/deserialize, poll for packets, and build your own request/response protocol; with RPCs you call a function and pass arguments.
- ENetMultiplayerPeer supports up to roughly 4,095 simultaneous connections.
- RPCs cannot transmit objects (nodes/resources) directly — send serialized data or a path/ID and reconstruct on the other side.
- WHY: the high-level API removes the most error-prone parts (packet loss, ordering, request routing) and shortens development time.

## Checklist
- [ ] Chosen transport justified: ENet unless a concrete low-level need exists.
- [ ] Any object sent over RPC is serialized to primitives or referenced by ID/path.
- [ ] Connection limits considered against expected player count.

## Anti-patterns
- Hand-rolling packet polling and request IDs when RPCs would do the job.
- Sending a `Node` or `Resource` as an RPC argument.
- Mixing raw UDP and ENet for the same logical channel without a clear reason.

---
name: lobby-authentication-flow
topic: Server-authoritative login with session tokens
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Server setup: `peer.create_server(PORT)` (book uses port 9999), then `multiplayer.multiplayer_peer = peer`, then load the user database.
- Load the fake database once at startup: `FileAccess.open(path, FileAccess.READ)` → `get_as_text()` → `JSON.parse_string()` into a dictionary.
- Client sends credentials with `rpc_id(get_multiplayer_authority(), "authenticate_player", user, password)`.
- Server validates in this order: user exists → password matches → generate token with `randi()` → store `logged_users[user] = token` → `rpc_id(peer_id, "authentication_succeed", token)`.
- On failure, reply `rpc_id(peer_id, "authentication_failed", message)` with a human-readable reason (e.g. "User doesn't exist").
- Client stores `user` and `session_token` in an autoload singleton (`AuthenticationCredentials`) so later scenes can reuse them, then switches scene to the lobby.
- Every later privileged request must re-send the session token and be validated server-side against `logged_users`.
- WHY: tokens let the server trust subsequent RPCs without re-sending the password, and the singleton survives scene changes.

## Checklist
- [ ] Server: create peer → assign `multiplayer_peer` → load database, in that order.
- [ ] `authenticate_player` and `retrieve_avatar` marked `@rpc("any_peer", "call_remote")`.
- [ ] `authentication_succeed` / `authentication_failed` marked `@rpc` (authority-only).
- [ ] Token stored server-side in `logged_users` and client-side in the autoload.
- [ ] Scene change to lobby only after a successful token reply.

## Anti-patterns
- Trusting a client-supplied username without a token on later requests.
- Sending the password again for each subsequent action.
- Storing credentials only in the scene — they are lost on scene change.

---
name: lobby-avatar-sync
topic: Synchronizing lobby avatars across peers
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Client requests its avatar on `_ready()`: `rpc_id(get_multiplayer_authority(), "retrieve_avatar", user, session_token)`.
- Server validates in `retrieve_avatar`: user present in `logged_users`, then `session_token == logged_users[user]`; return early otherwise.
- On success, rebuild the whole list rather than appending: `rpc("clear_avatars")` first, then loop `logged_users` and `rpc("add_avatar", name, texture_path)` for each.
- `clear_avatars()` iterates `container.get_children()` and calls `queue_free()` on each.
- `add_avatar()` instantiates the avatar card, adds it to the container, `await get_tree().process_frame`, then calls `update_data(name, path)`.
- WHY: full rebuild guarantees every peer shows the same ordered list; the one-frame await ensures the card's nodes exist before writing to them.

## Checklist
- [ ] `retrieve_avatar` guarded by both login check and token match.
- [ ] Clear-then-rebuild, never append-only.
- [ ] `await get_tree().process_frame` between `add_child` and `update_data`.
- [ ] Avatar container is a deterministic-order container (e.g. `HBoxContainer` inside `ScrollContainer`).

## Anti-patterns
- Appending new avatars without clearing — duplicates appear for players who joined earlier.
- Calling `update_data()` immediately after `add_child()` without awaiting the frame.
- Skipping the token check in `retrieve_avatar`, letting any peer enumerate avatars.

---
name: lobby-testing-multi-instance
topic: Testing a lobby with multiple Godot instances
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 3 (pp. 47-72)"]
---
## Rules
- Use Debug → Run Multiple Instances → Run 3 Instances to simulate one server and two clients.
- Instance 1: press Server. Instances 2 and 3: press Client, then log in with distinct credentials (`user1`/`test`, `user2`/`test`).
- Verify after the second login that **both** client windows show the same two avatars in the same order.
- WHY: the second login is the real test — it exercises the clear-and-rebuild path, not just the initial load.

## Checklist
- [ ] Server instance started before any client connects.
- [ ] First client sees exactly one avatar after login.
- [ ] Second client login results in two avatars on both clients, same order.
- [ ] No duplicate or stale avatar cards after the second join.

## Anti-patterns
- Testing with a single client only — misses the resync bug entirely.
- Reusing the same credentials on two clients, which collides in `logged_users`.

<!-- 4 Creating an Online Chat (pp. 73-82) -->
---
name: rpc-reliability-and-channels
topic: Godot 4 RPC reliability modes and channel separation
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 4 (pp. 73-82)"]
---
## Rules
- Use `"reliable"` for chat messages, inventory changes, score updates, and any data where order and delivery must be guaranteed. WHY: reliable transport retransmits and reorders, so the conversation stays coherent.
- Use unreliable (omit `"reliable"`) for high-frequency, self-correcting data such as player position or real-time movement updates. WHY: unreliable is faster and cheaper; a dropped position packet is replaced by the next one.
- Assign each data category its own channel by passing an integer as the last argument of `@rpc(...)`. Default is channel 0. Example split: channel 0 = general, channel 1 = game state, channel 2 = chat.
- Keep chat on a dedicated channel (the chapter uses channel 2). WHY: a reliable channel blocks its own queue while waiting for retransmission; if chat shares a channel with movement, a slow chat packet stalls movement.
- Channel numbers must match on every peer for the same RPC method. WHY: the channel is part of the RPC routing, not a per-call choice.
- Use channels to isolate failure: loss or corruption on one channel does not affect others. WHY: prevents desync and corrupted game data from spreading across systems.

## Checklist
- [ ] List every RPC method and tag it reliable or unreliable.
- [ ] Group RPCs by data type and assign a distinct channel integer per group.
- [ ] Verify no high-frequency unreliable data shares a channel with reliable data.
- [ ] Confirm the same channel number is used on all peers for each method.

## Anti-patterns
- Putting all RPCs on channel 0 (default) — one congested queue blocks everything.
- Sending chat or state changes unreliably — messages can be lost or reordered.
- Sending per-frame movement reliably — retransmits pile up and add latency.
- Using a channel number on one peer that differs from another — calls silently fail to route.

---
name: chat-message-rpc
topic: Implementing a chat message RPC and input handler
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 4 (pp. 73-82)"]
---
## Rules
- Annotate the display method with `@rpc("any_peer", "call_local", "reliable", 2)` so any peer can trigger it, the sender also sees its own message, and delivery is guaranteed on the chat channel.
- Format the line as `"%s: %s" % [avatar_name, message]` and append with a newline to the existing label text.
- After appending, set `container.scroll_vertical = label.size.y` to auto-scroll to the newest message. WHY: without it the player sees stale history and misses new messages.
- Connect `LineEdit.text_submitted` to a handler; inside it, return early if `new_text == ""`. WHY: blocks empty/whitespace-only messages from being broadcast.
- Broadcast with `rpc("add_message", avatar_name, new_text)` — the `rpc()` call (no id) reaches all connected peers.
- Call `line_edit.clear()` after sending. WHY: gives immediate visual feedback that the message was accepted.

## Checklist
- [ ] `add_message` has `any_peer`, `call_local`, `reliable`, and a dedicated channel.
- [ ] Empty input is rejected before the RPC call.
- [ ] Input field is cleared after a successful send.
- [ ] Scroll position updates to the bottom on every new message.
- [ ] The same method exists at the same NodePath on every peer.

## Anti-patterns
- Omitting `call_local` — the sender never sees their own message.
- Omitting `any_peer` — only the server can post messages.
- Sending the RPC before the empty-string check — spams peers with blank lines.
- Forgetting to clear the LineEdit — players think the message failed and resend.

---
name: rpc-node-path-and-authority
topic: RPC node paths, authority, and remote data updates
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 4 (pp. 73-82)"]
---
## Rules
- Every peer must have the RPC method on a node at the same NodePath. WHY: Godot routes RPCs by node path, so a missing or moved node breaks the call.
- Place RPC methods on the child node that owns the data (for example `ChatControl`) rather than the scene root. WHY: avoids bloating one class with unrelated RPCs and keeps responsibilities local.
- With no options in `@rpc()`, only the Multiplayer Authority (the server) may call the method remotely. Use this default for server-authoritative setters such as `set_avatar_name`.
- Use `multiplayer.get_remote_sender_id()` inside a server RPC to learn who sent the last call. WHY: needed to reply to the correct peer.
- Reply to a single peer with `node.rpc_id(peer_id, "method", args)` instead of broadcasting. WHY: targeted updates avoid unnecessary traffic and leaks.
- Keep server and client scene trees structurally identical for shared nodes. WHY: identical NodePaths are what make `rpc_id` on a child node resolve correctly on the remote side.

## Checklist
- [ ] Confirm each RPC method exists at the same NodePath on server and all clients.
- [ ] Decide per method whether it is server-only (default) or `any_peer`.
- [ ] Use `get_remote_sender_id()` when the server must answer a specific peer.
- [ ] Use `rpc_id()` for per-peer data, `rpc()` only for true broadcasts.

## Anti-patterns
- Defining an RPC on the root node only — remote peers cannot resolve the path.
- Letting clients call server-authoritative setters (missing default authority restriction).
- Broadcasting per-peer data with `rpc()` — wastes bandwidth and can leak other players' data.
- Divergent scene trees between server and client — NodePath lookups fail silently.

> CHECK: The chapter states `@rpc` "transmit data securely ... using different transport protocols such as UDP and TCP"; Godot's ENet peer is UDP-based, so treat the TCP mention as loose wording and verify transport claims against Godot 4 docs.

<!-- 5 Making an Online Quiz Game (pp. 83-100) -->
---
name: quiz-lobby-rpc-authority-pattern
topic: multiplayer lobby and match start synchronization
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 5 (pp. 83-100)"]
---
## Rules
- Client-side `start_game()` uses `@rpc("authority", "call_local")` so only the server can trigger it and the server also runs it locally. WHY: prevents a single client from forcing a match start for everyone.
- The Start button handler must call `rpc_id(get_multiplayer_authority(), "start_game")` instead of calling the method directly. WHY: the request goes to the server, which then broadcasts to all peers.
- Server-side `start_game()` uses `@rpc("any_peer", "call_remote")` so any peer may request it and the caller does not run it locally. WHY: the server is the single point that decides when the match begins.
- Inside server `start_game()`, first change the server's own scene with `get_tree().change_scene_to_file(quiz_screen_scene_path)`, then call `rpc("start_game")` to move every client to its own scene. WHY: server and clients use different scenes (server vs client quiz screen).
- Append new player names to the lobby label with `label.text = label.text + "\n%s" % player_name`. WHY: simple cumulative list without a separate model.
- Keep authentication identical to earlier chapters (credentials checked against the fake database) before allowing lobby access. WHY: reuse of proven flow, only registered players enter.

## Checklist
- [ ] `@rpc` options on each method match the intended caller (authority vs any_peer) and local execution (call_local vs call_remote).
- [ ] Start button never calls `start_game()` directly.
- [ ] Server changes its own scene before broadcasting.
- [ ] New player names appear in the "Players in Match" panel for all peers.
- [ ] Optional: add a countdown timer before match start.

## Anti-patterns
- Letting a client call `start_game()` locally on itself or on other peers without server mediation.
- Using `call_local` on the server's `start_game()` when the server must not re-run the caller's path.
- Broadcasting the scene change before the server has switched its own scene.

> CHECK: OCR shows the client `start_game()` body as `pass` in one snippet and as a scene change in another; verify which is the final client implementation.

---
name: quiz-pseudo-turn-locking
topic: preventing answers after a valid response (pseudo-turn system)
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 5 (pp. 83-100)"]
---
## Rules
- Server `answered(user)` and `missed(user)` use `@rpc("any_peer")` so any client can report its result. WHY: each client reports only its own outcome.
- On a correct answer, server calls `quiz_panel.rpc("update_winner", database[user]["name"])`; on a wrong answer, `quiz_panel.rpc("player_missed", database[user]["name"])`. WHY: all peers must see the same round outcome.
- After either outcome, start a local timer with `timer.start(turn_delay_in_seconds)` and mirror it with `wait_label.rpc("wait", turn_delay_in_seconds)`. WHY: gives players time to read feedback before the next question.
- `update_winner()` and `player_missed()` on QuizPanel use `@rpc("call_local")` so the server's own panel updates too. WHY: server also renders the quiz panel.
- `lock_answers()` iterates `answer_container.get_children()` and sets `disabled = true`; `unlock_answers()` sets `disabled = false`. WHY: single loop covers all answer buttons regardless of count.
- To convert this into a true turn-based system, turn `lock_answers()`/`unlock_answers()` into RPCs and use `rpc_id()` to lock/unlock per player based on whose turn it is. WHY: only the active player should be able to answer.

## Checklist
- [ ] Both `answered` and `missed` are `@rpc("any_peer")` on the server.
- [ ] Both panel callbacks are `@rpc("call_local")`.
- [ ] Timer delay and wait label delay use the same `turn_delay_in_seconds` value.
- [ ] Buttons are locked immediately when a round ends and unlocked only when the next question loads.
- [ ] No client can answer while buttons are disabled.

## Anti-patterns
- Locking only the local player's buttons instead of broadcasting the lock to all peers.
- Forgetting `call_local` so the server's own panel stays interactive.
- Using different delay values for the timer and the wait label, causing desync in the UI.

---
name: quiz-question-database-and-loading
topic: JSON question data and per-round question loading
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 5 (pp. 83-100)"]
---
## Rules
- Store each question as a dictionary with exactly three keys: `text` (string), `alternatives` (array), `correct_answer_index` (int index into `alternatives`). WHY: minimal schema that maps directly to UI and validation.
- Provide four entries in `alternatives` because the UI has four AnswerButtons by default. WHY: avoids writing a dynamic button factory.
- Load the question with `available_questions.pop_at(new_question_index)` so the used question is removed from the pool. WHY: prevents repeating questions and detects exhaustion via `null`.
- If `pop_at()` returns `null`, set the question label to "No more questions" and call `lock_answers()`. WHY: clean end-of-match state.
- On a valid question: set `question_label.text` from `text`, store `correct_answer = questions[question]["correct_answer_index"]`, fill each button via `answer_container.get_child(i).text = alternatives[i]` for `i in range(0, 4)`, then call `unlock_answers()`. WHY: unlocks the round only after the question is fully rendered.
- `update_question()` is an `@rpc` called by the server so every peer loads the same question index. WHY: keeps all clients on the same question.

## Checklist
- [ ] Every question has exactly 3 keys and 4 alternatives.
- [ ] `correct_answer_index` is within `0..3`.
- [ ] `available_questions` is populated in `_ready()`.
- [ ] `update_question()` is `@rpc` and only the server calls it.
- [ ] Exhausted pool path sets "No more questions" and locks answers.

## Anti-patterns
- Reusing `available_questions` entries without popping, causing repeated questions.
- Hardcoding button count in the UI while allowing variable-length `alternatives`.
- Letting clients pick the question index themselves.

---
name: quiz-answer-evaluation-and-reporting
topic: client-side answer evaluation and server notification
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 5 (pp. 83-100)"]
---
## Rules
- `evaluate_answer(answer_index)` is a plain (non-RPC) method: compute `is_answer_correct = answer_index == correct_answer` and emit `answered.emit(is_answer_correct)`. WHY: evaluation is local; only the result travels over the network.
- In `QuizScreenClient`, connect to `QuizPanel.answered` and branch on the boolean: on true call `rpc_id(get_multiplayer_authority(), "answered", AuthenticationCredentials.user)`; on false call `rpc_id(get_multiplayer_authority(), "missed", AuthenticationCredentials.user)`. WHY: the server is the authority that updates all peers.
- Pass the user identifier (not the display name) to the server; the server resolves the display name from the database. WHY: keeps the wire payload small and the name source authoritative.
- The server, on receiving `answered`/`missed`, broadcasts the outcome to all peers' QuizPanels and starts the round delay. WHY: single source of truth for round state.

## Checklist
- [ ] `evaluate_answer()` is not an RPC.
- [ ] `answered` signal is connected in `QuizScreenClient._ready()`.
- [ ] Correct and incorrect paths call different server RPCs (`answered` vs `missed`).
- [ ] Server resolves names from the database before broadcasting.
- [ ] Round delay starts on the server after the outcome RPC.

## Anti-patterns
- Making `evaluate_answer()` an RPC so every peer re-evaluates the answer.
- Sending the display name from the client instead of the user id.
- Letting the client decide the round winner instead of the server.

> CHECK: OCR truncates the `rpc_id(...)` calls (missing closing parenthesis and possibly a trailing argument); verify the exact argument list in the source.

<!-- 6 Building an Online Checkers Game (pp. 101-126) -->
---
name: multiplayer-synchronizer-piece-position
topic: Godot 4 MultiplayerSynchronizer for property sync
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Add a `MultiplayerSynchronizer` node as a child of any node whose properties must stay identical across peers (e.g. `Piece` position). WHY: it replicates the chosen properties automatically without manual RPC code.
- Configure it in the inspector: select the synchronizer, open the **Replication** tab, click **Add property to sync**, pick the target node, then pick the property (e.g. `position`). WHY: the synchronizer only replicates properties explicitly registered in this list.
- Use `MultiplayerSynchronizer` for continuous/visual state (positions, transforms, animation flags). WHY: it is designed for frequent, small property updates, not for one-shot game events.
- Keep authoritative game logic (board data, turn order, win checks) out of the synchronizer and drive it with RPCs. WHY: the synchronizer only copies node properties; it does not update your abstract data model such as `meta_board`.
- After the synchronizer moves a piece visually, still update the abstract board data via RPC. WHY: otherwise the visual and logical board diverge and move validation breaks.

## Checklist
- [ ] Synchronizer is a direct child of the node it replicates.
- [ ] Only the minimum needed properties are registered (position, not the whole transform, unless rotation/scale matter).
- [ ] Abstract state (board dictionary) is updated separately through RPCs.
- [ ] Test with two peers: move a piece and confirm both views match.

## Anti-patterns
- Registering many properties "just in case" — wastes bandwidth every sync tick.
- Relying on the synchronizer to keep your game-logic data structure in sync — it only touches node properties.
- Putting the synchronizer on a non-authoritative node and expecting it to push changes from clients without authority setup.

> CHECK: The chapter does not state the default replication interval or visibility settings; verify in Godot 4 docs whether `replication_interval` and `public_visibility` need tuning for your tick rate.

---
name: rpc-annotations-turn-sync
topic: RPC annotations and call modes for turn-based games
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Annotate any method that must run on all peers with `@rpc(...)` and call it via `rpc("method_name", args...)` instead of a direct call. WHY: a plain call only runs locally; the `rpc()` form broadcasts it.
- For player-driven actions (move, capture, crown, end turn), use `@rpc("any_peer", "call_local")`. WHY: any player may trigger their own move, and the caller's own board must also update.
- For server-only setup (assigning team authorities), use `@rpc("authority", "call_local")`. WHY: only the server should decide who controls which team.
- Always include `call_local` when the caller also needs the effect applied on their own machine. WHY: without it the caller's state desyncs from everyone else's.
- Pass only serializable, primitive data over RPCs (ints, enums, `Vector2i`). WHY: object references are not valid across the network.
- Abstract teams as an `enum` (e.g. `Teams.BLACK`, `Teams.WHITE`) and pass the enum value, then resolve it to the local node on each peer. WHY: each peer must look up its own node instance.
- Keep RPC payloads minimal: send only the changed cell coordinates, not the whole board. WHY: bandwidth is the scarce resource in real-time games.

## Checklist
- [ ] Every method that changes shared state is either an RPC or called from one.
- [ ] `call_local` present on all RPCs whose effect the caller must also see.
- [ ] No Node/Object arguments in RPC signatures.
- [ ] Direct calls replaced by `rpc(...)` at every call site (search for the old method name).
- [ ] Tested in single-player mode: RPCs with `call_local` still work without connected peers.

## Anti-patterns
- Calling an `@rpc` method directly instead of via `rpc()` — silently runs locally only.
- Sending the entire board state each turn instead of the two changed cells.
- Using `@rpc("authority")` for player actions — clients would be unable to move their own pieces.

---
name: multiplayer-authority-team-setup
topic: Multiplayer authority assignment for player-owned nodes
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Assign each player-owned subtree (e.g. `BlackTeam`, `WhiteTeam`) to its player's peer ID with `set_multiplayer_authority(peer_id)`. WHY: it recursively marks the node and all children as owned by that peer, protecting them from other players.
- Do the assignment on the server only: guard with `if multiplayer.get_peers().size() > 0:` and `if is_multiplayer_authority():`. WHY: the server is the single source of truth for who controls what.
- Map the first connected peer to one team and the second to the other, using `multiplayer.get_peers()[0]` and `[1]`. WHY: deterministic, simple assignment for a two-player game.
- Check ownership before enabling interaction: `node.get_multiplayer_authority() == multiplayer.get_unique_id()`. WHY: prevents a player from selecting or moving the opponent's pieces.
- Keep the server itself without a team so it cannot move pieces. WHY: the server acts as referee; giving it a team would let it play.
- Guard all network setup with a peer-count check so the same script works offline. WHY: a single codebase must support both local and online play.

## Checklist
- [ ] `setup_team(team, peer_id)` is `@rpc("authority", "call_local")`.
- [ ] Called from `_ready()` only when peers are connected and the node is the authority.
- [ ] Both teams assigned before any turn logic runs.
- [ ] Offline path (`get_peers().size() == 0`) still enables the correct local pieces.

## Anti-patterns
- Letting clients call `set_multiplayer_authority` — any peer could claim any team.
- Assigning authority after the first turn starts — early moves may be rejected or duplicated.
- Forgetting the offline branch, so the game is unplayable without a network session.

---
name: turn-toggle-authority-gated
topic: Turn switching with authority checks
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Make `toggle_turn()` an `@rpc("any_peer", "call_local")` method and invoke it via `rpc("toggle_turn")` after a move completes. WHY: every peer must disable the old team's pieces and re-enable the new team's pieces in lockstep.
- On each turn switch, disable both teams' pieces first, then re-enable only the team whose turn it now is. WHY: guarantees no piece from the wrong team stays interactive.
- Re-enable a team's pieces only if the local peer is that team's authority: `team.get_multiplayer_authority() == multiplayer.get_unique_id()`. WHY: each client should only be able to interact with its own pieces.
- In offline mode (`get_peers().size() == 0`), enable the team unconditionally. WHY: there is no authority to compare against locally.
- Check for a winner before switching turns; if there is one, emit the win signal and return without toggling. WHY: avoids enabling pieces after the game has ended.

## Checklist
- [ ] `clear_free_cells()` runs at the start of every turn toggle.
- [ ] Both teams disabled before the new team is enabled.
- [ ] Win check precedes the enable step.
- [ ] `toggle_turn` called via `rpc()` from the free-cell selection handler.
- [ ] Selected piece deselected after the move.

## Anti-patterns
- Enabling the new team's pieces on every peer — both players could then move simultaneously.
- Skipping the win check, so a finished game keeps accepting moves.
- Calling `toggle_turn()` directly instead of via `rpc()` — the opponent's board never updates.

---
name: win-lose-and-rematch-rpc
topic: Win/lose signalling and rematch flow over the network
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Detect the win condition by counting remaining pieces per team at the end of each turn; a team with zero pieces loses. WHY: this is the checkers end condition and it is cheap to evaluate locally on every peer.
- Connect the board's `player_won` signal to a handler in the game scene, and inside that handler call `rpc("update_winner", winner)` rather than updating locally. WHY: all peers must show the same result screen.
- Annotate `update_winner()` and `rematch()` with `@rpc("any_peer", "call_local")`. WHY: any player may trigger a rematch, and the caller must also see the state change.
- Wire the rematch button's `pressed` signal to a handler that calls `rpc("rematch")`. WHY: a direct call would only reset the local instance.
- Let the rematch RPC reset the board state on all peers so players can play consecutive matches without leaving the session. WHY: avoids forcing a reconnect between games.

## Checklist
- [ ] `player_won` signal connected to the game scene handler.
- [ ] `update_winner` and `rematch` both annotated and called via `rpc()`.
- [ ] Rematch button handler uses `rpc("rematch")`.
- [ ] Verified both peers return to a playable board after rematch.

## Anti-patterns
- Showing the win screen only on the peer that made the capturing move.
- Resetting the board locally on rematch without an RPC — the two peers end up in different states.
- Reusing the initial connection flow for a rematch instead of a lightweight reset RPC.

---
name: board-abstraction-and-cell-updates
topic: Abstract board model and minimal-state RPC updates
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Represent the board as a `Dictionary` keyed by `Vector2i` cell coordinates, with values being the `Piece` node or `null` for empty cells. WHY: gives O(1) lookup of any cell's content and is trivially serializable.
- Build the dictionary from `TileMap.get_used_cells(0)` so only real board cells are included. WHY: avoids allocating entries for blank tiles.
- Convert between world positions and cells with `TileMap.local_to_map()` and `map_to_local()`. WHY: keeps all game logic in integer row/column space instead of floats.
- Update the board with a two-line swap: `meta_board[target] = meta_board[previous]; meta_board[previous] = null`. WHY: a move only ever changes two cells, so this is the minimum work and the minimum data to transmit.
- Make `update_cells(previous_cell, target_cell)` an `@rpc("any_peer", "call_local")` method and call it via `rpc(...)` from the move handler. WHY: both peers must apply the same two-cell change.
- Make `crown(cell)` an RPC with the same options and call it via `rpc("crown", target_cell)` when a piece reaches the king row. WHY: the king state must be identical on both boards.
- Make `remove_piece(piece_cell)` an RPC with the same options and call it via `rpc("remove_piece", cell)` when a capture occurs. WHY: the captured piece must disappear on both boards.
- Guard `remove_piece` with `is_on_board(cell)` and `is_free_cell(cell)` early returns. WHY: prevents freeing an invalid or already-empty cell.

## Checklist
- [ ] `create_meta_board()` runs before any piece is mapped.
- [ ] `map_pieces(team)` called for both teams at setup.
- [ ] `Piece.selected` signal connected to the board's selection handler with the piece bound as an argument.
- [ ] All three mutating methods (`update_cells`, `crown`, `remove_piece`) are RPCs called via `rpc()`.
- [ ] Capture path calls `remove_piece` before `move_selected_piece`.

## Anti-patterns
- Sending the whole `meta_board` dictionary each turn — unnecessary bandwidth.
- Updating `meta_board` only locally while the synchronizer moves the sprite — visual/logic desync.
- Using float positions as dictionary keys — precision errors break cell lookup.

---
name: piece-and-freecell-interaction
topic: Piece selection and free-cell UI in a board game
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 6 (pp. 101-126)"]
---
## Rules
- Give each `Piece` an `Area2D` child whose `input_event` signal handles left-click selection. WHY: `Area2D` gives per-piece hit detection without manual coordinate math.
- Track selection with a `"selected"` group: on select, call `get_tree().call_group("selected", "deselect")` first, then `add_to_group("selected")`. WHY: enforces single-selection without a central manager.
- Emit `selected` and `deselected` signals from the piece so the board can react without polling. WHY: decouples piece visuals from board logic.
- Toggle interactivity with `area.input_pickable` plus a visible `ColorRect` overlay in `enable()` / `disable()`. WHY: a single flag controls both input and the visual affordance.
- Represent legal destinations as `FreeCell` instances (`Area2D` + `CollisionShape2D` + `ColorRect`) created dynamically and shown in green. WHY: gives the player an unambiguous picture of legal moves.
- Have `FreeCell` emit `selected(position)` on left click; the board converts that position with `local_to_map()` to get the target cell. WHY: keeps the cell scene ignorant of board coordinates.
- Use a setter on `is_king` that awaits `ready` if the node is not yet in the tree before swapping the sprite texture. WHY: prevents errors when the flag is set from the inspector before `_ready`.

## Checklist
- [ ] `SelectionArea2D` present on every piece.
- [ ] `EnabledColorRect` and `SelectedColorRect` wired to enable/disable/select/deselect.
- [ ] `FreeCell` scene has `Area2D`, `CollisionShape2D`, `ColorRect`.
- [ ] Free cells cleared at the start of every turn toggle.
- [ ] King texture applied through the `is_king` setter, not directly.

## Anti-patterns
- Letting a piece stay selected after a move — always call `deselect()`.
- Enabling pieces via `visible` instead of `input_pickable` — the piece still receives clicks.
- Hardcoding free-cell positions instead of instantiating `FreeCell` scenes from the move rules.

<!-- 7 Developing an Online Pong Game (pp. 127-144) -->
---
name: pong-paddle-authority-setup
topic: multiplayer authority assignment for player-controlled paddles
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 7 (pp. 127-144)"]
---
## Rules
- Wrap the paddle's authority assignment in an RPC so every peer learns who owns which paddle: `@rpc("call_local") func setup_multiplayer(player_id): set_multiplayer_authority(player_id)`. WHY: the server decides ownership, but all peers must apply the same authority locally or they will disagree about who simulates what.
- Inside that RPC, disable local simulation for non-owners: `if not is_multiplayer_authority(): set_physics_process(false); set_process_unhandled_input(false)`. WHY: if the opponent's paddle keeps running `move_and_slide()` and reading input on your machine, its locally computed position fights the position you receive over the network.
- Only the server picks the player IDs. Guard the assignment with `if multiplayer.get_peers().size() > 0:` and `if is_multiplayer_authority():`. WHY: with zero peers the game must still run as local single-player, and only one peer may decide the mapping.
- Assign peers by index: `player_1 = multiplayer.get_peers()[0]`, `player_2 = multiplayer.get_peers()[1]`, then `player_1_paddle.rpc("setup_multiplayer", player_1)` and the same for paddle 2. WHY: deterministic index-based assignment keeps both peers agreeing on who is who.
- Delay the setup by one frame-ish before calling RPCs: `await get_tree().create_timer(0.1).timeout` at the top of `_ready()`. WHY: remote nodes may not exist yet when `_ready()` runs, so RPCs would target missing nodes.
- Keep the paddle as a `Node2D` wrapper whose child is the `CharacterBody2D`; move the body, not the wrapper. WHY: separates the game entity from its physics body so authority and syncing can be applied at the entity level.
- Paddle movement model: constant speed on key press, zero velocity on release, and on release of one key check whether the opposite key is still held before zeroing. WHY: prevents the paddle from stopping when the player rolls from one key to the other.

## Checklist
- [ ] `setup_multiplayer(player_id)` exists on the paddle and is decorated `@rpc("call_local")`.
- [ ] Non-authority paddles have physics process and unhandled input disabled.
- [ ] Server-only branch assigns `get_peers()[0]` and `[1]` to the two paddles.
- [ ] `_ready()` awaits a short timer before issuing RPCs.
- [ ] Local (no peers) mode still starts the ball and plays normally.

## Anti-patterns
- Letting both paddles simulate and read input on every peer — the remote paddle's position gets overwritten by stale local physics.
- Calling `set_multiplayer_authority()` without an RPC — only the server's copy changes, peers keep the old owner.
- Assigning peers without checking `is_multiplayer_authority()` — multiple peers race to assign, producing inconsistent ownership.
- Using `get_peers()` order as a stable identity without any handshake — peer list order is only reliable if all peers read it from the same authoritative source.

> CHECK: the book's `@rpc("call_local")` snippet omits an explicit `"any_peer"`/`"authority"` mode; verify which RPC mode the chapter intends for `setup_multiplayer` in Godot 4.0 (default is `"authority"`).

---
name: pong-ball-sync
topic: syncing the ball across peers with MultiplayerSynchronizer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 7 (pp. 127-144)"]
---
## Rules
- Add a `MultiplayerSynchronizer` as a child of the ball and replicate `CharacterBody2D:position` only. WHY: position is the only state other peers need; replicating velocity too invites divergence.
- Set the synchronizer's `Visibility Update` to `Physics` for any physics body. WHY: sync then happens on the same tick as the physics simulation, so collisions and positions stay consistent.
- Server-authoritative ball: in the ball's `_ready()`, `if not is_multiplayer_authority(): set_physics_process(false)`. WHY: only one peer may integrate the ball's motion; everyone else just displays the replicated position.
- Ball motion: randomize initial direction with `body.velocity.x = [-speed, speed][randi()%2]` and the same for `y`; bounce with `body.velocity = body.velocity.bounce(collision.get_normal())` using `move_and_collide`. WHY: `bounce()` reflects the velocity around the collision normal, which is exactly Pong's reflection rule.
- `reset()` should teleport the body to the ball node's `global_position` and then call `move()` to re-randomize direction. WHY: a fresh serve must not reuse the previous trajectory.
- Do not disable `_physics_process` on the ball via the paddle's setup path; the ball has its own authority check. WHY: mixing the two setup flows makes it unclear who owns the ball.

## Checklist
- [ ] `MultiplayerSynchronizer` is a child of the ball node.
- [ ] Replication list contains exactly `CharacterBody2D:position`.
- [ ] `Visibility Update` = `Physics`.
- [ ] Non-authority peers have the ball's physics process off.
- [ ] Ball resets to center and re-randomizes direction after each score.

## Anti-patterns
- Replicating the ball's velocity as well as position — the two can disagree and cause visible jitter or double bounces.
- Leaving `Visibility Update` on `Idle` for a physics body — sync drifts relative to the physics tick.
- Letting every peer simulate the ball — each peer ends up with a different ball trajectory and players react to a ball that does not exist on the server.

---
name: pong-paddle-sync
topic: syncing paddle positions across peers
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 7 (pp. 127-144)"]
---
## Rules
- Add a `MultiplayerSynchronizer` as a child of the paddle and replicate `CharacterBody2D:position`. WHY: the opponent must see your paddle move even though they do not simulate it.
- Set `Visibility Update` to `Physics` on the paddle synchronizer too. WHY: paddles are physics bodies and must be synced on the physics tick to stay aligned with the ball.
- Do not add an extra `set_physics_process(false)` for the paddle here — the authority setup already disabled it for non-owners. WHY: duplicating the disable logic in two places makes the ownership rules hard to trace.
- Keep the paddle's collision layer/mask so it interacts with the ball and walls but not with the score areas. WHY: the score area must only detect the ball.

## Checklist
- [ ] `MultiplayerSynchronizer` is a child of the paddle node.
- [ ] Replication list contains exactly `CharacterBody2D:position`.
- [ ] `Visibility Update` = `Physics`.
- [ ] Authority-based physics/input disabling is done once, in `setup_multiplayer()`.

## Anti-patterns
- Syncing the paddle's velocity or input state instead of position — extra bandwidth and a second source of truth.
- Forgetting the synchronizer on one of the two paddles — that player's opponent appears frozen.

---
name: pong-scoring-and-collision-layers
topic: score detection and collision layer separation
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 7 (pp. 127-144)"]
---
## Rules
- Score with an `Area2D` (`ScoreArea`) that emits `scored(score)` on `body_entered`, incrementing an exported `score` int. WHY: decouples score detection from the game controller; `PongGame` just connects to the signal.
- Put the ball on its own physics layer (layer 2) and have it mask layer 1 (paddles, floor, ceiling). WHY: the ball must collide with walls and paddles but be the only thing the score areas see.
- Give `ScoreArea` a mask of layer 2 only and no collision layer of its own. WHY: guarantees the score area can never be triggered by the floor, ceiling, or a paddle.
- Leave the `CollisionShape2D` off the `ScoreArea` scene and add it in the final scene. WHY: each score area needs a differently sized/placed shape, so the reusable scene stays shape-agnostic.
- Display score with a `Label` whose `update_score(new_score)` sets `text = "%s" % new_score`. WHY: keeps formatting in one place and accepts the int emitted by the signal.
- `PongGame` owns the wiring: connect both `ScoreArea.scored` signals, update the labels, show the winner overlay at the target score, and reset the ball on each score. WHY: the leaf scenes are intentionally uncoupled; the game controller is the only place that knows the rules.

## Checklist
- [ ] Ball: layer 2, mask 1.
- [ ] ScoreArea: layer none, mask 2.
- [ ] `ScoreArea.scored` connected in `PongGame`, not inside `ScoreArea`.
- [ ] Winner overlay appears at the target score and offers a rematch that restarts the match.
- [ ] Ball recentered and re-launched after every score.

## Anti-patterns
- Putting the score area on the same layer as the ball — the area triggers on walls and paddles.
- Letting `ScoreArea` update the label directly — the score logic then lives in two places and cannot be reset centrally.
- Hardcoding the score area's shape inside the reusable scene — forces a duplicate scene per side.

---
name: pong-architecture-and-tooling
topic: project structure, tool scripts, and version constraints
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 7 (pp. 127-144)"]
---
## Rules
- Use Godot 4.0 exactly for this project; do not open it in other 4.x versions. WHY: the book's API surface (RPC annotations, `MultiplayerSynchronizer` properties) matches 4.0.
- Model each entity as a plain `Node2D` root with the physics body as a child. WHY: the entity is not a body; it is a thing that has a body, which keeps authority and syncing concerns at the entity level.
- Use `@tool` scripts for editor-only visualization, e.g. a `CollisionShape2D` tool script that draws the circle with `draw_circle(Vector2.ZERO, shape.radius, color)`. WHY: lets you see collision shapes in the editor without running the game.
- Expose tunables as `@export` (`speed`, `up_action`, `down_action`, `score`, `color`) rather than constants. WHY: designers can tune per-instance without editing scripts.
- Cache child references with `@onready var body = $CharacterBody2D`. WHY: avoids repeated `get_node` calls in `_physics_process`.
- Call `randomize()` before randomizing the ball direction. WHY: without it the same "random" serve repeats every run.

## Checklist
- [ ] Engine version pinned to 4.0.
- [ ] Entity roots are `Node2D`; physics bodies are children.
- [ ] Editor visualization uses `@tool` + `_draw()`.
- [ ] Tunables are `@export`.
- [ ] `randomize()` called in `PongGame._ready()`.

## Anti-patterns
- Making the entity root itself the `CharacterBody2D` — couples game logic to physics and complicates authority handling.
- Hardcoded speeds and input action names — untunable without code edits.
- Skipping `randomize()` — deterministic, repetitive serves.

> CHECK: the OCR shows the `PongGame` script body duplicated from the `Ball` script (same `move()`/`reset()`/`_physics_process` code). Verify the actual `PongGame.gd` contents in the repository before transcribing it.

<!-- 8 Creating an Online Co-op Platformer Prototype (pp. 145-166) -->
---
name: multiplayer-spawner-player-avatars
topic: MultiplayerSpawner for player avatar replication
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 8 (pp. 145-166)"]
---
## Rules
- Add a `MultiplayerSpawner` node as a child of your spawner node (e.g. `PlayerSpawner`, a `Marker2D`). WHY: the spawner replicates any locally instantiated scene to all peers automatically.
- Set `MultiplayerSpawner.spawn_path` to the node that should parent the spawned scenes. WHY: without it the spawner has no target container and replication fails.
- Add the player `PackedScene` to `MultiplayerSpawner.auto_spawn_list`. WHY: only scenes in this list are replicated when instantiated locally.
- On the server, instantiate one player per connected peer: loop `range(0, multiplayer.get_peers().size())`. WHY: `get_peers()` excludes the local peer, so the server must create its own avatar separately.
- Set `player.name = str(player_id)` **before** `add_child(player)`. WHY: unique names prevent RPC and MultiplayerSpawner errors and let you map node → peer ID.
- After each `add_child`, `await get_tree().create_timer(0.1).timeout` before the next spawn. WHY: gives peers time to register the new node before the follow-up RPC.
- Then call `player.rpc("setup_multiplayer", player_id)` to configure authority on all peers.
- Connect `MultiplayerSpawner.spawned` to a handler that runs `node.rpc("setup_multiplayer", int(str(node.name)))`. WHY: avatars created on remote peers by the spawner also need their authority and input flags set.
- Add `await get_tree().create_timer(0.1).timeout` at the top of `_ready()`. WHY: lets the multiplayer connection finish initializing before you query peers.
- Branch on `multiplayer.get_peers().size() < 1` to keep the local (joypad) path and `return` early. WHY: local and online sessions need different controller setup.

## Checklist
- [ ] `MultiplayerSpawner` child added, `spawn_path` and `auto_spawn_list` set.
- [ ] Server loop creates one avatar per peer plus its own.
- [ ] Node name set to peer ID string before `add_child`.
- [ ] 0.1 s await between spawns and before the setup RPC.
- [ ] `spawned` signal wired to a handler that RPCs `setup_multiplayer`.
- [ ] Local-session path preserved and returns early.

## Anti-patterns
- Adding the player as a child before naming it — breaks RPC routing and spawner bookkeeping.
- Spawning avatars on every peer instead of only the authority — duplicate nodes and desync.
- Skipping the initialization delay — RPCs fire before the peer list is populated.
- Using `get_peers()` as the total player count — it omits the local peer.

> CHECK: OCR shows `player.setup_controller(i)` iterating `for i in Input.get_connected_joypads()` (iterating the array, not indices) — verify against the repo whether it should be `range(...)`.

---
name: player-multiplayer-authority-setup
topic: Assigning per-player authority and input ownership
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 8 (pp. 145-166)"]
---
## Rules
- Implement `setup_multiplayer(player_id)` on the Player and decorate it `@rpc("any_peer", "call_local")`. WHY: any peer may request setup, and the caller must also apply it locally.
- First line: `set_multiplayer_authority(player_id)`. WHY: authority decides which peer may mutate the node and drive its RPCs.
- Compute `var is_player = str(player_id) == str(name)`. WHY: the node name holds the owning peer ID, so this identifies the local player's own avatar.
- Apply `set_physics_process(is_player)` and `set_process_unhandled_input(is_player)`. WHY: only the owning peer simulates and reads input; remote avatars must not fight for control.
- Update the label with `"P%s" % get_index()`. WHY: `get_index()` counts children of the spawner (the MultiplayerSpawner is child 0), so player numbering starts at 1.
- Keep the local joypad path (`setup_controller(index)`) for offline sessions: duplicate each InputMap action with an index suffix and set `new_event.device = index`. WHY: each device must map to exactly one avatar.

## Checklist
- [ ] `setup_multiplayer` is `@rpc("any_peer", "call_local")`.
- [ ] Authority set from the passed peer ID.
- [ ] Physics and unhandled-input processing gated on `is_player`.
- [ ] Label shows a 1-based player index.
- [ ] Local path still assigns distinct controllers per device.

## Anti-patterns
- Leaving physics/input enabled on remote avatars — they drift or respond to the wrong player's input.
- Comparing `player_id` to `name` without string conversion — `StringName` vs `int` comparison silently fails.
- Setting authority without also gating processing — the node still runs locally on non-owners.

---
name: multiplayer-synchronizer-player-state
topic: Syncing player position and animation with MultiplayerSynchronizer
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 8 (pp. 145-166)"]
---
## Rules
- Add a `MultiplayerSynchronizer` as a child of the Player scene.
- Set `Visibility Update Mode` to `Physics`. WHY: state is sampled on physics ticks, matching `CharacterBody2D` movement and avoiding jitter.
- In the Replication list, add: the character body's `Position`, the `AnimatedSprite2D`'s `Animation` and `Frame`, and the sprite container's `Scale`. WHY: position alone leaves remote avatars visually frozen in idle.
- Only replicate small, primitive values (vectors, ints, floats, strings). WHY: objects cannot be serialized over the network and heavy payloads (e.g. `Texture`) fail replication.
- Keep the replication set minimal — every added property costs bandwidth each tick.

## Checklist
- [ ] Synchronizer is a child of the node whose state it replicates.
- [ ] Update mode set to Physics.
- [ ] Position, animation name, frame, and facing scale all listed.
- [ ] No resource/object properties in the replication list.

## Anti-patterns
- Replicating a `Texture` or other resource — replication fails.
- Leaving update mode on Idle while the body moves in `_physics_process` — visible stutter.
- Syncing only position — remote players appear to slide without animation.

---
name: crate-dynamic-authority-grab
topic: Dynamic authority transfer for grabbable objects
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 8 (pp. 145-166)"]
---
## Rules
- Build interactables from an `Area2D`-based `InteractiveArea2D` with signals `interacted`, `interaction_available`, `interaction_unavailable`, and an exported `interact_input_action` (default `"interact"`).
- Keep `_unhandled_input` disabled by default (`set_process_unhandled_input(false)` in `_ready`); enable it in `_on_area_entered` and disable in `_on_area_exited`. WHY: only the nearest overlapping interactable should consume the input.
- On interact, emit `interacted` and call `get_viewport().set_input_as_handled()`. WHY: prevents the same press from triggering other handlers.
- On the crate, give it its own `MultiplayerSynchronizer` with `Visibility Update Mode = Physics` and replicate only the `CharacterBody2D.Position`.
- In the crate's `_on_interactive_area_2d_area_entered(area)`, call `set_multiplayer_authority(area.get_multiplayer_authority())`. WHY: the grabbing player's interaction area carries that player's authority, so the crate's authority transfers to whoever touches it.
- Use a `RemoteTransform2D` on the player (`GrabbingRemoteTransform2D`) and set its `remote_path` to the crate body on interact. WHY: the grabbing player then drives the crate's transform locally, and the synchronizer replicates it to everyone.

## Checklist
- [ ] Interactable has `InteractiveArea2D` with the three signals.
- [ ] Unhandled input toggled by area enter/exit.
- [ ] Crate has a `MultiplayerSynchronizer` replicating body position.
- [ ] Crate authority reassigned on area entry from the entering area's authority.
- [ ] Player's `RemoteTransform2D.remote_path` set to the grabbed body on interact.

## Anti-patterns
- Fixed crate authority — only one peer could ever move it, breaking co-op.
- Setting `remote_path` before authority transfer — the transform update is rejected on the owner.
- Letting multiple players grab the same crate without reassigning authority — conflicting position writes.

> CHECK: OCR shows the crate script referencing `GrabbingRemoteTransform2D` in one place and `GrabberRemoteTransformer2D` in the Player scene description — confirm the exact node name in the repo.

<!-- 9 Creating an Online Adventure Prototype (pp. 167-208) -->
---
name: persistent-world-login-auth
topic: Persistent-world client/server authentication
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- In a persistent world there is no lobby: the server runs the world continuously and players join mid-session. The server must therefore own both hosting setup and credential checking.
- Put a dedicated `Authentication` node as a direct child of a node named `Main` on **both** sides, at the same node path. RPCs resolve by node path, so both peers must expose the same methods even if only one side calls them.
- Server `_ready()`: `if multiplayer.is_server(): peer.create_server(PORT); multiplayer.multiplayer_peer = peer; load_database()`. Client branch: `peer.create_client(ADDRESS, PORT)` then assign the peer.
- Client start button sends `rpc_id(1, "start_game")` — never starts the scene locally.
- Server `start_game()` uses `@rpc("any_peer", "call_remote")`, reads `multiplayer.get_remote_sender_id()`, and replies with `rpc_id(peer_id, "start_game")`.
- Client `start_game()` uses `@rpc("authority", "call_local")` and calls `get_tree().change_scene_to_file(next_scene)`.
- WHY: the server decides who may enter; a client that presses start without a server reply simply hangs, which blocks local-only play and trivial spoofing.

## Checklist
- [ ] Both `Authentication` nodes share identical method names and paths.
- [ ] Server branch creates the ENet peer before any client connects.
- [ ] Client scene change happens only inside the authority RPC.
- [ ] `rpc_id()` used for direct peer-to-peer messages (works client-to-client too).

## Anti-patterns
- Starting the game scene locally on button press (bypasses authentication).
- Attaching auth logic to the `Main` node on the server side, which has other world duties.
- Assuming a lobby-style "all peers start together" flow in a persistent world.

---
name: syncing-existing-world-objects
topic: Syncing pre-existing world objects to late joiners
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- Only the server spawns world objects (e.g. 30 asteroids). Clients request a sync instead: `if not multiplayer.get_unique_id() == 1: rpc_id(1, "sync_world")`.
- Add a `MultiplayerSpawner` per object type, with `Spawn Path` pointing at the container node and the scene in `Auto Spawn List`. Server-side spawns then appear on all clients.
- Add a `MultiplayerSynchronizer` to each replicated object; replicate only what changes (e.g. `position`, `top_level`).
- Turn **Public Visibility off** on the synchronizer and grant visibility per peer with `set_visibility_for(peer_id, true)`.
- Put all such synchronizers in a group (e.g. `Sync`) so the server can grant visibility in one call: `get_tree().call_group("Sync", "set_visibility_for", player_id, true)`.
- `sync_world()` is `@rpc("any_peer", "call_local")`; the requester's own ID comes from `multiplayer.get_remote_sender_id()`, so whoever asks gets synced.
- WHY: clients cannot know object positions they never received; per-peer visibility avoids sending the whole world to peers who have not entered it yet.

## Checklist
- [ ] Spawner `Spawn Path` and `Auto Spawn List` set correctly.
- [ ] Synchronizer replicates the minimum property set.
- [ ] Public Visibility disabled; visibility granted on join.
- [ ] Synchronizers grouped for bulk visibility calls.

## Anti-patterns
- Letting clients spawn world objects (positions will diverge).
- Leaving Public Visibility on, replicating objects to peers not yet in the world.
- Relying on spawn order/name to identify objects instead of explicit IDs.

---
name: spawning-and-owning-players
topic: Remote player spawning and authority assignment
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- Make `create_spaceship()` an `@rpc("any_peer", "call_remote")` on the World script; the server instantiates the player scene.
- Name the instance after the owner's peer ID (`spaceship.name = str(player_id)`) before adding it to the spawner's container, so the name doubles as the authority key.
- Add a `PlayersMultiplayerSpawner` with `Spawn Path` = players container and the player scene in `Auto Spawn List`, so existing players are replicated to new joiners.
- Connect the spawner's `spawned` signal and call `Node.rpc("setup_multiplayer", int(str(Node.name)))` — the name is used because the spawner does not know the owner ID.
- `setup_multiplayer(player_id)` is `@rpc("any_peer", "call_local")` and must: compare `multiplayer.get_unique_id() == player_id` into `is_player`; `set_process(is_player)`; `set_physics_process(is_player)`; `camera.enabled = is_player`; `camera.make_current()` if owner; finally `set_multiplayer_authority(player_id)`.
- Set the player's `MultiplayerSynchronizer` **Visibility Update Mode = Physics** when syncing physics properties, to avoid overlapping bodies and mishandled collisions.
- WHY: disabling process on non-owned instances stops clients from overwriting network-synced properties and from driving someone else's ship.

## Checklist
- [ ] Instance name equals owner peer ID before `add_child`.
- [ ] `setup_multiplayer` called both on direct spawn and on `spawned` signal.
- [ ] Camera enabled/current only for the owner.
- [ ] Authority set last, after process toggles.

## Anti-patterns
- Spawning the player locally on each client (duplicate, unsynced ships).
- Leaving `_process`/`_physics_process` on for remote-owned instances.
- Using `Idle` visibility update mode for physics-driven transforms.

---
name: server-authoritative-damage
topic: Server-authoritative damage and destruction
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- Clients simulate visuals only; the server resolves outcomes. In `_on_hurt_area_2d_damage_taken(damage)`: `if multiplayer.is_server(): apply_damage(damage)`.
- Built-in nodes (e.g. `AnimationPlayer`) have no RPC, so wrap the behaviour in your own RPCs: `@rpc("authority", "call_local") func hit()` / `func explode()` that play the animation.
- `apply_damage()` decrements health and calls `rpc("explode")` when health < 1, else `rpc("hit")` when health > 0.
- Only the server may free the object: in `_on_animation_player_animation_finished`, `if multiplayer.is_server() and anim_name == "explode": queue_free()`.
- WHY: the server is the mediator; letting clients apply damage or delete objects enables cheating and conflicting outcomes when two players shoot the same target.
- Freeing on the server propagates removal through the `MultiplayerSpawner` to all clients automatically — no manual despawn RPC needed.

## Checklist
- [ ] Damage application guarded by `is_server()`.
- [ ] Animation/feedback replicated via `@rpc("authority", "call_local")` wrappers.
- [ ] `queue_free()` guarded by `is_server()`.
- [ ] Client still despawns the bullet on hit (local visual only).

## Anti-patterns
- Applying damage on every peer (health diverges, double kills).
- Calling `queue_free()` from clients.
- Trying to RPC a built-in node method directly.

---
name: replicating-shooting-with-rpc
topic: Replicating projectile fire without syncing bullets
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- For constant-trajectory projectiles, do not spawn/sync each bullet. Instead RPC the fire call: replace `weapon.fire()` with `weapon.rpc("fire")` in the player's `_process()`.
- This works because the spawn origin and direction derive from the ship transform, which the player's `MultiplayerSynchronizer` already replicates.
- Keep the weapon's local fire-rate `Timer` check (`if timer.is_stopped()`) so RPC spam cannot exceed the fire rate.
- WHY: bullets are deterministic given origin + direction, so replicating them individually wastes bandwidth for no visual gain.

## Checklist
- [ ] `fire()` reachable by RPC on all peers.
- [ ] Fire-rate timer still gates the call.
- [ ] Bullet spawner uses the ship's synced `global_rotation`.

## Anti-patterns
- Using `MultiplayerSpawner` + `MultiplayerSynchronizer` for every bullet.
- Syncing bullet velocity/position when the trajectory is fixed.

---
name: server-side-quest-database
topic: Server-owned quest data with per-user keys
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- Structure progress data per user: `PlayerProgress.json` maps `user -> quest_id -> {completed, progress}`. Quest definitions (`QuestDatabase.json`) map `quest_id -> {title, description, target_amount}`.
- Only the server loads and stores files: guard `load_database()` in `_ready()` and `store_database()` in `_notification()` with `multiplayer.is_server()`; keep the `NOTIFICATION_WM_CLOSE_REQUEST` save.
- Client `QuestSingleton.retrieve_quests()`: return early if server, wait ~0.1 s for setup, then `QuestDatabase.rpc_id(1, "get_player_quests", AuthenticationCredentials.user)`.
- `create_quest(quest_data)` on the client is `@rpc("authority", "call_remote")` — only the server creates quest nodes on clients.
- Server `get_player_quests(user)` is `@rpc("any_peer", "call_remote")`; capture `multiplayer.get_remote_sender_id()` as `requester_id`, build each `quest_data` dict, and reply with `Quests.rpc_id(requester_id, "create_quest", quest_data)`.
- `update_player_progress(quest_id, current_amount, completed, user)` is `@rpc("any_peer", "call_remote")` and writes only `if multiplayer.is_server()`.
- Client `increase_quest_progress()` updates the local quest node then sends `QuestDatabase.rpc_id(1, "update_player_progress", ...)` including the user.
- Always pass the authenticated user (`AuthenticationCredentials.user`) as an argument; never trust a client-supplied identity for anything else.
- WHY: keeping the authoritative copy server-side prevents clients from editing their own progress files to complete quests instantly.

## Checklist
- [ ] File load/save guarded by `is_server()`.
- [ ] Every data RPC carries the `user` argument.
- [ ] Server replies to the requester ID, not broadcast.
- [ ] Client-side `create_quest` restricted to authority.

## Anti-patterns
- Loading or writing the JSON on clients.
- Broadcasting quest data to all peers instead of the requester.
- Letting clients write progress directly into the database.

> CHECK: The OCR shows `get_player_quests()` both with and without a `user` parameter; the final signature used in the RPC call is `get_player_quests(user)`. Verify against the repository source.

---
name: quest-node-and-ui
topic: Quest node model and quest log UI
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- Model a quest as a `Node` with exported `id`, `title`, `description`, `target_amount` (designer-editable in the Inspector) plus runtime `current_amount` and `completed`.
- Give `current_amount` a setter that clamps to `[0, target_amount]`, emits `updated(quest_id, new_amount)`, and emits `finished(quest_id)` when `current_amount >= target_amount`.
- `QuestSingleton` keeps `quests: Dictionary` keyed by quest ID; `create_quest()` instantiates the quest scene, copies fields from the data dict, adds it as a child, stores it by ID, and emits `quest_created(new_quest)`.
- `increase_quest_progress(quest_id, amount)` increments the quest node and forwards the new value to the database.
- `QuestProgress` is a tiny leaf node with an exported `quest_id` and `increase_progress(amount = 1)` that calls `Quests.increase_quest_progress(quest_id, amount)`; trigger it from gameplay signals such as the asteroid's `tree_exiting`.
- `QuestPanel` extends `ScrollContainer` with a `VBoxContainer` child; in `_ready()` connect `Quests.quest_created` to `add_quest` then call `Quests.retrieve_quests()`.
- `add_quest()` builds a `Label` (with `AUTOWRAP_WORD_SMART`), connects `quest.updated` to `update_quest`, and stores the label in a `quest_labels` dict keyed by quest ID; `update_quest()` re-renders that label's text.
- WHY: keying everything by `quest_id` lets gameplay objects, the singleton, the database and the UI communicate without direct references.

## Checklist
- [ ] Setter clamps and emits both signals.
- [ ] Quest nodes stored by ID in the singleton.
- [ ] UI label dict keyed by quest ID for O(1) updates.
- [ ] `QuestProgress` placed on the object whose destruction counts as progress.

## Anti-patterns
- Storing quest progress only in the UI.
- Rebuilding the whole quest list on every progress tick instead of updating one label.
- Hardcoding quest data in scripts instead of the JSON database.

---
name: world-scene-composition
topic: World scene composition and initialization
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 9 (pp. 167-208)"]
---
## Rules
- Structure the World scene as: `Main` root with an `Asteroids` radial spawner, a `Players` spawner, and CanvasLayers for visuals (`BackgroundLayer` ColorRect, `ParallaxBackground`/`ParallaxLayer` with a `GPUParticles2D` starfield) and UI (`InterfaceCanvasLayer` containing `QuestPanel`).
- Server `_ready()` spawns 30 asteroids and calls `create_spaceship()`; keep the player spawn behind a named method rather than calling the spawner inline, so the online version can override it with an RPC.
- Player scene: `Node2D` root holding a `Spaceship` (`RigidBody2D`), `Weapon2D` (`Marker2D`), `Sprite2D`, `HurtArea2D`, `CameraRemoteTransform2D`, and `Camera2D`.
- Spaceship movement: `linear_velocity += acceleration * delta * Vector2.RIGHT.rotated(rotation)` for thrust; `angular_velocity += direction * turn_torque * delta` for turning. Defaults: `acceleration = 600.0`, `turn_torque = 10.0`, zero gravity, very low friction.
- Weapon: `fire()` only when the timer is stopped; play the fire animation, spawn a bullet, then `timer.start(1.0 / fire_rate)` with `fire_rate = 3` (three shots per second).
- Asteroid: `max_health = 3`, 1 damage per bullet hit, 1 damage to ships that touch it; play `"explode"` then `queue_free()` on animation finish.
- WHY: separating spawners, visuals and UI keeps the networking changes localized to the spawner/root scripts.

## Checklist
- [ ] Spawners are dedicated child nodes, not inline loops in `_ready`.
- [ ] Camera driven via `CameraRemoteTransform2D` from the ship.
- [ ] Fire rate expressed as shots/second and converted with `1.0 / fire_rate`.

## Anti-patterns
- Calling `player_spawner.spawn()` directly from `_ready` (blocks the RPC-based online path).
- Putting UI nodes outside a CanvasLayer.
- Using gravity/friction defaults on a top-down space ship.

<!-- 10 Debugging and Profiling the Network (pp. 209-232) -->
---
name: godot-debugger-stack-trace
topic: Godot Debugger — Stack Trace tab
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- Use the Stack Frames panel to read the call chain that led to an error or breakpoint; the topmost frame is where execution stopped.
- Use Step Into to execute the next line and descend into indented blocks (function calls). Use Step Over to execute the next line but skip the body of called functions. Pick Step Over when you trust the callee; pick Step Into when the bug is inside it.
- Use Break to pause a running game as if it hit a breakpoint, and Continue to resume. Use Skip Breakpoints to run past all breakpoints without deleting them.
- Inspect and edit live variable values in the Members panel while paused; this lets you test a fix hypothesis without recompiling or restarting the game.
- Use the Filter Stack Variables field to narrow the Members list when a script has many variables.
- Use Copy Error to put the current error text on the clipboard for pasting into an issue or chat.
- Place breakpoints liberally across scripts to observe when, how, and why object state changes. WHY: the chain of cause and effect is invisible from reading code alone, especially in multiplayer where the trigger comes from a remote peer.
## Checklist
- [ ] Reproduce the bug with the Debugger dock open.
- [ ] Read the full stack frames list before touching code.
- [ ] Check Members values at the failing frame; compare with expected values.
- [ ] Step Over through trusted calls, Step Into suspected ones.
- [ ] Remove or disable temporary breakpoints before committing.
## Anti-patterns
- Reading only the top stack frame and ignoring the caller chain — the real cause is often one or two frames up.
- Leaving dozens of breakpoints in shipped code; they halt the game for anyone running a debug build.
- Editing a variable in Members and assuming the fix is permanent — it only affects the current paused session.

---
name: godot-debugger-errors-tab
topic: Godot Debugger — Errors tab and per-instance logging
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- Treat the Errors tab as the primary triage surface: it lists fatal errors, non-fatal errors, and warnings. Click an entry to jump to the offending script line; double-click to expand or collapse the code stack behind it.
- Use Expand All / Collapse All / Clear to manage long lists; Clear only empties the panel, it does not fix anything.
- In multiplayer, use `push_error()` and `push_warning()` instead of `print()` for diagnostics. WHY: the Output dock is shared across all running instances, so `print()` output is ambiguous, while `push_error()`/`push_warning()` appear only in the Errors tab of the instance that triggered them.
- Use per-instance error routing to identify which session is the server and which are clients, and to detect errors that occur on only one peer.
- Read the total error/warning counter on the Debugger button: it aggregates all instances, so a session's Errors tab may show fewer entries than the total.
- Address warnings deliberately: decide to fix or consciously accept each one. Unused-argument warnings are common and usually harmless, but they hide real issues if ignored in bulk.
## Checklist
- [ ] Replace `print()` diagnostics with `push_error()`/`push_warning()` in any code that runs on multiple peers.
- [ ] After a playtest, check the Errors tab of every instance, not just the one you were watching.
- [ ] Clear the panel between test runs so old entries do not mask new ones.
- [ ] Confirm the error counter on the Debugger button matches the sum of per-instance entries.
## Anti-patterns
- Using `print()` for network diagnostics in a multi-instance session — you cannot tell which peer logged it.
- Ignoring warnings until they number in the hundreds; the signal-to-noise ratio collapses.
- Assuming a silent failure is fine: a packet that never arrives produces no error at all, so absence of errors is not proof of correctness.

---
name: godot-profiler-tab
topic: Godot Debugger — Profiler tab (script/CPU timing)
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- Profiling is off by default because it is resource-intensive; press Start to begin measuring and Clear to reset gathered data.
- Choose the measurement with the Measure dropdown:
  - Frame Time (ms) — total milliseconds Godot spends processing a frame.
  - Average Time (ms) — mean duration of a single function call.
  - Frame % — share of the frame's rendering time consumed by a function.
  - Physics Frame % — same as Frame % but relative to the physics frame.
- Choose the aggregation with the Time Scope dropdown:
  - Inclusive — time of the function plus all nested calls it made.
  - Self — time of the function alone, excluding calls it made.
  Use Self to find the function that is actually expensive; use Inclusive to find the subsystem that is expensive.
- Use the Frame # stepper to inspect measurements for one specific frame instead of an aggregate.
- Read the Measurement Graph to spot spikes; each tracked function gets its own color.
- Do not optimize before measuring. Diagnose first, then decide whether the target hardware actually needs the optimization.
## Checklist
- [ ] Press Start before reproducing the performance problem.
- [ ] Switch between Self and Inclusive scope for the same suspect function.
- [ ] Note the Frame # of any spike and inspect that frame specifically.
- [ ] Record the baseline numbers before changing code, so the change can be validated.
## Anti-patterns
- Premature optimization: rewriting code for speed before any measurement shows it is a bottleneck.
- Profiling with the tool left running during normal development — it distorts the very timings you care about.
- Reading only Average Time and missing rare but severe spikes; check the graph and the Frame # stepper too.

---
name: godot-visual-profiler-tab
topic: Godot Debugger — Visual Profiler tab (rendering/GPU)
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- Use the Visual Profiler to attribute frame cost to rendering tasks (culling, lighting, draw calls) on CPU and GPU separately.
- The Tasks panel groups rendering tasks by category and breaks them down per viewport and canvas layer; use this to find which viewport or layer is expensive.
- Profiling is off by default; press Start to begin and Clear to reset.
- Measure options are Frame Time (ms) and Frame % — the same two shapes as the script Profiler.
- Enable Fit to Frame to keep the graph on the default frame scale; disable it to inspect portions running above 60 FPS.
- Enable Linked to zoom the CPU and GPU graphs to the same scale, so you can compare them directly.
- Use the Frame # stepper to correlate a task list with one specific frame.
## Checklist
- [ ] Determine whether the bottleneck is CPU-side or GPU-side before optimizing.
- [ ] Check per-viewport and per-canvas-layer breakdown, not just the total.
- [ ] Enable Linked when comparing CPU and GPU graphs.
- [ ] Disable Fit to Frame when investigating high-FPS spikes.
## Anti-patterns
- Optimizing draw calls when the graph shows the cost is on the CPU side (or vice versa).
- Looking only at the aggregate rendering time and never at the per-viewport breakdown.

---
name: godot-monitors-tab
topic: Godot Debugger — Monitors tab and custom monitors
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- The Monitors tab always tracks; there is no Start/Stop/Clear. Only monitors checked in the Monitor panel are plotted in the Graphs panel.
- Default monitors cover three groups: time (FPS, process time, physics process time), memory (static, dynamic, message buffers), and objects (object count, resource count, node count, orphan nodes).
- Create a custom monitor with `Performance.add_custom_monitor(id, callable, [args])`. The `id` string becomes the monitor name; use a `"Category/Name"` prefix (for example `"Network/Quests Updates"`) to group related monitors.
- Build the callable with `Callable(self, "method_name")` and register it in `_ready()`. The method must return the value to plot.
- Increment the tracked counter at the exact event you care about (for example, inside the server-only branch after a successful update), not on every frame.
- Register server-side monitors only on the server (`if multiplayer.is_server()`) and client-side monitors only on clients (`if not multiplayer.is_server()`). WHY: a monitor registered on the wrong peer plots meaningless data and wastes the counter.
- Use custom monitors to test a proposed optimization before implementing it: track the counter under the current logic, then track it again under the candidate logic and compare.
## Checklist
- [ ] Define a member variable for the counter, default 0.
- [ ] Add a getter method that returns it.
- [ ] Register the monitor in `_ready()` with a `"Category/Name"` id.
- [ ] Increment the counter at the correct event and only on the correct peer role.
- [ ] Tick the monitor's checkbox in the Monitor panel to plot it.
- [ ] Compare counts before and after a candidate fix.
## Anti-patterns
- Registering a monitor on both server and clients when the data is only meaningful on one role.
- Incrementing the counter every frame instead of per event — the graph becomes noise.
- Forgetting to tick the checkbox and concluding the monitor is broken.

---
name: godot-network-profiler
topic: Godot Debugger — Network Profiler (RPC and synchronizer cost)
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- The Network Profiler tracks only the High-Level Network API by default. Low-level transports (`PacketPeerUDP`, `UDPServer`, `StreamPeerTCP`, `TCPServer`) are not counted unless you add custom monitors for them.
- Profiling is off by default; press Start to begin and Clear to reset.
- Read the RPC panel per node:
  - Node — node path of the sender/receiver.
  - Incoming RPC — count and byte size of RPCs other peers call on this node.
  - Outgoing RPC — count and byte size of RPCs this node calls on other peers.
- Read the Bandwidth meter for total bytes/second: Down (received) and Up (sent).
- Read the Synchronization panel per `MultiplayerSynchronizer`: Root node, Synchronizer node, Config (`SceneReplicationConfig`), Count (number of syncs), Size (total bytes synced this session).
- Judge RPCs by event ratio, not raw count. A 1:1 ratio (one game event, one RPC) is healthy; a high count for a method that only carries a state toggle is a bottleneck.
- Judge RPCs by bytes as well as count: a low-count RPC with large payloads can cost more bandwidth than a high-count RPC with tiny payloads.
- Use the Debugger Misc tab to identify which running instance is the server (the one whose last Clicked Control is the server button) before interpreting per-session profiler data.
- Run multiple instances via Debug → Run Multiple Instances (for example, Run 3 Instances) and start the Network Profiler on every instance.
## Checklist
- [ ] Start the Network Profiler on all instances before the playtest.
- [ ] Identify the server instance via the Misc tab.
- [ ] Reproduce a fixed, countable workload (for example, destroy all 30 asteroids) so counts are comparable.
- [ ] Inspect the RPC panel for methods with high counts but low information content.
- [ ] Inspect the Synchronization panel for nodes that sync constantly but rarely change.
- [ ] Check the bandwidth meter before and after any change.
## Anti-patterns
- Assuming a symmetric RPC count between server and clients means there is nothing to optimize; the server may be doing work (animations, local calls) it does not need to do.
- Leaving `MultiplayerSynchronizer` nodes replicating static objects every frame.
- Profiling only one instance and drawing conclusions about the whole network.

---
name: network-bottleneck-triage
topic: Network optimization triage from profiler data
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- Replace per-shot RPCs with a state toggle. If a weapon fires 693 times and the only states are firing / not firing, send one boolean RPC on press and one on release, and let `process()` spawn bullets locally at the fire rate. WHY: the RPC count collapses while behavior is unchanged.
- Change RPC annotations so server-only logic does not run locally. If the server computes damage and removes the node, mark the hit RPC `call_remote` so the hit animation plays only on clients. WHY: a headless server has no reason to play animations.
- Stop replicating objects that do not move. Call the synchronizer's `update_visibility()` (or otherwise gate syncing) inside the world-sync method instead of letting it replicate every frame. WHY: constant sync of static transforms is pure wasted bandwidth.
- Cap repeated progress updates: if a quest is already completed, stop sending updates for it. WHY: without the cap, updates scale with the number of peers and events rather than with meaningful progress.
- Prefer a 1:1 event-to-RPC ratio. If one game event triggers two RPCs, look for a way to merge or gate them.
- When count is already minimal but payload is large, attack the payload (compression, smaller types) rather than the count.
- Measure the candidate fix with a custom monitor before committing to it; compare counts under old and new logic.
## Checklist
- [ ] List every RPC with high count and ask: does this carry state or an event?
- [ ] Convert state-carrying RPCs into toggle RPCs plus local simulation.
- [ ] Audit RPC annotations for server-only logic that should be `call_remote`.
- [ ] Audit `MultiplayerSynchronizer` nodes for objects that never change.
- [ ] Add a completion guard to any progress-update RPC.
- [ ] Re-run the profiler and compare bandwidth before/after.
## Anti-patterns
- Optimizing payload size when the real problem is a per-frame or per-shot RPC count.
- Assuming symmetry between server and client RPC counts proves correctness.
- Implementing an optimization without a before/after measurement.

---
name: godot-video-ram-and-misc-tabs
topic: Godot Debugger — Video RAM and Misc tabs
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 10 (pp. 209-232)"]
---
## Rules
- Video RAM tab: read the table with four columns — Resource Path, Type, Format, Usage. Usage is the memory the resource actually occupies.
- Use the Video RAM tab to decide whether to pack sprites into an atlas: compare the combined Usage of separate textures against a single `AtlasTexture`. WHY: fewer, larger textures reduce memory and draw overhead, which matters for low-end devices.
- Export the Video RAM table as CSV for offline analysis or presentations.
- Misc tab: read Clicked Control and Clicked Control Type to see the last `Control` node that consumed a click at runtime.
- Use the Misc tab to diagnose input consumption bugs. A `ColorRect` used as a screen fade will swallow mouse events unless its Mouse Filter is set to Ignore.
- Use the Misc tab in point-and-click style games to determine which UI element handled a click when two overlapping elements could both claim it.
- Live Edit Root shows the current root node of the live SceneTree instance.
- Export Misc measures as CSV to keep a record of UI interaction flow.
## Checklist
- [ ] Check Video RAM Usage before and after atlas packing.
- [ ] Set Mouse Filter to Ignore on any full-screen overlay that should not consume input.
- [ ] Use Clicked Control to confirm which node actually received a click.
- [ ] Export CSV when you need to compare across runs.
## Anti-patterns
- Leaving a full-screen `ColorRect` (fade, vignette, overlay) with default mouse filter — it silently blocks all UI beneath it.
- Guessing which UI element consumed an input instead of reading the Misc tab.
- Packing textures into an atlas without checking whether Video RAM Usage actually drops.

> CHECK: The Misc tab's "Set From Tree" button is described in the source as undocumented and apparently always disabled; verify its behavior in your Godot 4.x version before relying on it.

<!-- 11 Optimizing Data Requests (pp. 233-248) -->
---
name: network-resources-bandwidth-throughput
topic: Network resource budgeting (bandwidth vs throughput)
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 11 (pp. 233-248)"]
---
## Rules
- Treat bandwidth (capacity of the pipe) and throughput (actual packets/size flowing) as the two metrics you optimize; measure both with the Debugger's Network Profiler before and after every change.
  - WHY: you cannot claim an optimization without a before/after measurement, and these two numbers are the only objective evidence.
- Budget for ~5 Mbps per player as a realistic target for modern online multiplayer games; if your profiled peak exceeds that, cut data before adding features.
  - WHY: mainstream online titles run comfortably in that envelope, so exceeding it excludes players on shared household connections.
- Optimize throughput, not just bandwidth: reduce packet count AND packet size, and keep packet size/frequency consistent.
  - WHY: inconsistent packet sizes and rates cause packet loss, and loss leaves clients unable to reconstruct the world state.
- Prefer unreliable/latest-state transmission for continuously changing values; only send what the client needs to reconstruct the server's world, since assets already exist on the client.
  - WHY: games rarely need a full reliable stream; sending only deltas/latest state is the single biggest bandwidth saver.
- Accept that network optimization cannot invent new mechanics — it must reproduce existing mechanics within the available resources.
  - WHY: unlike CPU/GPU work, network work has no "happy accidents"; any behavior change is a regression.
- Reserve headroom in your budget for future mechanics that will need more bandwidth.
  - WHY: once you squeeze the pipe to 100%, every new feature forces a redesign.

## Checklist
- [ ] Profile a representative session (e.g. ~20 s of play) and record peak/typical sent and received bytes.
- [ ] Identify the top offenders by RPC count and by synchronizer update count.
- [ ] Fix the highest-count offender first, then re-profile.
- [ ] Confirm packet sizes and send intervals are stable, not spiky.
- [ ] Verify the game experience is unchanged after each optimization.

## Anti-patterns
- Optimizing without profiling first (guessing at bottlenecks).
- Comparing profiler sessions of different durations and treating the numbers as a unit test.
- Adding mechanics while the network budget is already saturated.
- Assuming a video-conference-style workload model applies to games (it does not; games ship assets locally).

> CHECK: The "5 Mbps" figure is stated as a general industry observation, not a measured requirement of this project — verify against your own profiler data.

---
name: reduce-rpc-count-state-toggle
topic: Replacing per-frame RPCs with state-change RPCs
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 11 (pp. 233-248)"]
---
## Rules
- Never call an RPC every frame from `_process()` while an input is held; instead send one RPC on press and one on release that toggles a boolean state.
  - WHY: in the book's measurement this cut weapon-fire RPCs from 693 to 6 in a ~20 s session (>115x fewer).
- Implement the toggle as `@rpc("any_peer", "call_local") func set_firing(firing)`; on `true` fire immediately, on `false` stop the timer.
  - WHY: `call_local` keeps the local player's weapon in sync without a separate code path, and `any_peer` lets the owning client drive its own weapon.
- Drive repeated firing from a `Timer` node's `timeout` signal calling `fire()`, and restart the timer inside `fire()` with `timer.start(1.0 / fire_rate)`.
  - WHY: the timer becomes the single authority for cadence, so no per-frame polling is needed.
- Remove the `@rpc` annotation and the `if timer.is_stopped()` guard from `fire()` once the timer owns the cadence.
  - WHY: `fire()` is now a local effect only; leaving RPC annotations creates redundant network calls.
- Read input in `_unhandled_input()` and branch on `event.is_action_pressed("shoot")` / `event.is_action_released("shoot")`, calling `weapon.rpc("set_firing", true/false)`.
  - WHY: input events are edge-triggered, which is exactly the granularity the state toggle needs.
- Gate input processing per-instance in your setup function: `set_process(is_player)`, `set_physics_process(is_player)`, `set_process_unhandled_input(is_player)`.
  - WHY: remote player instances must not read local input, or they will fire their own weapons.

## Checklist
- [ ] `fire()` contains no RPC annotation and no timer-stopped guard.
- [ ] `Timer.timeout` is connected to a callback that calls `fire()`.
- [ ] `set_firing` is `@rpc("any_peer", "call_local")` and takes a bool.
- [ ] `_process()` no longer contains firing logic.
- [ ] `set_process_unhandled_input(is_player)` is set in the multiplayer setup.
- [ ] Re-profile: RPC count for the weapon should drop by orders of magnitude.

## Anti-patterns
- Keeping `_process()`-driven firing "just in case" alongside the toggle (double firing).
- Forgetting `call_local`, causing the shooter to see no muzzle flash.
- Forgetting to disable unhandled input on remote instances.

---
name: manual-synchronizer-visibility
topic: Manual MultiplayerSynchronizer updates for static objects
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 11 (pp. 233-248)"]
---
## Rules
- For nodes that never move after spawn (asteroids, pickups, static props), set `MultiplayerSynchronizer.visibility_update_mode` to `None` and sync manually.
  - WHY: automatic visibility updates keep re-sending identical data every frame for the whole session.
- Trigger the manual sync from a single coordinator (e.g. `World.sync_world()`), calling `get_tree().call_group("Sync", "set_visibility_for", player_id, true)` then `get_tree().call_group("Sync", "update_visibility", player_id)`.
  - WHY: one group call syncs every static object to exactly the requesting peer, so each object syncs once per player instead of every frame.
- Get the target peer from `multiplayer.get_remote_sender_id()` inside the RPC, not from a parameter.
  - WHY: it is authoritative and cannot be spoofed by the caller.
- Pass `0` to `update_visibility()` only when you intend to sync all peers; otherwise pass the specific peer ID.
  - WHY: `0` broadcasts, which defeats the purpose for per-player sync.
- Remember that `update_visibility()` respects the filters set by `set_visibility_for()`; a peer not added via `set_visibility_for()` will not be synced even if you pass its ID.
  - WHY: this is a common silent failure — the call succeeds but nothing is sent.

## Checklist
- [ ] `visibility_update_mode = None` on every static object's synchronizer.
- [ ] Objects are in the `"Sync"` group.
- [ ] `sync_world()` calls `set_visibility_for` before `update_visibility`.
- [ ] Profiler shows each static object's sync count incrementing once per joining player, not per frame.

## Anti-patterns
- Leaving automatic visibility updates on for objects whose properties never change.
- Calling `update_visibility()` without first calling `set_visibility_for()` for that peer.
- Syncing static objects from multiple places instead of one coordinator.

---
name: enet-compression-mode
topic: ENetConnection compression configuration
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 11 (pp. 233-248)"]
---
## Rules
- Set the compression mode on `peer.host` via `peer.host.compress(ENetConnection.COMPRESS_*)` BEFORE assigning `multiplayer.multiplayer_peer`.
  - WHY: the mode must be configured before the connection is established; setting it afterwards has no effect.
- Apply the same compression mode on every connection path (server, main client, and any secondary screen such as a login screen) so both ends match.
  - WHY: mismatched compression settings between peers break the connection.
- Choose the mode with this table:
  - `COMPRESS_NONE` — most bandwidth, least CPU; use for Wireshark-style debugging.
  - `COMPRESS_RANGE_CODER` — ENet's built-in range encoding; good on small packets, inefficient above 4 KB.
  - `COMPRESS_FASTLZ` — less CPU than ZLib, more bandwidth.
  - `COMPRESS_ZLIB` — less bandwidth than FastLZ, more CPU.
  - `COMPRESS_ZSTD` — inefficient on packets under 4 KB; avoid for small packets.
  - WHY: the trade-off is always bandwidth vs CPU, and the 4 KB threshold decides which algorithms are worth it.
- Pick `COMPRESS_ZLIB` when CPU is not a bottleneck and you want bandwidth savings.
  - WHY: in the book's test, ZLib cut server sent-data peak from 80,234 to 48,802 bytes and received peak from 14,470 to 12,509 bytes, even with sub-kilobyte packets.
- Do not expect large gains from compression if your packets are well under 4 KB; measure before assuming.
  - WHY: most algorithms are tuned for either below or above the 4 KB boundary.

## Checklist
- [ ] `compress()` called before `multiplayer.multiplayer_peer = peer` on every peer.
- [ ] Same mode used on server and all clients.
- [ ] Sent/received byte monitors added (see custom-monitor card) to compare modes.
- [ ] CPU usage checked after switching to a heavier algorithm.

## Anti-patterns
- Calling `compress()` after the peer is assigned.
- Using `COMPRESS_ZSTD` on tiny packets.
- Enabling compression on one side only.

---
name: custom-network-monitors
topic: Custom Performance monitors for ENet traffic
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 11 (pp. 233-248)"]
---
## Rules
- Expose sent and received byte counters as custom monitors so they appear in the Debugger's Monitors tab:
  - `get_received_data()` returns `multiplayer.multiplayer_peer.host.pop_statistic(ENetConnection.HOST_TOTAL_RECEIVED_DATA)`.
  - `get_sent_data()` returns `multiplayer.multiplayer_peer.host.pop_statistic(ENetConnection.HOST_TOTAL_SENT_DATA)`.
  - WHY: the Monitors tab gives a live graph, which is far easier to compare across compression modes than raw profiler rows.
- Register them with `Performance.add_custom_monitor("Network/Received Data", Callable(self, "get_received_data"))` (and the sent equivalent) in `_ready()`.
  - WHY: the `"Network/"` prefix groups them under one category in the Monitors tab.
- The callable must return an int or float; `pop_statistic()` already does.
  - WHY: the Performance singleton rejects other return types.
- Use these monitors to A/B test compression modes and to catch regressions after refactors.
  - WHY: they show cumulative totals, so a slope change is immediately visible.

## Checklist
- [ ] Both monitor callables defined on a node that exists for the whole session (e.g. `World`).
- [ ] `add_custom_monitor` called once, in `_ready()`.
- [ ] Monitors visible under the `Network/` category in the Debugger.
- [ ] Baseline recorded with `COMPRESS_NONE` before switching modes.

## Anti-patterns
- Registering monitors on a node that is freed and recreated (duplicate or stale monitors).
- Comparing monitors recorded over different session lengths.
- Treating monitor peaks as precise benchmarks rather than directional evidence.

<!-- 12 Implementing Lag Compensation (pp. 249-270) -->
---
name: lag-compensation-overview
topic: networking / lag compensation
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 12 (pp. 249-270)"]
---
## Rules
- Treat lag compensation as three complementary techniques, not one: **interpolation** (fill gaps between received states), **prediction** (guess the next state from physics), **extrapolation** (interpolate into the future using the prediction). Use all three together.
- Prefer unreliable packets (ENet default) for high-frequency state such as position/rotation; they have lower latency than reliable packets. Reliable delivery is for events that must not be lost.
- When packets arrive out of order, discard stale data and keep only the newest state — old positions are irrelevant to the current frame.
- Keep one authoritative instance (the server) as the fallback source of truth; clients reconcile against it.
- Measure real latency instead of guessing: on a client, read `multiplayer.multiplayer_peer.get_peer(1).get_statistic(ENetPacketPeer.PEER_ROUND_TRIP_TIME)` and feed that into interpolation/extrapolation durations.
- For testing, fake latency with a `Timer` node (e.g. `wait_time = 0.1` ≈ 100 ms) rather than relying on real network conditions.
- WHY: unreliable packets lose and reorder data, so the client must never render raw network state directly; it must smooth, guess, and periodically re-sync to the server.

## Checklist
- [ ] Decide per property whether it is synced by `MultiplayerSynchronizer` or by RPC (do not do both).
- [ ] Confirm which node is the multiplayer authority for each synced property.
- [ ] Have a way to read round-trip time at runtime for tuning durations.
- [ ] Have a fake-latency switch (Timer) for local testing.
- [ ] Verify behaviour at 0 ms, ~100 ms, and a high-latency case.

## Anti-patterns
- Rendering the latest received position directly → visible teleporting/jitter.
- Using reliable packets for per-frame position updates → added latency and head-of-line blocking.
- Applying out-of-order packets in arrival order → rubber-banding and impossible movement.
- Assuming zero latency during development → the game only feels right on LAN.

> CHECK: The chapter uses "lag" and "latency" loosely and interchangeably in places; the distinction drawn (lag = perceived delay between action and effect, latency = round-trip data travel time) is the author's framing, not a strict industry definition.

---
name: server-authoritative-motion
topic: networking / authority model
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 12 (pp. 249-270)"]
---
## Rules
- Move simulation authority to the server: clients send **input state** (thrusting, turning, direction), the server simulates the ship and owns position/rotation.
- Disable position and rotation sync on the `MultiplayerSynchronizer` (both Spawn and Sync) once the server simulates motion; otherwise you fight your own replication.
- On the client, keep only `_unhandled_input()` enabled for the local player; disable `_physics_process()`/`_process()` on remote instances.
- Send input changes as RPCs to peer 1 (the server) using `rpc_id(1, ...)`, e.g. `spaceship.rpc_id(1, "set_thrusting", true)`.
- Model input as a small set of state variables with setters, not as per-frame deltas: `thrusting: bool`, `turning: bool`, `direction: int` in `[-1, 1]`.
- Annotate the setters as `@rpc("any_peer", "call_local")` so any peer can call them and the local instance also applies them.
- Keep the physics step on the server: `_physics_process(delta)` calls `thrust(delta)` / `turn(delta)` only when the corresponding state flag is true.
- WHY: a single authoritative simulation gives every client a consistent value to fall back to and lets the server arbitrate discrepancies (e.g. hit validation).

## Checklist
- [ ] `MultiplayerSynchronizer` no longer replicates position/rotation.
- [ ] Input RPCs target peer id 1 explicitly.
- [ ] Input state variables have `@export` + setter so they are inspectable and replicable.
- [ ] `thrust()`/`turn()` take `delta` as a parameter (no hidden per-frame assumptions).
- [ ] Camera is enabled only for the local player's instance.

## Anti-patterns
- Client-authoritative movement plus server sync → cheating and divergence.
- Sending raw input events every frame over RPC instead of state changes → bandwidth waste.
- Leaving `_physics_process()` active on remote player instances → double simulation.

---
name: interpolation-with-tween
topic: networking / interpolation
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 12 (pp. 249-270)"]
---
## Rules
- Interpolate between the **previous known value** and the **newest received value** over the expected update interval; never snap.
- Store `previous_position` and `previous_rotation` as state; update them after each interpolation completes.
- Use `Tween` for the animation: `create_tween()`, then `tween_property(node, "position", final_value, duration)`.
- Set the tween to physics processing: `tween.set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)` — required when the target is a physics body.
- Set the tween's start explicitly with `tweener.from(previous_position)` so it animates from the last known value rather than the current one.
- Use `lerp()` for position and `lerp_angle()` for rotation; `lerp_angle()` picks the shortest angular path, which plain `lerp()` cannot.
- Compute `final_value = lerp(previous, target, 1.0)` (or `lerp_angle(..., 1.0)`) to normalise the target before handing it to the tween.
- Drive interpolation from a `Timer` (e.g. `InterpolationTimer`, `wait_time = 0.1`, process callback = Physics) whose `wait_time` doubles as the interpolation duration.
- Gate the interpolation RPCs as `@rpc("authority", "call_remote")` — only the server sends them, and it does not need to run them locally.
- WHY: sparse updates arrive at irregular intervals; animating between two known values hides packet loss and jitter without inventing data.

## Checklist
- [ ] `previous_*` variables initialised from the node's starting transform.
- [ ] Tween process mode set to physics.
- [ ] `from()` called on the returned `PropertyTweener`.
- [ ] `previous_*` updated to the new target after starting the tween.
- [ ] Interpolation timer started only on the server instance.

## Anti-patterns
- Using `lerp()` on angles → the ship spins the long way round.
- Forgetting `set_process_mode(TWEEN_PROCESS_PHYSICS)` on a `CharacterBody2D`/`RigidBody2D` → interpolation fights the physics step.
- Creating a new tween each tick without tracking old ones → overlapping tweens on the same property.

---
name: prediction-and-resync
topic: networking / prediction
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 12 (pp. 249-270)"]
---
## Rules
- Interpolation alone leaves the client permanently behind the server; add a periodic **synchronization** tick that snaps to the true state and resets the interpolation baseline.
- Run the synchronization timer at a **faster pace than the interpolation timer** (e.g. sync every 0.05 s vs interpolate every 0.1 s).
- On each sync, first stop all running tweens: iterate `get_tree().get_processed_tweens()` and call `tween.stop()`. If your game has unrelated tweens, keep your own list and stop only those.
- Predict with Newtonian physics from the last two known positions:
  - `distance = previous_position.distance_to(new_position)`
  - `direction = previous_position.direction_to(new_position)`
  - `linear_velocity = (direction * distance) / seconds_ahead`
- Write the predicted velocity back onto the body (`spaceship.linear_velocity = linear_velocity`) so it keeps moving between updates instead of idling.
- Predict the next position as `new_position + linear_velocity * seconds_ahead`; return it for use by extrapolation.
- Predict rotation analogously: `angular_velocity = lerp_angle(previous_rotation, new_rotation, 1.0) / seconds_ahead`, then `next_rotation = rotation + angular_velocity * seconds_ahead`.
- After snapping, set `previous_position`/`previous_rotation` to the newly received values so the next tick has a correct baseline.
- Prediction is also a **server-side** tool: to validate a PvP hit, rewind/predict where the target's ship was at the moment the shot was fired, and let the server decide whether the hit lands.
- WHY: without periodic re-sync, interpolation lag accumulates until the client is no longer playing in real time.

## Checklist
- [ ] `SynchronizationTimer` exists and starts only on the server.
- [ ] Sync RPCs are `@rpc("authority", "call_remote")`.
- [ ] Tweens are stopped before the manual position/rotation assignment.
- [ ] `predict_position()` / `predict_rotation()` run locally on the client (no RPC annotation).
- [ ] `seconds_ahead` is sourced from the sync timer's `wait_time`.

## Anti-patterns
- Never re-syncing → the client drifts further behind with every missed packet.
- Stopping *all* tweens in the scene tree when unrelated tweens exist → broken UI/animation.
- Predicting without writing velocity back to the body → the ship still idles between updates.

---
name: extrapolation-into-the-future
topic: networking / extrapolation
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 12 (pp. 249-270)"]
---
## Rules
- Treat extrapolation as "interpolation into the future": animate from the previous known value to the **predicted** next value over `seconds_ahead`.
- Implement it with the same `Tween` pattern as interpolation: `create_tween()`, `set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)`, `tween_property(node, "position", next_position, seconds_ahead)`, then `tweener.from(previous_position)`.
- Call extrapolation from inside the synchronization handler, before assigning the authoritative position:
  1. stop running tweens
  2. `future_position = predict_position(new_position, synchronization_tic)`
  3. `extrapolate_position(future_position, synchronization_tic)`
  4. `spaceship.position = new_position`; `previous_position = new_position`
- Do the same for rotation with `extrapolate_rotation(future_rotation, synchronization_tic)`.
- Extrapolation functions run client-side only — no `@rpc` annotation needed.
- WHY: it hides missed updates and prevents hiccups/idling in fast-paced games where a split-second gap is visible.

## Checklist
- [ ] Extrapolation is invoked from the sync handler, not from the interpolation timer.
- [ ] Duration equals the sync tick, matching the prediction horizon.
- [ ] `from()` uses the previous known value, not the current node transform.
- [ ] Rotation extrapolation uses the angle-aware prediction, not raw subtraction.

## Anti-patterns
- Extrapolating far beyond the sync interval → visible overshoot and rubber-banding when the real update arrives.
- Extrapolating without a subsequent re-sync → error accumulates and is never corrected.
- Running extrapolation on the server → wasted work; the server already has the true state.

> CHECK: The chapter's `predict_rotation()` snippet appears truncated in the source (`/ second\ns_ahead`); verify the exact expression against the book's repository before copying it verbatim.

<!-- 13 Caching Data to Decrease Bandwidth (pp. 271-296) -->
---
name: caching-overview-and-transport-choice
topic: Caching strategy and transport selection for large assets
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 13 (pp. 271-296)"]
---
## Rules
- Cache any asset that is likely to be requested more than once (images, sounds, 3D models, text/JSON data) on the local device instead of re-fetching it from the server. WHY: repeated downloads waste bandwidth and add loading latency for no new information.
- Choose the transport by payload size: use RPC / MultiplayerSynchronizer for small, frequent, latency-critical state (bytes); use HTTP for large, one-off or infrequent payloads (kilobytes to megabytes). WHY: ENet rides on UDP, which is fast but unordered and lossy — unsuitable for reliably moving large blobs.
- Before any download, check the local cache first; only issue a network request on a cache miss. WHY: this is the entire bandwidth saving; a cache that is never consulted is dead weight.
- Store cached files under `user://` (e.g. `user://.cache/`), never under `res://`. WHY: `res://` is read-only in exported builds and `user://` is remapped per platform by Godot.
- Treat a failed custom-sprite download as non-fatal: keep the default sprite and continue. WHY: cosmetic assets must not block core gameplay.
- Measure the effect: register a custom monitor with `Performance.add_custom_monitor()` returning `HTTPRequest.get_downloaded_bytes()`. WHY: you cannot claim a bandwidth win without before/after numbers.

## Checklist
- [ ] Identify which assets are re-requested across sessions or across peers.
- [ ] Pick transport per asset: RPC for small state, HTTP for large files.
- [ ] Define a cache directory under `user://` and create it if missing.
- [ ] Guard every download with an existence check on the cached file.
- [ ] Await `request_completed` before using the downloaded data.
- [ ] Return an error code from download helpers so callers can fall back.
- [ ] Add a custom monitor to compare first-download vs cached bytes.

## Anti-patterns
- Sending image or audio bytes through RPCs/ENet. WHY: UDP gives no ordering or delivery guarantee for large payloads, and it inflates per-tick traffic.
- Downloading the same texture every time a peer enters view. WHY: this is exactly the case caching exists to eliminate.
- Hardcoding an absolute OS path instead of `user://`. WHY: the path breaks on other platforms and in exported builds.
- Assuming the download finished synchronously after calling `request()`. WHY: `HTTPRequest` is asynchronous; using the file before `request_completed` reads stale or missing data.

> CHECK: OCR shows `@export_global_dir` / `@export_global_file` annotations on the cache path variables; verify the exact annotation names in Godot 4.0 before copying.

---
name: httprequest-download-pattern
topic: HTTPRequest node setup and download flow
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 13 (pp. 271-296)"]
---
## Rules
- Use one dedicated `HTTPRequest` node per distinct download responsibility (e.g. one for the JSON database, one for textures) rather than sharing a single node. WHY: each node has a single `download_file` target and one in-flight request; sharing causes races.
- Set `download_file` to the destination path *before* calling `request(url)`. WHY: `HTTPRequest` streams the response body straight to that file; without it you only get the body in memory.
- `request()` defaults to the GET method — correct for downloading files. Pass custom headers as the second argument and a different method as the third only when needed. WHY: GET is the HTTP verb for retrieval.
- `await request_completed` (or `await request(...)`) before any logic that consumes the file. WHY: the request is asynchronous and the file does not exist until the signal fires.
- Have the download helper return the error from `request()` (or `FAILED` when preconditions fail) so callers can branch. WHY: callers need to distinguish "downloaded" from "no such user / no database".
- Create the cache directory with `DirAccess.make_dir_absolute()` when `DirAccess.open()` returns null. WHY: writing to a non-existent directory fails silently.
- Parse JSON with `JSON.parse_string(file.get_as_text())` into a `Dictionary`. WHY: gives direct key lookup for user → URL mapping.

## Checklist
- [ ] One `HTTPRequest` node per download role, named for that role.
- [ ] Cache dir path, cache file path, and remote URL exposed as exported variables.
- [ ] Directory existence checked and created if absent.
- [ ] File existence checked before requesting.
- [ ] `download_file` assigned before `request()`.
- [ ] `await request_completed` present.
- [ ] Error returned to the caller; `FAILED` returned on missing file or missing key.

## Anti-patterns
- Calling `request()` without setting `download_file` when you intend to persist the payload. WHY: the bytes stay in memory and are lost.
- Ignoring the return value of `request()`. WHY: malformed URLs and missing files then fail silently.
- Blocking the main loop waiting for the download. WHY: use `await` on the signal instead of polling.

---
name: texture-cache-load-and-apply
topic: Loading cached textures and applying them to sprites
confidence: consensus
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 13 (pp. 271-296)"]
---
## Rules
- Build the cache path deterministically from the identity key, e.g. `"user://.cache/" + user + "_spaceship.png"`. WHY: a deterministic path is what makes the existence check a valid cache lookup.
- Expose the sprite swap as an RPC with `@rpc("authority", "call_local")` so only the server can trigger it and the server's own instance also updates. WHY: `call_local` prevents the server from showing a stale default sprite.
- Convert the file to a texture with `Image.load_from_file(path)` then `ImageTexture.create_from_image(image)`, and assign it to the `Sprite2D.texture`. WHY: this is the runtime path from a PNG on disk to a drawable texture.
- On cache hit, apply immediately; on miss, download then apply only if the download returned `OK`. WHY: avoids assigning a texture for a file that was never written.

## Checklist
- [ ] `HTTPRequest` child node added to the player scene and referenced via `@onready`.
- [ ] Cache path derived from the user key with a fixed suffix.
- [ ] `FileAccess.file_exists()` branch for hit vs miss.
- [ ] `await` on the download before applying the texture.
- [ ] Sprite update isolated in its own method so both branches reuse it.

## Anti-patterns
- Assigning the texture before the download completes. WHY: `Image.load_from_file()` on a missing file yields nothing usable.
- Making the sprite RPC callable by any peer. WHY: clients could spoof another player's appearance; use `"authority"`.

---
name: database-cache-and-sync
topic: Caching the shared database and syncing sprites to all peers
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 13 (pp. 271-296)"]
---
## Rules
- Download the shared JSON database once on the client at startup (after a short timer, e.g. 0.1 s) and only when not the server. WHY: the server already owns the authoritative data; clients need a local copy for lookups.
- Keep a `player_users` dictionary mapping the player node name (stringified peer ID) to the username. WHY: it lets any peer resolve a peer ID back to the database key needed for the sprite URL.
- Pass the username as an extra argument when the client RPCs `create_spaceship` to the server. WHY: the server needs the key to look up the URL and to populate `player_users`.
- After spawning a player, RPC `setup_multiplayer` and then RPC `load_spaceship` with the username. WHY: the new player's sprite is set for everyone at spawn time.
- For players already in the world when someone joins, add a `sync_spaceship(player_id)` RPC that resolves the username and calls `load_spaceship` on the requester only via `rpc_id`. WHY: targeted RPC avoids re-broadcasting to every peer on every join.
- Note this chapter modifies the signature of `World.create_spaceship()`; the author accepts this because the project is a prototype. WHY: in a shipped codebase, changing a public method contract risks breaking callers.

## Checklist
- [ ] Database download node instanced as a child of the World node.
- [ ] `player_users` populated at spawn time, keyed by node name.
- [ ] `create_spaceship` accepts the username argument.
- [ ] `load_spaceship` RPC issued right after `setup_multiplayer`.
- [ ] `sync_spaceship` RPC issued by non-server peers for pre-existing players.
- [ ] `sync_spaceship` uses `rpc_id(requester, ...)`, not a broadcast.

## Anti-patterns
- Broadcasting the sprite update to all peers when only the newly joined peer needs it. WHY: it multiplies traffic by player count for no benefit.
- Deriving the username from the peer ID alone. WHY: peer IDs are not usernames; the mapping must come from the database.
- Changing a core method signature in production code without auditing callers. WHY: the author explicitly flags this as acceptable only for a prototype.

---
name: rest-api-and-beyond-textures
topic: Extending caching to REST APIs and non-image assets
confidence: opinion
sources: ["The Essential Guide to Creating Multiplayer Games with Godot 4.0, Henrique Campos, ch. 13 (pp. 271-296)"]
---
## Rules
- Anything served over HTTP can be cached with the same pattern: JSON, text, images, and even `PackedScene` files with their dependencies. WHY: the cache logic is transport-agnostic; only the post-processing differs.
- When assets are not on a public static URL, expect a REST API: pass parameters in the URL query string and auth in headers, e.g. `request(url, ["Content-Type: application/json", "x-session-token: %s" % token])`. WHY: this mirrors an RPC call over HTTP.
- Read the response body from the `request_completed` signal when the server returns metadata rather than the file itself. WHY: APIs commonly return JSON containing the real download URL, which you then fetch in a second request.
- Cache purchased or user-owned content (skins, scenes) locally so the player always has a copy. WHY: it removes a network dependency from content the player already paid for.

## Checklist
- [ ] Confirm whether the asset has a direct public URL or requires an API call.
- [ ] Build the URL with query parameters; put credentials in headers, not the URL.
- [ ] Connect `request_completed` and inspect the body for a nested URL when applicable.
- [ ] Cache the resolved file, not the API response, when the response is just a pointer.

## Anti-patterns
- Putting session tokens in the URL query string. WHY: URLs leak into logs and referrers; use headers.
- Assuming one request is enough when the API returns a JSON envelope. WHY: you must follow the returned URL to get the actual asset.

> CHECK: the chapter references an external video and LootLocker API example; the exact endpoint/response schema is not reproduced here and should be verified against current LootLocker docs.