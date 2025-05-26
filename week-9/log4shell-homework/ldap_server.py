from ldap3 import Server, Connection, ALL

# Use localhost to connect to the LDAP container
server = Server('localhost', port=389, get_info=ALL)

try:
    connection = Connection(server, auto_bind=True)
    print("Connected to LDAP server on port 389. Waiting for queries...")
except Exception as e:
    print(f"Failed to connect to LDAP server: {e}")
