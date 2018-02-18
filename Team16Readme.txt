Assignment1 Report--Team 16

Members:
	Angel Isiadinso--ati@vt.edu:
		Handled writing client raspberry pi Python script, to read tweets from Twitter stream
		that included #ECE4564. Encrypts, Hashes (through MD5), and serializes (through pickle()) the question and s
		sends to the server raspberry pi. After recieving a payload from the server, the client then
		decrypts the answer and speaks it through GTTS. 
	Teriencio Solano II --terencio@vt.edu:
		Handled writing servery raspberry pi Python script, to listen/accept payload from the client pi. Upon
		receiving a payload from the client, the server decrypts the question using the key, supplied in the client
		payload, and speaks the answer through GTTS. The server then uses the wolfram alpha API to determine the answer
		to the tweeted question and then encrypts, hashes, and serializes (thorugh pickle()) the answer and sends this a
		a payload to the client pi. 
	Marcello Balboa--mgbalboa@vt.edu:
		Handled integrating the GTTS API into the client and server raspberry pi python scripts. Tested both to verify that
		the server pi effectively spoke the tweeted question, and the client pi effectively spoke the tweeted answer. 


APIs/Libraries used: 

	tweepy (Twitter Python API)
	wolframalpha (WolframAlpha Python API)
	gtts (Google Text To Speech Python API)
	hashlib (library to perform md5 cryptographic hash)
	Cryptography (libray that used Fernet to derive a key for symmetric encryption)
	sys (library that interfaced Python script with the physical Raspberry Pi system)
	pickle (library to serialize data between a client and server)

